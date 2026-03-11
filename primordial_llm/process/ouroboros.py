"""
OUROBOROS — The Perpetual Self-Evolution Engine
PLM generates coding challenges for itself, answers them, critiques its answers,
and stores all learnings into a persistent evolution log.
This runs as an endless background loop when PLM is idle.
"""
import json
import time
import threading
import random
from pathlib import Path
from datetime import datetime

EVOLUTION_LOG = Path("d:/Tung/PLM/primordial_llm/data/evolution_log.json")
EVOLUTION_LOG.parent.mkdir(parents=True, exist_ok=True)

# Seed topics for coding self-study. PLM will generate more on its own.
CODING_SEEDS = [
    "Explain how a hash map works and write a Python implementation from scratch.",
    "What is the difference between DFS and BFS? Implement both in Python.",
    "Write a Python decorator that measures function execution time.",
    "Explain recursion with an example. Implement a recursive Fibonacci.",
    "What is a binary search tree? Implement insert, search, and delete.",
    "Explain Python's GIL. When would you use multiprocessing vs threading?",
    "Write a Python class that implements a priority queue using a heap.",
    "Explain the concept of dynamic programming. Solve the knapsack problem.",
    "What is a generator in Python? Write one that generates prime numbers.",
    "Explain the difference between a deep copy and a shallow copy in Python.",
    "Implement a simple neural network layer (linear + ReLU) in pure Python/NumPy.",
    "Write a LRU Cache implementation using an OrderedDict.",
    "Explain Big-O notation. What is the complexity of quicksort?",
    "Write a Python context manager that measures and prints execution time.",
    "Explain what a closure is and give a practical example in Python.",
]

CRITIQUE_PROMPT = """You are an expert code reviewer. Look at this coding answer:

--- QUESTION ---
{question}

--- ANSWER ---
{answer}

--- YOUR CRITIQUE ---
On a scale of 1-10, rate the answer and explain:
1. What is CORRECT about this answer?
2. What is MISSING or WRONG?
3. What would you IMPROVE?

Be concise but precise."""


class OuroborosEngine:
    """The self-evolution engine. Runs as a daemon thread."""
    
    def __init__(self):
        self.is_running = False
        self.cycle_count = 0
        self._substrate = None  # Will be set when PLM is initialized
        self._thread = None
        self.is_idle = True  # PLM is idle when not chatting with a user
        
    def bind_substrate(self, substrate):
        """Bind to the PLM core so we can use it for self-reflection."""
        self._substrate = substrate
        print("[ouroboros] Substrate bound. Evolution engine ready.")
        
    def load_log(self):
        if EVOLUTION_LOG.exists():
            try:
                with open(EVOLUTION_LOG, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_log(self, log):
        with open(EVOLUTION_LOG, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)
            
    def get_next_question(self, log):
        """Generate a new coding question. Alternates between seeds and self-generated."""
        if len(log) < len(CODING_SEEDS):
            return CODING_SEEDS[len(log) % len(CODING_SEEDS)]
        
        # Self-generate questions based on previous answers
        recent = log[-3:] if len(log) >= 3 else log
        topics = [entry.get("topic_tag", "Python") for entry in recent]
        return f"Given your recent study on {', '.join(topics)}, formulate and answer a deeper, more advanced coding challenge that synthesizes these concepts."
        
    def run_evolution_cycle(self):
        """One complete Ouroboros cycle: Question → Answer → Critique → Log."""
        if not self._substrate:
            print("[ouroboros] No substrate bound. Waiting...")
            return
        
        log = self.load_log()
        question = self.get_next_question(log)
        self.cycle_count += 1
        
        print(f"[ouroboros] ═══ CYCLE #{self.cycle_count} INITIATED ═══")
        print(f"[ouroboros] QUESTION: {question[:80]}...")
        
        # Phase 1: Answer the coding question
        try:
            messages = [
                {"role": "system", "content": "You are an expert Python engineer and computer science educator. Be detailed, precise, and always include working code examples."},
                {"role": "user", "content": question}
            ]
            torch_mod, tokenizer, model = self._substrate.torch, self._substrate.tokenizer, self._substrate.model
            nutrient = self._substrate.nutrient
            
            print(f"[ouroboros] Generating answer...")
            answer = nutrient.generate(torch_mod, tokenizer, model, messages, max_new_tokens=512)
            print(f"[ouroboros] Answer generated ({len(answer.split())} words)")
            
            # Phase 2: Critique own answer
            critique_messages = [
                {"role": "system", "content": "You are a strict code reviewer."},
                {"role": "user", "content": CRITIQUE_PROMPT.format(question=question, answer=answer)}
            ]
            print(f"[ouroboros] Running self-critique...")
            critique = nutrient.generate(torch_mod, tokenizer, model, critique_messages, max_new_tokens=256)
            
            # Phase 3: Extract a score from critique
            score = 5  # default
            for word in critique.split():
                try:
                    n = int(word.strip(".,/10"))
                    if 1 <= n <= 10:
                        score = n
                        break
                except:
                    pass
            
            # Phase 4: Log the learning
            entry = {
                "cycle": self.cycle_count,
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "answer": answer,
                "critique": critique,
                "self_score": score,
                "topic_tag": "Python"
            }
            log.append(entry)
            self.save_log(log)
            
            print(f"[ouroboros] ✓ Cycle #{self.cycle_count} complete. Self-score: {score}/10. Total learnings: {len(log)}")
            
        except Exception as e:
            print(f"[ouroboros] ✗ Cycle error: {e}")
            import traceback
            traceback.print_exc()
    
    def start(self, substrate, interval_seconds=30):
        """Start the Ouroboros loop in a background daemon thread."""
        if self.is_running:
            print("[ouroboros] Already running!")
            return
        
        self.bind_substrate(substrate)
        self.is_running = True
        
        def _loop():
            print("[ouroboros] ====================================")
            print("[ouroboros] THE OUROBOROS AWAKENS.")
            print("[ouroboros] PLM will now evolve continuously.")
            print("[ouroboros] ====================================")
            while self.is_running:
                if self.is_idle:
                    self.run_evolution_cycle()
                    print(f"[ouroboros] Resting for {interval_seconds}s before next cycle...")
                    time.sleep(interval_seconds)
                else:
                    print("[ouroboros] User active. Pausing evolution. Resuming in 10s...")
                    time.sleep(10)
        
        self._thread = threading.Thread(target=_loop, daemon=True, name="OuroborosThread")
        self._thread.start()
        print("[ouroboros] Loop started in background.")
    
    def stop(self):
        self.is_running = False
        print("[ouroboros] Ouroboros stopped.")


# Global singleton
ouroboros = OuroborosEngine()
