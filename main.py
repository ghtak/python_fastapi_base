import asyncio
import os

import click
import uvicorn

from core.app_context import AppContext
from core.config import Config, Env
from core.database import Database

# for init-db
from application.user.model import *


@click.group()
def cli():
    pass


@cli.command()
@click.option('--drop', default=False)
def init_db(drop: bool):
    AppContext.init_logging()
    AppContext.logger.debug(AppContext.config)
    Database.init(AppContext.config)
    asyncio.run(Database.sync_models(drop=drop))


@cli.command()
def main():
    config = Config.from_env()
    uvicorn.run(
        app='application.main:app',
        host=config.app_host,
        port=config.app_port,
        reload=True if os.getenv("ENV", Env.LOCAL.value) == Env.LOCAL.value else False,
        workers=1
    )


if __name__ == '__main__':
    cli()
