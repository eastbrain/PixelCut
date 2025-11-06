# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 11:24:43 2025

@author: gtphr
"""


import os
import sys
import cv2
import warnings
import argparse
import imutils
import csv
import numpy as np
import pandas as pd
import subprocess
import threading

import pytesseract
from pytesseract import pytesseract
import PIL
from PIL import Image
import matplotlib.pyplot as plt

import ast
import json

from datetime import datetime


class Main:

############################################################################################################################
    def get_Color_Name_(self,R,G,B):
       index = ["color","color_name","hex","R","G","B"]
       csv=pd.read_csv('colors.csv', names=index, header=None)
       minimum = 10000
       for i in range(len(csv)):
           d = abs(int(R)- int(csv.loc[i,"R"])) + abs(int(G)- int(csv.loc[i,"G"]))+ abs(int(B)- int(csv.loc[i,"B"]))
           if(d<=minimum):
               minimum = d
               cname = csv.loc[i,"color_name"]
       return cname 
############################################################################################################################
    def get_Color_Name(self,R,G,B,csv):
       #index = ["color","color_name","hex","R","G","B"]
       #csv=pd.read_csv('colors.csv', names=index, header=None)
       minimum = 10000
       for i in range(len(csv)):
           d = abs(int(R)- int(csv.loc[i,"R"])) + abs(int(G)- int(csv.loc[i,"G"]))+ abs(int(B)- int(csv.loc[i,"B"]))
           if(d<=minimum):
               minimum = d
               cname = csv.loc[i,"color_name"]
       return cname
############################################################################################################################
    def listToString(self,s):
      str1 = " ",
      return (' '.join(map(str, str(s))))
############################################################################################################################
    def stream_output(process):
      for line in process.stdout:
        print(line.decode().strip())
############################################################################################################################
    def detection(self,r1,r2):
      def stream_output(process, prefix):
         for line in iter(process.stdout.readline, b''):
           if line:
             print(f"{prefix} {line.decode().strip()}")
           else:
             break 

      extract_py  = "extract_quality_plot_fastqc.py"
      tracking_py = "tracking_low_quality_area.py" 
      len1 = subprocess.run(['python',extract_py,r1], capture_output=True, text=True).stdout.strip()
      len2 = subprocess.run(['python',extract_py,r2], capture_output=True, text=True).stdout.strip()
      print("Read1 Length: " + len1)
      print("Read2 Length: " + len2)
      
      p1 = subprocess.Popen(['python',tracking_py,r1+".jpg",len1], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
      p2 = subprocess.Popen(['python',tracking_py,r2+".jpg",len2], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

      t1 = threading.Thread(target=stream_output, args=(p1,'[Read1]'))
      t2 = threading.Thread(target=stream_output, args=(p2,'[Read2]'))

      t1.start()
      t2.start()

      p1.wait()
      p2.wait()

      t1.join()
      t2.join()

              
############################################################################################################################    
    def __init__(self):
       pass
############################################################################################################################
    def main(self):

       start_time = datetime.now()
       
       main = Main()

       warnings.filterwarnings('ignore')

       parser = argparse.ArgumentParser(description='Microbiome 16S PixelCut (Dongin Kim, gtphrase@inu.ac.kr, gtphrase@naver.com, ISPLab@INU)')
       parser.add_argument('r1'  ,type=str,help='read1 fastqc html')
       parser.add_argument('r2'  ,type=str,help='read2 fastqc html')

       args = parser.parse_args(sys.argv[1:])
       r1   = args.r1
       r2   = args.r2 
       
       main.detection(r1,r2)
       end_time = datetime.now()
       elapsed = end_time - start_time

       print("Total time:", elapsed)

if __name__ == '__main__':
   #main()
   main = Main()
   main.main()

