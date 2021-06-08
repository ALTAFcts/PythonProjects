import requests
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


# options = Options()
# options.add_argument('-no-sandbox')
# #options.add_argument("--disable-infobars")
# options.add_argument("start-maximized")
# options.add_argument("--disable-extensions")
# # Pass the argument 1 to allow and 2 to block
# options.add_experimental_option("prefs", { 
#     "profile.default_content_setting_values.notifications": 2 
# })
# driver = webdriver.Chrome(chrome_options=options,executable_path="D:/VSProjects/DemoPython/chromedriver.exe")

def getExistingDetails(AutoId):
    print(green("Taking Details from People Service",['bold', 'underlined']))
    # 993277596 Partha id.
    objTest = FM.FMTEST.FMInfo(AutoId) #"98745874")
    objJson = objTest.main()
    # objJson = FM.FM.main("993277596")
    Details = ""
    Fname = ""
    Lname = ""
    FullName = ""
    Country = ""
    DYear = ""
    Dmonth = ""
    Dday = ""
    Find_More_ID = ""
    DOB = ""
    AknowAs = ""
    city = ""
    SUMMARY = ""
    PROFILE_PIC = ""
    Rule_1_Params = []
    Social_Accounts = ""
    contact_details = ""
    Acount_Dict = []
    FM_Social_list = []
    
    try:
        try:
            Social_Accounts =objJson[0]['Social_Media']
        except Exception as Err1:
            print("Error @Social_Accounts:"+str(Err1))
            Social_Accounts = ""

        Details = objJson[0]['Details']
        contact_details = objJson[0]['phone']
        
        if len(Details) > 0:
            print("Existing Know Facts found from People Service")
            #print(Details)
            #break
        try:
            FullName = Details[0]['FULL_NAME'].strip()
            FullName = ' '.join(FullName.split())
            print("Full Name of the Person :="+str(FullName))
        except:
            pass
        if len(Social_Accounts) > 0:
            print("Social Account Exists")
            for Acnt in Social_Accounts:
                acname = Acnt['SCREEN_NAME']
                acSrc = Acnt['MODULE_TYPE_DESC']
                d = {
                    "Screen":acname,
                    "Source":acSrc
                }
                Acount_Dict.append(d)
            social_list = []
            value = "Twitter"
            FB_name = ""
            Insta_name = ""
            Twtr_name = ""
            for acnt in Acount_Dict:
                SocName = acnt['Source']
                social_list.append(SocName)
                if SocName == "Facebook":
                    FB_name = acnt['Screen']
                elif SocName == "Twitter":
                    Twtr_name = acnt['Screen']
                elif SocName == "Instagram":
                    Insta_name = acnt['Screen']
                
            if "Instagram" not in social_list:
                print("Instagram not in Social list")
                if FB_name != "":
                    screen = FB_name
                else:
                    screen = Twtr_name
                if screen != "":
                    FindMore_InstaName = ""
                    try:
                        json_Insta = ""
                        json_Insta = Osint_Instagram(screen)
                    except Exception as Err2:
                        print("Err2 At JsonInsta:="+str(Err2))
                        json_Insta = ""
                    if json_Insta != "":
                        try:
                            y =""
                            Fmore_InstaUM = ""
                            Fmore_Website = ""
                            Update_Status = ""
                            y = json.loads(json_Insta)
                            FindMore_InstaName = y["FULL_NAME"]
                            Fmore_InstaUM = y["USER_NAME"]
                            Fmore_Website = y['WEBSITE']
                            Update_Status = y['UPDATE_STATUS']
                            FindMore_InstaName = string.capwords(FindMore_InstaName)
                            FullName = string.capwords(FullName)
                            if FindMore_InstaName == FullName:
                                
                                d = {
                                        "Instagram":Fmore_InstaUM,
                                        "Website":Fmore_Website
                                    } 
                                FM_Social_list.append(d)
                            if FindMore_InstaName == "Null":
                                NewFullName = FullName.replace(" ","") 
                                #screen = string.upper()
                                
                                #Fmore_InstaUM = string.upper()
                                if screen == Fmore_InstaUM:

                                #Fmore_InstaUM in NewFullName
                                    
                                    d = {
                                        "Instagram":Fmore_InstaUM,
                                        "Website":Fmore_Website
                                    } 
                                    FM_Social_list.append(d)
                            if len(FM_Social_list) == 0:
                                NewFullName = ""
                                NewFullName = FullName.replace(" ","")
                                json_Insta = Osint_Instagram(NewFullName)
                                if json_Insta != "":
                                    try:
                                        y =""
                                        y = json.loads(json_Insta)
                                        FindMore_InstaName = y["FULL_NAME"]
                                        FindMore_InstaName = string.capwords(FindMore_InstaName)
                                        FullName = string.capwords(FullName)
                                        if FindMore_InstaName == FullName:
                                            Fmore_InstaUM = ""
                                            Fmore_Website = ""
                                            Fmore_InstaUM = y["USER_NAME"]
                                            Fmore_Website = y['WEBSITE']
                                            d = {
                                                "Instagram":Fmore_InstaUM,
                                                "Website":Fmore_Website
                                            }
                                            FM_Social_list.append(d)
                                    except:
                                        pass


                        except Exception as FM_err2:
                            print(str(FM_err2))
                    
                else:
                    json_Insta = ""
            if "Facebook" not in social_list:
                print("Facebook not in Social list")
                if Twtr_name != "":
                    screen = Twtr_name
                else:
                    screen = Insta_name
                if screen != "":
                    f= ""
                    FindMore_FacebokName = ""
                    try:
                        json_FB = ""
                        json_FB = osint_facebook(screen)
                    except Exception as FB_eer3:
                        print(str(FB_eer3))
                        json_FB = ""
                    
                    if json_FB != "":
                        f = json.loads(json_FB)
                        if "Invalid Profile Has Been Requested" in f:
                            json_FB = ""
                        if json_FB != "":
                            FindMore_FacebokName = f["FULL_NAME"]
                            FullName = string.capwords(FullName)
                            FindMore_FacebokName = string.capwords(FindMore_FacebokName)
                            if FindMore_FacebokName == FullName:
                                Fmore_FBUM = ""
                                Fmore_FBUM = f['USER_NAME']
                                FM_Social_list.append(Fmore_FBUM)
                            else:
                                print("Full Name Not Matched for FB")
                        else:
                            print("Invalid Profile Has Been Requested FB Account")

                else:
                    json_FB = ""
            if "Twitter" not in social_list:
                print("Twitter not in Social list")
                if FB_name !=  "":
                    screen = FB_name
                else:
                    screen = Insta_name
                if screen != "":
                    try:
                        json_Twitr = ""
                        FindMore_TwtrkName = ""
                        json_Twitr = osint_twitter(screen)
                    except Exception as twitErr:
                        print(twitErr)
                        json_Twitr = ""
                    if "Cannot serialize the DataTable" not in json_Twitr:
                        #t = json.loads(json_Twitr)
                        time.sleep(60)
                        try:
                            json_Twitr = ""
                            FindMore_TwtrkName = ""
                            json_Twitr = osint_twitter(screen)
                        except Exception as twitErr:
                            print(twitErr)
                    if json_Twitr != "":
                        t = json.loads(json_Twitr)
                        try:
                            FindMore_TwtrkName= t["USER_NAME"]
                            FindMore_TwtrkName = string.capwords(FindMore_TwtrkName)
                            FullName = string.capwords(FullName)
                            if FindMore_TwtrkName == FullName:
                                Fmore_TwtrUM = ""
                                Fmore_TwtrUM = json_Twitr['SCREEN_NAME']
                                FM_Social_list.append(Fmore_TwtrUM)
                        except Exception as Twt_err:
                            print(str(Twt_err))
                else:
                    json_Twitr = ""
        else:
            print("SOCIAL Accounts Does not Exists for Any Source")
        
        if len(FM_Social_list) > 0:
            print("Social Accounts are Found for Find More Search")
            print(FM_Social_list)
        else:
            print("SOCIAL Accounts Does not Exists in All Three Sources")
        
        try:
            Fname = Details[0]['FIRST_NAME']
            Lname = Details[0]['LAST_NAME']
        except:
            pass
        
        try:
            Country = Details[0]['CITIZEN'].strip()
            Country = ' '.join(Country.split())
        except:
            pass
        try:
            DYear = Details[0]['BIRTH_YEAR']
        except:
            pass
        try:
            Dmonth = Details[0]['BIRTH_MONTH']
        except:
            pass
        try:
            Dday = Details[0]['BIRTH_DAY']
        except:
            pass
        try:
            Find_More_ID = Details[0]['AUTO_ID']
        except:
            pass
        try:
            Dplace = Details[0]['BIRTH_PLACE'].strip()
            Dplace = ' '.join(Dplace.split())
        except:
            pass
        try:
            DOB = Details[0]['DOB']
        except:
            pass
        try:
            AknowAs = Details[0]['KNOWNAS']
        except:
            pass
        try:
            SUMMARY = Details[0]['SUMMARY']
        except:
            pass
        
        pdict = {
            'Full_Name':FullName,
            'First_Name':Fname,
            'Last_Name':Lname,
            'Country':Country,
            'Birth_Year':DYear,
            'Birth_Month':Dmonth,
            'Birth_Day':Dday,
            'Birth_Place':Dplace,
            'DOB':DOB,
            'KNOWNAS':AknowAs,
            'ProfileImg':PROFILE_PIC,
            'Summary':SUMMARY
        }
        Rule_1_Params.append(pdict)

    
    except Exception as ferr:
        print(str(ferr))
    stringP = "Rule Parameters are Below:"
    strRulstring = UnderlineText(stringP)
    # print(strRulstring)
    # print(pdict)
    #print("Find More ID:-"+str(Find_More_ID))
    customSrchfacebook(Details,Rule_1_Params,Find_More_ID)
    #customSrchInstagram(Details,Rule_1_Params)

