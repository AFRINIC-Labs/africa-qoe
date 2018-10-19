import requests
import json
import time
import pandas as pd

api_url = 'https://kong.speedcheckerapi.com:8443/ProbeAPIv2/'
apikey = '<ADD YOUR API KEY>'

ccs = [
'EG', 'BJ', 'CI', 'CV', 'GH', 'GM', 'GN', 'GW', 'AO', 'CF', 'CG', 'CM', 'GA', 'GQ', 'TD', 'BI', 'DJ', 'ER', 'ET', 'KM', 'BW', 'MA', 'SD', 'TN', 'LR', 'ML', 'MR', 'NE', 'NG', 'SL', 'SN', 'TG', 'ST', 'KE', 'MG', 'MU', 'MW', 'MZ', 'RE', 'RW', 'SC', 'SO', 'UG', 'LS', 'NA', 'SZ', 'ZA', 'DZ', 'EH', 'LY', 'BF', 'SH', 'CD', 'TZ', 'YT', 'ZM', 'ZW']


# filter the probe ID from the results in json format 
# input: a json that contains the detailed response from POST request 
def get_probe_id(request_response):
    probe_ids = []
    probes = request_response['GetNewProbesResult']['Probes']
    for probe in probes:
        try:
            if probe["CountryCode"] in ccs:
                probe_ids.append(probe['ProbeID'])
        except KeyError:
            pass 
        
    return(probe_ids)

# check country has live probes
def check_probe_in_cc(request_response):
    probe_ids = []
    probes = request_response['GetNewProbesResult']['Probes']

    return(len(probes))
# retrieve page load result 
# input: test id
def retrieve_video_result(test_id):
    vdo_result_ep= api_url + 'GetvideoResults?apikey=' + apikey + '&testID=' +  test_id
    vdo = requests.get(vdo_result_ep)
    
    return(vdo.json())

