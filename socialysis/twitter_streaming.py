#Requeriments
# pip install tweepy # install join to conda enviroment: '3.3.0'
#
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        return True
    def on_error(self, status):
        print(status)
l=StdOutListener()
stream = Stream(auth,l)
#stream.filter(track=['#python','#java','#javascript'])
stream.filter(track=['python','java','javascript'])

