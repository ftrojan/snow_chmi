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

driver = webdriver.PhantomJS()
driver_resort = webdriver.PhantomJS()
url = "http://www.snehove-spravodajstvo.sk"
driver.get(url)
panel = driver.find_element_by_id(id_='navbar-collapse')
resorts = panel.find_elements_by_tag_name("a")
with open('%s/snehove_sk.txt' % wdir, 'w', encoding="utf-8") as f:
    f.write("country|url|station|snowdepth|date\n")
    country = "sk"
    for resort in resorts:
        resort_url = resort.get_attribute('href')
        print(resort_url)
        driver_resort.get(resort_url)
        subpage = driver_resort.find_element_by_id(id_='subpage')
        tbodies = subpage.find_elements_by_tag_name("tbody")
        for tbody in tbodies:
            for row in tbody.find_elements_by_tag_name("tr"): # table row
                cell = row.find_elements_by_tag_name("td")
                if len(cell) >= 4:
                    datarow = "%s|%s|%s|%s|%s" % (country, resort_url, cell[1].text, cell[2].text, cell[3].text)
                    print(datarow)
                    f.write("%s\n" % datarow)
