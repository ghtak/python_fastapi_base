import asyncio

import click
import uvicorn

from app.app_state import AppState
from app.config import Config, Env


@click.group()
def cli():
    pass


@cli.command()
@click.option('--drop', default=False)
def init_db(drop: bool):
    app_state = AppState(config=Config.from_env())
    app_state.init_logging()
    asyncio.run(app_state.database.init_models(drop=drop))


@cli.command()
def main():
    config = Config.from_env()
    uvicorn.run(
        app="app.server:app",
        host=config.app_host,
        port=config.app_port,
        reload=True if config.env == Env.LOCAL else False,
        workers=1
    )


if __name__ == '__main__':
    cli()
