import pathlib
import sys
import json
from readability import Document
from bs4 import BeautifulSoup
from flask import Flask,jsonify
import requests
from flask import request
import logging
import os

from torch import res
import TextSummary as Ts
import FactCheck as Fc
import TextNet as Tn
import DocumentNet as Dn
import HtmlContent as hc
import relevancescorerupdated as Rs
from sentence_transformers import SentenceTransformer, util
import multipro as mp
import SearchBrowser as sb
import queue
import threading
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
import trafilatura
import time, random

app = Flask(__name__)
logging.disable(logging.WARNING)
log = logging.getLogger('werkzeug')
log.disabled = True
classify = []

model = SentenceTransformer("all-mpnet-base-v2")


selenium_queue = queue.Queue()


def create_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")    
    options.add_argument("--disable-features=OptimizationGuideModelDownloading,OptimizationHints")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-background-networking")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    service = Service(
        executable_path="D:/Python/Projects/FindMore/chromedriver_win32/chromedriver.exe"
    )

    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    driver.set_page_load_timeout(60)
    driver.set_script_timeout(20)

    return driver


def get_with_retry(driver, url, retries=2):
    for attempt in range(1, retries + 1):
        try:
            driver.get(url)
            return
        except TimeoutException:
            raise                                   # let your existing handler salvage the DOM
        except WebDriverException as e:
            if "ERR_CONNECTION" in str(e) and attempt < retries:
                wait = 2 ** attempt + random.uniform(0, 2)
                print(f"Connection reset ({url}), retry {attempt}/{retries} in {wait:.0f}s")
                time.sleep(wait)
                continue
            raise 

def selenium_worker():
    driver = None
    try:
        driver = create_driver()
        driver.set_page_load_timeout(30)
        print("Selenium Chrome started")
        while True:
            job = selenium_queue.get()
            try:
                if job is None:
                    break

                url = job["url"]
                result_queue = job["result_queue"]
                timed_out = False
                try:
                    get_with_retry(driver, url)
                except TimeoutException:
                    timed_out = True
                    print("PAGE LOAD TIMEOUT:", url)

                    # Stop further loading and try to get partial HTML.
                    try:
                        driver.execute_script("window.stop();")
                    except WebDriverException:
                        pass

                html = driver.page_source

                result_queue.put({"ok": True,"html": html,"timed_out": timed_out})

            except Exception as e:
                if job is not None:
                    job["result_queue"].put({"ok": False,"error": str(e)})
            finally:
                selenium_queue.task_done()
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception as e:
                print("Error closing Chrome:", e)

        print("Selenium Chrome stopped")



selenium_thread = threading.Thread(
    target=selenium_worker,
    daemon=True
)

selenium_thread.start()


@app.route("/hello")
def hello():
    return "Hello World!"

@app.route('/GetTextSummary', methods=['POST'])
def GetTextSummary():
    event_data = request.json
    token = event_data["Token"]    
    id = event_data["Id"]    
    url = event_data["Url"]   
    trans = Ts.ExtractDetailSummary(hc,token,id,url)
    return trans

@app.route('/GetContentSummary', methods=['POST'])
def GetContentSummary():
    event_data = request.json
    token = event_data["Token"]    
    id = event_data["Id"]    
    content = event_data["Content"]   
    print(content)
    trans = Ts.ExtractTextSummary(hc,token,id,content)
    return trans    

@app.route('/GetFactCheck', methods=['POST'])
def GetFactCheck():
    event_data = request.json
    token = event_data["Token"]    
    id = event_data["Id"]    
    url = event_data["Url"]    
    claims = event_data["Claims"]    
    mods = Fc.ValidateFactCheck(token,id,claims,url)
    return mods

@app.route('/GetFactCheckContent', methods=['POST'])
def GetFactCheckContent():
    event_data = request.json
    token = event_data["Token"]    
    id = event_data["Id"]        
    content = event_data["Text"] 
    claims = event_data["Claims"]      
    mods = Fc.ValidateFactCheckOnContent(token,id,claims,content)
    return mods


