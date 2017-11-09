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
    print(S_max)
    for i in range(0, 40, 20):#S_max*20, 20):
        newUrl = base_URL + "?s=" + str(i) + "&o=listingdate-desc"
        r = requests.get(newUrl)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        all=soup.find_all("div",{"class":"property-card-primary-info"})

        for item in all:
            d= {}
            d["Price"]=item.find("a",{"class":"listing-price"}).text.strip()
            l.append(d)

    print(l)
    print(len(l))

    # print("last item's price: ", all[-1].find("a",{"class":"listing-price"}).text.strip())

    #page_nr=soup.find_all("a",{"class":"Page"})[-1].text
    #print(page_nr,"number of pages were found")
