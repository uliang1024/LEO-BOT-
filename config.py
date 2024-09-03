import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")  # 提供默认值
    LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///:memory:")
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def init_app(cls, app):
        """可以在这里添加配置的额外初始化逻辑"""
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