def customSrchfacebook(Details,Rule_1_Params,Find_More_ID):
    print(green("Under Facebook Search Function",['bold', 'underlined']))
    p = 1
    Facebook_list = []
    Lang = ""
    Full_Name = ""
    country = ""
    kcode = ""
    cCode = ""
    N_FName = ""
    N_CName = ""
    cityknown = "" 
    sumary = ""
    knownAs = ""
    knownAs = Rule_1_Params[0]['KNOWNAS']
    sumary = Rule_1_Params[0]['Summary']
    cityknown = Rule_1_Params[0]['Birth_Place']
    Full_Name = Rule_1_Params[0]['Full_Name']
    country = Rule_1_Params[0]['Country']
    N_CName = string.capwords(country)
    constring = "Taking Country From Known Facts"
    strCstring = UnderlineText(constring)
    print(str(strCstring)+" :=  "+str(N_CName))
    # if N_CName.strip() !="":
    #     kcode = GetCountryCode(N_CName,kcode)
    # cCode = kcode
    #print("Getting CountryCode of AutoID Record:=  "+str(cCode))
    #Full_Name = "رنجن كومار داس"
    N_FName = string.capwords(Full_Name)
    fulNstring = "Taking Full Name from Know Facts"
    strFNstring = UnderlineText(fulNstring)
    print(str(strFNstring)+" :=  "+yellow(Full_Name)+",   Formatted Full Name :=  "+green(N_FName))
    driver.get('https://www.facebook.com/')
    print ("Opened facebook")
    time.sleep(1)
    usr= "mikelatham.cnn@outlook.com"
    pwd="Creative_1234"
    username_box = driver.find_element_by_id('email')
    username_box.send_keys(usr)
    #print ("Email Id entered")
    time.sleep(1)
    password_box = driver.find_element_by_id('pass')
    password_box.send_keys(pwd)
    #print ("Password entered")
    fullname = "Partha Bhattacharya"
    login_box = driver.find_element_by_name('login')
    login_box.click()
    time.sleep(15)
    driver.get("https://www.facebook.com/search/people?q="+str(N_FName)+"")
    # Serchbox = driver.find_element_by_name("global_typeahead")
    # Serchbox.send_keys("Partha Bhattacharya")
    # Serchbox.send_keys(Keys.ENTER)
    time.sleep(1)
    try:
        SeeAll = driver.find_element_by_link_text("See all")
        SeeAll.click()
        time.sleep(1)
    except:
        pass
    try:
        driver.execute_script("document.body.style.zoom='25%'")  
        SCROLL_PAUSE_TIME = 5
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        hgt = int(0)
        while hgt <= 3:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            hgt = hgt+1
        print("scrolling Done")
        driver.execute_script("window.scrollTo(0, 0);")

    except Exception as hgth:
        print(str(hgth))
    
    time.sleep(3)
    #logout = "https://www.facebook.com/logout.php?button_location=settings&button_name=logout"
    
    Facebook_list = []
    people = driver.find_elements_by_xpath(".//div[@role='article']")
    time.sleep(2)
    try:
        print("Searching Under Facebook, Pls Wait..")
        for x in people:
            plname = ""
            plhref = ""
            plfnameF = ""
            plfname = ""
            city =""
            citytxt = ""
            gmask = ""
            gpic = ""
            gimg =""
            try:
                gmask = x.find_elements_by_tag_name("image")
                gpic = gmask[0].get_attribute("xlink:href").strip().replace("'","")
                #print(gpic)
            except Exception as picEr:
                gpic = ""
                print("PicERRor:-"+str(picEr))
                pass
            plname = x.find_elements_by_xpath(".//div[@class='qzhwtbm6 knvmm38d']")
            time.sleep(1)
            plhref = plname[0].find_element_by_tag_name("a").get_attribute('href')
            #print(plhref)
            plfname = plname[0].find_elements_by_tag_name("span")
            for plf in plfname[3:]:
                try:
                    plfnameF = plf.text.strip().replace("'","")
                    time.sleep(1)
                    #print(str(plfnameF))
                except:
                    plfnameF = ""
                    pass
            try:  
                city = plname[1].find_elements_by_xpath(".//div[@class='jktsbyx5']")
                citytxt = city[0].text.strip().replace("'","")
                #print(citytxt)
            except:
                citytxt = ""
                pass
            try:
                d= {
                    'Name':plfnameF,
                    'Link':plhref,
                    'Address':citytxt,
                    'ImgLink':gpic
                }
                Facebook_list.append(d)
            except Exception as dier:
                print(str(dier))
            
    except Exception as err:
        print(str(err))
        pass
    
    #print(Facebook_list)
    Facebook_list_New = []
    tRec = ""
    try:
        tRec = len(Facebook_list)
    except:
        pass
    print("TOTAL RESULTS By Applying RULE PARAMS:[Full Name] from FACEBOOK :=  "+str(tRec))
    for item in Facebook_list:
        try:
            peoplN = ""
            peoplName= ""
            peoplcty = ""
            peoplFNH = ""
            peoplN = item['Name']
            peoplcty = item['Address']
            peoplName = peoplN.strip()
            try:
                #if Full Name and city OR Full Name and Country
                if peoplN == N_FName and peoplcty != "":
                    if cityknown in peoplcty:
                        Facebook_list_New.append(item)                        
                        print("Name and city Get match")
                    if country in peoplcty:
                        Facebook_list_New.append(item)
            except:
                pass
            
            try:    
                # if knownAS and Country OR KKnownAS and city Name Matches
                if knownAs == peoplN and peoplcty != "":   
                    if country in peoplcty:
                        Facebook_list_New.append(item)
                    if cityknown in peoplcty:
                        Facebook_list_New.append(item)
            except:
                pass
            
            try:    
                # If city Found in Summary Text and Full Name in Name      
                if peoplcty in  sumary and peoplN == N_FName:
                    Facebook_list_New.append(item)
            except:
                pass
            try:
                # If city Found in Summary Text and KKnownAS Name in Name 
                if peoplcty in  sumary and knownAs == N_FName:
                    Facebook_list_New.append(item)
            except:
                pass
            
        except Exception as Refne:
            print(str(Refne))
            pass
    fcount = ""
    try:
        fcount = len(Facebook_list_New)
    except:
        pass
    if fcount == "":
        for item in Facebook_list:
            try:
                peoplN = ""
                peoplName= ""
                peoplcty = ""
                peoplFNH = ""
                peoplN = item['Name']
                peoplcty = item['Address']
                peoplName = peoplN.strip()
                try:
                    #if Full Name and city OR Full Name and Country
                    if peoplN == N_FName or knownAs == peoplN and peoplcty == "":
                        Facebook_list_New.append(item)
                except:
                    pass                        
            except:
                pass
        fcount = len(Facebook_list_New)    
        

    print("Total FACEBOOK LINKS After Applying More Filteration{city,country,knownAS,birthPlace} :=  "+str(fcount))

    #driver.delete_all_cookies()
    LinkedInnPeople(Details,Rule_1_Params,Find_More_ID,Facebook_list_New)

