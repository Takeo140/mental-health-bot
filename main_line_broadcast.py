import os
import requests
import json

# OpenRouterのAPIキーを読み込む
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# OpenRouterのエンドポイント
openrouter_url = "https://openrouter.ai/api/v1/chat/completions"

# メッセージ作成リクエスト
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openrouter_api_key}"}

data = { "model": "openai/gpt-3.5-turbo",  # 必要なら他のモデルにも変更可
    "messages": [ {"role": "system", "content": "あなたはメンタルヘルスの専門家です。メンタルヘルス向上について啓発メッセージを考えてください。"},
        {"role": "user", "content": "70文字程度のメッセージを1つ作って。"} ],"max_tokens": 200}

# メッセージ生成
response = requests.post(openrouter_url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    message = response.json()["choices"][0]["message"]["content"]
    print(f"作成メッセージ: {message}")
else:
    print(f"OpenRouterエラー: {response.status_code}, {response.text}")
    exit()

# --- LINEへのブロードキャスト送信設定 ---
line_api_url = 'https://api.line.me/v2/bot/message/broadcast'
line_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

line_headers = { 'Content-Type': 'application/json',
    'Authorization': f'Bearer {line_access_token}'}

payload = {'messages': [ { 'type': 'text','text': message  } ]}

line_response = requests.post(line_api_url, headers=line_headers, data=json.dumps(payload))

# 結果確認
if line_response.status_code == 200:
    print("LINEブロードキャスト送信完了")
else:
    print(f"LINE送信失敗: {line_response.status_code}, {line_response.text}")
