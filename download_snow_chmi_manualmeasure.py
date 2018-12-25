# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 19:43:34 2018

@author: com-ftrojan
"""
import datetime
from selenium import webdriver

# https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python
wdir = "data/%s" % datetime.datetime.today().strftime('%Y-%m-%d')

url = "http://portal.chmi.cz/aktualni-situace/aktualni-stav-pocasi/ceska-republika/snehove-zpravodajstvi/mereni-chmu/snih-v-CR"
driver = webdriver.PhantomJS()
driver.get(url)
table = driver.find_element_by_id(id_='right-content-wide')
with open('%s/chmi_manualmeasure.txt' % wdir, 'w', encoding="utf-8") as f:
    f.write("station|elevation|snowdepth_new|snowdepth_total\n")
    for row in table.find_elements_by_class_name("portlet-table-body"): # odd rows
        cell = row.find_elements_by_tag_name("td")
        print("%s|%s|%s|%s" % (cell[0].text, cell[1].text, cell[2].text, cell[3].text))
        f.write("%s|%s|%s|%s\n" % (cell[0].text, cell[1].text, cell[2].text, cell[3].text))
    for row in table.find_elements_by_class_name("portlet-table-alternate"): # even rows
        cell = row.find_elements_by_tag_name("td")
        print("%s|%s|%s|%s" % (cell[0].text, cell[1].text, cell[2].text, cell[3].text))
        f.write("%s|%s|%s|%s\n" % (cell[0].text, cell[1].text, cell[2].text, cell[3].text))
