#!/usr/bin/env python3
import os
import sys
import argparse
import logging
import warnings
import urllib.request
import httplib2

from bs4 import BeautifulSoup, SoupStrainer

import base64
from bs4 import BeautifulSoup as BS
from urllib.request import urlopen

import base64
from io import BytesIO
from PIL import Image


class Extractor():
    
    def get_links(self, url):

        http = httplib2.Http()
        response, content = http.request(url)

        images =  BeautifulSoup(content).find_all('img')

        image_links=[]

        for image in images:
            image_links.append(image['src'])
        
        return image_links

    
    def get_images(self, image_links):
        
        for link in image_links:
            filename = link.split("/")[-1].split("?")[0]
            urllib.request.urlretrieve(image_url, filename=filename)


class Main:

    def extractor_(self,html):
       with open(html) as html_wr:
           html_data = html_wr.read()

       soup = BS(html_data)
    
       for ind,imagetag in enumerate(soup.findall('img')): 
            image_data_base64 = imagetag['src'].split(',')[1]
            decoded_img_data = base64.b64decode(image_data_base64)
            with open(f'site_{ind}.png','wb+') as img_wr:
                img_wr.write(decoded_img_data) 

    def extractor(self,html):

       binary_fc   = open(html, 'rb').read() 
       base64_utf8 = base64.b64encode(binary_fc).decode('utf-8')

       with open(html) as html_wr:
           html_data = html_wr.read()

       images = BS(html_data).findAll('img')
       quality_img=""
       i=0
       for image in images:
         if i==14:
          quality_img=image
         i=i+1

       ext = html.split('.')[-1]
       encoded_data = f'data:image/{ext};base64,{quality_img}' 
       encoded_data=encoded_data.split(",")[2].split("\"")[0]
       decoded_data=base64.b64decode(encoded_data)
       
       im = Image.open(BytesIO(decoded_data))
       #if im.mode == 'RGBA':
       #  im = im.convert('RGB')
       im.save(html+'.jpg','jpeg')
       #im.save(html+'.png','png')
       
       with open(html, 'r', encoding='utf-8') as file:
         soup = BeautifulSoup(file, 'html.parser')       
       main_div = soup.find_all('div', class_='main')
       
       if main_div:
        table = soup.table
        if table:
            data = {}
            rows = table.find_all('tr')
            for row in rows:
              cols = row.find_all('td')
              if len(cols) == 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                data[key] = value
            read_len = data.get("Sequence length")
            if "-" in read_len:
              read_len = read_len.split("-")[1]
            print(read_len)
    def __init__(self):
       pass

    def main(self):

       main = Main()

       warnings.filterwarnings('ignore')

       parser = argparse.ArgumentParser(description='MICROBIOME PixelCut version (gtphrase@inu.ac.kr,gtphrase@naver.com)')
       parser.add_argument('html' ,type=str,help='fastqc html files')

       args = parser.parse_args(sys.argv[1:])
       html = args.html 
       main.extractor(html)

if __name__ == '__main__':
   #main()
   main = Main()
   main.main()
