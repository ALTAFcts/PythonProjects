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
import sherlock.sherlockTest


options = Options()
options.add_argument('-no-sandbox')
driver = webdriver.Chrome(chrome_options=options,executable_path="D:/VSProjects/DemoPython/chromedriver.exe")


def getExistingDetails(AutoId):
    print(green("Taking Details from People Service",['bold', 'underlined']))
    # 993277596 Partha id.
    objTest = FM.FMTEST.FMInfo(AutoId) #"98745874")
    objJson = objTest.main()
    # objJson = FM.FM.main("993277596")
    #print("before calling print")
    #print(objJson)
    # objsite = []
    # objsite.append("Facebook")
    # objsite.append("Twitter")
    # objsite.append("Instagram")
    # objsite.append("Linkedin")
    # # python sherlock.py rohit_chahal --timeout 5 --site Facebook --site Twitter --site Instagram --site Linkedin --print-all
    # try:
    #     objRetVal = sherlock.sherlockTest.main("rohit_chahal",5,objsite)
    #     print(str(objRetVal))
    # except Exception as sherEr:
    #     print(str(sherEr))

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
    Rule_1_Params = []
    
    try:
        Details = objJson[0]['Details']
        if len(Details) > 0:
            print("Existing Know Facts found from People Service")
            print(Details)
            #break
        try:
            FullName = Details[0]['FULL_NAME'].strip()
            FullName = ' '.join(FullName.split())
        except:
            pass
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
            'KNOWNAS':AknowAs
        }
        Rule_1_Params.append(pdict)

    
    except Exception as ferr:
        print(str(ferr))
    
    stringP = "Rule Parameters are Below:"
    strRulstring = UnderlineText(stringP)
    print(strRulstring)
    print(pdict)
    #print("Find More ID:-"+str(Find_More_ID))
    customSrchfacebook(Details,Rule_1_Params,Find_More_ID)
    #customSrchInstagram(Details,Rule_1_Params)

