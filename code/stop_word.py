from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
import re
def swremover(tweet):
	text = ' '.join([word for word in tweet.split() if word not in ENGLISH_STOP_WORDS])
	return text

def replaceTwoOrMore(tweet):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", tweet)

def getFeatureVector(tweet):
	featureVector = []
	tweet = swremover(tweet)
	words = tweet.split()
	for w in words:
		w = replaceTwoOrMore(w)
		w = w.strip('\'"?,.')
		val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)

		featureVector.append(w.lower())
	return featureVector
