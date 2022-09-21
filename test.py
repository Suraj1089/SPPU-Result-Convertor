import nltk
import string 
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.metrics import accuracy_score

###########################################################################
messages = pd.read_csv('SMSSpamCollection',sep='\t',names=['label','message'])


#############################################################################
def text_process(mess):
  """
    1. remove puntuation
    2.remove stop words
    3.return list of clean data
  """
  no_punct = ''.join([words for words in mess if words not in string.punctuation])
  no_punct = no_punct.split()
  preprocessed_text = [word for word in no_punct if word.lower() not in stopwords.words('english')]
  return preprocessed_text


###########################################################################
#splitting the data
#split the data 
X = messages['message']
y = messages['label']
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=42)


##################################################################################
#create a pipline
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer,CountVectorizer
import pickle

pipeline = Pipeline(
    [
        ('vectorize',CountVectorizer()),
        ('tfidf',TfidfTransformer()),
        ('classifier_model',MultinomialNB())
    ]
)

pipeline.fit(X_train,y_train)
predictions = pipeline.predict(X_test)
pickle.dump(pipeline,open('spammodel.pkl','wb'))
accurency = accuracy_score(y_test,predictions)

