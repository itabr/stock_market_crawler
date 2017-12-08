from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
import re
from nltk.tokenize import word_tokenize
import preprocessor as tweetPreprocessor

def swremover(tweet):
	text = ' '.join([word for word in tweet.split() if word not in ENGLISH_STOP_WORDS])
	return text

def replaceTwoOrMore(tweet):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", tweet)

def clean_tweet(tweet):
	processedTweet = tweetPreprocessor.clean(tweet)
	processedTweet = swremover(processedTweet)
	processedTweet = replaceTwoOrMore(processedTweet)
	processedTweet = re.sub('[^A-Za-z0-9]+', ' ', processedTweet)
	return processedTweet
