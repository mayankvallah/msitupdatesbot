from bs4 import BeautifulSoup
import requests
import os
import psycopg2
import sqlite3 as lite
import schedule



def crawlingNews():
    #'''
    #Args: website_link = string; link of website to be crawled
          #link_class = string; class name for job link on website
    #Returns: jobs_link = list; list of jobs 
    #'''
    
    website_request = requests.get('http://msit.in/latest_news')
    website_content = BeautifulSoup(website_request.content, 'html.parser')

    #extract job description
    jobs_link = website_content.select('div.tab-content a')
    return jobs_link
    #links = []
    #titles = []
    #x = 0

    #for anchors in main_div:
        #titles.append(anchors.text)
        #links.append(f"http://msit.in/media/news{anchors['href']}\n\n")
    
    

def crawlingNotice():
    #'''
    #Args: website_link = string; link of website to be crawled
          #link_class = string; class name for job link on website
    #Returns: jobs_link = list; list of jobs 
    #'''
    
    website_request = requests.get('http://msit.in/notices')
    website_content = BeautifulSoup(website_request.content, 'html.parser')

    #extract job description
    notices_link = website_content.select('div.tab-content a')
    return notices_link
    #links = []
    #titles = []
    #x = 0


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def send_message(chat_id, text, doc):
    TOKEN = "1638409055:AAHgC5KE51zFqpLZbw5V5qXRfzdKeczlL-c"
    URL = "https://api.telegram.org/bot{}/".format(TOKEN)
    url = URL + f"sendDocument?chat_id=-1001454545667&caption={text}&document={doc}"
    print(url)
    get_url(url)
    
    #parameters = {'chat_id': chat_id, 'text': text}
    #message = requests.post("1638409055:AAHgC5KE51zFqpLZbw5V5qXRfzdKeczlL-c" + 'sendMessage', data=parameters)



def check_result_send_mess():    
    try:
       DATABASE_URL = os.environ['DATABASE_URL']
       conn = psycopg2.connect(DATABASE_URL, sslmode='require')
       jobs_db = conn.cursor()
       jobs_db.execute('CREATE TABLE IF NOT EXISTS jobs (id SERIAL, job TEXT NOT NULL)')
    except:
       send_message(chat_id, 'The database could not be accessed')

    jobs_link_pm = crawlingNews()
    notices_link = crawlingNotice()
    
    for item in reversed(jobs_link_pm):
        job_exists = jobs_db.execute('SELECT job FROM jobs WHERE job = %s', [item.text])
        
        if len(jobs_db.fetchall()) != 1:
            mess_content = f"LATEST NEWS: {item.text}"
            doc = f"http://msit.in{item['href']}"
            print(doc)
            send_message("-1001454545667", mess_content, doc)
            jobs_db.execute('INSERT INTO jobs (job) VALUES (%s);', [item.text])
            conn.commit()
        else:
            continue
        
    for item in reversed(notices_link):
        job_exists = jobs_db.execute('SELECT job FROM jobs WHERE job = %s', [item.text])
        
        if len(jobs_db.fetchall()) != 1:
            mess_content = f"LATEST NOTICE: {item.text}"
            doc = f"http://msit.in{item['href']}"
            print(doc)
            send_message("-1001454545667", mess_content, doc)
            jobs_db.execute('INSERT INTO jobs (job) VALUES (%s);', [item.text])
            conn.commit()
        else:
            continue

    jobs_db.close()
    
    
    
    
    
    
    
# bot and chat ids
bot = "1638409055:AAHgC5KE51zFqpLZbw5V5qXRfzdKeczlL-c"
chat_id = "-1001454545667"
check_result_send_mess()
#schedule crawler
schedule.every().hour.do(check_result_send_mess)
while True:
    schedule.run_pending()
