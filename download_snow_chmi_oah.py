# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 19:43:34 2018

@author: com-ftrojan
"""
import os
import datetime
from selenium import webdriver

# https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python
wdir = "data/%s" % datetime.datetime.today().strftime('%Y-%m-%d')
if not os.path.exists(wdir):
    os.makedirs(wdir)

url = "http://portal.chmi.cz/aktualni-situace/aktualni-stav-pocasi/ceska-republika/snehove-zpravodajstvi/mereni-chmu/mereni-OAH"
driver = webdriver.PhantomJS()
driver.get(url)
table = driver.find_element_by_id(id_='loadedcontent')
with open('%s/chmi_oah.txt' % wdir, 'w', encoding="utf-8") as f:
    f.write("station|elevation|date|snowdepth_total\n")
    for row in table.find_elements_by_class_name("portlet-table-body"): # odd rows
        cell = row.find_elements_by_tag_name("td")
        if len(cell) == 6 and len(cell[0].text) > 0 and len(cell[0].find_elements_by_tag_name("strong")) == 0:
            datarow = "%s|%s|%s|%s" % (cell[0].text, cell[1].text, cell[2].text, cell[3].text)
            print(datarow)
            f.write("%s\n" % datarow)
    for row in table.find_elements_by_class_name("portlet-table-alternate"): # even rows
        cell = row.find_elements_by_tag_name("td")
        if len(cell) == 6 and len(cell[0].text) > 0 and len(cell[0].find_elements_by_tag_name("strong")) == 0:
            datarow = "%s|%s|%s|%s" % (cell[0].text, cell[1].text, cell[2].text, cell[3].text)
            print(datarow)
            f.write("%s\n" % datarow)
