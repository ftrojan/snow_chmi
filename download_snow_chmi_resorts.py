# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 19:43:34 2018

@author: com-ftrojan
"""
import os
import datetime
import re
from selenium import webdriver

# https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python
wdir = "data/%s" % datetime.datetime.today().strftime('%Y-%m-%d')
if not os.path.exists(wdir):
    os.makedirs(wdir)

url = "http://portal.chmi.cz/aktualni-situace/aktualni-stav-pocasi/ceska-republika/snehove-zpravodajstvi/mereni-horske-sluzby"
driver = webdriver.Safari()
driver.get(url)
table = driver.find_element_by_id(id_='loadedcontent')
header = table.find_element_by_tag_name('h1').text
print(header)
pattern = re.compile(r'ze dne\s+(\d+)\.(\d+)\.\s*(\d+)\s*(\d+:\d+)')
m = pattern.search(header)
print(m)
timestamp = "%04d-%02d-%02d %s" % (int(m.group(3)), int(m.group(2)), int(m.group(1)), m.group(4))
print(header)
print(timestamp)
with open('%s/chmi_resorts.txt' % wdir, 'w', encoding="utf-8") as f:
    f.write("station|temperature|weather|snowdepth_total|snowdepth_new|snowtype|km_trails|date\n")
    rows = table.find_elements_by_tag_name("tr")
    for row in rows:
        if row.get_attribute('class') != "portlet-section-subheader":
            cells = row.find_elements_by_tag_name("td")
            if len(cells) >= 7:
                datarow = "%s|%s|%s|%s|%s|%s|%s|%s" % (cells[0].text, cells[1].text, cells[2].text, cells[3].text, cells[4].text, cells[5].text, cells[6].text, timestamp)
                print(datarow)
                f.write("%s\n" % datarow)
driver.quit()
