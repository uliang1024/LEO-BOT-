from flask import request
from app import app
import os
import importlib
import pkgutil

# 用于存储意图与处理函数的映射
intent_handlers = {}


def intent_handler(intent_name):
    """自定义装饰器用于注册 intent 处理函数"""

    def decorator(func):
        intent_handlers[intent_name] = func
        return func

    return decorator


@app.route("/")
def home():
    return "<h1>Hello World</h1>"


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    reText = req["queryResult"]["fulfillmentText"]  # 取得 Dialogflow 的回應文字
    intent = req["queryResult"]["intent"]["displayName"]  # 取得 intent 分類
    replytoken = req["originalDetectIntentRequest"]["payload"]["data"][
        "replyToken"
    ]  # 取得 LINE replyToken
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    # 使用字典来查找对应的处理函数
    handler = intent_handlers.get(intent)

    if handler:
        return handler(req, token, replytoken)  # 调用对应的处理函数
    else:
        # 处理没有匹配到的意图
        return {"fulfillmentText": f"{reText} ( webhook )"}


def load_intent_modules():
    """动态加载所有意图处理模块"""
    import app.intents

    package = app.intents
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{package.__name__}.{module_name}")


# 加载所有意图模块
load_intent_modules()
