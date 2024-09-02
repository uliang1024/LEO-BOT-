from flask import request, jsonify
from app import app
import requests, json, time
import os


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

    img = f"https://cwbopendata.s3.ap-northeast-1.amazonaws.com/MSC/O-A0058-003.png?{time.time_ns()}"

    if intent == "radar(氣象)":
        send_line_message(token, replytoken, img)
        return {"source": "webhookdata"}
    else:
        return {"fulfillmentText": f"{reText} ( webhook )"}


def send_line_message(token, replytoken, img_url):
    """发送图片消息到 LINE"""
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
    }
    body = {
        "replyToken": replytoken,
        "messages": [
            {"type": "image", "originalContentUrl": img_url, "previewImageUrl": img_url}
        ],
    }

    response = requests.post(
        "https://api.line.me/v2/bot/message/reply",
        headers=headers,
        data=json.dumps(body).encode("utf-8"),
    )

    if response.status_code != 200:
        app.logger.error(f"Failed to send message: {response.text}")
