import uvicorn

from app.config import config


def main():
    uvicorn.run(
        app="app.server:app",
        host=config.app_host,
        port=config.app_port,
        reload=False if config.env == "prod" else True,
        workers=1
    )


if __name__ == '__main__':
    main()
