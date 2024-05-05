import uvicorn

from app.config import Config


def main():
    config = Config.from_env()
    uvicorn.run(
        app="app.server:app",
        host=config.app_host,
        port=config.app_port,
        reload=True if config.env == "dev" else False,
        workers=1
    )


if __name__ == '__main__':
    main()