def LinkedInnPeople(Details,Rule_1_Params,Find_More_ID,Facebook_list_New):
    print(green("Under Linkedin Search Function",['bold', 'underlined']))
    requrl = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
    driver.get(requrl)
    try:
        User = "ranaayyubi748@gmail.com"
        paswrd = "cts@1234"
        UserName = driver.find_element_by_xpath("//input[@id='username']")
        UserName.send_keys(str(User))
        paswd = driver.find_element_by_xpath("//input[@id='password']")
        paswd.send_keys(str(paswrd))
        submit = driver.find_element_by_xpath("//button[@data-litms-control-urn='login-submit']")
        submit.click()
        time.sleep(5)
        
    except:
        pass
    Lang = ""
    Full_Name = ""
    country = ""
    kcode = ""
    cCode = ""
    N_FName = ""
    N_CName = ""
    cityknown = "" 
    sumary = ""
    knownAs = ""
    knownAs = Rule_1_Params[0]['KNOWNAS']
    sumary = Rule_1_Params[0]['Summary']
    cityknown = Rule_1_Params[0]['Birth_Place']
    Full_Name = Rule_1_Params[0]['Full_Name']
    country = Rule_1_Params[0]['Country']
    N_CName = string.capwords(country)
    constring = "Taking Country From Known Facts"
    strCstring = UnderlineText(constring)
    print(str(strCstring)+" :=  "+str(N_CName))
    N_FName = string.capwords(Full_Name)
    fulNstring = "Taking Full Name from Know Facts"
    strFNstring = UnderlineText(fulNstring)
    print(str(strFNstring)+" :=  "+yellow(Full_Name)+",   Formatted Full Name :=  "+green(N_FName))
    
    #NO Need of 25% zoom scrolling in Linkedin as its paging concept
   
    Linkedin_People = []
    page = 1
    while page <= 5:
        driver.get("https://www.linkedin.com/search/results/people/?keywords="+str(N_FName)+"&origin=GLOBAL_SEARCH_HEADER&page="+str(page)+"")
        time.sleep(2)
        li_item = driver.find_elements_by_xpath(".//li[@class='reusable-search__result-container ']")
        time.sleep(1)
        
        for i in li_item:
            try:
                try:
                    img = ""
                    img = i.find_elements_by_tag_name("img")
                except:
                    pass
                if len(img) == 0:
                    img = i.find_elements_by_class_name("EntityPhoto-circle-3-ghost-person ivm-view-attr__ghost-entity ")
                try:
                    imgsrc = img[0].get_attribute("src").replace("'","")
                except:
                    imgsrc = ""
                #print(imgsrc)
                try:
                    name = ""
                    name = img[0].get_attribute('alt').strip()
                    name = name.replace("'","")
                except:
                    pass
                if len(name) == 0:
                    name = i.find_elements_by_class_name("visually-hidden")
                    name = name[0].text.strip().replace("'","")
                print(name)
                link = i.find_elements_by_tag_name('a')
                for a in link:
                    plink = ""
                    try:
                        plink = a.get_attribute('href')
                        if "?miniProfileUrn=urn" in plink:
                            #print(plink)
                            plink = plink.replace("'","")
                    except:
                        pass
                    
                try:
                    desc = ""
                    desc = i.find_elements_by_class_name("entity-result__primary-subtitle")
                    desc = desc[0].text.strip().replace("'","")
                    #print(desc)
                except:
                    desc = ""
                    pass
                try:
                    loc = i.find_elements_by_class_name("entity-result__secondary-subtitle")
                    loc = loc[0].text.strip().replace("'","")
                    #print(loc)
                except:
                    loc = ""
                    pass
                d={
                    'NAME':name,
                    'DESC':desc,
                    'pLOCATION':loc,
                    'pIMG':imgsrc,
                    'Lklink':plink
                }
                Linkedin_People.append(d)
             
            except:
                pass
        page = page +1
        print("Next Page")
    print(Linkedin_People)

