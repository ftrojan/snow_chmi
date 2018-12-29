# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 19:59:19 2018

@author: com-ftrojan
"""
import pandas as pd
import os
from dfply import X, mutate, select, rename
import re

def date_cz2iso(cz):
    p = re.compile('(\d+)\.(\d+)\.(\d+)')
    m = p.match(cz)
    dd = m.group(1)
    mm = m.group(2)
    yyyy = m.group(3)
    iso = "%04d-%02d-%02d" % (int(yyyy), int(mm), int(dd))
    return iso

def snow_sumavaeu(x):
    p = re.compile('(\d+) cm')
    m = p.match(x)
    if m is None:
        y = ''
    else:
        y = m.group(1)
    return y

sh = list()
for d in os.listdir("data"):
    print(d)
    if os.path.isdir("data/%s" % d):
        f01 = "data/%s/chmi_manualmeasure.txt" % d
        if os.path.isfile(f01):
            d01 = pd.read_csv(f01, sep="|")
            y01 = d01 >> \
                mutate(source = 'chmi_man', country = 'cz', date_valid = d) >> \
                rename(snow = X.snowdepth_total) >> \
                select(X.date_valid, X.source, X.country, X.station, X.snow)
            sh.append(y01)
        f02 = "data/%s/chmi_oah.txt" % d
        if os.path.isfile(f02):
            d02 = pd.read_csv(f02, sep="|")
            y02 = d02 >> \
                mutate(source = 'chmi_oah', country = 'cz')
            y02['date_valid'] = [date_cz2iso(row['date']) for i, row in d02.iterrows()]
            y02 = y02 >> rename(snow = X.snowdepth_total) >> \
                select(X.date_valid, X.source, X.country, X.station, X.snow)
            sh.append(y02)
        f03 = "data/%s/chmi_resorts.txt" % d
        if os.path.isfile(f03):
            d03 = pd.read_csv(f03, sep="|")
            y03 = d03 >> \
                mutate(source = 'chmi_resorts', country = 'cz')
            y03 = y03 >> rename(snow = X.snowdepth_total, date_valid = X.date) >> \
                select(X.date_valid, X.source, X.country, X.station, X.snow)
            sh.append(y03)
        f04 = "data/%s/sumava.eu.txt" % d
        if os.path.isfile(f04):
            d04 = pd.read_csv(f04, sep="|")
            y04 = d04 >> \
                mutate(source = 'sumava.eu', country = 'cz')
            y04['date_valid'] = [date_cz2iso(row['date']) for i, row in d04.iterrows()]
            y04['snow'] = [snow_sumavaeu(row['snowdepth']) for i, row in d04.iterrows()]
            y04 = y04 >> select(X.date_valid, X.country, X.source, X.station, X.snow)
            sh.append(y04)
df = pd.concat(sh, ignore_index=True)
df.to_csv("data/snow_history.txt", sep="\t", index=False, encoding='utf-8')
