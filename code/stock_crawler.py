import tweepy
import preprocessor as tweetPreprocessor
import json

consumer_key = "WMBaLdmJmWysb7kisqdKBD3Wd"
consumer_secret = "mrCiHxnSv7ZV5HsC1Sywu44N7R0n3x4d4wmiSTszNt50Gq5ObX"
access_token = "926633743841771520-gcJR5HWYH5pcneR0gJnP73jxuFdsgKC"
access_token_secret = "4iNT66uZmufHLh79wkhz4WyI7tW0TrGkWW4auxRczbLcX"

if __name__ == "__main__":

	# stock_name = "AAPL", "iPhone", "apple", "stock"
	stock_name = "iPhone"

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	# request tweet
	f = open("output.txt", "w+")


	max_tweets=100

	searched_tweets = [status._json for status in tweepy.Cursor(api.search, q=stock_name).items(max_tweets)]
	json_strings = [json.dumps(json_obj) for json_obj in searched_tweets]
	for json_obj in searched_tweets:
		f.write(json.dumps(json_obj))
		f.write("\n")
	print("Write to output file success!")

	f.close()

	# r = api.search(q=stock_name, since="2017-11-01", lang="en")
	# print("Total number of tweets fetched from page ", pageNum, "is: ", len(r))
	# for tweet in r:
	# 	# print(tweet._json)

	# 	# Remove emojis, hashtags, and URLS 
	# 	cleanedStr = tweetPreprocessor.clean(tweet.text)

	# 	# Tokenize cleaned tweet into a string of words (separated by spaces)
	# 	tokenizedStr = tweetPreprocessor.tokenize(cleanedStr)

	# 	# Convert tokenized string to list of strings
	# 	tokenizedStrList = tokenizedStr.split();

	# 	# print("************************************************************")
	# 	# print("----> Original String:", tweet.text)
	# 	# print("----> Tokenized String List:", tokenizedStrList)
	# 	# print("************************************************************")
