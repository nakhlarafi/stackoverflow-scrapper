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
PAGE_LIMIT = 1000000000000

app = Flask(__name__)

def build_url(base_url=URL, tab='newest', page=1, page_size=15):
    return f"{base_url}?tab={tab}&page={page}&{page_size}" # example: stackoverflow

def scrape_page_v2(page=1):
    # Function to scrap a single page
    response = requests.get(build_url(page=page))
    page_questions = []
    soup = BeautifulSoup(response.text, 'html.parser')
    question_summary = soup.find_all('div', class_='question-summary')
    for summary in question_summary:
        post_time = summary.find(class_='relativetime')
        post_fulltime = post_time['title'].split(' ')[0].split('-')
        post_fulltime = list(map(int, post_fulltime))
        question = summary.find(class_='question-hyperlink').text
        link = 'https://stackoverflow.com'+summary.find(class_='question-hyperlink')['href']
        description = summary.find(class_='excerpt').text.strip().replace('\n',' ')
        vote_count = summary.find(class_='vote-count-post').find('strong').text
        answer_count = summary.find(class_='status').find('strong').text
        view_count = summary.find(class_='views').text.split()[0]
        time = summary.find(class_='relativetime').text
        page_questions.append({
            'question':question,
            'description':description,
            'answer':answer_count,
            'views':view_count,
            'votes':vote_count,
            'time':time,
            'post_time':post_fulltime,
            'page_count': page,
            'link': link
        })
    return page_questions
        

def scrape():
    # To scrap multiple pages
    questions = []
    page_questions = scrape_page_v2(1)
    questions.extend(page_questions)
    return questions

