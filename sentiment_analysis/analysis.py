import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import nltk
nltk.download("punkt")
nltk.download("stopwords")
from nltk.corpus import stopwords
import string
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from sklearn.naive_bayes import GaussianNB,MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import StackingClassifier

class analyzer():
    def __init__(self):
        self.stop=stopwords.words("english")
        self.re=re
        self.joblib=joblib
        self.punctuation=string.punctuation
        self.stem=PorterStemmer()
        self.TfidfVectorizer=TfidfVectorizer
        self.word_tokenize=word_tokenize
        self.LogisticRegression=LogisticRegression
        self.MultinomialNB=MultinomialNB
        self.clean="@\S+|https?:\S+|http?:\S|"
        self.full_words={"can't":"can not","aren't":"are not","isn't":"is not","that's":"that is","i'm":"i am","it's":"it is"}
    def preprocess(self,text):
        corp=self.re.sub(self.clean,"",str(text).lower())
        words=self.word_tokenize(corp)
        out=""
        for i in words:
            if i not in self.stop and self.punctuation:
                out+=" "+self.stem.stem(i)
        
        V=joblib.load('saved_V')
        transformed=V.transform([out])
        return transformed
        



    def output(self,text):
        self.nb=self.MultinomialNB()
        self.lr=self.LogisticRegression(n_jobs=-1,random_state=32)
        stacking=self.joblib.load('stacked_model')
        out=self.preprocess(text)
        result=stacking.predict(out)
       
        if result == 0:
            return 0
            # print(f"{text} ==> Negative sentiment")

        if result == 4:
            return 1
            # print(f"{text} ==>Positive sentiment")
