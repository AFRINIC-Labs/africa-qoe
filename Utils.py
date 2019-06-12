import requests
import json, re, time
from datetime import datetime
import pandas as pd

API_ENDPOINT = 'https://kong.speedcheckerapi.com:8443/ProbeAPIv2/'

with open('api-ri.key','r') as f:
    APIKEY = f.read()
    
SMALL_RES = '&pw=320&ph=240&pq=small'
MEDIUM_RES = '&pw=640&ph=360&pq=medium'
LARGE_RES = '&pw=853&ph=480&pq=large'
HD720_RES = '&pw=1280&ph=720&pq=hd720'
HD1080_RES = '&pw=1920&ph=1080&pq=hd1080'
NOT_SPECIFIED_RES = ''

ccs = [
'EG', 'BJ', 'CI', 'CV', 'GH', 'GM', 'GN', 'GW', 'AO', 'CF', 'CG', 'CM', 'GA', 'GQ', 'TD', 'BI', 'DJ', 'ER', 'ET', 'KM', 'BW', 'MA', 'SD', 'TN', 'LR', 'ML', 'MR', 'NE', 'NG', 'SL', 'SN', 'TG', 'ST', 'KE', 'MG', 'MU', 'MW', 'MZ', 'RE', 'RW', 'SC', 'SO', 'UG', 'LS', 'NA', 'SZ', 'ZA', 'DZ', 'EH', 'LY', 'BF', 'SH', 'CD', 'TZ', 'YT', 'ZM', 'ZW']

HEADERS = {'apikey': APIKEY,
            'accept': 'application/json',
            'content-type': 'application/json'
          }

probeInfoProperties = [
        "ASN",
        "CityName",
        "ConnectionType",
        "CountryCode",
        "DNSResolver",
        "GeolocationAccuracy",
        "IPAddress",
        "Latitude",
        "Longitude",
        "Network",
        "NetworkID",
        "Platform",
        "ProbeID",
        "Version",
        "Screensize"
    ]

def getVideoTestSettings(cc, video_id):
    json_test = {
      "testSettings": {
        "VideoUrl": "http://pcsucdn.com/YoutubeVideoTest2.html?v=" + video_id ,
        "VideoControlScript": "Youtube-Empty.js",
        "TestCount": 10,
        "Sources": [
          {
            "CountryCode": cc
          }
        ],
        "ProbeInfoProperties": probeInfoProperties,
        "TestResultProperties": [
              "VideoDownloadSpeed"
        ]
      }
    }
    
    return json_test

def getTracerouteTestSettings(cc, destination):
    json_test = {
      "testSettings": {
        "BufferSize": 32,
        "Count": 3,
        "Fragment": 1,
        "Ipv4only": 0,
        "Ipv6only": 0,
        "MaxFailedHops": 0,
        "Resolve": 1,
        "Sleep": 300,
        "Ttl": 128,
        "TtlStart": 1,
        "Timeout": 60000,
        "HopTimeout": 1000,
        "TestCount": 10,
        "Sources": [
          {
            "CountryCode": cc
          }
        ],
        "Destinations": [
          destination
        ],
        "ProbeInfoProperties": probeInfoProperties
      }
    }
    
    return json_test

