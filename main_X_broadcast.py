import os
import requests
import json
from requests_oauthlib import OAuth1

# OpenRouterのAPIキーを読み込む
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# OpenRouterのエンドポイント
openrouter_url = "https://openrouter.ai/api/v1/chat/completions"

# メッセージ作成リクエスト
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openrouter_api_key}"
}

data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "あなたはメンタルヘルスの専門家です。メンタルヘルス向上について啓発メッセージを考えてください。"},
        {"role": "user", "content": "70文字程度のメッセージを1つ作って。"}
    ],
    "max_tokens": 200
}

# メッセージ生成
response = requests.post(openrouter_url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    message = response.json()["choices"][0]["message"]["content"]
    print(f"作成メッセージ: {message}")
else:
    print(f"OpenRouterエラー: {response.status_code}, {response.text}")
    exit()

# --- X(Twitter)への投稿設定 ---

# X APIキーとトークンの読み込み
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# 認証設定
auth = OAuth1(api_key, api_secret, access_token, access_token_secret)

# Xの投稿用エンドポイント
twitter_api_url = 'https://api.twitter.com/1.1/statuses/update.json'

# 投稿データ
tweet_data = {'status': message}

# 投稿リクエスト
twitter_response = requests.post(twitter_api_url, auth=auth, data=tweet_data)

# 結果確認
if twitter_response.status_code == 200:
    print("Xへの投稿完了")
else:
    print(f"X投稿失敗: {twitter_response.status_code}, {twitter_response.text}")
