import sqlite3
import requests, re
from bs4 import BeautifulSoup



def requestPage_Emlakjet(base_URL):
    global message2

    if "emlakjet" not in base_URL:
        message2 = "URL doesn't match the target website\nPlease check and try again!EJ"
        return message2

    r=requests.get(base_URL)
    c=r.content

    soup=BeautifulSoup(c,"html.parser")

    Property_List = soup.find_all("a",{"class":"listing-url"})
    for i in range (len(Property_List)):
        print(i, "    ", str(Property_List[i].get("href")))

    print("Length of array: ", len(Property_List))

    Subdomain_list = []
    for i in range (len(all)):
        Subdomain_list.append(str(all[i].get("href")))
        print(i, "    ", str(all[i].get("href")))
    print(len(Subdomain_list))

    data = []
    for i in range (3):
        req = requests.get("https://www.emlakjet.com" + Subdomain_list[i])
        cont = req.content
        soup=BeautifulSoup(cont,"html.parser")
        soup
        data.append(soup.find_all("div",{"class":"element"}))
    print("Length: ", len(data))
    print(data)

    message2 = "emlakjet bitti"
    return message2
# def sValue():
#     global s_val
#     if s_val < S_max:
#         s_val += 20
#
#     print("S Value: ", s_val)
#     return s_val

def requestPage_Century(base_URL):
    global message
    global S_max
    global totalResult_num
    global prop_count

    if "century" not in base_URL:
        message = "URL doesn't match the target website\nPlease check and try again!CENT"
        return message


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

    message = "Mission completed!"
    return message

    # print("last item's price: ", all[-1].find("a",{"class":"listing-price"}).text.strip())

    #page_nr=soup.find_all("a",{"class":"Page"})[-1].text
    #print(page_nr,"number of pages were found")
