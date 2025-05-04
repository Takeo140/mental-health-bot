import openai
import os
import tweepy
import facebook

# OpenAIのAPIキーを読み込む
openai.api_key = os.getenv("OPENAI_API_KEY")

# AIに啓発メッセージを作らせる
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",  # gpt-4 ではなく gpt-3.5-turbo を使用
  messages=[
    {"role": "system", "content": "あなたは精神保健福祉の専門家です。患者の人権向上について啓発メッセージを考えてください。"},
    {"role": "user", "content": "100文字程度のメッセージを1つ作って。"}
  ],
  max_tokens=200
)

# 結果を取得し、message変数に格納
message = response.choices[0].message["content"]

# 結果を表示
print(message)

# --- X（旧Twitter）への投稿設定 ---
consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
twitter_api = tweepy.API(auth)
twitter_api.update_status(message)
print("Xに投稿完了")

# --- Facebookへの投稿設定 ---
fb_access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
graph = facebook.GraphAPI(access_token=fb_access_token)
graph.put_object(parent_object='me', connection_name='feed', message=message)
print("Facebookに投稿完了")
