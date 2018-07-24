import sqlite3
import requests, re
from bs4 import BeautifulSoup
import pandas as pd


def SaveAsCsv(website):
    if website == "EmlakJet":
        try:
            connex = sqlite3.connect("EmlakJet_Search_Results.db")
            cur = connex.cursor()
            df = pd.read_sql('SELECT * FROM Property_Features', connex)
            df.to_csv("Emlakjet_CSV.csv")
        except:
            print("Error SAVING EmlakJet")

    elif website == "Century21":
        try:
            connex = sqlite3.connect("Century21_Search_Results.db")
            cur = connex.cursor()
            df = pd.read_sql('SELECT * FROM Property_Features', connex)
            df.to_csv("Century21_CSV.csv")
        except:
            print("Error SAVING Century21")

def SaveAsJson(website):
    if website == "EmlakJet":
        try:
            connex = sqlite3.connect("EmlakJet_Search_Results.db")
            cur = connex.cursor()
            df = pd.read_sql('SELECT * FROM Property_Features', connex)
            df.to_json("Emlakjet_JSON.json")
        except:
            print("Error SAVING EmlakJet")

    elif website == "Century21":
        try:
            connex = sqlite3.connect("Century21_Search_Results.db")
            cur = connex.cursor()
            df = pd.read_sql('SELECT * FROM Property_Features', connex)
            df.to_json("Century21_JSON.json")
        except:
            print("Error SAVING Century21")

def SaveAsExcel(website):
    if website == "EmlakJet":
        try:
            connex = sqlite3.connect("EmlakJet_Search_Results.db")
            cur = connex.cursor()
            df = pd.read_sql('SELECT * FROM Property_Features', connex)
            df.to_excel("Emlakjet_EXCEL.xlsx")
        except:
            print("Error SAVING EmlakJet")

    elif website == "Century21":
        try:
            connex = sqlite3.connect("Century21_Search_Results.db")
            cur = connex.cursor()
            df = pd.read_sql('SELECT * FROM Property_Features', connex)
            df.to_excel("Century21_EXCEL.xlsx")
        except:
            print("Error SAVING Century21")


def requestPage_Emlakjet(base_URL):
    global message2

    if "emlakjet" not in base_URL:
        message2 = "URL doesn't match the target website. Please check and try again!"
        return message2

    try:
        r=requests.get(base_URL)
        c=r.content

        soup=BeautifulSoup(c,"html.parser")
    except:
        message2 = "Error loading page!"
        return message2

    #Extract all rows of properties.
    Property_List = soup.find_all("a",{"class":"listing-url"})
    for i in range (len(Property_List)):
        print(i, "    ", str(Property_List[i].get("href")))

    print("Length of array: ", len(Property_List))

    #Website holds all info in subdomains therefore get related 'href' from html.
    Subdomain_list = []
    for i in range (len(Property_List)):
        Subdomain_list.append(str(Property_List[i].get("href")))
        print(i, "    ", str(Property_List[i].get("href")))
    print(len(Subdomain_list))

    EmlakJetData = []
    for i in range (len(Subdomain_list)): #Denemek icin 3 elemana baktım.
        data={}
        req = requests.get("https://www.emlakjet.com" + Subdomain_list[i])
        cont = req.content
        soup=BeautifulSoup(cont,"html.parser")

        elements=soup.find_all("div",{"class":"element"})

        for item in elements:
            data[item.find_all("span")[0].get_text()] = item.find_all("span")[1].get_text()
        EmlakJetData.append(data)

    print(EmlakJetData, "\nLength of emlakjetdata list: ", len(EmlakJetData))

    df = pd.DataFrame(EmlakJetData)

    try:
        connex = sqlite3.connect("EmlakJet_Search_Results.db")  # Opens file if exists, else creates file
        cur = connex.cursor()  # This object lets us actually send messages to our DB and receive results

        df.to_sql(name="Property_Features", con=connex, if_exists="replace", index=False)  #"name" is name of table
    except:
        message2 = "Error connecting to database!"


    message2 = "Extraction completed!"
    return message2

def requestPage_Century(base_URL):
    global message
    global S_max
    global totalResult_num
    global prop_count

    if "century" not in base_URL:
        message = "URL doesn't match the target website. Please check and try again!CENT"
        return message


    try:
        r=requests.get(base_URL + "?s=0&o=listingdate-desc")
        c=r.content

        soup=BeautifulSoup(c,"html.parser")
    except:
        message = "Error loading the webpage!"
        return message


    # """Find number of results found"""
    totalResult_num = int(soup.find("div",{"class":"results-label"}).get("data-count"))

    l=[]
    S_max = totalResult_num // 20
    print("remainder is: ", totalResult_num % 20)
    print("Number of total results: ", totalResult_num)
    print("S_max is: ", S_max)

    for page in range(0,20,20):# S_max*20, 20):
        newUrl = base_URL + "?s=" + str(page) + "&o=listingdate-desc"
        r = requests.get(newUrl)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        all=soup.find_all("div",{"class":"property-card-primary-info"})

        for item in all:
            d= {}
            d["Price"]=item.find("a",{"class":"listing-price"}).text.strip()
            d["Address"]=item.find("div",{"class":"property-address"}).text.strip()
            try:
                d["City"]=item.find("div",{"class":"property-city"}).text.strip()
            except:
                d["City"]=None
            try:
                d["Beds"]=item.find("div",{"class":"property-beds"}).text.replace("beds", "").strip()
            except:
                d["Beds"]=None
            try:
                d["Full Baths"]=item.find("div",{"class":"property-baths"}).text.strip()[0]
            except:
                d["Full Baths"]=None
            try:
                d["Half Baths"]=item.find("div",{"class":"property-half-baths"}).text.strip()[0]
            except:
                d["Half Baths"]=None
            try:
                d["Area (sq-feet)"]=item.find("div",{"class":"property-sqft"}).text.replace("sq. ft", "").strip()
            except:
                d["Area (sq-feet)"]=None
            l.append(d)



    print(l)
    print("Length of array: ", len(l))

    df = pd.DataFrame(l)

    try:
        connex = sqlite3.connect("Century21_Search_Results.db")  # Opens file if exists, else creates file
        cur = connex.cursor()  # This object lets us actually send messages to our DB and receive results

        df.to_sql(name="Property_Features", con=connex, if_exists="replace", index=False)  #"name" is name of table
    except:
        message = "Error connecting to the database!"


    message = "Extraction completed!"
    return message
