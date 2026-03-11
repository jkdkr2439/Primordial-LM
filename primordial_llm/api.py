import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path

import asyncio
from sse_starlette.sse import EventSourceResponse
import queue
import logging

from primordial_llm.data.context_registry import build_runtime_context
from primordial_llm.data.models import ChatSessionState, ChatRuntimeConfig
from primordial_llm.output.substrate_adapter import PrimordialSubstrateAdapter
from primordial_llm.process.action_cycle import PrimordialActionCycle
from primordial_llm.process.bootstrap import PrimordialBootstrapper
from primordial_llm.process.ouroboros import ouroboros

CONFIG_FILE = Path("d:/Tung/PLM/plm_config.json")

def save_plm_config(weights_dir: str, load_4bit: bool):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"last_weights_dir": weights_dir, "last_load_in_4bit": load_4bit}, f)

def load_plm_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

app = FastAPI(title="Primordial Language Machine API")

# Global state for the PLM instance
class PLMState:
    def __init__(self):
        self.config = None
        self.runtime = None
        self.session = None
        self.cycle = None
        self.substrate_adapter = PrimordialSubstrateAdapter()

plm = PLMState()

class ChatRequest(BaseModel):
    message: str

class InitRequest(BaseModel):
    weights_dir: str
    load_in_4bit: bool = False

@app.post("/api/init")
async def initialize(req: InitRequest):
    if req.weights_dir == "INTERNAL_CORE_SUBSTRATE":
        weights_path = plm.substrate_adapter.INTERNAL_SUBSTRATE_PATH
    else:
        weights_path = Path(req.weights_dir)
        
    if not weights_path.exists():
        raise HTTPException(status_code=400, detail=f"Weights directory not found: {weights_path}")
    
    plm.config = ChatRuntimeConfig(
        repo_root=Path("."),
        weights_dir=weights_path,
        load_in_4bit=req.load_in_4bit
    )
    plm.runtime = build_runtime_context(plm.config)
    bootstrapper = PrimordialBootstrapper(plm.runtime)
    report = bootstrapper.bootstrap()
    
    substrate = plm.substrate_adapter.load_substrate(
        plm.config.weights_dir,
        plm.config.load_in_4bit,
        plm.config.max_new_tokens
    )
    
    plm.cycle = PrimordialActionCycle(plm.runtime, substrate)
    plm.session = ChatSessionState.create(plm.runtime.system_prompt)
    plm.session.memory_pointers.active_context_path = report.short_term_note_path
    plm.session.memory_pointers.identity_anchor_path = report.long_term_note_path
    plm.session.memory_pointers.latest_report_path = report.report_path
    plm.cycle.bootstrap_session(plm.session)
    
    # Persist these settings
    save_plm_config(req.weights_dir, req.load_in_4bit)
    
    # Start Ouroboros self-evolution
    ouroboros.start(substrate, interval_seconds=60)
    
    return {"status": "initialized", "model": weights_path.name}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not plm.cycle or not plm.session:
        raise HTTPException(status_code=400, detail="PLM not initialized")
    
    print(f"[api] Received message: {req.message}")
    ouroboros.is_idle = False  # Pause Ouroboros during user chat
    
    try:
        import anyio
        # Run the heavy generation in a separate thread so Uvicorn stays alive
        await anyio.to_thread.run_sync(plm.cycle.run_turn, plm.session, req.message)
    except Exception as e:
        print(f"[api] Error during run_turn: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        ouroboros.is_idle = True  # Resume Ouroboros after chat
    
    # Return the latest assistant message
    conversation = plm.session.transcript.conversation
    responses = [m for m in conversation if m["role"] == "assistant"]
    
    print(f"[api] Turn complete. Responses: {len(responses)}")
    
    return {
        "response": responses[-1]["content"] if responses else "System: No response generated.",
        "stats": {
            "state_changes": plm.session.state_changes,
            "organs": len(plm.session.replication.blueprints) if plm.session.replication else 0
        }
    }

@app.get("/api/session")
async def get_session():
    last_config = load_plm_config()
    
    # Check for internal substrate (The Merger)
    internal_path = plm.substrate_adapter.get_internal_substrate_path()
    has_internal = internal_path is not None
    
    if not plm.session:
        return {
            "status": "uninitialized", 
            "last_config": last_config,
            "has_internal": has_internal,
            "internal_model": internal_path.name if has_internal else None
        }
    return {
        "status": "ready",
        "state_changes": plm.session.state_changes,
        "history": plm.session.transcript.conversation[-20:],
        "last_config": last_config,
        "has_internal": has_internal
    }

@app.get("/api/ouroboros")
async def ouroboros_status():
    """Get Ouroboros evolution status."""
    from primordial_llm.process.ouroboros import ouroboros, EVOLUTION_LOG
    log = ouroboros.load_log()
    return {
        "running": ouroboros.is_running,
        "cycle_count": ouroboros.cycle_count,
        "total_learnings": len(log),
        "latest": log[-1] if log else None
    }

@app.post("/api/ouroboros/stop")
async def ouroboros_stop():
    ouroboros.stop()
    return {"status": "stopped"}

@app.post("/api/ouroboros/start")
async def ouroboros_start_manual():
    if not plm.substrate_adapter or not hasattr(ouroboros, '_substrate') or not ouroboros._substrate:
        raise HTTPException(status_code=400, detail="Initialize PLM first.")
    ouroboros.is_running = True
    return {"status": "started"}

# Telemetry stream for the Observer console
telemetry_queue = asyncio.Queue()

# Injecting into PLM internal logic (Global mask)
import builtins
_orig_print = builtins.print
def plm_print(*args, **kwargs):
    msg = " ".join(map(str, args))
    _orig_print(f"[telemetry] {msg}")
    try:
        loop = asyncio.get_running_loop()
        loop.call_soon_threadsafe(telemetry_queue.put_nowait, msg)
    except Exception:
        pass
builtins.print = plm_print

@app.get("/api/telemetry")
async def telemetry_stream():
    async def event_generator():
        while True:
            msg = await telemetry_queue.get()
            yield {"data": msg}
    return EventSourceResponse(event_generator())

# Serve static files from primordial_ui
ui_path = Path("d:/Tung/PLM/primordial_ui")
if not ui_path.exists():
    ui_path.mkdir(parents=True)

app.mount("/", StaticFiles(directory=str(ui_path), html=True), name="ui")