@app.route('/GetTextNetwork', methods=['POST'])
def GetTextNetwork():
    event_data = request.json
    token = event_data["Token"]    
    id = event_data["Id"]    
    url = event_data["Url"]     
    mods = Tn.ProcessTextNet(hc,token,id,url)
    return mods

@app.route('/GetDocumentNetwork', methods=['POST'])
def GetDocumentNetwork():
    event_data = request.json
    indexurl = event_data["Index_Url"]    
    colname = event_data["Field"]    
    colval = event_data["Unique_Key"]
    docid = event_data["Doc_No"]
    mods = Dn.ProcessTextNet(indexurl,colname,colval,docid)
    return mods

@app.route('/HttpUrlContent', methods=['GET'])
def HttpUrlContent():
    urlpath = request.headers['url']       
    html=""
    if(urlpath == "" or urlpath is None):
        return html
    
    bfromhttp = False
    res = hc.GetLinkHttpResponse(urlpath)    
    if res["success"]:
        bfromhttp = True
        html = res["content"]

    if(html is None or html == ""):        
        result_queue = queue.Queue()
        selenium_queue.put({"url": urlpath,"result_queue": result_queue})
        result = result_queue.get()
        if result["ok"]:
            html = result["html"]             

    if(len(html) !=  0):
        text =''
        doc = Document(html)
        clean_html = doc.summary()
        soup = BeautifulSoup(clean_html, "html.parser")
        result_ = soup.get_text(separator=" ", strip=True)
        if(len(result_) < 200):
            if(bfromhttp):
                result_queue = queue.Queue()
                selenium_queue.put({"url": urlpath,"result_queue": result_queue})
                result = result_queue.get()
                if result["ok"]:
                    html = result["html"] 
            
            text = mp.clean_article_html(html)
        else:
            text = result_

        if(text is None or text == ""): 
            text = trafilatura.extract(
                    html,
                    include_comments=False,
                    include_tables=False,
                    include_links=False,
                    include_images=False,
                    favor_precision=True
                    )            
           
        html = text.replace("\"","")

    return html

@app.route('/GetKnownFacts', methods=['GET'])
def GetKnownFacts():
    autoid = request.headers['autoid']   
    facts = Rs.GetKnownFacts(autoid)
    return facts 

@app.route('/ContentRelevance', methods=['POST'])
def ContentRelevance():
    text = ""
    event_data = request.json
    url = event_data["url"]  
    autoid= event_data["autoid"]  
    prompts= event_data["knownfact"]  
    mode =event_data["mode"]
    try: 
        text =event_data["text"] 
    except:pass
    osintflag =event_data["score"]
    trans = Rs.ContentExtraction(hc,model,url,autoid,prompts,mode,osintflag,text)
    return trans 

@app.route('/HtmlContent', methods=['GET'])
def HtmlContent():
    urlpath = request.headers['url']   
    #trans = tx.GET_HTML_SOURCE(urlpath)
    trans = mp.GET_HTML_SOURCE(urlpath)    
    return trans 


@app.route('/SearchGoogleContent', methods=['GET'])
def SearchGoogleContent():
    # query = request.headers['query']   
    # browser = QWebEngineView()    
    # #trans = tx.GET_HTML_SOURCE(urlpath)
    # sb.main(browser,app_,query)    
    # sys.exit(app_.exec_())
    return "Processed" 

# @app.route('/GenerativeText', methods=['POST'])
# def GenerativeText():
#     event_data = request.json   
#     id = event_data["Id"]
#     type = event_data["Type"]
#     query = event_data["Query"]    
#     trans = Og.GenerateText(type,id,query)
#     return trans

if __name__ == '__main__':    
    app.run(host='127.0.0.1',port=5001,debug=True)
    


# @app.route('/MatchImage', methods=['POST'])
# def MatchImage():
#     text = request.headers['ApiKey']
#     event_data = request.json
#     src = event_data["src"]
#     trgt = event_data["trg"]
#     for i in trgt:
#         print(i)
#     print(src)
#     print(text)
#     print(trgt)
#     return str(src)
