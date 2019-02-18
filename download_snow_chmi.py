# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 13:40:49 2018

@author: com-ftrojan
"""

import pandas as pd
import os
import datetime
from pypac import PACSession

# https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python
wdir = "data/%s" % datetime.datetime.today().strftime('%Y-%m-%d')
if not os.path.exists(wdir):
    os.makedirs(wdir)
s = PACSession()  # https://pypac.readthedocs.io/en/latest/
print(s.proxies)
get_timeout = 1.0
stations = pd.read_csv('stations_v1.txt', sep='|')
for irow, srow in stations.iterrows():
    station_name = srow['station']
    station_id = srow['id']
    cn_snowdepth = srow['cn_snowdepth']
    cn_temperature = srow['cn_temperature']
    if cn_snowdepth > 0:
        url = 'http://www.hladiny.cz/snih/draw_image.php?stN=%d&act=DG&cN=%d' % (station_id, cn_snowdepth)
        print("%s snowdepth" % url)
        img = s.get(url, timeout=get_timeout)
        with open('%s/snowdepth_%s.png' % (wdir, station_name), 'wb') as f:
            f.write(img.content)
    if cn_temperature > 0:
        url = 'http://www.hladiny.cz/snih/draw_image.php?stN=%d&act=DG&cN=%d' % (station_id, cn_temperature)
        print("%s temperature" % url)
        img = s.get(url, timeout=get_timeout)
        with open('%s/temperature_%s.png' % (wdir, station_name), 'wb') as f:
            f.write(img.content)
stations2 = pd.read_csv('stations_v2.txt', sep='|')
for irow, srow in stations2.iterrows():
    station_name = srow['station']
    plot_url = srow['url']
    print("%s %s" % (station_name, plot_url))
    with open('%s/v2_%s.png' % (wdir, station_name), 'wb') as f:
        img = s.get(plot_url, timeout=get_timeout)
        f.write(img.content)
