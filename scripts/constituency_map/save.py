import re
import os
import requests

initial="http://www.election.gov.np/ecn/uploads/userfiles/maps/"

txt=open('maps.html').read()
# <p style="box-sizing: border-box; margin: 0px; padding: 0px; font-size: 14px; border: 0px; font-variant-numeric: inherit; font-variant-east-asian: inherit; font-stretch: inherit; line-height: inherit; font-family: Arial, Helvetica, sans-serif; vertical-align: baseline; color: #000000;"><span style="color: #3598db;"><a style="box-sizing: border-box; margin: 0px; padding: 0px; background-color: transparent; color: #3598db; border: 0px; font: inherit; vertical-align: baseline; outline: none 0px !important;" href="http://www.election.gov.np/ecn/uploads/userfiles/maps/PANCHTHAR.pdf">2.<span style="box-sizing: border-box; margin: 0px; padding: 0px; border: 0px; font: inherit; vertical-align: baseline; white-space: pre;"> </span>Panchthar<br style="box-sizing: border-box; margin: 0px; padding: 0px;"></a></span></p>
links=re.findall('(?<='+initial+r').*?(?=.pdf)',txt)
# get pdf file names

if not os.path.exists('maps/'):
    os.mkdir('maps/')

total= len(links)
count=0
for link in links:
    count+=1
    # if count<=1: continue
    print(f'Downloading {count}/{total}: {link}.pdf')
    with open('maps/'+link+'.pdf','wb') as f:
        f.write(requests.get(initial+link+'.pdf').content)