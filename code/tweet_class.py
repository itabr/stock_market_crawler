from stop_word import *
import csv
import nltk
from nltk.tokenize import word_tokenize
import re

def tweet_trainer(f_training):
	reader = csv.reader(f_training)
	tweets = []
	for row in reader:
		sentiment = row[0]
		timestamp = row[1]
		processedTweet = clean_tweet(row[2])
		tweets.append((processedTweet,sentiment))

	all_words = set(word.lower() for tweet in tweets for word in word_tokenize(tweet[0]))
	t = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in tweets]
	classifier = nltk.NaiveBayesClassifier.train(t)
	#classifier.show_most_informative_features()

	return (classifier,all_words)


def tweet_classyfier(f_testing,f_output,classifier,all_words):
	reader_testing = csv.reader(f_testing)
	for row in reader_testing:
		timestamp = row[0]
		processedTweet = clean_tweet(row[1])
		test_sent_features = {word.lower(): (word in word_tokenize(processedTweet.lower())) for word in all_words}
		sentiment = classifier.classify(test_sent_features)
		
		line = sentiment + "," + timestamp + "," + processedTweet
		f_output.write(line)
		f_output.write('\n')

		print(sentiment,timestamp,processedTweet)





f_training = open("../tweet_training_tesla.csv", 'r', encoding='mac_roman', newline='')
f_testing = open("../tweets_tesla.csv", 'r', encoding='mac_roman', newline='')
f_output = open("tweets_classifed_using_classifier.csv","w+")

train = tweet_trainer(f_training)

tweet_classyfier(f_testing,f_output,train[0],train[1])