def osint_facebook(screen):
    Method_ID = "20"
    ScreenName = screen
    payload = ""
    url = "http://94.236.4.172/services/service.asmx?op=GetFacebookProfileInfo"

    payload = payload +"<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\r\n  <soap:Header>\r\n    <AuthHeader xmlns=\"http://tempuri.org/\">\r\n      <userName>QmLW7qVBSB1lsY8f1AVQhw==</userName>\r\n      <passWord>/x01gfHE72J2MyGQCPY1SV8HKCsvqnYAQgabKJ2usio=</passWord>\r\n      <ipAddress></ipAddress>\r\n      <requestUrl></requestUrl>\r\n      <clientKey></clientKey>\r\n"
    payload = payload +"<WebMethodId>"+str(Method_ID)+"</WebMethodId>\r\n      <waaudit>\r\n        <WEB_SERVICE_ID>"+str(Method_ID)+"</WEB_SERVICE_ID>\r\n        <CLIENT_ID>1</CLIENT_ID>        \r\n        <INPUT_PARAMS>"+str(ScreenName)+"</INPUT_PARAMS>\r\n        <REQUEST_URL>"+str(ScreenName)+"</REQUEST_URL>\r\n      </waaudit>\r\n      <TOKEN>1</TOKEN>\r\n      <CLIENT_ID>1</CLIENT_ID>\r\n      <CLIENT_FB_CALLBACK></CLIENT_FB_CALLBACK>\r\n    </AuthHeader>\r\n  </soap:Header>\r\n"
    payload = payload +"<soap:Body>\r\n    <GetFacebookProfileInfo xmlns=\"http://tempuri.org/\">\r\n <screenName>"+str(ScreenName)+"</screenName>\r\n      <Priority>101</Priority>\r\n    </GetFacebookProfileInfo>\r\n  </soap:Body>\r\n</soap:Envelope>"
    headers = {
    'Content-Type': 'text/xml'
    }
    Result = ""
    result = ""
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        time.sleep(5)
        Result = response.text
    except:
        Result = ""
    if Result.strip() != "":
        data_dict = ""
        result = Result.replace("&lt;","<")
        result = result.replace("&gt;",">")
        data_dict = xmltodict.parse(result)
        try:
            obj = ""
            obj = data_dict['soap:Envelope']['soap:Body']['GetFacebookProfileInfoResponse']['GetFacebookProfileInfoResult']['ResponseXML']["DocumentElement"]["PageDetails"]
        except:
            obj = data_dict['soap:Envelope']['soap:Body']['GetFacebookProfileInfoResponse']['GetFacebookProfileInfoResult']['message']
    #print(obj)
    if obj.strip() != "":
        json_FB = ""
        json_FB = json.dumps(obj,ensure_ascii=False)
    #print(json_FB)
    return json_FB
    
