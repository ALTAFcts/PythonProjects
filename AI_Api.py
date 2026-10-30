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
import multiprocessing
import subprocess


app = Flask(__name__)
#logging.disable(logging.WARNING)
#log = logging.getLogger('werkzeug')
#log.disabled = True

classify = []
model = SentenceTransformer("all-mpnet-base-v2")

CHROMEDRIVER_PATH = ("D:/Python/Projects/FindMore/chromedriver_win32/chromedriver.exe")

SELENIUM_PAGE_TIMEOUT = 30
SELENIUM_HARD_TIMEOUT = 75
SELENIUM_CLEANUP_TIMEOUT = 5
MAX_SELENIUM_PROCESSES = 2

logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s")

log = logging.getLogger(__name__)

# Prevent too many Chrome instances.
selenium_semaphore = threading.BoundedSemaphore(MAX_SELENIUM_PROCESSES)


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

    # Don't wait for every image, stylesheet and other resource.
    options.page_load_strategy = "eager"
    service = Service(executable_path=CHROMEDRIVER_PATH)

    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    driver.set_page_load_timeout(SELENIUM_PAGE_TIMEOUT)
    driver.set_script_timeout(15)

    return driver

def selenium_fetch_process(url, conn):
    driver = None
    try:
        log.info("Selenium started: %s", url)
        driver = create_driver()
        timed_out = False
        try:
            driver.get(url)
        except TimeoutException:
            timed_out = True
            log.warning("Page load timeout: %s",url)
            # Try to stop further resource loading.
            try:
                driver.execute_script("window.stop();")
            except Exception:
                pass

        # Get available page HTML.
        html = driver.page_source
        conn.send({"ok": True,"html": html,"timed_out": timed_out})
    except Exception as e:
        log.exception("Selenium worker failed: %s",url)
        try:
            conn.send({"ok": False,"error": str(e)})
        except Exception:
            pass
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception as e:
                log.error("Chrome cleanup error: %s",str(e))
        try:
            conn.close()
        except Exception:
            pass

        log.info("Selenium worker stopped: %s",url)

def terminate_process_tree(process):
    if process is None:
        return

    if not process.is_alive():
        process.join(timeout=1)
        return

    try:
        # Windows: terminate worker and its child processes,
        # including ChromeDriver and Chrome.
        subprocess.run(
            [
                "taskkill",
                "/PID",
                str(process.pid),
                "/T",
                "/F"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
            check=False
        )
    except Exception as e:
        log.error("Taskkill error: %s",str(e))
        try:
            process.terminate()
        except Exception:
            pass

    process.join(timeout=3)
    if process.is_alive():
        try:
            process.kill()
        except Exception:
            pass

        process.join(timeout=2)

def get_selenium_html(url):
    if not selenium_semaphore.acquire(timeout=10):
        return {"ok": False,"error": "Maximum Selenium workers are busy"}

    ctx = multiprocessing.get_context("spawn")

    parent_conn = None
    child_conn = None
    process = None

    try:
        parent_conn, child_conn = ctx.Pipe(duplex=False)
        process = ctx.Process(target=selenium_fetch_process,args=(url, child_conn))
        process.start()
        # Parent must close its copy of the child endpoint.
        child_conn.close()
        child_conn = None
        # Wait for worker result.
        if parent_conn.poll(SELENIUM_HARD_TIMEOUT):
            try:
                result = parent_conn.recv()
            except EOFError:
                result = {"ok": False,"error": "Selenium worker closed without result"}

            # Allow graceful cleanup.
            process.join(timeout=SELENIUM_CLEANUP_TIMEOUT)

            # If Chrome cleanup is stuck, kill the process tree.
            if process.is_alive():
                log.warning("Selenium cleanup stuck. Killing process: %s",url)
                terminate_process_tree(process)
            return result
        else:
            log.error("SELENIUM HARD TIMEOUT: %s",url)
            terminate_process_tree(process)
            return {"ok": False,"error": "Selenium hard timeout"}
    except Exception as e:
        log.exception("Selenium execution error")
        if process is not None:
            terminate_process_tree(process)
        return {"ok": False,"error": str(e)}
    finally:
        if parent_conn is not None:
            try:
                parent_conn.close()
            except Exception:
                pass

        if child_conn is not None:
            try:
                child_conn.close()
            except Exception:
                pass

        if process is not None:
            if process.is_alive():
                terminate_process_tree(process)

            try:
                process.close()
            except Exception:
                pass

        selenium_semaphore.release()

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
        log.info("HTTP failed. Trying Selenium: %s",urlpath)
        result = get_selenium_html(urlpath)
       
        if result["ok"]:
            html = result["html"]     

        if result.get("timed_out"):        
            log.warning("Using partial HTML after page timeout: %s",urlpath)        

    if(len(html) !=  0):
        text =''
        doc = Document(html)
        clean_html = doc.summary()
        soup = BeautifulSoup(clean_html, "html.parser")
        result_ = soup.get_text(separator=" ", strip=True)
        if(len(result_) < 200):
            if(bfromhttp):
                result = get_selenium_html(urlpath)
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
        if(text is None or text == ""): 
            return result_
        else:
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
    multiprocessing.freeze_support()
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
