import tweepy
import preprocessor as tweetPreprocessor
import json
import time

consumer_key = "WMBaLdmJmWysb7kisqdKBD3Wd"
consumer_secret = "mrCiHxnSv7ZV5HsC1Sywu44N7R0n3x4d4wmiSTszNt50Gq5ObX"
access_token = "926633743841771520-gcJR5HWYH5pcneR0gJnP73jxuFdsgKC"
access_token_secret = "4iNT66uZmufHLh79wkhz4WyI7tW0TrGkWW4auxRczbLcX"

if __name__ == "__main__":

	# stock_name = "AAPL", "iPhone", "apple", "stock"
	# stock_name = "Apple", "stock", "win", "dow"
	# print(stock_name)

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	# request tweet
	f = open("tweet_generated_tesla_alot.csv", "w+")


	query_list = [("Tesla","stock")]
	# query_list = [("Tesla", "stock", "dow", "win"), ("Tesla", "stock", "lose"), ("Tesla", "stock", "win"), ("Tesla", "stock", "up"), ("Tesla", "stock", "down"), ("Tesla", "stock")]
	max_tweets=1500
	tweet_set = set()
	for query in query_list:
		searched_tweets = [status._json for status in tweepy.Cursor(api.search, q=query, lang="en").items(max_tweets)]
		json_strings = [json.dumps(json_obj) for json_obj in searched_tweets]
		for json_obj in searched_tweets:
			# tweet_text = tweetPreprocessor.clean(json_obj["text"]).replace(',', '')
			tweet_text = json_obj["text"].replace(',', '').replace('\n', ' ')
			if (tweetPreprocessor.clean(tweet_text) in tweet_set): continue
			tweet_set.add(tweetPreprocessor.clean(tweet_text))
			f.write(json_obj["created_at"])
			f.write(',')
			f.write(tweet_text)
			f.write("\n")
		print("Write to output file success for query ", query)
		print("sleep 1 second")
		time.sleep(1)
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
