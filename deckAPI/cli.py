#!/usr/bin/env python3
"""CLI for Deck API server."""
import click
import uvicorn


@click.command()
@click.option(
    "--host",
    default="127.0.0.1",
    help="Host to bind to (default: 127.0.0.1)"
)
@click.option(
    "--port",
    type=int,
    default=8000,
    help="Port to bind to (default: 8000)"
)
@click.option(
    "--reload",
    is_flag=True,
    help="Enable auto-reload for development"
)
def main(host, port, reload):
    """Run the Deck API server."""
    click.echo(f"Starting Deck API server on {host}:{port}")
    uvicorn.run("deckAPI.main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    main()

