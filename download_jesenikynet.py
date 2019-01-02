# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 19:43:34 2018

@author: com-ftrojan
"""
import datetime
from selenium import webdriver

# https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python
wdir = "data/%s" % datetime.datetime.today().strftime('%Y-%m-%d')

url = "http://jeseniky.net/pocasi.php"
driver = webdriver.PhantomJS()
driver.get(url)
station = ""
with open('%s/jeseniky.net.txt' % wdir, 'w', encoding="utf-8") as f:
    f.write("station|date|snowdepth_total|snowdepth_new|temperature|weather|conditions\n")
    rows = driver.find_elements_by_tag_name("tr")
    for tr in rows:
        if tr.get_attribute("bgcolor") == "#A5CEFA":
            td = tr.find_elements_by_tag_name("td")
            if len(td) == 1 and td[0].get_attribute("colspan") == "8": # headline
                anchors = td[0].find_elements_by_tag_name("a")
                station = anchors[0].text
        elif tr.get_attribute("bgcolor") == "white":
            td = tr.find_elements_by_tag_name("td")
            if len(td) == 6: # data
                datarow = "%s|%s|%s|%s|%s|%s|%s" % (station, td[0].text, td[1].text, td[2].text, td[3].text, td[4].text, td[5].text)
                print(datarow)
                f.write("%s\n" % datarow)
