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
        rows = table.find_elements_by_tag_name("tr")
        for row in rows:  # odd rows
            cell = row.find_elements_by_tag_name("td")
            if len(cell) >= 6:
                resort = cell[0].get_attribute('data-value')
                snowdepth_valley = cell[1].get_attribute('data-value')
                snowdepth_mountain = cell[2].get_attribute('data-value')
                snowdepth_new = cell[3].get_attribute('data-value')
                lifts = cell[4].get_attribute('data-value')
                date = cell[5].get_attribute('data-value')
                datarow = f"{country}|{resort}|{snowdepth_valley}|{snowdepth_mountain}|{snowdepth_new}|{lifts}|{date}"
                print(datarow)
                f.write("%s\n" % datarow)
driver.quit()
