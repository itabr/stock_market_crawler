import tweepy

consumer_key = "WMBaLdmJmWysb7kisqdKBD3Wd"
consumer_secret = "mrCiHxnSv7ZV5HsC1Sywu44N7R0n3x4d4wmiSTszNt50Gq5ObX"
access_token = "926633743841771520-gcJR5HWYH5pcneR0gJnP73jxuFdsgKC"
access_token_secret = "4iNT66uZmufHLh79wkhz4WyI7tW0TrGkWW4auxRczbLcX"

class listener(tweepy.StreamListener):
	def on_data(self, data):
		print(data)
		return(True)

	def on_error(self, status):
		print(status)



if __name__ == "__main__":

	stock_name = "APPL"

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	# stream data
	#
	# twitterStream = tweepy.Stream(auth, listener())
	# twitterStream.filter(track=[stock_name])

	# request tweet

	r = api.search(q=stock_name)
	for tweet in r:
		print(tweet._json)