#function to launch a video test
def startVideoTest(test_settings):
    
    test_url = API_ENDPOINT + "StartVideoTest"
    
    data = json.dumps(test_settings)
    
    try:
        r = requests.post(test_url, data=data, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        return "Request FAILED"
    
    res = json.loads(r.text)
    
    #print(res)
        
    #if (res['StartVideoTestResult']['Status']['StatusCode'].in()):
    #    return res['StartVideoTestResult']['TestID']
    #else:
    #    return "FAILED"
    
    return res['StartVideoTestResult']['TestID']

#function to launch a traceroute
def startTracertTest(test_settings):
    
    test_url = API_ENDPOINT + "StartTracertTest"
    
    data = json.dumps(test_settings)
    
    try:
        r = requests.post(test_url, data=data, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        return "Request FAILED"
    
    res = json.loads(r.text)
    
    print(res)
        
    if ("OK" == res['StartTracertTestResult']['Status']['StatusText']):
        return res['StartTracertTestResult']['TestID']
    else:
        return "FAILED"
    
#
# function to get a list of video by geolocation and radius
#
def getVideoList(latitude, longitude, radius, qty):
    
    test_url = "https://www.googleapis.com/youtube/v3/search/?part=snippet&location=" + latitude + "%2C" + longitude + "&locationRadius=" + radius + "&type=video"+ "&maxResults=" +  qty + "&key=AIzaSyCS79dB7v57KItm9LUjZx6-K63mKlRdZZ8"
            
    try:
        r = requests.get(test_url, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        return "Request FAILED"
    
    res = json.loads(r.text)
    
    videos = []
    
    try:    
        for v in res['items']:
            videos.append(v['id']['videoId'])
    except KeyError as e:
        print('No video items')
        pass
    
    return videos

    
def retrieveVideoTestResults(testID):
    
    url = API_ENDPOINT + "GetVideoResults?apikey=" + APIKEY + "&testID=" + testID
    
    try:    
        r = requests.get(url, headers=HEADERS)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return []
    
    res = json.loads(r.text)
    print(res)
    return res['VideoTestResults']

def retrieveTracertTestResults(testID):
    
    url = API_ENDPOINT + "GetTracertResults?apikey=" + APIKEY + "&testID=" + testID
    
    try:    
        r = requests.get(url, headers=HEADERS)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return []
    
    res = json.loads(r.text)
    print(res)
    return res['TracerouteTestResults']

def getProbes(cc):
    
    test_url = API_ENDPOINT + "GetProbes"
    
    test_settings = {
      "criteria": {
        "FromXMinutes": 60,
        "Sources": [
          { 
            "Platform":"PC",
            "CountryCode": cc
          }
        ],
        "ProbeInfoProperties": probeInfoProperties
      }
    }
    
    data = json.dumps(test_settings)
    
    try:
        r = requests.post(test_url, data=data, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        return "Request FAILED"
    
    res = json.loads(r.text)
    
    probes = []
            
    if ("200" == res['GetProbesResult']['ResponseStatus']['StatusCode']):
        
        for probe in res['GetProbesResult']['Probes']:
            
            try:
                screensize = probe['Screensize']
            except KeyError as e: 
                screensize = 'NA'
            
            p = {"ProbeID": probe['ProbeID'], "Latitude" : probe['Latitude'], "Longitude" : probe['Longitude'], "Screensize": screensize}
            probes.append(p)
        
        return probes
        
    else:
        return None

    
def getProbesByCC(df, cc):
    
    df_probes = df.loc[df['CountryCode']==cc]
    probes = []
    
    for index, probe in df_probes.iterrows():
        try:
            screensize = probe['Screensize']
        except KeyError as e: 
            screensize = 'NA'

        p = {"ProbeID": probe['ProbeID'], "Latitude" : probe['Latitude'], "Longitude" : probe['Longitude'], "Screensize": screensize}
        probes.append(p)

    return probes

def runVideoTest(videoID, probeID, res):
    
    video_url = "http://pcsucdn.com/YoutubeVideoTest2.html?v=" + videoID + eval(res) 
    #print(video_url)
    
    json_test = {
      "testSettings": {
        "VideoUrl": video_url,
        "VideoControlScript": "Youtube-Empty.js",
        "TestCount": 1,
        "Sources": [
          {
            "ProbeID": probeID
          }
        ],
        "ProbeInfoProperties": probeInfoProperties,
        "TestResultProperties": [
              "VideoDownloadSpeed"
        ]
      }
    }
    
    return startVideoTest(json_test)

def runVideoTestByCC(videoID, cc, testCount):
    
    video_url = "http://pcsucdn.com/YoutubeVideoTest2.html?v=" + videoID
    #print(video_url)
    
    json_test = {
      "testSettings": {
        "VideoUrl": video_url,
        "VideoControlScript": "Youtube-Empty.js",
        "TestCount": testCount,
        "Sources": [
          {
            "CountryCode": cc
          }
        ],
        "ProbeInfoProperties": probeInfoProperties,
        "TestResultProperties": [
              "VideoDownloadSpeed"
        ]
      }
    }
    
    return startVideoTest(json_test)
    
    
def retrieveVideoTestResults(testID):
    
    url = API_ENDPOINT + "GetVideoResults?apikey=" + APIKEY + "&testID=" + testID
    
    try:    
        r = requests.get(url, headers=HEADERS)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return []
    
    res = json.loads(r.text)
    print(res)
    return res['VideoTestResults']

def getAvailablePCProbesCC():
    
    json_test = {
                  "criteria": {
                    "Sources": [
                      { 
                        "Platform":"PC",
                        "BoundingBox": {
                          "MinLatitude": -47.131349,
                          "MaxLatitude": 37.5359,
                          "MinLongitude": -25.383911,
                          "MaxLongitude": 63.808594
                        }
                      }
                    ],
                    "ProbeInfoProperties": probeInfoProperties
                  }
                }
    
    url = API_ENDPOINT + "GetProbes?apikey=" + APIKEY
    
    data = json.dumps(json_test)
    
    try:
        r = requests.post(url, data=data, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        return "Request FAILED"
       
    j = r.json()

    df = pd.DataFrame.from_dict(j)
    
    df = pd.DataFrame(df['GetProbesResult']['Probes'])
    
    return df

    
    

    
    
    
    