def osint_twitter(screen):
    Method_ID = "19"
    ScreenName = screen
    payload = ""
    url = "http://94.236.4.172/services/service.asmx?op=GetTwiterUserDetails"

    payload = payload +"<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\r\n  <soap:Header>\r\n    <AuthHeader xmlns=\"http://tempuri.org/\">\r\n      <userName>QmLW7qVBSB1lsY8f1AVQhw==</userName>\r\n      <passWord>/x01gfHE72J2MyGQCPY1SV8HKCsvqnYAQgabKJ2usio=</passWord>\r\n      <ipAddress></ipAddress>\r\n      <requestUrl></requestUrl>\r\n      <clientKey></clientKey>\r\n"
    payload = payload +"<WebMethodId>"+str(Method_ID)+"</WebMethodId>\r\n      <waaudit>\r\n        <WEB_SERVICE_ID>"+str(Method_ID)+"</WEB_SERVICE_ID>\r\n        <CLIENT_ID>1</CLIENT_ID>        \r\n"
    payload = payload +"<INPUT_PARAMS>"+str(ScreenName)+"</INPUT_PARAMS>\r\n  <REQUEST_URL>"+str(ScreenName)+"</REQUEST_URL>\r\n      </waaudit>\r\n      <TOKEN>1</TOKEN>\r\n      <CLIENT_ID>1</CLIENT_ID>\r\n      <CLIENT_FB_CALLBACK></CLIENT_FB_CALLBACK>\r\n    </AuthHeader>\r\n  </soap:Header>\r\n" 
    payload = payload +"<soap:Body>\r\n <GetTwiterUserDetails xmlns=\"http://tempuri.org/\">\r\n <screenName>"+str(ScreenName)+"</screenName>\r\n      <Priority>101</Priority>\r\n    </GetTwiterUserDetails>\r\n  </soap:Body>\r\n</soap:Envelope>"
    headers = {
    'Content-Type': 'text/xml'
    }
    Result = ""
    result = ""
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        time.sleep(3)
        Result = response.text
    except:
        Result = ""
    if Result != "":
        data_dict = ""
        result = Result.replace("&lt;","<")
        result = result.replace("&gt;",">")
        data_dict = xmltodict.parse(result)
        try:
            obj = ""
            obj = data_dict['soap:Envelope']['soap:Body']['GetTwiterUserDetailsResponse']['GetTwiterUserDetailsResult']['TwitterUserDetails']["UserInfo"]
        except:
            obj = data_dict['soap:Envelope']['soap:Body']['GetTwiterUserDetailsResponse']['GetTwiterUserDetailsResult']
    #print(obj)
    if obj != "":
        json_Twtr = ""
        json_Twtr = json.dumps(obj,ensure_ascii=False)
    #print(json_data)

    return json_Twtr

