from flask import Flask, render_template
import requests
import json
from typing import Text
from bs4 import BeautifulSoup
import requests
import os
import sys
import datetime
from pprint import pprint
from operator import itemgetter

URL = 'https://stackoverflow.com/questions/tagged/android'

def scrape_question_page(url):
    # Function to scrap a single page
    response = requests.get(url)
    page_questions = []
    soup = BeautifulSoup(response.text, 'html.parser')
    question_summary = soup.find_all('div', class_='inner-content clearfix')
    for summary in question_summary:
        question_title = summary.find(class_='question-hyperlink').text
        description = summary.find(class_='s-prose js-post-body')
        question_answer_all = summary.find_all('div', class_="answercell post-layout--right")
        up_votes = summary.find_all('div',class_='js-vote-count flex--item d-flex fd-column ai-center fc-black-500 fs-title')
        print(up_votes)
        q = []
        v = []
        for i in up_votes:
            v.append(i.text.strip())
        
        que_vote = v[0]
        comment_vote = v[1:]
        counter = 0
        for i in question_answer_all:
            q.append({ 
                'comment_vote': comment_vote[counter],
                'html_data': i.find(class_='s-prose js-post-body')
            })
            counter += 1
            #print(q)
        print(q)

        page_questions.append({
            'question': question_title,
            'description': description,
            'answers': q,
            'question_votes': que_vote,
            'comment_vote': comment_vote,
            'url': url
        })
    return page_questions
        

def scrape(url):
    # To scrap multiple pages
    questions = []
    print(url)
    page_questions = scrape_question_page(url)
    
    return page_questions

