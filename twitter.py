import tweepy
import time
import _json
from requests_oauthlib import OAuth1
import requests
import os
import re
from dotenv import load_dotenv

class Twitter:
    def __init__(self):
        print("initializing twitter....")
        self.inits = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SCRET'])
        self.inits.set_access_token(os.environ['ACCESS_KEY'], os.environ['ACCESS_SECRET'])
        self.api = tweepy.API(self.inits)


    def read_dm(self):
        print("Get direct messages...")
        dms = list()
        try:
            api = self.api
            dm = api.list_direct_messages()
            for x in range(len(dm)):
                sender_id = dm[x].message_create['sender_id']
                message = dm[x].message_create['message_data']['text']
                message_data = str(dm[x].message_create['message_data'])
                json_data = _json.encode_basestring(message_data)
                print("Getting message -> "+str(message)+" by sender id "+str(sender_id))

                if "attachment" not in json_data:
                    print("Dm does not have any media...")
                    d = dict(message=message, sender_id=sender_id, id=dm[x].id, media = None)
                    dms.append(d)
                    dms.reverse()

                else:
                    print("Dm have an attachment..")
                    attachment = dm[x].message_create['message_data']['attachment']
                    d = dict(message=message, sender_id=sender_id, id=dm[x].id, media = attachment['media']['media_url'])
                    dms.append(d)
                    dms.reverse()

            print(str(len(dms)) + " collected")
            time.sleep(60)
            return dms

        except Exception as ex:
            print(ex)
            time.sleep(60)
            pass


    def delete_dm(self, id):
        print("Deleting dm with id = "+ str(id))
        try:
            self.api.destroy_direct_message(id)
            time.sleep(40)
        except Exception as ex:
            print(ex)
            time.sleep(40)
            pass


    def post_tweet(self, tweet):
        self.api.update_status(tweet)

    def post_tweet_with_media(self, tweet, media_url, id):
        arr = str(media_url).split('/')
        auth = OAuth1(client_key= os.environ['CONSUMER_KEY'],
                      client_secret= os.environ['CONSUMER_SCRET'],
                      resource_owner_secret= os.environ['ACCESS_SECRET'],
                      resource_owner_key= os.environ['ACCESS_KEY'])
        r = requests.get(media_url, auth = auth)
        with open(arr[9], 'wb') as f:
            f.write(r.content)
        tweet = re.sub(r'http\S+', '', tweet)
        url = "https://twitter.com/messages/media/"+ str(id)
        print("url -> " + url)
        tweet = tweet.replace(url, "")
        self.api.update_with_media(filename= arr[9], status = tweet)
        os.remove(arr[9])