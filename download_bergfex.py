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

list_countries = ["oesterreich", "schweiz", "deutschland", "italien", "slovenia", "frankreich"]
driver = webdriver.Safari()
with open('%s/bergfex.txt' % wdir, 'w', encoding="utf-8") as f:
    f.write("country|station|snowdepth_valley|snowdepth_mountain|snowdepth_new|lifts|date\n")
    for country in list_countries:
        url = "https://www.bergfex.com/%s/schneewerte/" % country
        driver.get(url)
        table = driver.find_element_by_id(id_='detail')
        for row in table.find_elements_by_tag_name("tr"): # odd rows
            cell = row.find_elements_by_tag_name("td")
            if len(cell) >= 7:
                datarow = "%s|%s|%s|%s|%s|%s|%s" % (country, cell[0].get_attribute('data-value'), cell[1].get_attribute('data-value'), cell[2].get_attribute('data-value'), cell[3].get_attribute('data-value'), cell[4].get_attribute('data-value'), cell[6].get_attribute('data-value'))
                print(datarow)
                f.write("%s\n" % datarow)
driver.quit()