def customSrchfacebook(Details,Rule_1_Params,Find_More_ID):
    print(green("Under Custom Search facebook",['bold', 'underlined']))
    p = 1
    Facebook_list = []
    Lang = ""
    Full_Name = ""
    country = ""
    kcode = ""
    cCode = ""
    N_FName = ""
    N_CName = ""
    Full_Name = Rule_1_Params[0]['Full_Name']
    country = Rule_1_Params[0]['Country']
    N_CName = string.capwords(country)
    constring = "Taking Country From Known Facts"
    strCstring = UnderlineText(constring)
    print(str(strCstring)+" :=  "+str(N_CName))
    if N_CName.strip() !="":
        kcode = GetCountryCode(N_CName,kcode)
    cCode = kcode
    #print("Getting CountryCode of AutoID Record:=  "+str(cCode))
    #Full_Name = "رنجن كومار داس"
    N_FName = string.capwords(Full_Name)
    fulNstring = "Taking Full Name from Know Facts"
    strFNstring = UnderlineText(fulNstring)
    print(str(strFNstring)+" :=  "+yellow(Full_Name)+",   Formatted Full Name :=  "+green(N_FName))
    driver.get("https://www.facebook.com/search/top?q=Partha%20Bhattacharyya")
    driver.maximize_window()

    while p <=10:
        
        page = p
        # constructing the URL
        # doc: https://developers.google.com/custom-search/v1/using_rest
        # calculating start, (page=2) => (start=11), (page=3) => (start=21)
        start = (page - 1) * 10 + 1
        # Ram Mohan
        # ramm16833@gmail.com
        # 7075807215
        # cts@1234
        ## Email : ranaayyubi748@gmail.com, pwd : cts@1234
        apiCX = "017c6b99e921dc077"
        apikey = "AIzaSyBErNU07qrFARpzcgdvKQTWyiCmtcUBEzw"
        #AIzaSyATqO-ETAIhjg4-M9OjjCHosrWNhb9ypwg
        
        Qry = '"{}"'.format(N_FName)+"site:https://www.facebook.com"
        try:
            API = "https://www.googleapis.com/customsearch/v1?key="+str(apikey)+"&cx="+str(apiCX)+"&gl="+str(cCode)+"&q="+Qry+"&start="+str(start)+""
            response = requests.get(API).json()
            time.sleep(2)
        except Exception as apiError:
            print("apiError:"+str(apiError))
        #resultjson = json.loads(response.get("Result"))
        #print(response)
        
        try:
            #search_items = ""
            search_items = response.get("items")
        except Exception as itemError:
            print("itemError:"+str(itemError))
        try:
            if len(search_items) > 0:
                for srch in search_items:
                    if N_FName in srch['title']:
                        if "public" not in srch['link']:
                            if "posts" not in srch['link']:
                                if "people" not in srch['link']:
                                    if "/photos" not in srch['link']:
                                        if "/videos" not in srch['link']:
                                            if "/likes" not in srch['link']:
                                                if "/about" not in srch['link']:
                                                    Facebook_list.append(srch)
        except Exception as FErr:
            if "NoneType" in str(FErr):
                break
            pass
        else:
            pass
            #print("-")
            #print("Else: Loop in Progress ")
            
        #print("FIND_MORE in facebook")

        p = p+1
    #print(Facebook_list)
    Facebook_list_New = []
    tRec = ""
    try:
        tRec = len(Facebook_list)
    except:
        pass
    print("TOTAL RESULTS By Applying RULE PARAMS:[Full Name,Country] from Google :=  "+str(tRec))
    for item in Facebook_list:
        try:
            titleN = ""
            titleName= ""
            titleFN = ""
            titleFNH = ""
            titleN = item['title']
            titleName = titleN.split("|")
            titleFN = titleName[0].strip()
            if titleFN == N_FName:
                Facebook_list_New.append(item)
            if "Home" in titleFN:
                titleFNH = titleFN.split("-")
                titleFNH = titleFNH[0].strip()
                if titleFNH == N_FName:
                    Facebook_list_New.append(item)
        except Exception as Refne:
            print(str(Refne))
            pass
    fcount = ""
    try:
        fcount = len(Facebook_list_New)
    except:
        pass
    print("Total FACEBOOK LINKS After Applying More Filteration :=  "+str(fcount))
    customSrchLinkedin(Details,Facebook_list_New,Rule_1_Params,Find_More_ID,cCode,fcount)
   
