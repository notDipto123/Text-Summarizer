import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from flask import Flask, request, render_template
from lib2to3.pgen2 import token
from string import punctuation
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import heapq

punctuation = punctuation+'\n'
stwords = list(STOP_WORDS)
stopword = stopwords.words('english')


nlp = spacy.load('en_core_web_sm')

def nltk_sum(text,n):
    word_frequency = {}
    for word in nltk.word_tokenize(text):
        if word.lower() not in stopword:
            if word.lower() not in punctuation:
                if word not in word_frequency.keys():
                    word_frequency[word] = 1
                else:
                    word_frequency[word] += 1

    max_frequency = max(word_frequency.values())
    for word in word_frequency.keys():
        word_frequency[word] = (word_frequency[word]/max_frequency)


    sentences = nltk.sent_tokenize(text)
    sentences_value = {}
    for sent in sentences:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequency.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentences_value.keys():
                        sentences_value[sent] = word_frequency[word]
                    else:
                        sentences_value[sent] += word_frequency[word]


    summary_sentences = heapq.nlargest(int(len(sentences)*float(n)*0.01), sentences_value, key=sentences_value.get)

    summary1 = ' '.join(summary_sentences)
    return summary1

def spacy_sum(a,n):
    document = nlp(a)
    tokens = [ token.text for token in document]

    
    frequency = {}
    for i in document:
        if i.text.lower() not in STOP_WORDS:
            if i.text.lower() not in punctuation:
                if i.text not in frequency.keys():
                    frequency[i.text]  = 1
                else:
                    frequency[i.text] += 1



    max_frequency = max(frequency.values())
    for i in frequency.keys():
        frequency[i] = frequency[i]/max_frequency


    sentances_token = [sent for sent in document.sents]
    sentance_value = {}
    for i in sentances_token:
        for j in i:
            if j.text.lower() in frequency.keys():
                if i not in sentance_value.keys():
                    sentance_value[i] = frequency[j.text.lower()]
                else:
                    sentance_value[i] += frequency[j.text.lower()]


    valid_sentance = int(len(sentances_token)*float(n)*0.01)
    summary2 = nlargest(valid_sentance, sentance_value, key=sentance_value.get)

    b = [i.text for i in summary2]

    summary2 = ' '.join(b)
    return summary2


app = Flask(__name__)  
 

@app.route('/', methods =["GET", "POST"])
def op():
    if request.method == "POST":
        text = request.form.get("ftxt")
        num = request.form.get("fnam")
        choice = request.form.get("falgo")
        choice = str(choice)
        if choice == "Spacy":
            s = spacy_sum(text,num)
        elif choice == "NLTK":
            s = nltk_sum(text,num)
        else:
            s = "Error selecting algorithm" 
        return render_template("result.html", summ = s, algo = choice+" algorithm:")
    return render_template("front.html")
 
if __name__=='__main__':
   app.run(debug=True)





