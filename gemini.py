import tweepy
import schedule
import time
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Initialize Tweepy client
client = tweepy.Client(
    consumer_key="XXX",
    consumer_secret="XXX",
    access_token="XXX",
    access_token_secret="XXX"
)

# Configure Google API key
os.environ["GoogleApiKey"] = "XXX"
genai.configure(api_key=os.environ["GoogleApiKey"])

# Configure generation parameters
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize GenerativeModel
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
)

# Start chat session
chat_session = model.start_chat(history=[])

# Function to split content into chunks by sentences
def split_content_by_sentences(content, max_length=250):
    sentences = content.split('. ')
    tweets = []
    tweet = ""

    for sentence in sentences:
        if len(tweet) + len(sentence) + 1 > max_length:
            tweets.append(tweet.strip() + ".")
            tweet = sentence
        else:
            tweet = tweet + ". " + sentence if tweet else sentence

    if tweet:
        tweets.append(tweet.strip() + ".")

    return tweets

# Function to post a tweet
def post_tweet():
    # Generate content from Gemini AI
    response = chat_session.send_message("Write me a story.")
        
    # Extract text content from the response
    content = response.text
    print(content)
    # Split content into tweets
    tweets = split_content_by_sentences(content)
    
    # Post tweets
    previous_tweet_id = None
    for tweet in tweets:
        if previous_tweet_id:
            response = client.create_tweet(text=tweet, in_reply_to_tweet_id=previous_tweet_id)
        else:
            response = client.create_tweet(text=tweet)
        previous_tweet_id = response.data["id"]
    
    print("Tweet başarıyla gönderildi:", content)

# Schedule the function to run every 10 minutes
post_tweet()

