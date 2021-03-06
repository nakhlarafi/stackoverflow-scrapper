from bs4.element import Comment
from flask import Flask, render_template
import requests
from typing import Text
from bs4 import BeautifulSoup
from operator import itemgetter

URL = 'https://stackoverflow.com/questions/tagged/android'

'''
Scraps the answers and top voted comment of the question. It also takes the accepted answer from the user and shows it in the first answer.
'''

def scrape_question_page(url):
    # Function to scrap a single page
    response = requests.get(url)
    page_questions = []
    soup = BeautifulSoup(response.text, 'html.parser')
    question_title = soup.find('a', class_='question-hyperlink').text

    question = soup.find('div', class_='question')
    question_description = question.find('div', class_='s-prose js-post-body')
    question_vote = question.find('div', class_="js-vote-count flex--item d-flex fd-column ai-center fc-black-500 fs-title").text
    
    question_comments = question.find_all('li', class_='comment js-comment')
    #print(question_comments)
    

    comment_list = []
    for c in question_comments:
        comment_vote = c.find(class_='comment-score js-comment-edit-hide').text.strip()
        
        if comment_vote == '':
            comment_vote = '0'

        comment_description = c.find(class_='comment-copy')
        
        comment_list.append({
            'comment_vote' : int(comment_vote),
            'comment_desc' : comment_description
        })
    if len(comment_list) > 0:
        comment_list = sorted(comment_list, key=itemgetter('comment_vote'), reverse=True)
    else:
        comment_list = [{
            'comment_vote' : 0,
            'comment_desc' : "No comments"
        }]

    question_list = [{
        'question_title': question_title,
        'question_description': question_description,
        'question_vote': question_vote,
        'question_url': url
    }]

    answers = soup.find_all('div', class_='answer')
    answers_count = 0
    answer_list = []
    for a in answers:
        answer_vote = a.find(class_='js-vote-count flex--item d-flex fd-column ai-center fc-black-500 fs-title').text.strip()
        answer_body = a.find(class_='s-prose js-post-body')
        answer_accepted = a.find(class_='js-accepted-answer-indicator flex--item fc-green-500 py6 mtn8')
        if answer_accepted != None:
            acceptance = True
        else:
            acceptance = False
        answer_list.append({
            'answer_vote': answer_vote,
            'answer_body': answer_body,
            'answer_accepted': acceptance
        })
        answers_count += 1
    
    page_questions = [question_list,answer_list, answers_count, comment_list[0]]

    return page_questions
        

def scrape(url):
    # To scrap multiple pages

    page_questions = scrape_question_page(url)
    
    return page_questions

