import asyncio
import os

import click
import uvicorn

from core.app_state import AppState
from core.config import Config, Env


@click.group()
def cli():
    pass


@cli.command()
@click.option('--drop', default=False)
def init_db(drop: bool):
    app_state = AppState()
    app_state.init_logging()
    asyncio.run(app_state.database.init_models(drop=drop))


@cli.command()
def main():
    config = Config.from_env()
    uvicorn.run(
        app="application.main:app",
        host=config.app_host,
        port=config.app_port,
        reload=True if os.getenv("ENV", Env.LOCAL.value) == Env.LOCAL.value else False,
        workers=1
    )


if __name__ == '__main__':
    cli()
