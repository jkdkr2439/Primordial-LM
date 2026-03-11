import argparse
import os
from pathlib import Path

from primordial_llm.data.models import ChatRuntimeConfig


def parse_args() -> ChatRuntimeConfig:
    parser = argparse.ArgumentParser(description="Primordial Language Machine runtime")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--weights-dir", default=os.environ.get("PLM_WEIGHTS_DIR"))
    parser.add_argument("--sandbox-root", default="llm_sandbox")
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--load-in-4bit", action="store_true")
    args = parser.parse_args()
    return ChatRuntimeConfig(
        repo_root=Path(args.repo_root),
        weights_dir=Path(args.weights_dir) if args.weights_dir else None,
        sandbox_root_name=args.sandbox_root,
        max_new_tokens=args.max_new_tokens,
        load_in_4bit=args.load_in_4bit,
    )


def read_user_input() -> str:
    return input("you> ").strip()