def customSrchLinkedin(Details,Facebook_list_New,Rule_1_Params,Find_More_ID,cCode,fcount):
    
    print(green("Under Custom Search Linkedin",['bold', 'underlined']))

    p = 1
    LinkedIN_list = []
    Full_Name = ""
    country = ""
    Full_Name = Rule_1_Params[0]['Full_Name']
    country = Rule_1_Params[0]['Country']
    N_FName = string.capwords(Full_Name)
    #print(N_FName)
    while p <=10:
        
        page = p
        # constructing the URL
        # doc: https://developers.google.com/custom-search/v1/using_rest
        # calculating start, (page=2) => (start=11), (page=3) => (start=21)
        start = (page - 1) * 10 + 1
        # email : fareedpasha5544@gmail.com , Pwd : cts@1234
        apiCX = "d1cfb51b56ce9eb08"
        apikey = "AIzaSyDFf5t3Rinx2oK6_Soyw-w0Zz91YxW11dc"
        #AIzaSyATqO-ETAIhjg4-M9OjjCHosrWNhb9ypwg
        # Full_Name = ""
        # Full_Name = 'Partha Bhattacharyya'
        Qry = '"{}"'.format(N_FName)+"site:https://www.linkedin.com"
        try:
            #API = "https://www.googleapis.com/customsearch/v1?key="+str(apikey)+"&cx="+str(apiCX)+"&q="+Qry+"&start="+str(start)+""
            API = "https://www.googleapis.com/customsearch/v1?key="+str(apikey)+"&cx="+str(apiCX)+"&gl="+str(cCode)+"&q="+Qry+"&start="+str(start)+""
            response = requests.get(API).json()
        except Exception as apiError:
            print("apiError:"+str(apiError))
        #resultjson = json.loads(response.get("Result"))
        #print(response)
        
        try:
            #search_items = ""
            search_items = response.get("items")
        except Exception as itemError:
            print("itemError:"+str(itemError))
        try:
            if len(search_items) > 0:
                for srch in search_items:
                    if N_FName in srch['title']:
                        #if country in srch['title']:
                        if "public" not in srch['link']:
                            if "pub/dir" not in srch['link']:
                                if "/pulse" not in srch['link']:
                                    if "search-card" not in srch['link']:
                                        LinkedIN_list.append(srch)
        except Exception as LNKErr:
            if "NoneType" in str(LNKErr):
                break
            pass
        else:
            pass
            #print("Else: Loop in Progress ")
           
        #print("FIND_MORE in Linkedin")

        p = p+1
    #print(Details)
    #print(Rule_1_Params)
    #print(Facebook_list)
    LinkedIN_list_New = []
    #print(LinkedIN_list)
    linCount = ""
    try:
        linkCount = len(LinkedIN_list)
    except:
        pass
    print("TOTAL RESULTS By Applying RULE PARAMS:[Full Name,Country] from Google :=  "+str(linkCount))
    for lk in LinkedIN_list:
        try:
            Ltitle = ""
            LtitleName= ""
            LtitleFN = ""
            LtitleFNH = ""
            LtitleN = lk['title']
            LtitleName = LtitleN.split("-")
            LtitleFN = LtitleName[0].strip()
            if LtitleFN == N_FName:
                LinkedIN_list_New.append(lk)
        except Exception as Refne:
            print(str(Refne))
            pass
    
    Lcount = ""
    try:
        Lcount = len(LinkedIN_list_New)
    except:
        pass
    print("Total LINKEDIN LINKS After Applying More Filteration :=  "+str(Lcount))
    Fcbk_links = []
    Lnkd_links = []
    

    for f in Facebook_list_New:
        f_lnk = f['link']
        f_title = f['title']
        df={
            'FTitle':f_title,
            'FProfileLink':f_lnk
        }
        Fcbk_links.append(df)
    for l in LinkedIN_list_New:
        L_lnk = l['link']
        L_title = l['title']
        dL= {
            'LTitle':L_title,
            'LProfileLink':L_lnk
        }
        Lnkd_links.append(dL)
    #print(Fcbk_links)
    #print(Lnkd_links)
    customSrchInstagram(Details,Rule_1_Params,Fcbk_links,Lnkd_links,Find_More_ID,cCode,fcount,Lcount)

