import os
import requests
import json
import tweepy

# OpenRouter APIキー
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# OpenRouterエンドポイント
openrouter_url = "https://openrouter.ai/api/v1/chat/completions"

# メッセージ生成用ヘッダーとデータ
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openrouter_api_key}"
}

data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "あなたはメンタルヘルスの専門家です。70文字のメンタルヘルス啓発メッセージを考えてください。"},
        {"role": "user", "content": "70文字程度のメッセージを1つ作って。"}
    ],
    "max_tokens": 200
}

# OpenRouterにメッセージ生成依頼
response = requests.post(openrouter_url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    message = response.json()["choices"][0]["message"]["content"]
    print(f"生成メッセージ: {message}")
else:
    print(f"OpenRouterエラー: {response.status_code}, {response.text}")
    exit()

# X(Twitter) API認証情報
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# tweepyで認証
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# ツイート投稿
try:
    api.update_status(message)
    print("✅ Xに投稿完了")
except Exception as e:
    print(f"X投稿エラー: {e}")
