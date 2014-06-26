#!/bin/bash

cat cols.txt > nhldraft.csv
for i in `ls *.html`
do ./parse_nhldraft.py $i
done >> nhldraft.csv
