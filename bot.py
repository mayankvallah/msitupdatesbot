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

def crawlingMarq():
    #'''
    #Args: website_link = string; link of website to be crawled
          #link_class = string; class name for job link on website
    #Returns: jobs_link = list; list of jobs 
    #'''
    
    website_request = requests.get('http://msit.in/')
    website_content = BeautifulSoup(website_request.content, 'html.parser')

    #extract job description
    marq_link = website_content.select('div.marquee-text a')
    return marq_link
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

def send_marq(chat_id, text, doc):
    TOKEN = "1638409055:AAHgC5KE51zFqpLZbw5V5qXRfzdKeczlL-c"
    URL = "https://api.telegram.org/bot{}/".format(TOKEN)
    url = URL + f"sendMessage?chat_id=-1001454545667&parse_mode=html&text={text} \n {doc}"
    print(url)
    get_url(url)

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
    marquee_link = crawlingMarq()
    for item1,item2 in zip(reversed(jobs_link_pm),reversed(notices_link)):
        job_exists = jobs_db.execute('SELECT job FROM jobs WHERE job = %s', [item1.text])
        job_exists = jobs_db.execute('SELECT job FROM jobs WHERE job = %s', [item2.text])
        
        if len(jobs_db.fetchall()) != 1:
            news_content = f"LATEST NEWS: {item1.text}"
            news_doc = f"http://msit.in{item1['href']}"
            send_message("-1001454545667", news_content, news_doc)
            
            notices_content = f"LATEST NOTICE: {item2.text}"
            notices_doc = f"http://msit.in{item2['href']}"
            send_message("-1001454545667", notices_content, notices_doc)
            jobs_db.execute('INSERT INTO jobs (job) VALUES (%s);', [item1.text])
            jobs_db.execute('INSERT INTO jobs (job) VALUES (%s);', [item2.text])
            conn.commit()
        else:
            continue
        
    for item in reversed(marquee_link):
        job_exists = jobs_db.execute('SELECT job FROM jobs WHERE job = %s', [item.text])
        
        if len(jobs_db.fetchall()) != 1:
            mess_content = f"<b>Newsflash!</b>: {item.text}"
            checker = item['href'].find("media")
            if checker!=-1:
                doc = f"http://msit.in{item['href']}"
            else:
                doc = f"{item['href']}"
            print(doc)
            send_marq("-1001454545667", mess_content, doc)
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
#schedule.every().hour.do(check_result_send_mess)
#while True:
    #schedule.run_pending()
