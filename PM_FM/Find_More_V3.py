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
    print("Taking Details from People Service := ")
    # strRulstring = UnderlineText(stringP)
    # print(strRulstring)
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
    Dplace = ""
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
        try:
            Details = objJson[0]['Details']
            print(json.dumps(Details, indent = 4,ensure_ascii=False))
        except Exception as Err0:
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

    
        try:
            stringP = "Contact Details are below :="
            strRulstring = UnderlineText(stringP)
            #print(strRulstring)
            #print(pdict)
        except:
            pass

        contact_details = objJson[0]['phone']
        
        if len(Details) > 0:
            print("Existing KNOWN FACTS found from PEOPLE Service")
            #print(Details)
            #break
        try:
            FullName = Details[0]['FULL_NAME'].strip()
            FullName = ' '.join(FullName.split())
            print("Full Name of the Person := "+ str(FullName))

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
            social_Source = []
            
            FB_name = ""
            Insta_name = ""
            Twtr_name = ""
            
            for acnt in Acount_Dict:
                try:
                    
                    SocSource = ""
                    SocName = ""
                    SocSource = acnt['Source']
                    SocName = acnt['Screen']
                    d={
                        "Source":SocSource,
                        "screen":SocName
                    }
                    social_Source.append(d)
                    social_list.append(SocSource)
                    if SocSource == "Facebook":
                        FB_name = acnt['Screen']
                    elif SocSource == "Twitter":
                        Twtr_name = acnt['Screen']
                    elif SocSource == "Instagram":
                        Insta_name = acnt['Screen']
                except:
                    pass
            
            print("Following Are the Social Accounts Found from KNOWN FACTS :=")
            # strRulstring = UnderlineText(stringP)
            # print(strRulstring)
            FM_Instagram_List = []
            FM_Facbook_List = []
            FM_Twitter_List = []
            print(json.dumps(social_Source, indent = 4))
            Allthree = False
            if "Instagram" in social_list and "Twitter" in social_list and "Facebook" in social_list:
                print("All three Social Accounts Exists")
                Allthree = True
                #input("Press ENTER to Exist From Tool")
            else:

                if "Instagram" not in social_list:
                    print("== Instagram not in Social list ==")
                    y = ""
                    screen = ""
                    FBName = ""
                    Update_Status = ""
                    FBName = FB_name.isalpha()


                    if FB_name != "":
                        screen = FB_name
                        print("Taking FACEBOOK SCREEN NAME and Passing To INSTAGRAM OSINT SERViCE")
                        print(screen)
                        try:
                            y,Update_Status = PassToOsintInsta(screen,y,Update_Status)
                        except Exception as ptoins:
                            print(str("PassToOsintInsta Get Error Pls Check"+str(ptoins)))

                        if Update_Status != "3" and y != "":
                            FM_Instagram_List = PassToInstaSocialList(y,Update_Status,FullName,Fname,Lname,FM_Instagram_List)
                            if len(FM_Instagram_List) > 0:
                                print("Instagram Details Found with Facebook Screen Name Added to FIND MORE FACTS")
                                #print(json.dumps(FM_Instagram_List,indent = 4,ensure_ascii = False))
                                FM_Social_list.extend(FM_Instagram_List)
                        elif Update_Status == "3":
                            print("Invalid FACEBOOK SCREEN NAME Passed to Instagram Osint Service := "+str(Update_Status))
                            print("Instagram Account Not Found with FACEBOOK SCREEN NAME")
                    if Twtr_name !="":
                        screen = Twtr_name
                        print("Taking TWITTER SCREEN NAME and Passing To INSTAGRAM OSINT SERVICE")
                        print(screen)
                        try:
                            y,Update_Status = PassToOsintInsta(screen,y,Update_Status)
                        except Exception as ptoins2:
                            print(str("PassToOsintInsta Get Error Pls Check"+str(ptoins2)))
                        if Update_Status != "3" and y != "":
                            FM_Instagram_List = PassToInstaSocialList(y,Update_Status,FullName,Fname,Lname,FM_Instagram_List,screen)
                            if len(FM_Instagram_List) > 0:
                                print("Instagram Details Found with Twitter Screen Name Added to FIND MORE FACTS")
                                #print(json.dumps(FM_Instagram_List, indent = 4,ensure_ascii=False))
                                FM_Social_list.extend(FM_Instagram_List)
                        elif Update_Status == "3":
                            print("Invalid TWITTER SCREEN NAME Passed to Instagram Osint Service := "+str(Update_Status))
                            print("Instagram Account Not Found with TWITTER SCREEN NAME")
                    
                    if len(FM_Instagram_List) == 0:
                            print("NOW APPLYING LOGIC of FULLNAME")
                            print(FullName)
                            NewFullName = ""
                            NewFullName = FullName.replace(" ","")
                            print("NewFullName = "+str(NewFullName))
                            print("FullName of PeopleName is AGAIN SENDING by Removing Spaces to INSTAGRAM OSINT SERViCE")
                            print("NewFullName = "+str(NewFullName))
                            y,Update_Status = PassToOsintInsta(NewFullName,y,Update_Status)
                            if Update_Status != "3" and y != "":
                                FM_Instagram_List = PassToInstaSocialList(y,Update_Status,FullName,Fname,Lname,FM_Instagram_List,screen)
                                if len(FM_Instagram_List) > 0:
                                    print("Instagram Account Found with Full NAME Logic")
                                    print("Instagram Details Found with Twitter Screen Name Added to FIND MORE FACTS")
                                    #print(json.dumps(FM_Instagram_List, indent = 4,ensure_ascii=False))
                                    FM_Social_list.extend(FM_Instagram_List)
                                else:
                                    print("Instagram Account Not Found with Full NAME Logic")

                if "Facebook" not in social_list:
                    f = ""
                    screen = ""
                    print("== Facebook not in Social list ==")
                    if Twtr_name != "":
                        screen = Twtr_name
                        print("Taking Twitter SCREEN NAME and Passing To FACEBOOK OSINT SERViCE")
                        print(screen)
                        try:
                            f = PassToOsintFacebok(f,screen)
                        except Exception as ptofck:
                            print(str("PassToOsintInsta Get Error Pls Check"+str(ptofck)))
                        
                        if f != "":
                            FM_Facbook_List = PassToFacebokSocialList(f,FullName,Fname,Lname,FM_Facbook_List,screen)
                            if len(FM_Facbook_List) > 0:
                                print("FACEBOOK Details Found with Twitter SCREEN NAME Added to FIND MORE FACTS")
                                #print(json.dumps(FM_Facbook_List, indent = 4,ensure_ascii=False))
                                FM_Social_list.extend(FM_Facbook_List)
                        else:
                            print("Facebook Details Not FOUND with Twitter SCREEN NAME")
                    if Insta_name != "":
                        screen = Insta_name
                        print("Taking Instagram SCREEN NAME and Passing To FACEBOOK OSINT SERViCE")
                        print(screen)
                        try:
                            f = PassToOsintFacebok(f,screen)
                        except Exception as ptofck:
                            print(str("PassToOsintInsta Get Error Pls Check"+str(ptofck)))
                        
                        if f != "":
                            FM_Facbook_List = PassToFacebokSocialList(f,FullName,Fname,Lname,FM_Facbook_List,screen)
                            if len(FM_Facbook_List) > 0:
                                print("FACEBOOK Details Found with Instagram Screen Name Added to FIND MORE FACTS")
                                #print(json.dumps(FM_Facbook_List, indent = 4,ensure_ascii=False))
                                FM_Social_list.extend(FM_Facbook_List)
                        elif len(FM_Facbook_List) == 0:
                            print("Facebook Details not FOUND with Instagram Screen Name Under Facebook OsintService")

                if "Twitter" not in social_list:
                    t = ""
                    screen = ""
                    print("== Twitter Not in Social List ==")
                
                    if FB_name != "":
                        screen = FB_name
                        print("Taking FACEBOOK SCREEN NAME and Passing To TWITTER OSINT SERViCE")
                        print(screen)
                        try:
                            t = PassToOsintTwitter(t,screen)
                        except Exception as ptotwt:
                            print(str("PassToOsintInsta Get Error Pls Check"+str(ptotwt)))
                        if t != "":
                            FM_Twitter_List = PassToTWITTERSocialList(t,FullName,Fname,Lname,FM_Twitter_List,screen)
                            if len(FM_Twitter_List) > 0 :
                                FM_Social_list.extend(FM_Twitter_List)
                                print("Twitter Details Found with FACEBOOK SCREEN NAME and Added to FIND MORE FACTS")
                                #print(json.dumps(FM_Twitter_List, indent = 4,ensure_ascii=False))
                            else:
                                if len(FM_Twitter_List) == 0:
                                    print("Twitter Details not FOUND with FACEBOOK SCREEN NAME")

                    if Insta_name != "":
                        screen = Insta_name
                        print("Taking INSTAGRAM SCREEN NAME and Passing To TWITTER OSINT SERViCE")
                        print(screen)
                        try:
                            t = PassToOsintTwitter(t,screen)
                        except Exception as ptotwt2:
                            print(str("PassToOsintInsta Get Error Pls Check"+str(ptotwt2)))
                        if t != "":
                            FM_Twitter_List = PassToTWITTERSocialList(t,FullName,Fname,Lname,FM_Twitter_List,screen)
                            if len(FM_Twitter_List) > 0 :
                                print("Twitter Details Found with Instagram Screen Name and Added to FIND MORE FACTS")
                                #print(json.dumps(FM_Twitter_List, indent = 4,ensure_ascii=False))
                                FM_Social_list.extend(FM_Twitter_List)
                            else:
                                if len(FM_Twitter_List) == 0:
                                    print("Twitter Details not FOUND with Instagram Screen Name")
                
            try:
                if Allthree == False:
                #print(FM_Social_list)
                    print("==> So Final Details from FIND MORE Tool Are as Follows:=")
                    print(json.dumps(FM_Social_list, indent = 4,ensure_ascii=False))
                    if len(FM_Social_list) == 0:
                        print("Nothing Get Found from FIND MORE Tool with Existing KNOWN FACTS")
                    else:
                        print("Please Find Above Details from FIND MORE Tool from Social Media KNOWN FACTS")
                else:
                    print("All Three Account Details(Facebook,Twitter,Instagram) are Already Present in KNOWN FACTS")
            except Exception as L1:
                print(str(L1))
            input("Press ENTER to exit")
            #if "Facebook" not in social_list:
        else:
            print("KNOWN FACTS of SOCIAL ACCOUNTS Does Not Exists To Search in FIND MORE")
            input("Press ENTER to exit")
    except Exception as MainError:
        print("MainError:="+str(MainError))