def Osint_Instagram(screen):
    Method_ID = "66"
    ScreenName = screen
    payload = ""
    url = "http://94.236.4.172/services/service.asmx?op=ObtainInstagramUserDetails"

    payload = payload +"<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\r\n  <soap:Header>\r\n    <AuthHeader xmlns=\"http://tempuri.org/\">\r\n      <userName>QmLW7qVBSB1lsY8f1AVQhw==</userName>\r\n      <passWord>/x01gfHE72J2MyGQCPY1SV8HKCsvqnYAQgabKJ2usio=</passWord>\r\n      <ipAddress></ipAddress>\r\n      <requestUrl></requestUrl>\r\n      <clientKey></clientKey>\r\n"
    payload = payload +"<WebMethodId>"+str(Method_ID)+"</WebMethodId>\r\n      <waaudit>\r\n        <WEB_SERVICE_ID>"+str(Method_ID)+"</WEB_SERVICE_ID>\r\n        <CLIENT_ID>1</CLIENT_ID>        \r\n"
    payload = payload +"<INPUT_PARAMS>"+str(ScreenName)+"</INPUT_PARAMS>\r\n        <REQUEST_URL>"+str(ScreenName)+"</REQUEST_URL>\r\n      </waaudit>\r\n      <TOKEN>1</TOKEN>\r\n      <CLIENT_ID>1</CLIENT_ID>\r\n      <CLIENT_FB_CALLBACK></CLIENT_FB_CALLBACK>\r\n    </AuthHeader>\r\n  </soap:Header>\r\n"
    payload = payload +"<soap:Body>\r\n     <ObtainInstagramUserDetails xmlns=\"http://tempuri.org/\">\r\n      <userName>"+str(ScreenName)+"</userName>\r\n      <Priority>101</Priority>\r\n    </ObtainInstagramUserDetails>\r\n  </soap:Body>\r\n</soap:Envelope>"
   
    headers = {
    'Content-Type': 'text/xml'
    }
    Result = ""
    result = ""
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        time.sleep(5)
        Result = response.text
    except:
        Result = ""
    if len(Result) > 0 or Result != "":
        data_dict = ""
        result = Result.replace("&lt;","<")
        result = result.replace("&gt;",">")
        data_dict = xmltodict.parse(result)
        try:
            obj = data_dict['soap:Envelope']['soap:Body']['ObtainInstagramUserDetailsResponse']['ObtainInstagramUserDetailsResult']['ResponseXML']["DocumentElement"]['InstagramUserDetails']
        except:
            obj = ""
    if obj != "":
        json_insta = ""
        json_insta = json.dumps(obj,ensure_ascii=False)
    #print(json_insta)
    if json_insta == "":
        print("Waiting for 2 Mins In-Progress......")
        time.sleep(100)
        Result = ""
        result = ""
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            time.sleep(5)
            Result = response.text
        except:
            Result = ""
        if len(Result) > 0 or Result.strip() != "":
            data_dict = ""
            result = Result.replace("&lt;","<")
            result = result.replace("&gt;",">")
            data_dict = xmltodict.parse(result)
            try:
                obj = data_dict['soap:Envelope']['soap:Body']['ObtainInstagramUserDetailsResponse']['ObtainInstagramUserDetailsResult']['ResponseXML']["DocumentElement"]['InstagramUserDetails']
            except:
                obj = ""
        if obj != "":
            json_insta = ""
            json_insta = json.dumps(obj,ensure_ascii=False)
    else:
        pass
    return json_insta

def DBExecute(Query,Tble,bRetval,strwikiID):
    print("under DBExecute Function")
    QueryCount = "Select COUNT(*) AS ReowsEffected From "+Tble+" with (nolock) where ice_link_record_id ="+str(strwikiID)+""
    try:
        #cursor = None
        #time.sleep(1)
        cnxn = pyodbc.connect("Driver={SQL Server};Server=CTS-IIS02;Database=ICE_WIKIORG_LINKEDINDATA;uid=USCOURT;pwd=123456")
        cursor = cnxn.cursor()
        cursor.execute(Query)
        
        cursor.execute(QueryCount)
        TtlRecords = cursor.fetchone()
                
        print("Data Inserted into ..."+str(Tble))
        print("Total Records Inserted so far......"+str(TtlRecords))
        
        cursor.commit()
        bRetval = True
        
    except Exception as exe:
        bRetval = False
        print(str(exe))
    
    return bRetval

