key = "c268c7f360854a62ae033b75205b916c"
endpoint = "https://openbooknlp.cognitiveservices.azure.com/"

# from azure.ai.textanalytics import single_analyze_sentiment
# from azure.ai.textanalytics import single_detect_language
# from azure.ai.textanalytics import single_recognize_entities

from flask import Flask
from datetime import datetime
from flask import render_template
import re
from bs4 import BeautifulSoup 
import requests as req

from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))

from urllib.request import urlopen as uReq


app = Flask(__name__)
def getText():
    print("test")
    my_url="http://127.0.0.1:8080"
   
    uClient = uReq(my_url)
    page_html = uClient.read()
    soup = BeautifulSoup(page_html, 'html.parser')

    # html parsing
    
 

    text=soup
    print(text)
    print("df","james")
    return text

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    print("start")
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    print("data")
    return app.send_static_file("data.json")

# Replace the existing home function with the one below
@app.route("/")
def home():
    print("homey1")
    
    return render_template("home.html")

# New functions
@app.route("/about/")
def about():
    getText()
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

def detect_language():
        # [START batch_detect_language]
        documents = [
            getText()
        ]

        result = text_analytics_client.detect_language(documents)
        print("pin")
        for idx, doc in enumerate(result):
            if not doc.is_error:
                print("Document text: {}".format(documents[idx]))
                print("Language detected: {}".format(doc.primary_language.name))
                print("ISO6391 name: {}".format(doc.primary_language.iso6391_name))
                print("Confidence score: {}\n".format(doc.primary_language.score))
            if doc.is_error:
                print(doc.id, doc.error)
        # [END batch_detect_language]

def extract_key_phrases():
        # [START batch_extract_key_phrases]
        documents = [
           getText()
        ]
        print("ex")
        result = text_analytics_client.extract_key_phrases(documents)
        for doc in result:
            if not doc.is_error:
                print(doc.key_phrases)
            if doc.is_error:
                print(doc.id, doc.error)
        # [END batch_extract_key_phrases]

def analyze_sentiment():
        # [START batch_analyze_sentiment]
        documents = [
            getText()
        ]
        print("din")
        result = text_analytics_client.analyze_sentiment(documents)
        docs = [doc for doc in result if not doc.is_error]

        for idx, doc in enumerate(docs):
            print("Document text: {}".format(documents[idx]))
            print("Overall sentiment: {}".format(doc.sentiment))
        # [END batch_analyze_sentiment]
            print("Overall scores: positive={0:.3f}; neutral={1:.3f}; negative={2:.3f} \n".format(
                doc.sentiment_scores.positive,
                doc.sentiment_scores.neutral,
                doc.sentiment_scores.negative,
            ))
            for idx, sentence in enumerate(doc.sentences):
                print("Sentence {} sentiment: {}".format(idx+1, sentence.sentiment))
                print("Sentence score: positive={0:.3f}; neutral={1:.3f}; negative={2:.3f}".format(
                    sentence.sentiment_scores.positive,
                    sentence.sentiment_scores.neutral,
                    sentence.sentiment_scores.negative,
                ))
                print("Offset: {}".format(sentence.offset))
                print("Length: {}\n".format(sentence.length))
            print("------------------------------------")

# def sentiment_analysis_example(endpoint, key):

#     document = "I had the best day of my life. I wish you were there with me."

#     response = single_analyze_sentiment(endpoint=endpoint, credential=key, input_text=document)
#     print("Document Sentiment: {}".format(response.sentiment))
#     print("Overall scores: positive={0:.3f}; neutral={1:.3f}; negative={2:.3f} \n".format(
#         response.document_scores.positive,
#         response.document_scores.neutral,
#         response.document_scores.negative,
#     ))
#     for idx, sentence in enumerate(response.sentences):
#         print("[Offset: {}, Length: {}]".format(sentence.offset, sentence.length))
#         print("Sentence {} sentiment: {}".format(idx+1, sentence.sentiment))
#         print("Sentence score:\nPositive={0:.3f}\nNeutral={1:.3f}\nNegative={2:.3f}\n".format(
#             sentence.sentence_scores.positive,
#             sentence.sentence_scores.neutral,
#             sentence.sentence_scores.negative,
#         ))

            
# sentiment_analysis_example(endpoint, key)




# def language_detection_example(endpoint, key):
#     try:
#         document = "Ce document est rédigé en Français."
#         response = single_detect_language(endpoint=endpoint, credential=key, input_text= document)
#         print("Language: ", response.primary_language.name)

#     except Exception as err:
#         print("Encountered exception. {}".format(err))
# language_detection_example(endpoint, key)



# def entity_recognition_example(endpoint, key):

#     try:
#         document = "I had a wonderful trip to Seattle last week."
#         result = single_recognize_entities(endpoint=endpoint, credential=key, input_text= document)
        
#         print("Named Entities:\n")
#         for entity in result.entities:
#                 print("\tText: \t", entity.text, "\tType: \t", entity.type, "\tSubType: \t", entity.subtype,
#                       "\n\tOffset: \t", entity.offset, "\tLength: \t", entity.offset, 
#                       "\tConfidence Score: \t", round(entity.score, 3), "\n")

#     except Exception as err:
#         print("Encountered exception. {}".format(err))
# entity_recognition_example(endpoint, key)

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)