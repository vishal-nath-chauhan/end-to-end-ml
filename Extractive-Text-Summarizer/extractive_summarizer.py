

#Extractive text summarizer 
import nltk
nltk.download("punkt")
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.stem import PorterStemmer
import bs4 as BeautifulSoup
import urllib.request
import re

##this function will dictionary of frequency of words
class text_summarizer():
    
    def __init__(self,link):
        self.link=str(link)
        self.stopwords=stopwords
        self.word_tokenize=word_tokenize
        self.sent_tokenize=sent_tokenize
        self.PorterStemmer=PorterStemmer
        self.BeautifulSoup=BeautifulSoup
        self.urllib=urllib.request
        self.re=re
    def get_data(self,link):
        fetched_data = urllib.request.urlopen(str(link))
        article_read = fetched_data.read()
        article_parsed = BeautifulSoup.BeautifulSoup(article_read,'html.parser')
        paragraphs = article_parsed.find_all('p')
        article_content = ''
        for p in paragraphs:  
            article_content += p.text
        article_content=re.sub(r"\[\d+\]"," ",article_content)
        return article_content    
    def create_dict(self,text):
        sent=text.lower()
        freq_dict=dict()
        stem=PorterStemmer()
        stopword=set(stopwords.words("english"))
        words=word_tokenize(sent)
        
        for word in words:
            
            word=stem.stem(word)
            
            if word in stopword:
                continue
            if word in freq_dict:
                freq_dict[word]+=1
            else:
                freq_dict[word]=1
        return freq_dict


#this fucntion will give weight to every sentence
    def sentence_weight(self,sentences,freq_dict):
        sent_weight=dict()
        for sent in sentences:
            word_count=len(word_tokenize(sent))
            sent_without_stopwords=0
            for word in freq_dict:
                if word in sent.lower():
                    sent_without_stopwords+=1
                    if sent[:7] in sent_weight:
                        sent_weight[sent[:7]]+=freq_dict[word]
                    else:
                        sent_weight[sent[:7]]=freq_dict[word] 
            sent_weight[sent[:7]]=sent_weight[sent[:7]]/sent_without_stopwords
        return sent_weight

#calculating average
    def calculate_avg(self,sent_weight):
        sum_values=0
        for entry in sent_weight:
            sum_values+=sent_weight[entry]
        avg_score=(sum_values/len(sent_weight))

        return avg_score

#generating 
    def get_summary(self,sentences,sent_weight,threshold):        
        summary=""
        counter=0
        for sent in sentences:
            if sent[:7] in sent_weight and sent_weight[sent[:7]]>=threshold:
                summary+=sent
        return summary

    def output(self):
        content=self.get_data(self.link)
        freq_dict=self.create_dict(content)
        text=self.sent_tokenize(content)
        sent_weight=self.sentence_weight(text,freq_dict)
        average=self.calculate_avg(sent_weight)
        summary=self.get_summary(text,sent_weight,1.5*average)            
        out=summary.split("\n")
        processed_output=""
        for i in out:
            if i =="":
                continue
            processed_output+=i

        return processed_output

# output=text_summarizer("https://en.wikipedia.org/wiki/India")
# print(output.output())