def GetCountryCode(country,kcode):
    #country = "United Kingdom"
    print("Getting Country Code for Country")
    print(str(country))
    coutryList = []
    kd = {
        'Afghanistan':	"af",
        'Albania':	"al",
        'Algeria':	"dz",
        'American':"as",
        'Andorra':"ad",
        'Angola':"ao",
        'Anguilla':	"ai",
        'Antarctica':"aq",
        'Antigua and Barbuda':"ag",
        'Argentina':	"ar",
        'Armenia':	"am",
        'Aruba':	"aw",
        'Australia':	"au",
        'Austria':	"at",
        'Azerbaijan':	"az",
        'Bahamas':	"bs",
        'Bahrain':	"bh",
        'Bangladesh':	"bd",
        'Barbados':	"bb",
        'Belarus':	"by",
        'Belgium':	"be",
        'Belize':	"bz",
        'Benin':	"bj",
        'Bermuda':	"bm",
        'Bhutan':	"bt",
        'Bolivia':"bo",
        'Bosnia and Herzegovina':	"ba",
        'Botswana':	"bw",
        'BouvetIsland':	"bv",
        'Brazil':	"br",
        'British Indian Ocean Territory':	"io",
        'Brunei Darussalam':	"bn",
        'Bulgaria':	"bg",
        'Burkina Faso':	"bf",
        'Burundi':	"bi",
        'Cambodia':	"kh",
        'Cameroon':	"cm",
        'Canada':	"ca",
        'CapeVerde':	"cv",
        'Cayman Islands':	"ky",
        'Central African Republic':	"cf",
        'Chad':	"td",
        'Chile':	"cl",
        'China':	"cn",
        'Christmas Island':	"cx",
        'Cocos Islands':	"cc",
        'Colombia':	"co",
        'Comoros':	"km",
        'Congo':	"cg",
        'Congo the Democratic Republic':	"cd",
        'Cook Islands':	"ck",
        'Costa Rica':	"cr",
        'Cote Divoire':	"ci",
        'Croatia':	"hr",
        'Cuba':	"cu",
        'Cyprus':	"cy",
        'Czech Republic':	"cz",
        'Denmark':	"dk",
        'Djibouti':	"dj",
        'Dominica':	"dm",
        'Dominican Republic':	"do",
        'Ecuador':	"ec",
        'Egypt':	"eg",
        'El Salvador':	"sv",
        'Equatorial Guinea':	"gq",
        'Eritrea':	"er",
        'Estonia':	"ee",
        'Ethiopia':	"et",
        'Falkland Islands(Malvinas)':	"fk",
        'Faroe Islands':	"fo",
        'Fiji':	"fj",
        'Finland':	"fi",
        'France':	"fr",
        'French Guiana':	"gf",
        'French Polynesia':	"pf",
        'French Southern Territories':	"tf",
        'Gabon':	"ga",
        'Gambia':	"gm",
        'Georgia':	"ge",
        'Germany':	"de",
        'Ghana':	"gh",
        'Gibraltar':	"gi",
        'Greece':	"gr",
        'Greenland':	"gl",
        'Grenada':	"gd",
        'Guadeloupe':	"gp",
        'Guam':	"gu",
        'Guatemala':	"gt",
        'Guinea':	"gn",
        'Guinea-Bissau':	"gw",
        'Guyana':	"gy",
        'Haiti':	"ht",
        'Heard Island and Mcdonald Islands':	"hm",
        'HolySee (VaticanCityState)':	"va",
        'Honduras':	"hn",
        'Hong Kong':	"hk",
        'Hungary':	"hu",
        'Iceland':	"is",
        'India':	"in",
        'Indonesia':	"id",
        'Iran':	"ir",
        'Iraq':	"iq",
        'Ireland':	"ie",
        'Israel':	"il",
        'Italy':	"it",
        'Jamaica':	"jm",
        'Japan':	"jp",
        'Jordan':"jo",
        'Kazakhstan':	"kz",
        'Kenya':	"ke",
        'Kiribati':	"ki",
        'Korea Democratic Republic':	"kp",
        'Korea':	"kr",
        'Kuwait':	"kw",
        'Kyrgyzstan':	"kg",
        'Lao Peoples Democratic Republic':	"la",
        'Latvia':	"lv",
        'Lebanon':	"lb",
        'Lesotho':	"ls",
        'Liberia':	"lr",
        'Libyan':	"ly",
        'Liechtenstein':	"li",
        'Lithuania':	"lt",
        'Luxembourg':	"lu",
        'Macao':	"mo",
        'Macedonia':	"mk",
        'Madagascar':	"mg",
        'Malawi':	"mw",
        'Malaysia':	"my",
        'Maldives':	"mv",
        'Mali':	"ml",
        'Malta':	"mt",
        'Marshal lIslands':	"mh",
        'Martinique':	"mq",
        'Mauritania':	"mr",
        'Mauritius':	"mu",
        'Mayotte':	"yt",
        'Mexico':	"mx",
        'Micronesia':	"fm",
        'Moldova':	"md",
        'Monaco':	"mc",
        'Mongolia':	"mn",
        'Montserrat':	"ms",
        'Morocco':	"ma",
        'Mozambique':	"mz",
        'Myanmar':	"mm",
        'Namibia':	"na",
        'Nauru':	"nr",
        'Nepal':	"np",
        'Netherlands':	"nl",
        'Netherlands Antilles':	"an",
        'New Caledonia':	"nc",
        'New Zealand':	"nz",
        'Nicaragua':	"ni",
        'Niger':	"ne",
        'Nigeria':	"ng",
        'Niue':	"nu",
        'Norfolk Island':	"nf",
        'Northern Mariana Islands':	"mp",
        'Norway':	"no",
        'Oman':	"om",
        'Pakistan':	"pk",
        'Palau':	"pw",
        'Palestinian Territory':	"ps",
        'Panama':	"pa",
        'Papua New Guinea':	"pg",
        'Paraguay':	"py",
        'Peru':	"pe",
        'Philippines':	"ph",
        'Pitcairn':	"pn",
        'Poland	':"pl",
        'Portugal':	"pt",
        'PuertoRico':	"pr",
        'Qatar':	"qa",
        'Reunion':	"re",
        'Romania':	"ro",
        'Russian Federation':	"ru",
        'Rwanda':	"rw",
        'Saint Helena':	"sh",
        'SaintKittsandNevis':	"kn",
        'Saint Lucia':	"lc",
        'Saint Pierre and Miquelon':"pm",
        'Saint Vincent and the Grenadines':	"vc",
        'Samoa':	"ws",
        'San Marino':	"sm",
        'Sao TomeandPrincipe':	"st",
        'Saudi Arabia':	"sa",
        'Senegal':	"sn",
        'Serbia and Montenegro':	"cs",
        'Seychelles':	"sc",
        'SierraLeone':	"sl",
        'Singapore':	"sg",
        'Slovakia':	"sk",
        'Slovenia':	"si",
        'Solomon Islands':	"sb",
        'Somalia':	"so",
        'South Africa':	"za",
        'South Georgia':	"gs",
        'South Sandwich Islands':	"gs",
        'Spain':	"es",
        'Sri Lanka':	"lk",
        'Sudan':	"sd",
        'Suriname':	"sr",
        'Svalbardand Jan Mayen':	"sj",
        'Swaziland':	"sz",
        'Sweden':	"se",
        'Switzerland':	"ch",
        'Syrian Arab Republic':	"sy",
        'Taiwan':	"tw",
        'Tajikistan':	"tj",
        'Tanzania':	"tz",
        'Thailand':	"th",
        'Timor-Leste':	"tl",
        'Togo':	"tg",
        'Tokelau':	"tk",
        'Tonga':	"to",
        'Trinidad and Tobago':	"tt",
        'Tunisia':	"tn",
        'Turkey':	"tr",
        'Turkmenistan':	"tm",
        'Turksand Caicos Islands':	"tc",
        'Tuvalu':	"tv",
        'Uganda':	"ug",
        'Ukraine':	"ua",
        'United Arab Emirates':	"ae",
        'United Kingdom':	"uk",
        'United States':	"us",
        'United States Minor Outlying Islands':	"um",
        'Uruguay':	"uy",
        'Uzbekistan':	"uz",
        'Vanuatu':	"vu",
        'Venezuela':	"ve",
        'VietNam':	"vn",
        'Virgin Islands British':	"vg",
        'Virgin Islands U.S.':	"vi",
        'Wallisand Futuna':	"wf",
        'Western Sahara':	"eh",
        'Yemen':	"ye",
        'Zambia':	"zm",
        'Zimbabwe':	"zw"
    }
    #coutryList.append(kd)
    #print(coutryList)
    res = [val for key, val in kd.items() if country in key]
    print("Getting CountryCode :=   "+str(res))
    kcode = res[0]
    
    return kcode