# change the json output to csv compatible format 
# input: json file that contains the response of the request 
def result_to_csv(result_json):
    vdo_results = result_json['VideoTestResults']
    results_lst = []
    
   
                                                            
    test_status = []
    test_date = []
    DurationOfEachRebuffering = []
    VideoID = []
    VideoPlayDuration = []
    VideoPlayFinishEvent = []
    VideoResolution = []
    InitialBufferingStartupLatency = []
    RebufferingTimes = []
    VideoDownloadSpeed = []
    
    ASN = []
    CityName = []
    ConnectionType = []
    CountryCode = []
    DNSResolver = []
    IPAddress = []
    Latitude = []
    Longitude = []
    Network = []
    NetworkID = []
    Platform = []
    ProbeID = []
    
                                    
    for vdo_result in vdo_results:
        
        status = vdo_result['TestStatus']['StatusCode']
        if int(status) != 200:
            continue
        
        probe_info = vdo_result['ProbeInfo']
        try:
            if None == vdo_result['TestStatus']['StatusCode']:
                continue
            test_status.append(vdo_result['TestStatus']['StatusCode'])
        except TypeError:
            test_status.append(-1)
            print(vdo_results['TestStatus'])
        if 'TestDateTime' in vdo_result.keys():
            test_date.append(str(vdo_result['TestDateTime']).replace('/Date(', '').split('+')[0])
        else:
             test_date.append('')
        if 'InitialBufferingStartupLatency' in vdo_result.keys():
            InitialBufferingStartupLatency.append(vdo_result['InitialBufferingStartupLatency'])
        else:
            InitialBufferingStartupLatency.append(-1)
        if 'VideoID' in vdo_result.keys():
            VideoID.append(vdo_result['VideoID'])
        else:
            VideoID.append('')    
        if 'VideoPlayDuration' in vdo_result.keys():
            VideoPlayDuration.append(vdo_result['VideoPlayDuration'])
        else:
            VideoPlayDuration.append(-1)
        if 'VideoPlayFinishEvent' in vdo_result.keys():
            VideoPlayFinishEvent.append(vdo_result['VideoPlayFinishEvent'])
        else:
            VideoPlayFinishEvent.append(-1)
        if 'VideoResolution' in vdo_result.keys():
            VideoResolution.append(vdo_result['VideoResolution'])
        else:
            VideoResolution.append(-1)
        if 'RebufferingTimes' in vdo_result.keys():
            RebufferingTimes.append(vdo_result['RebufferingTimes'])
        else:
            RebufferingTimes.append(-1)
        if 'VideoDownloadSpeed' in vdo_result.keys():
            VideoDownloadSpeed.append(vdo_result['VideoDownloadSpeed'])
        else:
            VideoDownloadSpeed.append(-1)
        if 'DurationOfEachRebuffering' in vdo_result.keys():
            DurationOfEachRebuffering.append(vdo_result['DurationOfEachRebuffering'])
        else:
            DurationOfEachRebuffering.append(-1)
        
        
        if 'ASN' in probe_info.keys():
            ASN.append(probe_info['ASN'])
        else:
            ASN.append(-1)
        if 'CityName' in probe_info.keys():
            CityName.append(probe_info['CityName'])
        else:
            CityName.append(-1)
        if 'ConnectionType' in probe_info.keys():
            ConnectionType.append(probe_info['ConnectionType'])
        else:
            ConnectionType.append(-1)
        if 'CountryCode' in probe_info.keys():
            CountryCode.append(probe_info['CountryCode'])
        else:
            CountryCode.append(-1)
        if 'DNSResolver' in probe_info.keys():
            DNSResolver.append(probe_info['DNSResolver'])
        else:
            DNSResolver.append(-1)
        if 'IPAddress' in probe_info.keys():
            IPAddress.append(probe_info['IPAddress'])
        else:
            IPAddress.append(-1)
        if 'Latitude' in probe_info.keys():
            Latitude.append(probe_info['Latitude'])
        else:
            Latitude.append(-1)
        if 'Longitude' in probe_info.keys():
            Longitude.append(probe_info['Longitude'])
        else:
            Longitude.append(-1)
        if 'Network' in probe_info.keys():
            Network.append(probe_info['Network'])
        else:
            Network.append(-1)
        if 'NetworkID' in probe_info.keys():
            NetworkID.append(probe_info['NetworkID'])
        else:
            NetworkID.append(-1)
        if 'Platform' in probe_info.keys():
            Platform.append(probe_info['Platform'])
        else:
            Platform.append(-1)
        if 'ProbeID' in probe_info.keys():
            ProbeID.append(probe_info['ProbeID'])
        else:
            ProbeID.append(-1)   
        
      

    result = {}
    result['test_status'] = test_status
    result['test_date'] = test_date
    result['DurationOfEachRebuffering'] = DurationOfEachRebuffering
    result['VideoID'] = VideoID
    result['VideoPlayDuration'] = VideoPlayDuration
    result['VideoPlayFinishEvent'] = VideoPlayFinishEvent
    result['VideoResolution'] = VideoResolution
    result['InitialBufferingStartupLatency'] = InitialBufferingStartupLatency
    result['RebufferingTimes'] = RebufferingTimes
    result['VideoDownloadSpeed'] = VideoDownloadSpeed
    

    result['ASN'] = ASN
    result['CityName'] = CityName
    result['ConnectionType'] = ConnectionType
    result['CountryCode'] = CountryCode
    result['DNSResolver'] = DNSResolver
    result['IPAddress'] = IPAddress
    result['Latitude'] = Latitude
    result['Longitude'] = Longitude
    result['Network'] = Network
    result['NetworkID'] = NetworkID
    result['Platform'] = Platform
    result['ProbeID'] = ProbeID

    
    return(result)