def customSrchInstagram(Details,Rule_1_Params,Fcbk_links,Lnkd_links,Find_More_ID,cCode,fcount,Lcount):
    
    print(green("Under Custom Search Instagram",['bold', 'underlined']))
    p = 1
    Instagram_list = []
    Full_Name = ""
    country = ""
    Full_Name = Rule_1_Params[0]['Full_Name']
    country = Rule_1_Params[0]['Country']
    #print(Full_Name)
    N_FName = string.capwords(Full_Name)
    #print(N_FName)
    while p <=1:
        
        page = p
        # constructing the URL
        # doc: https://developers.google.com/custom-search/v1/using_rest
        # calculating start, (page=2) => (start=11), (page=3) => (start=21)
        start = (page - 1) * 10 + 1
        # email : shaista0155@gmail.com , Pwd : cts@1234
        apiCX = "8612f3ee954bc0429"
        apikey = "AIzaSyATshbcubTxj7xGlPNWY-9qzeGMycLHQE4"
        #AIzaSyATqO-ETAIhjg4-M9OjjCHosrWNhb9ypwg
        # Full_Name = ""
        # Full_Name = 'Partha Bhattacharyya'
        Qry = '"{}"'.format(N_FName)+"site:https://www.instagram.com"
        try:
            #API = "https://www.googleapis.com/customsearch/v1?key="+str(apikey)+"&cx="+str(apiCX)+"&q="+Qry+"&start="+str(start)+""
            API = "https://www.googleapis.com/customsearch/v1?key="+str(apikey)+"&cx="+str(apiCX)+"&gl="+str(cCode)+"&q="+Qry+"&start="+str(start)+""
            response = requests.get(API).json()
        except Exception as apiError:
            print("apiError:"+str(apiError))
        #resultjson = json.loads(response.get("Result"))
        #print(response)
        
        try:
            #search_items = ""
            search_items = response.get("items")
        except Exception as itemError:
            print("itemError:"+str(itemError))
        try:
            if len(search_items) > 0 :
                for srch in search_items:
                    if N_FName in srch['title']:        
                        Instagram_list.append(srch)
        except Exception as INSerr: 
            if "NoneType" in str(INSerr):
                break
            pass
            
        else:
            pass
            #print("Else: Loop in Progress ")
            
        #print("FIND_MORE in Instagram")

        p = p+1
    #print(Instagram_list)
    instaCount = ""
    instaCount = len(Instagram_list)
    print("TOTAL RESULTS By Applying RULE PARAMS:[Full Name,Country] from Google :=  "+str(instaCount))
    Insta_links = []
    Instagram_list_New = []
    for ln in Instagram_list:
        try:
            ititle = ""
            ititleName= ""
            ititleFN = ""
            ititleFNH = ""
            ititleN = ln['title']
            ititleName = ititleN.split("(")
            ititleFN = ititleName[0].strip()
            if ititleFN == N_FName:
                Instagram_list_New.append(ln)
        except Exception as iefne:
            print(str(iefne))
            pass
    icount = ""
    icount = len(Instagram_list_New)
    print("Total INSTAGRAM LINKS After Applying More Filteration :=  "+str(icount))
    for Ilk in Instagram_list:
        i_lnk = Ilk['link']
        i_title = Ilk['title']
        di = {
            'iTitle':i_title,
            'iProfileLink':i_lnk
        }
        Insta_links.append(di)
    
    
    strFkont = "Facebook Links"
    strFRkont = UnderlineText(strFkont)
    print(str(strFRkont)+" :=  "+str(fcount))
    strLkont = "LinkedIn Links"
    strLRkont = UnderlineText(strLkont)
    print(str(strLRkont)+" :=  "+str(Lcount))
    strIkont = "Instagram Links"
    strIRkont = UnderlineText(strIkont)
    print(str(strIRkont)+" :=  "+str(icount))
    print("All Three Sources Done")
    print("-----------------------")
    print("Printing Facebook links")
    print(Fcbk_links)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("Printing Linkedin links")
    print(Lnkd_links)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("Printing Instagram links")
    print(Insta_links)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    # print(str :=  "+str(fcount))
    # print("Lnkd_links :=  "+str(Lcount))
    # print("Insta_links :=  "+str(icount))
    # FBQRY = ""
    # F_Site = "Facebook"
    # for item in Fcbk_links:
    #     try:
    #         strName = item['FTitle']
    #         strLink = item['FProfileLink']
            
    #         # jobQRY = jobQRY +"IF NOT EXISTS(SELECT ICE_LINK_RECORD_ID FROM ICE_JOB_DETAILS WHERE ICE_LINK_RECORD_ID='"+str(strLK_ID)+"' AND START_DATE = '"+str(strstD)+"' AND END_DATE = '"+str(strendD)+"' AND DESCRIPTION = '"+str(strDES)+"')"
    #         # jobQRY = jobQRY +"BEGIN   "
    #         FBQRY = FBQRY + "INSERT INTO FIND_MORE_DEV.DBO.FIND_MORE(FIND_MORE_ID,SITE_NAME,NAME,TITLE,LINK) VALUES (N'%s',N'%s',N'%s',N'%s',N'%s'); " % ( Find_More_ID, F_Site, N_FName, strName, strLink)
    #         # jobQRY = jobQRY +"END;   "
    #     except Exception as jdr:
    #         print(str(jdr))
    #         pass
    # print(FBQRY)

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
    getExistingDetails(AUTOID)