def PassToOsintInsta(screen,y,Update_Status):
    try:
        json_Insta = ""
        json_Insta = Osint_Instagram(screen)
    except Exception as Err2:
        print("Err2 At JsonInsta:="+str(Err2))
        json_Insta = ""
    if json_Insta != "":
        try:
            
            y = json.loads(json_Insta)
            Update_Status = y['UPDATE_STATUS']
            
        except Exception as Err5:
            print(str(Err5))
    else:
        y = ""
        Update_Status = ""
    return y,Update_Status

def PassToInstaSocialList(y,Update_Status,FullName,Fname,Lname,FM_Instagram_List,screen):
    FM_Instagram_List = []
    Fmore_InstaUM = ""
    Fmore_Website = ""
    Update_Status = ""
    Profile_Pic = ""
    
    FindMore_InstaName = y["FULL_NAME"]
    Fmore_InstaUM = y["USER_NAME"]
    Fmore_Website = y['WEBSITE']
    Update_Status = y['UPDATE_STATUS']
    Profile_Pic = y['PROFILE_PICTURE_URL']
    FindMore_InstaName = string.capwords(FindMore_InstaName)
    FullName = string.capwords(FullName)
    try:
        TS_list = []
        ts1= ""
        ts2 =""
        ts3 =""
        ts1= y["USER_NAME"]
        ts2 = y['WEBSITE']
        ts3 = y['PICTURE_URL']
        TS = {
            "Twitter":ts1,
            "Name":ts2,
            "Profile_Pic":ts3
        }
        TS_list.append(TS)
        print(json.dumps(TS_list,indent=4,ensure_ascii=False))
    except:
        pass
    if FindMore_InstaName != "Null":
        try:
            if FindMore_InstaName == FullName:
                d= ""
                print("FULL NAME of INSTAGRAM == FullName of PEOPLEMON")
                print(FindMore_InstaName+"=="+FullName)
                d = {
                        "Instagram":Fmore_InstaUM,
                        "Website":Fmore_Website,
                        "Insta_PIC":Profile_Pic
                    }
                #print("Instagram Account Adding to FIND MORE INSTAGRAM LIST")
                FM_Instagram_List.append(d)
            else: 
                Fname = string.capwords(Fname)
                Lname = string.capwords(Lname)
                if Fname in FindMore_InstaName and Lname in FindMore_InstaName:
                    if Update_Status != "3":
                        print("First and last Name Get MATCHED")
                        print(Fname)
                        print(Lname)
                        print(FindMore_InstaName)
                        d = {
                            "Instagram":Fmore_InstaUM,
                            "Website":Fmore_Website,
                            "Insta_PIC":Profile_Pic
                        }
                        print("Instagram Account Adding to FIND MORE INSTAGRAM LIST")
                        FM_Instagram_List.append(d)
                else:
                    screen = string.capwords(screen) 
                    Fmore_InstaUM = string.capwords(Fmore_InstaUM)
                    if screen == Fmore_InstaUM:
                        if Update_Status != "3":
                            # print("Full Name of People Not Matched")
                            # print("First and Last Name are not exists in Full Name of Instagram")
                            # print("But")
                            print("Need to Proceed for Next Step using PROFILE PHOTO Analysis")
                            print(screen+"=="+Fmore_InstaUM)
                            d = {
                                "Instagram":Fmore_InstaUM,
                                "Website":Fmore_Website,
                                "Insta_PIC":Profile_Pic
                            }
                            FM_Instagram_List.append(d)
        except Exception as Inst_1:
            print("Inst_1 Error:"+str(Inst_1))
    else:
        print("Full Name is NULL from KNOWN FACTS Data")
        try:
            screen = string.capwords(screen) 
            Fmore_InstaUM = string.capwords(Fmore_InstaUM)
            if screen == Fmore_InstaUM:
                print("Need to Proceed for Next Step using PROFILE PHOTO Analysis")
                print(screen+"=="+Fmore_InstaUM)
                d = {
                    "Instagram":Fmore_InstaUM,
                    "Website":Fmore_Website,
                    "Insta_PIC":Profile_Pic
                }
                FM_Instagram_List.append(d)
        except Exception as Inst_2:
            print("Inst_2 Error:"+str(Inst_2))

    return FM_Instagram_List

