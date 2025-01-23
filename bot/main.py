
import tweepy
import pandas as pd
import schedule
import time
from pytz import timezone
from datetime import datetime

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# TWITTER API CREDENTIALS

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")

# Authenticate Twitter using Client (v2)
client = tweepy.Client(bearer_token, 
                       api_key, 
                       api_secret, 
                       access_token, 
                       access_token_secret)
auth = tweepy.OAuth1UserHandler(bearer_token, 
                                api_key, 
                                api_secret, 
                                access_token, 
                                access_token_secret)
api = tweepy.API(auth)

# Import .txt and read files
def readTextFile(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        data = []
        for line in lines:
            # Split by "::" to separate character and dialogue
            if "::" in line:
                chara, dialogue = line.split("::", 1)
                data.append({"Character": chara.strip(), "Dialogue": dialogue.strip()})
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error reading text file: {e}")
        return pd.DataFrame()

# Randomize row pick
def randomizeRow(df):
    if df.empty:
        print("DataFrame is empty. Cannot randomize row.")
        return None
    randomRow = df.sample()
    charaName = randomRow.iloc[0]['Character']
    charaDialogue = randomRow.iloc[0]['Dialogue']
    return f"{charaName}: {charaDialogue}"

# Post a single tweet using API v2
def postTweet():
    try:
        # Check timezone
        now = datetime.now(timezone('Asia/Jakarta'))
        current_hour = now.hour  # Current hour in GMT+7
        if 9 <= current_hour < 21:
            # Replace with the path to your .txt file
            df = readTextFile("scriptFiltered.txt")
            if df.empty:
                print("No data available to tweet.")
                return

            tweet = randomizeRow(df)
            if not tweet:
                print("Failed to generate a tweet.")
                return

            # Post the tweet using create_tweet
            client.create_tweet(text=tweet)
            print(f"Tweeted successfully: {tweet}")
        else:
            print(f"Current time is outside posting hours: {now}")
    except Exception as e:
        print(f"Error posting tweet: {e}")

# Run the function to post a single tweet
schedule.every(30).minutes.do(postTweet)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(f"Error with schedule: {e}")
        break  # Optionally exit if there's an error
