import requests
import xmltodict
import json
from bs4 import BeautifulSoup


def fetchDBRequest():
    print("Fetch DB List")
    apiurl = restApi + "GetNotProcessedFBInfoProfile/1/3/100"
    
    try:
        response = requests.get(apiurl,timeout=connectiontimeout)

        if response.status_code == 200:
            payload = json.loads(response.content)            
            jdata = json.loads(payload)
            for dataobj in jdata:
                data = {
                    'fbid': str(dataobj["FACEBOOK_ID"]),
                    'desc': urllib.parse.unquote(str(dataobj["DESCRIPTION"])), #url decode added to handle special chars
                   # 'desc': str(dataobj["DESCRIPTION"]),
                    'posttypeid': str(dataobj["POSTTYPE_ID"]),
                    'userid': str(dataobj["USER_ID"]),
                    'ispage': str(dataobj["IS_PAGE"]),
                    'clientid': str(dataobj["CLIENT_ID"])
                    }
                pendinglist.append(data)
            # print(pendinglist)
        else:
            return None
    except Exception as e:
        # time.sleep(10)
        # AccessElectrolSearch()
        # print('Repeat In Loop')
        print(e)

OsintMethod = "http://94.236.4.172/services/service.asmx?op=GetFacebookProfileInfo"
HEADERS = {"user-agent":"Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
                }

def osintService():
    reqdata ={
        "Priority": "101",
        "ScreenName": "saadhariri"

    }
    
    #reqdata = "<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">" %(ScreenName,Priority)
    apiurl = "http://94.236.4.172/services/service.asmx?op=GetFacebookProfileInfo"
    # apiurl = restApi + "SaveFBProfileInfo_Mobile" #"SaveFBProfileInfo_Data" # "SaveFBProfileInfo"
    headers = {'Content-Type': 'text/xml'}
    try:
        response = requests.post(apiurl, headers=headers, data=reqdata,timeout=40)
        result = response.content
        
        if response.status_code == 200:    
            print("Send CALLBACK : "+ str(ScreenName))
            #pendinglist.pop(0) #removing top record after process
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    
    DATA = {
        "Screen": ScreenName,
        "Count": 0,
        "Exception": None,
        "Service_Flag": None,
        "Result": None,
        "Proxy": None
    }
    try:
        response = requests.post(OsintMethod , headers=HEADERS, json=DATA).json()
        result = json.loads(response.get("Result"))
        print(result)
    except Exception as e:
        print(e)
        result = {"Error": str(e)}
    return result
import requests


