import requests
import json
import datetime
from common.Report import Report

URL = 'https://ireactbe-test.azurewebsites.net/api/TokenAuth/Authenticate'

def get_jwt_token(user, pwd):
    """
    Acquire the authorization token by logging into the application
    :param user: Username
    :param pwd: Password
    :return: The JWT authorization token
    """

    #data = {"eventType": "AAS_PORTAL_START", "data": {"uid": "hfe3hf45huf33545", "aid": "1", "vid": "1"}}
    #params = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1}

    #requests.post(URL, params=params, data=json.dumps(data), headers=headers)


    headers = {'content-type': 'application/json'}
    payload = {'userNameOrEmailAddress': user, 'password': pwd}

    #tk = requests.post(URL, data=json.dumps(payload))
    tk = requests.post(URL, data = json.dumps(payload), headers=headers)
    #print("---------",tk.text)
    tkJson = json.loads(tk.text)
    accessToken = tkJson['result']
    #print(accessToken['accessToken'])
    return accessToken['accessToken']

def getWarnings(number):
    #query = 'https://ireactbe-test.azurewebsites.net/api/services/app/EmergencyCommunication/GetAlertAndWarningList' % city_name

    user = 'dss@ireact.eu'
    pwd = '123qwe'
    #user = 'pro.one@defaulttenant.com'
    #pwd = 'qwe123'
    token = get_jwt_token(user, pwd)
    url_warnings = 'https://ireactbe-test.azurewebsites.net/api/services/app/EmergencyCommunication/GetList'
    payload = {'type':'warning','sorting':'start','skipCount':0,'status':'ongoing', 'communicationStatus':'suggested','maxResultCount':number}
    headers = {'Authorization': 'Bearer '+token}

    warnings = requests.get(url_warnings, params=payload, headers=headers).text
    print(warnings)
    warningsJson = json.loads(warnings)
   # print(warningsJson)
    results = warningsJson['result']
    items = results['items']
    warningsValues = []
    for elements in items:
        fecha_end = elements['end']
        type_warning = elements['type']
        address = elements['address']
        fecha_start = elements['start']
        communication_status = elements['communicationStatus']
        is_ongoing = elements['isOngoing']
        level = elements['level']
        description = elements['description']


        values =('Type: {} | Address: {} at {} | Communication Status: {} | Is Ongoing?: {} | Level: {} | Description: {} | End: {}'.
                 format(type_warning, address, fecha_start, communication_status, is_ongoing, level,description, fecha_end))

        warningsValues.append(values)

    return (warningsValues)

def get_report_list(number):
    #query = 'https://ireactbe-test.azurewebsites.net/api/services/app/EmergencyCommunication/GetAlertAndWarningList' % city_name

    user = 'dss@ireact.eu'
    pwd = '123qwe'
    #user = 'pro.one@defaulttenant.com'
    #pwd = 'qwe123'
    token = get_jwt_token(user, pwd)
    url_report_list = 'https://ireactbe-test.azurewebsites.net/api/services/app/Report/GetList?&culture=it'
    payload = {'culture':'it'}
    headers = {'Authorization': 'Bearer '+token}

    reportList = requests.get(url_report_list, params=payload, headers=headers).text
    reportListJson = json.loads(reportList)

    results = reportListJson['result']
    featureCollection = results['featureCollection']
    features = featureCollection['features']
    reportValues = []
    for i in range(number):
        propertiesJson = features[i]
        #print(propertiesJson)
        properties = json.dumps(propertiesJson)
        print(propertiesJson['properties'])
        element = propertiesJson['properties']
        #print(json.loads(elementJson))
        #element = json.loads(elementJson)
        thumbnail = element['thumbnail']
        type = element['type']
        hazard = element['hazard']
        address = element['address']
        status = element['status']
        organization = element['organization']

        values = ('Type: {} | Address: {} | Hazard: {} | Status: {} | Organization: {} | Thumbnail: {}'.
              format(type, address, hazard, status,organization, thumbnail))

        myReport = Report(thumbnail, type, hazard, address, status, organization, values)
        reportValues.append(myReport)
    return (reportValues)