# Standard Library
import logging
from logging.config import dictConfig

import environ  # type: ignore

dictConfig(
    config=dict(
        version=1,
        formatters={
            'f': {
                'format':
                    '%(levelname)-4s %(asctime)s %(name)-12s %(message)s'}
        },
        handlers={
            'h': {'class': 'logging.StreamHandler',
                  'formatter': 'f',
                  'level': logging.INFO}
        },
        root={
            'handlers': ['h'],
            'level': logging.INFO,
        }
    )
)


@environ.config(prefix='')
class AppConfig:
    @environ.config(prefix="DB")
    class DB:
        username = environ.var()
        password = environ.var()
        host = environ.var()
        port = environ.var()
        name = environ.var()
        url = environ.var()

    @environ.config(prefix="API")
    class API:
        title = environ.var()
        version = environ.var()
        prefix = environ.var()
        debug = environ.var()
        allowed_hosts = environ.var()

    mode = environ.var()
    api: API = environ.group(API)
    db: DB = environ.group(DB)


CONFIG: AppConfig = AppConfig.from_environ()  # type: ignore
