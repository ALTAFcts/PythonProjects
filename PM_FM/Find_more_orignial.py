import requests
import json

FIND_MORE = "https://peoplemon.com/RestPeople/MA/MaWcf.svc/FetchResult"
HEADERS = {
    "User": "PmFindMore",
    "APIKey": "gZVChKAI6DmxwLIL2fbfnyK/3j4FE0CkRwSgYOvHGFU="
}

def find_more2(auto_id: str, inputParams):
    # service_flag = "FAMILY" if family  else "INFO"
    DATA = {
        "AutoID": auto_id,
        "Count": 0,
        "Exception": None,
        "Service_Flag": inputParams,
        "Result": None,
        "Criterias": [{"Field":"TYPE","Value":"1"}]
    }
    try:
        response = requests.post(FIND_MORE, headers=HEADERS, json=DATA).json()
        result = json.loads(response.get("Result"))
        print(result)
    except Exception as e:
        print(e)
        result = {"Error": str(e)}
    return result


def find_more(auto_id: str, inputParams):
    # service_flag = "FAMILY" if family  else "INFO"
    DATA = {
        "AutoID": auto_id,
        "Count": 0,
        "Exception": None,
        "Service_Flag": inputParams,
        "Result": None
    }
    try:
        response = requests.post(FIND_MORE, headers=HEADERS, json=DATA).json()
        result = json.loads(response.get("Result"))
        print(result)
    except Exception as e:
        print(e)
        result = {"Error": str(e)}
    return result


def main(auto_ids):
    for auto_id in auto_ids:
        details = find_more(auto_id,"INFO")
        family_details = find_more(auto_id, "FAMILY")
        Social_Accounts = find_more(auto_id, "SOURCE")
        Address_details = find_more(auto_id, "ADDRESS")
        Relative_Details = find_more(auto_id, "RELATIVE")
        Hobbies = find_more2(auto_id, "INTEREST")
        contact_details = find_more(auto_id, "PHONE")
        Profession_Details = find_more(auto_id,"BACKGROUND")
        Email_Details = find_more(auto_id, "PROBABLE_EMAILS")

        result = {
            "AutoID": auto_id,
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
        try:
            print(result['Details'][0]['FULL_NAME'])
        except Exception as err:
            print(str(err))
            pass
        with open(f"{auto_id}.json", "w") as file:
            json.dump(result, file)


if __name__ == "__main__":
    AUTOID = input("Enter AutoID or list of AutoIDs separated by commas: ")
    auto_ids = list(x.strip() for x in AUTOID.split(","))
    main(auto_ids)