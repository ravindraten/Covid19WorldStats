import pandas as pd
import requests

def apiStatus():
    df= pd.read_csv('api.csv')
    statusUp = ""
    statusError = ""
    for url in df['urls']:
        response= requests.get(url)
        status= response.status_code
        if status == 200:
            statusUp = str(status)
        if status == 404:
            statusError = str(status)

    return statusUp,statusError