def GetLangCode(Lang,lgCode):
    #lang = "English"
    print("Getting GetLangCode function")
    Lcd = {
        "lang_ar": 'Arabic',

        "lang_bg": 'Bulgarian',

        "lang_ca": 'Catalan',

        "lang_cs": 'Czech',

        "lang_da": 'Danish',

        "lang_de": 'German',

        "lang_el": 'Greek',

        "lang_en": 'English',

        "lang_es": 'Spanish',

        "lang_et": 'Estonian',

        "lang_fi": 'Finnish',

        "lang_fr": 'French',

        "lang_hr": 'Croatian',

        "lang_hu": 'Hungarian',

        "lang_id": 'Indonesian',

        "lang_is": 'Icelandic',

        "lang_it": 'Italian',

        "lang_iw": 'Hebrew',

        "lang_ja": 'Japanese',

        "lang_ko": 'Korean',

        "lang_lt": 'Lithuanian',

        "lang_lv": 'Latvian',

        "lang_nl": 'Dutch',

        "lang_no": 'Norwegian',

        "lang_pl": 'Polish',

        "lang_pt": 'Portuguese',

        "lang_ro": 'Romanian',

        "lang_ru": 'Russian',

        "lang_sk": 'Slovak',

        "lang_sl": 'Slovenian',

        "lang_sr": 'Serbian',

        "lang_sv": 'Swedish',

        "lang_tr": 'Turkish',

        "lang_zh-CN": 'Chinese (Simplified)',

        "lang_zh-TW": 'Chinese (Traditional)'
    }
    res = [key for key, val in Lcd.items() if lang in val]
    print(res)
    lgCode = res[0]
    
    return lgCode

def UnderlineText(string):
    emptystring = ''

    for i in range(0, len(string)):

        if string[i] == ' ':
            emptystring = emptystring + string[i]
        else:
            emptystring= emptystring+string[i]+str('\u0332')

    return emptystring

if __name__ == "__main__":
    AUTOID = input("Enter AutoID : ")
    getExistingDetails(AUTOID)  #24429432