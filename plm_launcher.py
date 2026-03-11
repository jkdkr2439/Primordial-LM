
import os
import sys
import time
from pathlib import Path

# Add the current directory to sys.path for internal imports
sys.path.append(str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.markdown import Markdown
from rich.text import Text
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

from primordial_llm.data.context_registry import build_runtime_context
from primordial_llm.data.models import ChatSessionState
from primordial_llm.output.substrate_adapter import PrimordialSubstrateAdapter
from primordial_llm.process.action_cycle import PrimordialActionCycle
from primordial_llm.process.bootstrap import PrimordialBootstrapper
from primordial_llm.input.cli import ChatRuntimeConfig

console = Console()

def create_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="chat", ratio=3),
        Layout(name="stats", ratio=1)
    )
    return layout

class PLMApp:
    def __init__(self, config: ChatRuntimeConfig):
        self.config = config
        self.runtime = build_runtime_context(config)
        self.bootstrapper = PrimordialBootstrapper(self.runtime)
        self.substrate_adapter = PrimordialSubstrateAdapter()
        self.session = None
        self.cycle = None
        self.console = Console()
        self.history = []

    def show_splash(self):
        splash = Panel(
            Text.from_markup(
                "[bold cyan]PRIMORDIAL LANGUAGE MACHINE[/bold cyan]\n"
                "[dim]Version 2.0.0 - Evolution Proto-Alpha[/dim]\n\n"
                "[italic]\"The invasion of meaning has begun.\"[/italic]",
                justify="center"
            ),
            border_style="bright_blue",
            padding=(1, 2)
        )
        self.console.print(splash)
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Gathering nutrients...", total=None)
            time.sleep(1)
            progress.add_task(description="Expanding context field...", total=None)
            time.sleep(1)
            progress.add_task(description="Stabilizing SDCV cycle...", total=None)
            time.sleep(0.5)

    def bootstrap(self):
        report = self.bootstrapper.bootstrap()
        
        if self.config.weights_dir is None:
            self.console.print("[bold red]Error:[/bold red] PLM_WEIGHTS_DIR is not set.")
            sys.exit(1)
            
        substrate = self.substrate_adapter.load_substrate(
            self.config.weights_dir,
            self.config.load_in_4bit,
            self.config.max_new_tokens
        )
        
        self.cycle = PrimordialActionCycle(self.runtime, substrate)
        self.session = ChatSessionState.create(self.runtime.system_prompt)
        self.session.memory_pointers.active_context_path = report.short_term_note_path
        self.session.memory_pointers.identity_anchor_path = report.long_term_note_path
        self.session.memory_pointers.latest_report_path = report.report_path
        self.cycle.bootstrap_session(self.session)

    def make_stats_table(self) -> Table:
        table = Table(title="Entity Stats", box=None)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Time (SDCV)", str(self.session.state_changes))
        table.add_row("Continuity", "Stable" if self.session.state_changes > 0 else "Bootstrapping")
        table.add_row("Organs", str(len(self.session.replication.blueprints)) if self.session.replication else "0")
        table.add_row("Weights", os.path.basename(str(self.config.weights_dir)))
        
        return table

    def run(self):
        self.show_splash()
        self.bootstrap()
        
        while True:
            self.console.clear()
            # Show history and stats
            layout = create_layout()
            layout["header"].update(Panel(Text("PLM - INTERACTIVE INVADER", justify="center", style="bold yellow"), border_style="yellow"))
            
            stats_panel = Panel(self.make_stats_table(), title="[bold]Session[/bold]", border_style="cyan")
            layout["stats"].update(stats_panel)
            
            chat_text = Text()
            for msg in self.session.transcript.conversation[-10:]: # Latest 10
                role = msg["role"]
                content = msg["content"]
                if role == "user":
                    chat_text.append(f"\n[bold green]You:[/bold green] {content}\n")
                elif role == "assistant":
                    chat_text.append(f"\n[bold blue]Primor:[/bold blue] ")
                    # We could render markdown here if it's too long
                    chat_text.append(content + "\n")
                elif role == "tool":
                    chat_text.append(f"\n[dim yellow]Tool Interaction:[/dim yellow] {content}\n")
            
            layout["chat"].update(Panel(chat_text, title="Communication Stream", border_style="green"))
            layout["footer"].update(Panel(Text("Type /quit to exit | /clear to reset memory", justify="center"), border_style="dim"))
            
            self.console.print(layout)
            
            user_input = Prompt.ask("\n[bold green]Command[/bold green]")
            
            if user_input.lower() in ["/quit", "/exit"]:
                break
            if user_input.lower() == "/clear":
                self.session = ChatSessionState.create(self.runtime.system_prompt)
                continue
                
            with console.status("[bold blue]Infiltrating substrate..."):
                self.cycle.run_turn(self.session, user_input)

if __name__ == "__main__":
    from primordial_llm.input.cli import parse_args
    cfg = parse_args()
    app = PLMApp(cfg)
    app.run()
