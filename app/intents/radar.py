from app.routes import intent_handler  # 引入装饰器
import requests
import json
import time


@intent_handler("radar(氣象)")
def handle_radar_intent(req, token, replytoken):
    """处理 'radar(氣象)' 意图"""
    img = f"https://cwbopendata.s3.ap-northeast-1.amazonaws.com/MSC/O-A0058-003.png?{time.time_ns()}"
    send_line_message(token, replytoken, img)
    return {"source": "webhookdata"}


def send_line_message(token, replytoken, img_url):
    """发送图片消息到 LINE"""
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
    }
    body = {
        "replyToken": replytoken,
        "messages": [
            {
                "type": "image",
                "originalContentUrl": img_url,
                "previewImageUrl": img_url,
            },
        ],
    }

    response = requests.post(
        "https://api.line.me/v2/bot/message/reply",
        headers=headers,
        data=json.dumps(body).encode("utf-8"),
    )

    if response.status_code != 200:
        from app import app

        app.logger.error(f"Failed to send message: {response.text}")
