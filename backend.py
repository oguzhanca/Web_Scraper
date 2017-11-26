import sqlite3
import requests, re
from bs4 import BeautifulSoup





# def sValue():
#     global s_val
#     if s_val < S_max:
#         s_val += 20
#
#     print("S Value: ", s_val)
#     return s_val

def requestPage(base_URL):
    global S_max
    global totalResult_num
    global prop_count

    r=requests.get(base_URL + "?s=0&o=listingdate-desc")
    c=r.content

    soup=BeautifulSoup(c,"html.parser")

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

    # print("last item's price: ", all[-1].find("a",{"class":"listing-price"}).text.strip())

    #page_nr=soup.find_all("a",{"class":"Page"})[-1].text
    #print(page_nr,"number of pages were found")