def PassToOsintFacebok(f,screen):
    try:
        json_FB = ""
        json_FB = osint_facebook(screen)
    except Exception as FB_eer3:
        print(str(FB_eer3))
        json_FB = ""
    if json_FB != "":
        f = json.loads(json_FB)
    if "Invalid Profile Has Been Requested" in f:
        print("OSINT FACEBOOK SERVICE:= Invalid Profile Has Been Requested")
        f = ""

    return f

def PassToFacebokSocialList(f,FullName,Fname,Lname,FM_Facbook_List,screen):
    FM_Facbook_List= []
    FindMore_FacebokName = ""
    ProfilePic_Fbk = ""
    Fmore_FBUM = ""
    Is_Page = ""
    Is_Page = f["IS_PAGE"]
    pf = ""
    try:
        TS_list = []
        TS = ""
        ts1= ""
        ts2 =""
        ts3 =""
        ts1= f["NAME"]
        ts2 = f['USERNAME']
        ts3 = f['PICTURE']
        TS = {
            "Facebook":ts2,
            "Name":ts1,
            "Profile_Pic":ts3
        }
        TS_list.append(TS)
        print(json.dumps(TS_list,indent=4,ensure_ascii=False))
    except:
        pass
    if Is_Page == "0":
        print("The Requested Screen Found As a Facebook Profile from Osint Service")
        if FullName != "":
            try:
                FindMore_FacebokName = f["NAME"]
                ProfilePic_Fbk = f['PICTURE']
                Fmore_FBUM = f['USERNAME']
                FullName = string.capwords(FullName)
                FindMore_FacebokName = string.capwords(FindMore_FacebokName)
               
                if FindMore_FacebokName == FullName:
                    print("Full Name Get Matched")
                    print(FindMore_FacebokName+"=="+FullName)
                    d={
                        "Facebook":Fmore_FBUM,
                        'Name':FindMore_FacebokName,
                        'Profile_Pic':ProfilePic_Fbk
                        }
                    FM_Facbook_List.append(d)
                
                else:
                    if Fname !="":
                        FindMore_FacebokName = f["NAME"]
                        ProfilePic_Fbk = f['PICTURE']
                        Fmore_FBUM = f['USERNAME']
                        print("Full Name Not Matched for FB")
                        Fname = string.capwords(Fname)
                        Lname = string.capwords(Lname)
                        if Fname in FindMore_FacebokName and Lname in FindMore_FacebokName:
                            print("Matching First and LAST Name present in Full Name")
                            print(Fname)
                            print(Lname)
                            print(FindMore_FacebokName)
                            d={
                                "Facebook":Fmore_FBUM,
                                'Name':FindMore_FacebokName,
                                'Profile_Pic':ProfilePic_Fbk
                            }
                            FM_Facbook_List.append(d)
                        else:
                            screen = string.capwords(screen)
                            Fmore_FBUM = string.capwords(Fmore_FBUM)
                            if Fmore_FBUM == screen:
                                # print("Full Name of People Not Matched")
                                # print("First and Last Name are not exists in Full Name of FACEBOOK")
                                # print("But")
                                print("Need to Proceed for Next Step using PROFILE PHOTO Analysis")
                                print(screen+"=="+Fmore_FBUM)
                                d={
                                    "Facebook":Fmore_FBUM,
                                    'Name':FindMore_FacebokName,
                                    'Profile_Pic':ProfilePic_Fbk
                                }
                                FM_Facbook_List.append(d)
                            
            except Exception as Fb1_err:
                print("Fb1_err:="+str(Fb1_err))
        else:
            try:
                print("Full Name is Null from KNOWN FACTS Facebook")
                if Fname !="":
                    FindMore_FacebokName = f["NAME"]
                    ProfilePic_Fbk = f['PICTURE']
                    Fmore_FBUM = f['USERNAME']
                    Fname = string.capwords(Fname)
                    Lname = string.capwords(Lname)
                    
                    if Fname in FindMore_FacebokName and Lname in FindMore_FacebokName:
                        print("First and LAST Name of KNOWN FACTS Get Matched with FindMore Name of facebook")
                        print(Fname)
                        print(Lname)
                        print(FindMore_FacebokName)
                        d={
                            "Facebook":Fmore_FBUM,
                            'Name':FindMore_FacebokName,
                            'Profile_Pic':ProfilePic_Fbk
                        }
                        FM_Facbook_List.append(d)
                    else:
                        screen = string.capwords(screen)
                        Fmore_FBUM = string.capwords(Fmore_FBUM)
                        if Fmore_FBUM == screen:
                            # print("Full Name of People Not Matched")
                            # print("First and Last Name are not exists in Full Name of FACEBOOK")
                            # print("But")
                            print("Need to Proceed for Next Step using PROFILE PHOTO Analysis")
                            print(screen+"=="+Fmore_FBUM)
                            d={
                                "Facebook":Fmore_FBUM,
                                'Name':FindMore_FacebokName,
                                'Profile_Pic':ProfilePic_Fbk
                            }
                            FM_Facbook_List.append(d)
                else:
                    pass
            except Exception as Fb2_err:
                print("Fb2_err:="+str(Fb2_err))
    else:
        if Is_Page == "1":
            print("The Requested Screen Found As a Facebook Page from Osint Service")
            if FullName != "":
                try:
                    FindMore_FacebokName = f["NAME"]
                    ProfilePic_Fbk = f['PICTURE']
                    Fmore_FBUM = f['USERNAME']
                    FullName = string.capwords(FullName)
                    FindMore_FacebokName = string.capwords(FindMore_FacebokName)
                    # pf = {
                    #     "Facebook":Fmore_FBUM,
                    #     'Name':FindMore_FacebokName,
                    #     'Profile_Pic':ProfilePic_Fbk
                    #     }
                    # print(pf)
                    if FindMore_FacebokName == FullName:

                        print("Full Name Get Matched")
                        print(FindMore_FacebokName+"=="+FullName)
                        d={
                            "Facebook":Fmore_FBUM,
                            'Name':FindMore_FacebokName,
                            'Profile_Pic':ProfilePic_Fbk
                            }
                        FM_Facbook_List.append(d)
                    
                    else:
                        if Fname !="":
                            FindMore_FacebokName = f["NAME"]
                            ProfilePic_Fbk = f['PICTURE']
                            Fmore_FBUM = f['USERNAME']
                            print("Full Name Not Matched for FB")
                            Fname = string.capwords(Fname)
                            Lname = string.capwords(Lname)

                            if Fname in FindMore_FacebokName and Lname in FindMore_FacebokName:
                                print("Matching First and LAST Name present in Full Name")
                                print(Fname)
                                print(Lname)
                                print(FindMore_FacebokName)
                                d={
                                    "Facebook":Fmore_FBUM,
                                    'Name':FindMore_FacebokName,
                                    'Profile_Pic':ProfilePic_Fbk
                                }
                                FM_Facbook_List.append(d)
                            else:
                                screen = string.capwords(screen)
                                Fmore_FBUM = string.capwords(Fmore_FBUM)
                                if Fmore_FBUM == screen:
                                    # print("Full Name of People Not Matched")
                                    # print("First and Last Name are not exists in Full Name of FACEBOOK")
                                    # print("But")
                                    print("Need to Proceed for Next Step using PROFILE PHOTO Analysis")
                                    print(screen+"=="+Fmore_FBUM)
                                    d={
                                        "Facebook":Fmore_FBUM,
                                        'Name':FindMore_FacebokName,
                                        'Profile_Pic':ProfilePic_Fbk
                                    }
                                    FM_Facbook_List.append(d)
                                
                except Exception as Fb1_err3:
                    print("Fb1_err3:="+str(Fb1_err3))
            else:
                try:
                    print("Full Name is Null from KNOWN FACTS for Facebook")
                    if Fname !="":
                        FindMore_FacebokName = f["NAME"]
                        ProfilePic_Fbk = f['PICTURE']
                        Fmore_FBUM = f['USERNAME']
                        Fname = string.capwords(Fname)
                        Lname = string.capwords(Lname)

                        if Fname in FindMore_FacebokName and Lname in FindMore_FacebokName:
                            print("First and LAST Name of KNOWN FACTS Get Matched with FindMore Name of facebook")
                            print(Fname)
                            print(Lname)
                            print(FindMore_FacebokName)
                            
                            d={
                                "Facebook":Fmore_FBUM,
                                'Name':FindMore_FacebokName,
                                'Profile_Pic':ProfilePic_Fbk
                            }
                            FM_Facbook_List.append(d)
                        else:
                            screen = string.capwords(screen)
                            Fmore_FBUM = string.capwords(Fmore_FBUM)
                            if Fmore_FBUM == screen:
                                # print("Full Name of People Not Matched")
                                # print("First and Last Name are not exists in Full Name of FACEBOOK")
                                # print("But")
                                print("Need to Proceed for Next Step using PROFILE PHOTO Analysis")
                                print(screen+"=="+Fmore_FBUM)
                                d={
                                    "Facebook":Fmore_FBUM,
                                    'Name':FindMore_FacebokName,
                                    'Profile_Pic':ProfilePic_Fbk
                                }
                                FM_Facbook_List.append(d)
                    else:
                        pass
                except Exception as Fb2_err4:
                    print("Fb2_err4:="+str(Fb2_err4))



    return FM_Facbook_List

