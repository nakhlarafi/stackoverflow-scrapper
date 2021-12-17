import requests
from typing import Text
from bs4 import BeautifulSoup
import requests
import datetime
from datetime import date
from operator import itemgetter

URL = 'https://stackoverflow.com/questions/tagged/android'
PAGE_LIMIT = 1000000000000

'''
Generatates an URL of the pages
'''
def build_url(base_url=URL, tab='newest', page=1, page_size=50):
    return f"{base_url}?tab={tab}&page={page}&{page_size}" # example: stackoverflow

'''
This function scraps all the pages that contain questions of the past 7 days
'''
def scrape_page_v2(page=1):
    today_date = str(date.today()).split('-')
    today_date = list(map(int, today_date))
    date1 = datetime.date(today_date[0], today_date[1], today_date[2])
    week_gap = datetime.timedelta(7)
    date1 = date1 - week_gap

    # Function to scrap a single page
    print(page)
    response = requests.get(build_url(page=page))
    page_questions = []
    soup = BeautifulSoup(response.text, 'html.parser')
    question_summary = soup.find_all('div', class_='question-summary')
    for summary in question_summary:
        post_time = summary.find(class_='relativetime')
        post_fulltime = post_time['title'].split(' ')[0].split('-')
        post_fulltime = list(map(int, post_fulltime))
        date2 = datetime.date(post_fulltime[0], post_fulltime[1], post_fulltime[2])
        if date2 >= date1:
            
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
        else:
            return False, page_questions
    return page_questions
        

def scrape_for_week():
    questions = []
    for i in range(1,PAGE_LIMIT + 1):
        page_questions = scrape_page_v2(i)
        if page_questions[0] == False:
            questions.extend(page_questions[1])
            break
        else:
            questions.extend(page_questions)
            
    sorted_list = sorted(questions, key=itemgetter('votes'), reverse=True)
    return sorted_list
