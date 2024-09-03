from app.routes import intent_handler  # 引入装饰器
import requests
import json


@intent_handler("meme(迷因)")
def handle_meme_intent(req, token, replytoken):
    """处理 'meme(迷因)' 意图"""
    meme_url = get_random_meme_url()
    if meme_url:
        send_line_message(token, replytoken, meme_url)
        return {
            "fulfillmentText": "Here is your meme!",
            "fulfillmentMessages": [{"image": {"imageUri": meme_url}}],
        }
    else:
        return {
            "fulfillmentText": "Unable to fetch meme at the moment. Please try again later."
        }


def get_random_meme_url():
    """从 Meme API 获取随机迷因 URL"""
    api_url = "https://meme-api.com/gimme"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data.get("url")
    except Exception as e:
        print(f"Error fetching meme: {e}")
        return None


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
