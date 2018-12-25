# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 19:43:34 2018

@author: com-ftrojan
"""
import datetime
from selenium import webdriver

# https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python
wdir = "data/%s" % datetime.datetime.today().strftime('%Y-%m-%d')

url = "http://www.sumava.eu/pocasi.php#snih"
driver = webdriver.PhantomJS()
driver.get(url)
table = driver.find_element_by_id(id_='snih')
with open('%s/sumava.eu.txt' % wdir, 'w', encoding="utf-8") as f:
    f.write("station|elevation|date|snowdepth\n")
    for row in table.find_elements_by_tag_name("tr"):
        cell = row.find_elements_by_tag_name("td")
        if len(cell) == 4:
            datarow = "%s|%s|%s|%s" % (cell[0].text, cell[1].text, cell[2].text, cell[3].text)
            print(datarow)
            f.write("%s\n" % datarow)
