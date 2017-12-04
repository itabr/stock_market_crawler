from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

def swremover(text):
	text = ' '.join([word for word in text.split() if word not in ENGLISH_STOP_WORDS])
	return text
