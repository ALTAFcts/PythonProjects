import FM.FMTEST
import string
from urllib.parse import quote
from simple_colors import *
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
import pysolr
import sys
import io
from dateutil.relativedelta import relativedelta
import threading
import xmltodict
from geotext import GeoText

options = Options()
options.add_argument('-no-sandbox')
#options.add_argument("--disable-infobars")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2 
})
driver = webdriver.Chrome(chrome_options=options,executable_path="D:/VSProjects/DemoPython/chromedriver.exe")

def getExistingDetails(AutoId):
    print("Taking Details from People Service := ")
    # strRulstring = UnderlineText(stringP)
    # print(strRulstring)
    # 993277596 Partha id.
    objTest = FM.FMTEST.FMInfo(AutoId) #"98745874")
    objJson = objTest.main()
    # objJson = FM.FM.main("993277596")
    Email_Account = []
    try:
        Email_Account = objJson[0]['Probable_Emails']
    except Exception as Err1:
        print(str(Err1))
    try:
        Details = objJson[0]['Details']
        print(json.dumps(Details, indent = 4,ensure_ascii=False))
    except Exception as Err0:
        pass
    try:
        FullName = Details[0]['FULL_NAME'].strip()
        FullName = ' '.join(FullName.split())
        print("Full Name of the Person := "+ str(FullName))
    except:
        pass
    try:
        knownEmail = "mohdidrees.mca@gmail.com"
        driver.get("https://www.flickr.com/search/people/?q="+knownEmail+"")
        Flkr_Tag = driver.find_elements_by_xpath(".//div[@class='sizer-cropper']")
        Flkr_name = Flkr_Tag[0].get_attribute('title').strip().replace("'","")
        print(Flkr_name)
        Flkr_UID = Flkr_Tag[0].find_element_by_xpath(".//div[@class = 'avatar-content']")
    except Exception as Err3:
        print(str(Err3))



if __name__ == "__main__":
    AUTOID = input("Enter AutoID : ")
    getExistingDetails(AUTOID)  #24429432
 