### list of videos in a country
ccs_video = {"AO":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"BF":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"BI":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"BJ":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"BW":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"CD":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"CF":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"CG":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"CI":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"CM":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"CV":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"DJ":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"DZ":["Ra-tiXq2jaE","ePHU-v2MqoE","Jr0TDLxWxzk","eWgyCHQLfvQ","5ly7785_xSo","cqMjxeLnEI8","qxNmEmg5FoI","KadI0NaO8SI","hlU_C3c3MS0","nNBNtBCBt7M"],"EG":[],"EH":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"ER":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"ET":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"GA":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"GH":["T2sFsf075Jk","Exh17CWb09o","VYOjWnS4cMY","SmqLQgkktT8","OqKqHmnMcic","IrywrQqNswg","UCnvggIdBMU","J6iuZc8JfcE","H2g7N_95Pp4","8B_9qrvtTWc"],"GM":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"GN":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"GQ":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"GW":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"KE":["4bsckGGbGs0","Wqy51uWkCJM","VYOjWnS4cMY","12BO5j_EWtg","1ATuvHiGhOA","ot21oGDENRA","LV2xlqq-3A8","NiN6OejwA3s","fS6-Cetb9UY","jPXkXdDEmwE"],"KM":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"LR":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"LS":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"LY":[],"MA":["km3RBWr2e4o","oaT6uMu1Eng","V-AFAo13-04","hnYmtQ-A7uU","Z_zwGVetvCI","P2AsUnEbRLc","zkVYJxwcayU","UvPt2OlurXY","h5bWyTziN2s","ofY5aazTjAE"],"MG":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"ML":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"MR":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"MU":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"MW":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"MZ":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"NA":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"NE":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"NG":["OqKqHmnMcic","UCnvggIdBMU","bn9uWZe6BMY","GbFQeyMX3Sc","bD2KiiFVO_0","bZU09kF8WsA","q727R1ikedM","9V530Ok7LFs","ktEnMAcrDrE","0U6kEjRKotk"],"RE":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"RW":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"SC":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"SD":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"SH":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"SL":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"SN":["Xgfau59G4PE","h4yUdpyGFGA","gD7MOR4CfLE","QK_93PDUd3w","aeEwDsq8O3M","xw_HkbBnZO8","I5ta21uhbBg","zRmGhnbu5tk","otgdDNJMGDc","bPgsNxhFnT4"],"SO":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"ST":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"SZ":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"TD":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"TG":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"TN":["uKUl-9PzMD0","2Ej920pFzWo","30QhFZozdp8","lHSk6NGgS-8","ieoBjyT4NmM","2QVNXLPW8QM","ZSgyaMiDbS0","gUmNzyWmjU0","houxG2rD26M","fSX1lpnfGRY"],"TZ":["4bsckGGbGs0","ot21oGDENRA","OpP5qEJF-bA","BzHkwBDWSQc","1nl_p53fb8I","tkBHD-PD1Fk","D68HVcXCW3w","Z6I5EBWa4nI","CRi_D9KD840","Fzu31Tw3U0E"],"UG":["VYOjWnS4cMY","HERs8UTzcrE","PQTqIK3KR6M","e3vFO0r1J_A","fY4vKXNpxWo","OM3SBV3hM9Q","HN6PDHheV-Y","7McuQ8ywelQ","85ko1b3Ykg8","7celeZ79cEE"],"YT":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"ZA":["4KjMc46_NNE","ap2YvNDn6xM","wI2sLhyziOY","uxbQATBAXf8","-eUJ5zM_0_k","9_LIP7qguYw","xzHJ2aZR6e4","MNXWJlqtopg","UAcwWdc3rRM"],"ZM":["QBL8IRJ5yHU","t4pRQ0jn23Q","j4KvrAUjn6c","MAjY8mCTXWk","xhs8tf1v__w","E21NATEP9QI","jzLlsbdrwQk","1RZYOeQeIXE","WF82ABLw8s4","r-3iathMo7o"],"ZW":["VYOjWnS4cMY","IvlY285KFtg","JaeTNiG0Em0","f06dLsaomN4","h7AWR_GLVzg","1C1iwYsK_14","76EErDmwrUY","WFEHsOoD5RM","p0zbQUVNjr8","EIl8xJUYbq8"]}
