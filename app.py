from flask import Flask, render_template, request
import requests
import json
from typing import Text
from bs4 import BeautifulSoup
import requests
import recent_que
import top_voted_question
import inside_que



app = Flask(__name__)

"""
Calls the function that generates the top 10 most
voted questions in the past week
"""
@app.route('/top_voted_question')
def top_weekly_posts():
    questions_gathered = top_voted_question.scrape_for_week()
    que = questions_gathered[0:10]
    return render_template('index.html', que=que, scrape_method='Top 10 Most Voted Android related questions')

"""
Calls the function that generates the top 10 
newest questions
"""
@app.route('/recent_que')
def top_recent_questions():
    questions_gathered = recent_que.scrape()
    que = questions_gathered[0:10]
    return render_template('index.html', que=que, scrape_method='Most Recent 10 Questions')
"""
Calls the function that shows the full thread
"""
@app.route('/inside_que')
def question_inside():
    url = request.args.get('url')
    questions_gathered = inside_que.scrape(url)
    return render_template('que.html', que=questions_gathered[0], ans=questions_gathered[1], count = questions_gathered[2])

"""
Home page call
"""
@app.route('/')
def get_beer():
    questions_gathered = recent_que.scrape()
    que = questions_gathered[0:10]
    #print(beer)
    return render_template('index.html', que=que, scrape_method='Most Recent 10 Questions')