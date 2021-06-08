import requests
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from time import strptime
from time import mktime
from datetime import datetime,timedelta
import json
import pyodbc
from selenium.webdriver.common.by import By
import os
import random
from uuid import uuid4
import keyboard
import bs4 as bs
import urllib.request
from urllib.parse import quote
import pysolr
import sys
import uuid
import io
from dateutil.relativedelta import relativedelta
import threading


options = Options()
options.add_argument('-no-sandbox')
options.add_argument("start-maximized")
driver = webdriver.Chrome(chrome_options=options,executable_path="D:/VSProjects/DemoPython/chromedriver.exe")


def save_cookie(driver):
    with open("D:\\VSProjects\\DemoPython\\Cookie_File.txt", 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

try:
    requrl = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
    driver.get(requrl)
    #driver.maximize_window()
    User = "ranaayyubi748@gmail.com"
    paswrd = "cts@1234"
    
    #UserName = driver.find_element_by_xpath("/html/body/main/section[1]/div[2]/form/div[2]/div[1]/input")
    UserName = driver.find_element_by_xpath("//input[@id='username']")
    #/html/body/div/main/div[2]/div[1]/form/div[1]/input
    UserName.send_keys(str(User))
    #paswd = driver.find_element_by_xpath("/html/body/main/section[1]/div[2]/form/div[2]/div[2]/input")
    #/html/body/div/main/div[2]/div[1]/form/div[2]/input
    paswd = driver.find_element_by_xpath("//input[@id='password']")
    paswd.send_keys(str(paswrd))
    #submit = driver.find_element_by_xpath("/html/body/main/section[1]/div[2]/form/button")
    submit = driver.find_element_by_xpath("//button[@data-litms-control-urn='login-submit']")
    submit.click()
    print("doing Login")
    time.sleep(5)
    print("doing Login")
    save_cookie(driver)
except:
    save_cookie(driver)
headers = {"user-agent":"Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
                }

Friends_link = 'https://www.linkedin.com/voyager/api/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search.SearchClusterCollection-103&origin=SEO_PSERP&q=all&query=(flagshipSearchIntent:SEARCH_SRP,queryParameters:(firstName:List(Mi),lastName:List(%2B),resultType:List(PEOPLE)),includeFiltersInResponse:false)&start=80'
frnd = "https://www.linkedin.com/search/results/people/?firstName=Mi&keywords=Mi&lastName=%2B&origin=GLOBAL_SEARCH_HEADER&page=100"
# with open("D:\\VSProjects\\DemoPython2\\Cookie_File.txt", 'wb') as filehandler:
#     pickle.dump(driver.get_cookies(),filehandler)

cookies = pickle.load(open("D:\\VSProjects\\DemoPython\\Cookie_File.txt", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
for cookie in cookies:
    try:
        SessionID = cookie['value'];
        if "ajax:" in SessionID:
            ssion_val = SessionID
            print(ssion_val)
        li_at = cookie['name']
        if li_at == "li_at":

            li_atVal = cookie['value'];
            print(li_atVal)
    except Exception as ckr:
        print(str(ckr))
with requests.session() as s:
    s.cookies['li_at'] = li_atVal
    s.cookies["JSESSIONID"] = ssion_val
    s.headers = headers
    s.headers["csrf-token"] = s.cookies["JSESSIONID"].strip('"')
    response = s.get(Friends_link)
    response_dict = response.json()
    #print(response_dict)
    try:
        link_elems = response_dict['elements']
    except:
        link_elems = ""
        pass
    print(link_elems)