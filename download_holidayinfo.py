# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 19:43:34 2018

@author: com-ftrojan
"""
import datetime
from selenium import webdriver

# https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python
wdir = "data/%s" % datetime.datetime.today().strftime('%Y-%m-%d')

url = "http://www.holidayinfo.cz/en/snowinfo"
driver = webdriver.PhantomJS()
driver.get(url)
table = driver.find_element_by_id(id_='datarows')
with open('%s/holidayinfo.cz.txt' % wdir, 'w', encoding="utf-8") as f:
    f.write("station|temperature|snow|type_of_snow|new_snow|lifts|slopes\n")
    for row in table.find_elements_by_css_selector("tr.hol3_snowinfo_rowodd.hol3_snowinfo_title_link"): # odd rows
        cell = row.find_elements_by_tag_name("td")
        if "hol3_snowinfo_locrow" in cell[0].get_attribute('class'):
            datarow = "%s|%s|%s|%s|%s|%s|%s" % (cell[1].text, cell[2].text, cell[3].text, cell[4].text, cell[5].text, cell[6].text, cell[7].text)
            print(datarow)
            f.write("%s\n" % datarow)
    for row in table.find_elements_by_css_selector("tr.hol3_snowinfo_roweven.hol3_snowinfo_title_link"): # even rows
        cell = row.find_elements_by_tag_name("td")
        if "hol3_snowinfo_locrow" in cell[0].get_attribute('class'):
            datarow = "%s|%s|%s|%s|%s|%s|%s" % (cell[1].text, cell[2].text, cell[3].text, cell[4].text, cell[5].text, cell[6].text, cell[7].text)
            print(datarow)
            f.write("%s\n" % datarow)
