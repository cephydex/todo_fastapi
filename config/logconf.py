# log settings
# LOG_NAME = "faster1"
# LOG_LEVEL = "DEBUG"
# LOG_FORMAT = "%(levelprefix)s | %(asctime)s | %(message)s"

# conf = {
#     "version": 1,
#     "formatters": {
#         "default": {
#             "()": "uvicorn.logging.DefaultFormatter",
#             "fmt": LOG_FORMAT,
#             "datefmt": "%Y-%m-%d %H:%M:%S"
#         }
#     },
#     "handlers": {
#         "default": {
#             "formatter": "default",
#             "class": "logging.StreamHandler",
#             "stream": "ext://sys.stdout",
#         }

#     },
#     "loggers": {
#         LOG_NAME: {
#             "handlers": ["default"], "level": LOG_LEVEL,
#         }
#     }
# }

LOGGER_NAME: str = "todo-app"
LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
LOG_LEVEL: str = "DEBUG"

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": LOG_FORMAT,
            # "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": "logs/app.log",
            "maxBytes": 1024,
            "backupCount": 3
        }
    },
    "loggers": {
        LOGGER_NAME: {
            "handlers": ["default", "file"],
            "level": LOG_LEVEL
        }
    }
}