def osint_facebook():
    Method_ID = "20"
    ScreenName = "saadhariri"
    payload = ""
    url = "http://94.236.4.172/services/service.asmx?op=GetFacebookProfileInfo"

    payload = payload +"<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\r\n  <soap:Header>\r\n    <AuthHeader xmlns=\"http://tempuri.org/\">\r\n      <userName>QmLW7qVBSB1lsY8f1AVQhw==</userName>\r\n      <passWord>/x01gfHE72J2MyGQCPY1SV8HKCsvqnYAQgabKJ2usio=</passWord>\r\n      <ipAddress></ipAddress>\r\n      <requestUrl></requestUrl>\r\n      <clientKey></clientKey>\r\n"
    payload = payload +"<WebMethodId>"+str(Method_ID)+"</WebMethodId>\r\n      <waaudit>\r\n        <WEB_SERVICE_ID>"+str(Method_ID)+"</WEB_SERVICE_ID>\r\n        <CLIENT_ID>1</CLIENT_ID>        \r\n        <INPUT_PARAMS>"+str(ScreenName)+"</INPUT_PARAMS>\r\n        <REQUEST_URL>"+str(ScreenName)+"</REQUEST_URL>\r\n      </waaudit>\r\n      <TOKEN>1</TOKEN>\r\n      <CLIENT_ID>1</CLIENT_ID>\r\n      <CLIENT_FB_CALLBACK></CLIENT_FB_CALLBACK>\r\n    </AuthHeader>\r\n  </soap:Header>\r\n"
    payload = payload +"<soap:Body>\r\n    <GetFacebookProfileInfo xmlns=\"http://tempuri.org/\">\r\n <screenName>"+str(ScreenName)+"</screenName>\r\n      <Priority>101</Priority>\r\n    </GetFacebookProfileInfo>\r\n  </soap:Body>\r\n</soap:Envelope>"
    headers = {
    'Content-Type': 'text/xml'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    Result = response.text
    result = Result.replace("&lt;","<")
    result = result.replace("&gt;",">")
    data_dict = xmltodict.parse(result)
    obj = data_dict['soap:Envelope']['soap:Body']['GetFacebookProfileInfoResponse']['GetFacebookProfileInfoResult']['ResponseXML']["DocumentElement"]["PageDetails"]
    print(obj)
    json_data = json.dumps(obj,ensure_ascii=False)
    print(json_data)
    print("mateen")

def osint_twitter():
    Method_ID = "19"
    ScreenName = "saadhariri"
    payload = ""
    url = "http://94.236.4.172/services/service.asmx?op=GetTwiterUserDetails"

    payload = payload +"<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\r\n  <soap:Header>\r\n    <AuthHeader xmlns=\"http://tempuri.org/\">\r\n      <userName>QmLW7qVBSB1lsY8f1AVQhw==</userName>\r\n      <passWord>/x01gfHE72J2MyGQCPY1SV8HKCsvqnYAQgabKJ2usio=</passWord>\r\n      <ipAddress></ipAddress>\r\n      <requestUrl></requestUrl>\r\n      <clientKey></clientKey>\r\n"
    payload = payload +"<WebMethodId>"+str(Method_ID)+"</WebMethodId>\r\n      <waaudit>\r\n        <WEB_SERVICE_ID>"+str(Method_ID)+"</WEB_SERVICE_ID>\r\n        <CLIENT_ID>1</CLIENT_ID>        \r\n"
    payload = payload +"<INPUT_PARAMS>"+str(ScreenName)+"</INPUT_PARAMS>\r\n  <REQUEST_URL>"+str(ScreenName)+"</REQUEST_URL>\r\n      </waaudit>\r\n      <TOKEN>1</TOKEN>\r\n      <CLIENT_ID>1</CLIENT_ID>\r\n      <CLIENT_FB_CALLBACK></CLIENT_FB_CALLBACK>\r\n    </AuthHeader>\r\n  </soap:Header>\r\n" 
    payload = payload +"<soap:Body>\r\n <GetTwiterUserDetails xmlns=\"http://tempuri.org/\">\r\n <screenName>"+str(ScreenName)+"</screenName>\r\n      <Priority>101</Priority>\r\n    </GetTwiterUserDetails>\r\n  </soap:Body>\r\n</soap:Envelope>"
    headers = {
    'Content-Type': 'text/xml'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    Result = response.text
    result = Result.replace("&lt;","<")
    result = result.replace("&gt;",">")
    data_dict = xmltodict.parse(result)
    obj = data_dict['soap:Envelope']['soap:Body']['GetTwiterUserDetailsResponse']['GetTwiterUserDetailsResult']['TwitterUserDetails']["UserInfo"]
    print(obj)
    json_data = json.dumps(obj,ensure_ascii=False)
    print(json_data)

def Osint_Instagram():
    Method_ID = "66"
    ScreenName = "ramprak320455363633"
    payload = ""
    url = "http://94.236.4.172/services/service.asmx?op=ObtainInstagramUserDetails"

    payload = payload +"<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\r\n  <soap:Header>\r\n    <AuthHeader xmlns=\"http://tempuri.org/\">\r\n      <userName>QmLW7qVBSB1lsY8f1AVQhw==</userName>\r\n      <passWord>/x01gfHE72J2MyGQCPY1SV8HKCsvqnYAQgabKJ2usio=</passWord>\r\n      <ipAddress></ipAddress>\r\n      <requestUrl></requestUrl>\r\n      <clientKey></clientKey>\r\n"
    payload = payload +"<WebMethodId>"+str(Method_ID)+"</WebMethodId>\r\n      <waaudit>\r\n        <WEB_SERVICE_ID>"+str(Method_ID)+"</WEB_SERVICE_ID>\r\n        <CLIENT_ID>1</CLIENT_ID>        \r\n"
    payload = payload +"<INPUT_PARAMS>"+str(ScreenName)+"</INPUT_PARAMS>\r\n        <REQUEST_URL>"+str(ScreenName)+"</REQUEST_URL>\r\n      </waaudit>\r\n      <TOKEN>1</TOKEN>\r\n      <CLIENT_ID>1</CLIENT_ID>\r\n      <CLIENT_FB_CALLBACK></CLIENT_FB_CALLBACK>\r\n    </AuthHeader>\r\n  </soap:Header>\r\n"
    payload = payload +"<soap:Body>\r\n     <ObtainInstagramUserDetails xmlns=\"http://tempuri.org/\">\r\n      <userName>"+str(ScreenName)+"</userName>\r\n      <Priority>101</Priority>\r\n    </ObtainInstagramUserDetails>\r\n  </soap:Body>\r\n</soap:Envelope>"
   
    headers = {
    'Content-Type': 'text/xml'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    Result = response.text
    result = Result.replace("&lt;","<")
    result = result.replace("&gt;",">")
    data_dict = xmltodict.parse(result)
    try:
        obj = data_dict['soap:Envelope']['soap:Body']['ObtainInstagramUserDetailsResponse']['ObtainInstagramUserDetailsResult']['ResponseXML']["DocumentElement"]['InstagramUserDetails']
    except:
        obj = data_dict['soap:Envelope']['soap:Body']['ObtainInstagramUserDetailsResponse']['ObtainInstagramUserDetailsResult']['message']
        pass
    print(obj)
    json_data = json.dumps(obj,ensure_ascii=False)
    print(json_data)  #message  Request Not Yet Processed

def New():
    url = 'http://94.236.4.172/services/service.asmx?op=GetFacebookProfileInfo'
    payload = {
        'param1':'101',
        'ScreenName':'saadhariri'
        } # add paramaters to the dictionary as needed
    r = requests.get(url,params=payload, auth=('webMiner', 'webMiner@zfp.com'))
    print(r.text)
    print(r.content)

    # GET Only
    #r = requests.get(url)

    # GET with parameters
    r1 = requests.get(url, params=payload)
    result = r1.content
    print(str(result))
    print(r1.text)

    # POST with parameters
    r2 = requests.post(url, data=payload)
    xml = r2.content
    r2.url
    r2.text
    #r2.status_code‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍
    print(str(xml))

if __name__ == "__main__":
    Osint_Instagram()
    # AUTOID = input("Enter AutoID or list of AutoIDs separated by commas: ")
    # auto_ids = list(x.strip() for x in AUTOID.split(","))
    # main(auto_ids)