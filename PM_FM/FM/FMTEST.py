import requests
import json


class FMInfo:
    def __init__(self,autoids):
        self.strAutoId = autoids
        self.FIND_MORE = "https://peoplemon.com/RestPeople/MA/MaWcf.svc/FetchResult"
        self.HEADERS = {
            "User": "PmFindMore",
            "APIKey": "gZVChKAI6DmxwLIL2fbfnyK/3j4FE0CkRwSgYOvHGFU="
        }
        #print("some test - "+autoids)


    def find_more(self,auto_id: str,service_flag):
        # service_flag = "FAMILY" if family else "INFO"
        DATA = {
            "AutoID": auto_id,
            "Count": 0,
            "Exception": None,
            "Service_Flag": service_flag,
            "Result": None
        }
        #print("b4 calling service - "+str(DATA))
        try:
            response = requests.post(self.FIND_MORE, headers=self.HEADERS, json=DATA).json()
            result = json.loads(response.get("Result"))
            #print(result)
        except Exception as e:
            print("Error From People's Service :=  "+str(e)+"  ||  Service Flag:= "+str(service_flag))
            result = {"Error": str(e)}
        return result


    def main(self):
        auto_ids = self.strAutoId
        objArray = []
        # for auto_id in auto_ids:
        objauto_ids = list(x.strip() for x in auto_ids.split(","))
        for ids in objauto_ids:
            details = self.find_more(ids,"INFO")
            family_details = self.find_more(ids, "FAMILY")
            Social_Accounts = self.find_more(ids, "SOURCE")
            Address_details = self.find_more(ids, "ADDRESS")
            Relative_Details = self.find_more(ids, "RELATIVE")
            Hobbies = self.find_more(ids, "INTEREST")
            contact_details = self.find_more(ids, "PHONE")
            Profession_Details = self.find_more(ids,"BACKGROUND")
            Email_Details = self.find_more(ids, "PROBABLE_EMAILS")
            result = {
                "AutoID": ids,
                "Details": details,
                "FamilyDetails": family_details,
                "Social_Media": Social_Accounts,
                "Adresses": Address_details,
                "Relatives":Relative_Details,
                "Profession": Profession_Details,
                "Eduction": Hobbies,
                "phone":contact_details,
                "Probable_Emails":Email_Details,
                }
            objArray.append(result)
            # with open(f"{auto_id}.json", "w") as file:
        #     json.dump(result, file)
        
        return objArray


# if __name__ == "__main__":
#     AUTOID = input("Enter AutoID or list of AutoIDs separated by commas: ")
#     auto_ids = list(x.strip() for x in AUTOID.split(","))
#     main(auto_ids)