def PassToOsintTwitter(t,screen):
    try:
        json_Twitr = ""
        FindMore_TwtrkName = ""
        json_Twitr = osint_twitter(screen)
    except Exception as twitErr:
        print(twitErr)
        json_Twitr = ""
    if json_Twitr != "":
        t = json.loads(json_Twitr)
    if "Cannot serialize the DataTable" in json_Twitr:
        print("Osint Twitter KeyError := Cannot serialize the DataTable. DataTable name is not set.")
        print("Profile Does not exists, Invalid Profile")
        t = ""
    else:
        print("json for twitter exists")
        
        #print("Waiting for 60 seconds,Pls Wait..")
        #time.sleep(60)
    return t

def PassToTWITTERSocialList(t,FullName,Fname,Lname,FM_Twitter_List,screen):
    FM_Twitter_List = []
    FindMore_TwtrkName = ""
    Fmore_TwtrUM = ""
    Profile_PicTwtr = ""
    d = ""
    #t = json.loads(json_Twitr)
    try:
        TS_list = []
        TS = ""
        ts1= ""
        ts2 =""
        ts3 =""
        ts1= t["USER_NAME"]
        ts2 = t['SCREEN_NAME']
        ts3 = t['PICTURE_URL']
        TS = {
            "Twitter":ts1,
            "Name":ts2,
            "Profile_Pic":ts3
        }
        TS_list.append(TS)
        print(json.dumps(TS_list,indent=4,ensure_ascii=False))
    except:
        pass
    if FullName != "":
        try:

            FindMore_TwtrkName= t["USER_NAME"]
            Fmore_TwtrUM = t['SCREEN_NAME']
            Profile_PicTwtr = t['PICTURE_URL']
            FindMore_TwtrkName = string.capwords(FindMore_TwtrkName)
            FullName = string.capwords(FullName)
            if FindMore_TwtrkName == FullName:
                print("Twitter Full Name is Matched with KNOWN FACTS Full Name")
                print(FindMore_TwtrkName+"=="+FullName)
                d ={
                    "Twitter":FindMore_TwtrkName,
                    "Name":Fmore_TwtrUM,
                    "Profile_Pic":Profile_PicTwtr
                }
                FM_Twitter_List.append(d)
            if Fname != "":
                Fname = string.capwords(Fname)
                Lname = string.capwords(Lname)
                FindMore_TwtrkName = string.capwords(FindMore_TwtrkName)
                if Fname in FindMore_TwtrkName and Lname in FindMore_TwtrkName:
                    print("KNOWN FACTS first Name and Last Name is Matched with twitter Full Name")
                    print(Fname)
                    print(Lname)
                    print(FindMore_TwtrkName)
                    d ={
                    "Twitter":FindMore_TwtrkName,
                    "Name":Fmore_TwtrUM,
                    "Profile_Pic":Profile_PicTwtr
                    }
                    FM_Twitter_List.append(d)
                else:
                    screen = string.capwords(screen)
                    Fmore_TwtrUM = string.capwords(Fmore_TwtrUM)
                    if screen == Fmore_TwtrUM:
                        # print("Full Name of People Not Matched")
                        # print("First and Last Name are not exists in Full Name of TWITTER")
                        # print("But")
                        print("Need to Proceed for Next Step using PROFILE PHOTO Analysis")
                        print(screen+"=="+Fmore_TwtrUM)
                        d ={
                        "Twitter":FindMore_TwtrkName,
                        "Name":Fmore_TwtrUM,
                        "Profile_Pic":Profile_PicTwtr
                        }
                        FM_Twitter_List.append(d)

        except Exception as Twt_err:
            print(str(Twt_err))
    else:
        try:
            print("Full name is NULL from Poeple's Data")
            FindMore_TwtrkName= t["USER_NAME"]
            Fmore_TwtrUM = t['SCREEN_NAME']
            Profile_PicTwtr = t['PICTURE_URL']
            print("Full Name is Null from KNOWN FACTS for Facebook")
            if Fname != "":
                Fname = string.capwords(Fname)
                Lname = string.capwords(Lname)
                FindMore_TwtrkName = string.capwords(FindMore_TwtrkName)
                if Fname in FindMore_TwtrkName and Lname in FindMore_TwtrkName:
                    print("KNOWN FACTS first Name and Last Name is Matched with twitter Full Name")
                    print(Fname)
                    print(Lname)
                    print(FindMore_TwtrkName)
                    d ={
                    "Twitter":FindMore_TwtrkName,
                    "Name":Fmore_TwtrUM,
                    "Profile_Pic":Profile_PicTwtr
                    }
                    FM_Twitter_List.append(d)
                else:
                    screen = string.capwords(screen)
                    Fmore_TwtrUM = string.capwords(Fmore_TwtrUM)
                    if screen == Fmore_TwtrUM:
                        
                        # print("First and Last Name are not exists in Full Name of TWITTER")
                        # print("But")
                        print("Need to Proceed for Next Step using PROFILE PHOTO Analysis")
                        print(screen+"=="+Fmore_TwtrUM)
                        d ={
                        "Twitter":FindMore_TwtrkName,
                        "Name":Fmore_TwtrUM,
                        "Profile_Pic":Profile_PicTwtr
                        }
                        FM_Twitter_List.append(d)
        except Exception as twt_err2:
            print(str(twt_err2))
            pass
    
    return FM_Twitter_List

            # if "Facebook" not in social_list:
            #     print(yellow("Facebook not in Social list",['bold']))
            #     TWName = ""
            #     TWName = Twtr_name.isalpha()
            #     if Twtr_name != "":
            #         screen = Twtr_name
            #     else:
            #         screen = Insta_name
            #     if screen != "":
            #         f= ""
            #         FindMore_FacebokName = ""
            #         try:
            #             json_FB = ""
            #             json_FB = osint_facebook(screen)
            #         except Exception as FB_eer3:
            #             print(str(FB_eer3))
            #             json_FB = ""
                    
            #         if json_FB != "":
            #             f = json.loads(json_FB)
            #             if "Invalid Profile Has Been Requested" in f:
            #                 json_FB = ""
            #             if json_FB != "":
            #                 FindMore_FacebokName = f["FULL_NAME"]
            #                 FullName = string.capwords(FullName)
            #                 FindMore_FacebokName = string.capwords(FindMore_FacebokName)
            #                 if FindMore_FacebokName == FullName:
            #                     Fmore_FBUM = ""
            #                     Fmore_FBUM = f['USER_NAME']
            #                     d={
            #                         "Facebook":Fmore_FBUM,
            #                         'Name':FindMore_FacebokName
            #                         }
            #                     FM_Social_list.append(d)
                                
            #                 else:
            #                     print("Full Name Not Matched for FB")
            #                     Fname = string.capwords(Fname)
            #                     Lname = string.capwords(Lname)
            #                     if Fname in FullName and Lname in FullName:
            #                         d={
            #                             "Facebook":Fmore_FBUM,
            #                             'Name':FindMore_FacebokName
            #                         }
            #                         FM_Social_list.append(d)
            #             else:
            #                 print(red("Invalid Profile Has Been Requested FB Account"))

            #     else:
            #         json_FB = ""
            # if "Twitter" not in social_list:
            #     print(yellow("Twitter not in Social list",['bold']))
            #     TWName = ""
            #     TWName = FB_name.isalpha()

            #     if FB_name != "" and FB_name == True:
                
            #         screen = FB_name
            #     else:
            #         screen = Insta_name
            #     if screen != "":
            #         try:
            #             json_Twitr = ""
            #             FindMore_TwtrkName = ""
            #             json_Twitr = osint_twitter(screen)
            #         except Exception as twitErr:
            #             print(twitErr)
            #             json_Twitr = ""
            #         if "Cannot serialize the DataTable" in json_Twitr:
            #             print(red("Osint Twitter KeyError := Cannot serialize the DataTable. DataTable name is not set."))
            #             print("Profile Does not exists, Invalid Profile")
            #             #t = json.loads(json_Twitr)
            #             #print("Waiting for 60 seconds,Pls Wait..")
            #             # time.sleep(60)
            #         else:
            #             t = json.loads(json_Twitr)
            #             try:
            #                 FindMore_TwtrkName= t["USER_NAME"]
            #                 FindMore_TwtrkName = string.capwords(FindMore_TwtrkName)
            #                 FullName = string.capwords(FullName)
            #                 if FindMore_TwtrkName == FullName:
            #                     Fmore_TwtrUM = ""
            #                     Fmore_TwtrUM = json_Twitr['SCREEN_NAME']
            #                     FM_Social_list.append(Fmore_TwtrUM)
            #             except Exception as Twt_err:
            #                 print(str(Twt_err))
            # if json_Twitr != "":
            #     t = json.loads(json_Twitr)
            #     try:
            #         FindMore_TwtrkName= t["USER_NAME"]
            #         FindMore_TwtrkName = string.capwords(FindMore_TwtrkName)
            #         FullName = string.capwords(FullName)
            #         if FindMore_TwtrkName == FullName:
            #             Fmore_TwtrUM = ""
            #             Fmore_TwtrUM = json_Twitr['SCREEN_NAME']
            #             FM_Social_list.append(Fmore_TwtrUM)
            #     except Exception as Twt_err:
            #         print(str(Twt_err))
    #             else:
    #                 json_Twitr = ""
    #     else:
    #         print("SOCIAL Accounts Does not Exists for Any Source from People's Service")
        
    #     if len(FM_Social_list) > 0:
    #         print(green("Following Are the Social Accounts Found from FIND MORE's Search := ",['bold','underlined']))
    #         print(json.dumps(FM_Social_list, indent = 4))
    #         time.sleep(5)
    #     else:
            
    #         print(magenta("SOCIAL Accounts Does not Exists in All Three Sources After FIND MORE's Search",['italic']))
    #         time.sleep(5)
    # except Exception as Err3:
    #     print(str(Err3))
    

    # input('Press ENTER to exit')

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
    if Result != "":
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
    json_FB = ""
    if obj != "":
        if "Invalid" in obj:
            print("Invalid Profile message from osint facebook Service")
            json_FB = ""
            return json_FB
    if obj != "":
        if "New Profile Request Has Been Recieved" in obj:
            print("Waiting for Osint Facebook Crawler To Process.. Please Wait more than 3 mins..")
            time.sleep(200)
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
            if "Request Not Yet Processed" in obj:
                print("Request not yet procesed, So waiting for more 1 min..")
                time.sleep(60)
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
                # if "Request Not Yet Processed" in obj:
                #     print("Request not yet procesed, So waiting for more 1 min..")
                #     time.sleep(60)
                if obj != "":
                    json_FB = ""
                    json_FB = json.dumps(obj,ensure_ascii=False)
                
            
                
            #     json_FB = json.dumps(obj,ensure_ascii=False)
        else:
            if obj != "":
                try:
                    json_FB = json.dumps(obj,ensure_ascii=False)
                except:
                    pass
            else:
                json_FB = ""

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
    json_Twtr = ""
    if obj != "":
        
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
            obj = ""
            obj = data_dict['soap:Envelope']['soap:Body']['ObtainInstagramUserDetailsResponse']['ObtainInstagramUserDetailsResult']['ResponseXML']["DocumentElement"]['InstagramUserDetails']
        except:
            obj = data_dict['soap:Envelope']['soap:Body']['ObtainInstagramUserDetailsResponse']['ObtainInstagramUserDetailsResult']['message']
    json_insta = ""
    if obj == "Request Not Yet Processed":
        print("Request not Yet Processed in Osint Instagram Service")
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
                obj = ""
                obj = data_dict['soap:Envelope']['soap:Body']['ObtainInstagramUserDetailsResponse']['ObtainInstagramUserDetailsResult']['ResponseXML']["DocumentElement"]['InstagramUserDetails']
            except:
                obj = data_dict['soap:Envelope']['soap:Body']['ObtainInstagramUserDetailsResponse']['ObtainInstagramUserDetailsResult']['message']
        
        
        if obj == "Request Not Yet Processed":
            print("Request not Yet Get Processed in Osint Instagram Service")
            print("Waiting for Another 1 Mins In-Progress......")
            time.sleep(60)
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
                    obj = ""
                    obj = data_dict['soap:Envelope']['soap:Body']['ObtainInstagramUserDetailsResponse']['ObtainInstagramUserDetailsResult']['ResponseXML']["DocumentElement"]['InstagramUserDetails']
                except:
                    obj = data_dict['soap:Envelope']['soap:Body']['ObtainInstagramUserDetailsResponse']['ObtainInstagramUserDetailsResult']['message']
            json_insta = ""
            json_insta = json.dumps(obj,ensure_ascii=False)
            print("Json Found Request Get Processed")
            
        else:
            json_insta = ""
            json_insta = json.dumps(obj,ensure_ascii=False)
            print("Json Found Request Get Processed")
            #print(json_insta)
    
    else:
        json_insta = json.dumps(obj,ensure_ascii=False)
        pass

    return json_insta

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