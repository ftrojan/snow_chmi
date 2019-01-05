# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 19:59:19 2018

@author: com-ftrojan
"""
import pandas as pd
import os
from dfply import X, mutate, select, rename
import re
import dateutil.parser


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


def country_bergfex2iso(c):
    lkp = {"oesterreich":'at', "schweiz":'ch', "deutschland":'de', "italien":'it', "slovenia":'sl', "frankreich":'fr'}
    y = lkp.get(c, 'NA')
    return y


def date_bergfex2iso(datestring):
    if type(datestring) == float: # nan
        iso = ""
    else:
        iso = datestring[:10]
    return iso


def snow_snehovesk(x):
    p = re.compile('(\d+) cm')
    m = p.match(x)
    if m is None:
        y = ''
    else:
        y = m.group(1)
    return y


def date_sk2iso(cz):
    p = re.compile('(\d+)\.\s*(\d+)\.\s*(\d+)')
    m = p.match(cz)
    dd = m.group(1)
    mm = m.group(2)
    yyyy = m.group(3)
    iso = "%04d-%02d-%02d" % (int(yyyy), int(mm), int(dd))
    return iso


def snow_jesenikynet(x):
    p = re.compile('(\d+) cm')
    m = p.match(x)
    if m is None:
        y = ''
    else:
        y = m.group(1)
    return y


def date_jeseniky2iso(cz, filedate):
    p = re.compile('(\d+)\.\s*(\d+)\.\s*(\d+:\d+)')
    m = p.match(cz)
    dd = int(m.group(1))
    mm = int(m.group(2))
    #hh = m.group(3) # not used
    # https://stackoverflow.com/questions/969285/how-do-i-translate-an-iso-8601-datetime-string-into-a-python-datetime-object
    fdt = dateutil.parser.parse(filedate)
    yy = fdt.year
    d1 = dateutil.parser.parse("%04d-%02d-%02d" % (yy, mm, dd))
    if d1 <= fdt: # in the past
        iso = "%04d-%02d-%02d" % (yy, int(mm), int(dd))
    else: # can happen at the year beginning
        iso = "%04d-%02d-%02d" % (yy-1, int(mm), int(dd))
    return iso


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
        f05 = "data/%s/bergfex.txt" % d
        if os.path.isfile(f05):
            d05 = pd.read_csv(f05, sep="|")
            y05 = d05 >> \
                mutate(source = 'bergfex') >> \
                rename(snow = X.snowdepth_mountain)
            y05['date_valid'] = [date_bergfex2iso(row.at['date']) for i, row in d05.iterrows()]
            y05['country'] = [country_bergfex2iso(row['country']) for i, row in d05.iterrows()]
            y05 = y05 >> select(X.date_valid, X.country, X.source, X.station, X.snow)
            sh.append(y05)
        f06 = "data/%s/snehove_sk.txt" % d
        if os.path.isfile(f06):
            d06 = pd.read_csv(f06, sep="|")
            y06 = d06 >> \
                mutate(source = 'snehove_sk')
            y06['snow'] = [snow_snehovesk(row['snowdepth']) for i, row in d06.iterrows()]
            y06['date_valid'] = [date_sk2iso(row['date']) for i, row in d06.iterrows()]
            y06 = y06 >> select(X.date_valid, X.country, X.source, X.station, X.snow)
            sh.append(y06)
        f07 = "data/%s/jeseniky.net.txt" % d
        if os.path.isfile(f07):
            d07 = pd.read_csv(f07, sep="|")
            y07 = d07 >> \
                mutate(source = 'jeseniky.net', country = "cz")
            y07['snow'] = [snow_jesenikynet(row['snowdepth_total']) for i, row in d07.iterrows()]
            y07['date_valid'] = [date_jeseniky2iso(row['date'], d) for i, row in d07.iterrows()]
            y07 = y07 >> select(X.date_valid, X.country, X.source, X.station, X.snow)
            sh.append(y07)
df = pd.concat(sh, ignore_index=True)
df.to_csv("data/snow_history.txt", sep="\t", index=False, encoding='utf-8')
