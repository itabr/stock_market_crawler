from stop_word import *
import csv
import nltk
from nltk.tokenize import word_tokenize
import re

def featureListgenerator(f):
	reader = csv.reader(f)
	tweets = []
	for row in reader:
		sentiment = row[0]
		timestamp = row[1]
		processedTweet = clean_tweet(row[2])
		tweets.append((processedTweet,sentiment))

	all_words = set(word.lower() for tweet in tweets for word in word_tokenize(tweet[0]))
	t = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in tweets]
	classifier = nltk.NaiveBayesClassifier.train(t)
	classifier.show_most_informative_features()

	test_sentence = "tesla stock price is going down bad terible"
	test_sent_features = {word.lower(): (word in word_tokenize(test_sentence.lower())) for word in all_words}

	print(classifier.classify(test_sent_features))





f = open("../tweet_training_tesla.csv", 'r', encoding='mac_roman', newline='')

featureListgenerator(f)
