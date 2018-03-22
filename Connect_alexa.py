from flask import Flask
from flask_ask import Ask, statement, question, session
import json ##interact with redit api
import requests ## interact with redit api
import time
import unidecode
import os, sys

app = Flask(__name__)
ask = Ask(app,"/")

def get_headlines():
    user_pass_dict = {'user' : 'Username',
                      'passwd' : 'Pass',
                      'api_type' : 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent' : 'I am testing Alexa'})
    sess.post('https://www.reddit.com/api/login',data = user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/worldnews/.json?limit=10'
    html =  sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data ['data']['children']]
    titles='...'.join([i for i in titles])
    return titles


@app.route('/')
def homepage():
    #print ("Alex connect")
    return "hi there, how ya doing ?"

@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like the news ?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headlines_msg = 'The current world news headlines are {}'.format(headlines)
    return statement(headlines_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text="I am not sure why you asked me to run"
    return statement(bye_text)

@ask.intent ("readPapan")
def just_papan ():
    papan_txt="kadak"
    return statement(papan_txt)

@ask.intent ("Runjob_EOC")
def job_run ():
    a = 'mkdir nwdir'
    b = os.popen(a, 'r', 1)
    print (b)
    job_txt="already ran the make dir command , please check if the dir is created"
    return statement(job_txt)

if __name__ == '__main__':
    app.run(debug=True)
    #app.run()




