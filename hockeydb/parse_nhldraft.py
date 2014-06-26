#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from bs4 import BeautifulSoup
import pprint
import csv
#import xml.etree.ElementTree as ET

pp = pprint.PrettyPrinter(indent=4)
cols = ["year","rank","round","team","teamid","player","playerid","position","team_from","league_from","junior","gp","g","a","pts","pim"]

if len(sys.argv) <= 1:
    sys.exit()

f = open(sys.argv[1])
intext = f.read()

#try:
#    root = ET.fromstring(intext)
#except Exception as e:
#    print str(e)
#    print sys.argv[1]
#    sys.exit()

soup = BeautifulSoup(intext)

title = soup.title.string
m = re.match(r"(\d{4}) NHL Entry Draft",title)
year = None
if m is not None:
    year = m.group(1)

trs = soup.tbody.find_all("tr", class_=False)

#print len(trs)
#print trs
cw = csv.DictWriter(sys.stdout, cols)
#out = list()
for tr in trs:
    r = dict()
    for col in cols:
        r[col] = None
    r["year"] = year
    i = -1
    for td in tr.contents:
        i += 1
        n = i / 2
        if i % 2 == 0:
            continue
        else:
            if n == 0:
                r["rank"] = int(td.string)
            elif n == 1:
                r["round"] = int(td.string)
            elif n == 2:
                r["team"] = td.string
                m = re.search(r"(\d+)", td.a["href"])
                if m is not None:
                    r["teamid"] = int(m.group(1))
            elif n == 3:
                r["player"] = td.string
                m = re.search(r"(\d+)", td.a["href"])
                if m is not None:
                    r["playerid"] = int(m.group(1))
            elif n == 4:
                r["position"] = td.string
            elif n == 5:
                r["team_from"] = td.string.split("[")[0].split("(")[0].strip()
                try:
                    if "[" in td.string:
                        r["league_from"] = td.string.split("[")[1].strip(" ]")
                        r["junior"] = 1
                    elif "(" in td.string:
                        r["league_from"] = td.string.split("(")[1].strip(" )")
                        r["junior"] = 0
                except:
                    pass
            elif n == 6:
                if td.string is not None:
                    r["gp"] = int(td.string)
            elif n == 7:
                if td.string is not None:
                    r["g"] = int(td.string)
            elif n == 8:
                if td.string is not None:
                    r["a"] = int(td.string)
            elif n == 9:
                if td.string is not None:
                    r["pts"] = int(td.string)
            elif n == 10:
                if td.string is not None:
                    r["pim"] = int(td.string)
            #print td
    #out.append(r)
    try:
        cw.writerow(r)
    except:
        r["team_from"] = r["team_from"].encode("utf8")
        cw.writerow(r)
#    tds = trs.find_all("td")
#    print tds

#cw.writeheader()
#cw.writerows(out)
