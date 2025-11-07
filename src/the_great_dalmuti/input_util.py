from typing import Any
import click

def prompt(*args, **kwargs) -> Any:
    response = click.prompt(*args, **kwargs)
    if response in ['q', 'quit', 'exit']:
        exit(0)
    return response