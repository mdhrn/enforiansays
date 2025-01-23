# import pandas as pd
# import tweepy
# import schedule
# import time
# import random

# #TWITTER API CREDENTIALS
# API_KEY = '7NgKkM3jyDw4UkPwbwNno4JPd'
# API_SECRET = 'mKRFQN8jgQDUdKswODonlz8g9LFsKDjxNgjJkAsVhn1PJJXLJX'
# ACCESS_TOKEN = '1862997901909311488-UPG3279i4FhLLsPWfAqJwinZbmKGGR'
# ACCESS_TOKEN_SECRET = '3YidoWDjqqO4j1dfTcmWOtvdtlX7VR5MUMbVAukRZ16tb'
# BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAHS6yAEAAAAAhEbcocw8YmBW48voho0yaFCKxUI%3DbZ4iBlwDH95IOPiKdi1KCTcTQO72xXY9k33O3HdXVTuqsP8zqH'

# #Authenticate Twitter
# def authenticateTwitter():
#     auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
#     auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#     return tweepy.API(auth)

# # Import .txt and read files
# # Import .txt and read files
# def readTextFile(file_path):
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             lines = file.readlines()
#         data = []
#         for line in lines:
#             # Split by "::" to separate character and dialogue
#             if "::" in line:
#                 chara, dialogue = line.split("::", 1)
#                 data.append({"Character": chara.strip(), "Dialogue": dialogue.strip()})
#         # Convert list of dictionaries to a Pandas DataFrame
#         return pd.DataFrame(data)
#     except Exception as e:
#         print(f"Error reading text file: {e}")
#         return pd.DataFrame()

    
# # Randomize row pick
# # Randomize row pick
# def randomizeRow(df):
#     if df.empty:
#         print("DataFrame is empty. Cannot randomize row.")
#         return None
#     randomRow = df.sample()
#     charaName = randomRow.iloc[0]['Character']
#     charaDialogue = randomRow.iloc[0]['Dialogue']
#     return f"{charaName}: {charaDialogue}"


# # Tweet framework
# def postTweet():
#     api = authenticateTwitter()
#     df = readTextFile("scriptFiltered.txt")
#     tweet = randomizeRow(df)
#     postUpdate(api, tweet)
    
# def postUpdate(api, text):
#     try:
#         api.update_status(text)  # Sends the tweet
#         print(f"Tweeted: {text}")
#     except Exception as e:
#         print(f"Error tweeting: {e}")  # Logs any errors
    
# schedule.every(30).minutes.do(postTweet)

# while True:
#     try:
#         print("Checking for scheduled tasks...")
#         schedule.run_pending()
#         time.sleep(1)
#     except Exception as e:
#         print(f"Error with schedule: {e}")
#         break  # Optionally exit if there's an error

import tweepy
import pandas as pd
import schedule
import time

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# TWITTER API CREDENTIALS
api_key = "DVfnSPcon5KltkZbt8srwnvv0"
api_secret = "qFCLQLQwGe8gZEKKKoqAkFk1Q7naLGF95e40YiEyglxx7jVjLy"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAHS6yAEAAAAALf0gHB7VLIZ1xnP4Fg%2FNn48yRrw%3DfJ5dZo8gTrvwkCLfqWp7UBpcnJspB3sujmYihoJjOlqwQplvO4"
access_token = "1862997901909311488-rzIso36EbfN7JFZVe8m6dOYJI2YhH3"
access_token_secret = "bxMNr8GThe0uZIIBWtVIah5xgdHffmUNGepwQumefUP8x"
client_id = 'R0F0WnBJMmRlWHFGNVE2Q0gzNlE6MTpjaQ'
client_secret = 't8wzqF0Vrl87i10IiJXcN7-zf9HCtPIz4zWV4galGBhQe2pQey'

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
    except Exception as e:
        print(f"Error posting tweet: {e}")

# Run the function to post a single tweet
schedule.every(15).minutes.do(postTweet)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(f"Error with schedule: {e}")
        break  # Optionally exit if there's an error
