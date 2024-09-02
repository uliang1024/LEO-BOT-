from flask import Flask
from config import DevelopmentConfig, ProductionConfig
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# 根据环境变量加载配置
if os.getenv("FLASK_ENV") == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)


# 设置日志处理器
def setup_logging():
    if not app.debug:
        file_handler = RotatingFileHandler("app.log", maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("Application startup")


setup_logging()

# 导入路由
from app import routes
