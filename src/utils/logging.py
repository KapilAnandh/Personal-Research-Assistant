from rich.console import Console

console = Console()


def info(msg: str):
    console.print(f"[bold cyan][INFO][/bold cyan] {msg}")


def warn(msg: str):
    console.print(f"[bold yellow][WARN][/bold yellow] {msg}")


def error(msg: str):
    console.print(f"[bold red][ERROR][/bold red] {msg}")
