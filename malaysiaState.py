import xlrd
import pandas as pd
import os
import re

def state_malaysia(stateMY):
    url = "https://covid19.ascube.net/regions"
        # Assign the table data to a Pandas dataframe 
    table = pd.read_html(url)[0] 
    # Store the dataframe in Excel file 
    table.to_excel("malaysiaStates.xlsx")
    loc = ("malaysiaStates.xlsx") 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(1, 1) 
    if stateMY == "Labuan":
        val = str((sheet.row_values(16)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(16)[5]))
        uT = str(sheet.row_values(16)[3])
    if stateMY == "Perlis":
        val = str((sheet.row_values(15)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(15)[5]))
        uT = str(sheet.row_values(15)[3])
    if stateMY == "Putrajaya":
        val = str((sheet.row_values(14)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(14)[5]))
        uT = str(sheet.row_values(14)[3])
    if stateMY == "Kedah":
        val = str((sheet.row_values(13)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(13)[5]))
        uT = str(sheet.row_values(13)[3])
    if stateMY == "Terengganu":
        val = str((sheet.row_values(12)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(12)[5]))
        uT = str(sheet.row_values(12)[3])
    if stateMY == "Penang":
        val = str((sheet.row_values(11)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(11)[5]))
        uT = str(sheet.row_values(11)[3])
    if stateMY == "Kelantan":
        val = str((sheet.row_values(10)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(10)[5]))
        uT = str(sheet.row_values(10)[3])
    if stateMY == "Melaka":
        val = str((sheet.row_values(9)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(9)[5]))
        uT = str(sheet.row_values(9)[3])
    if stateMY == "Perak":
        val = str((sheet.row_values(8)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(8)[5]))
        uT = str(sheet.row_values(8)[3])
    if stateMY == "Sabah":
        val = str((sheet.row_values(7)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(7)[5]))
        uT = str(sheet.row_values(7)[3])
    if stateMY == "Pahang":
        val = str((sheet.row_values(6)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(6)[5]))
        uT = str(sheet.row_values(6)[3])
    if stateMY == "Sarawak":
        val = str((sheet.row_values(5)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(5)[5]))
        uT = str(sheet.row_values(5)[3])
    if stateMY == "Johor":
        val = str((sheet.row_values(4)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(4)[5]))
        uT = str(sheet.row_values(4)[3])
    if stateMY == "Negeri Sembilan":
        val = str((sheet.row_values(3)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(3)[5]))
        uT = str(sheet.row_values(3)[3])
    if stateMY == "Selangor":
        val = str((sheet.row_values(2)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(2)[5]))
        uT = str(sheet.row_values(2)[3])
    if stateMY == "Kuala Lumpur":
        val = str((sheet.row_values(1)[4]))
        try:
            res = re.split(' +', val)
            confirmed = res[0]
            newcase = res[1]
        except:
            confirmed = val
            newcase = "0"
        deaths = str(int(sheet.row_values(1)[5]))
        uT = str(sheet.row_values(1)[3])
    #os.remove("malaysiaStates.xlsx")
    return confirmed,deaths,uT,newcase