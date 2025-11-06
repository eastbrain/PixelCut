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

import pytesseract
from pytesseract import pytesseract
import PIL
from PIL import Image
import matplotlib.pyplot as plt

import ast
import json

from datetime import datetime


class Main:

#Reading csv file with pandas and giving names to each column
#index=["color","color_name","hex","R","G","B"]
#csv = pd.read_csv('colors.csv', names=index, header=None)

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
    def detection(self,img,colors_csv,length):
        
      #color code
      index = ["color","color_name","hex","R","G","B"]
      csv=pd.read_csv(colors_csv, names=index, header=None)

      # image position
       #data=pytesseract.image_to_boxes(mimg)
       #print(data)

      ksize=(5,5)
      min_threshold=75
      max_threshold=200
      lang='eng'

      #pytesseract_options = " --psm 4 "

      image = cv2.imread(img)
      rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      gray      = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
      blurred   = cv2.GaussianBlur(gray, ksize, 0)
      edged     = cv2.Canny(blurred, min_threshold, max_threshold)
      
      # Get image dimensions
      height, width, _ = rgb_image.shape
      total_count = 0  # 첫 번째 칸 포함
      prev_color = ""
      start_pix  = 20
      for k in range(width):  # Loop over X-axis (Base Length)
         img_frag               = image[530:10+530,2+start_pix:12+start_pix] 
         rgb_image_img_frag     = rgb_image[530:10+530,2+start_pix:12+start_pix]
         
         pixels_tmp = eval((np.array2string(cv2.cvtColor(img_frag, cv2.COLOR_BGR2RGB)).replace("[[","[").replace("]]","]").replace(" ",",").replace(",,",",").replace(",,",",").replace("[,","[")))
         pixels=[pixels_tmp[x] for x in range(len(pixels_tmp)) if not(pixels_tmp[x] in pixels_tmp[:x])]
         color_name= ""
         for a in pixels:
             c = main.listToString(a).replace(" ","").replace("[","").replace("]","")
             r = c.split(",")[0]
             g = c.split(",")[1]
             b = c.split(",")[2]
             color_name = main.get_Color_Name(r,g,b,csv).lower()
         if color_name == "white":
             break;
         if color_name != prev_color:
             total_count += 1
             prev_color = color_name
         start_pix = start_pix + 14
      #print("total pixel count: ", total_count)
      
      target_pos   = 0
      real_pos     = 0
      target_count = total_count
      start_pix    = width - round(width*0.008407)
      start_pix2   = width
      for j in range(width):  
         # print(width)
          img_frag               = image[280:18+280,  start_pix:5+start_pix] #Q20 
          rgb_image_img_frag     = rgb_image[280:300, start_pix+1:5+start_pix] #Q20    
          
          if (2+start_pix) <= round(width*0.954497) and (5+start_pix) <= round(width*0.957671):
              #print(width,2+start_pix,5+start_pix)
              plt.imshow(rgb_image_img_frag)      
              plt.title("rgb_image_img_frag")
              plt.show()                  
                            
              pixels_tmp = eval((np.array2string(cv2.cvtColor(img_frag, cv2.COLOR_BGR2RGB)).replace("[[","[").replace("]]","]").replace(" ",",").replace(",,",",").replace(",,",",").replace("[,","[")))
              pixels=[pixels_tmp[x] for x in range(len(pixels_tmp)) if not(pixels_tmp[x] in pixels_tmp[:x])]
              color_name= ""
              for a in pixels:
                  c = main.listToString(a).replace(" ","").replace("[","").replace("]","")
                  r = c.split(",")[0]
                  g = c.split(",")[1]
                  b = c.split(",")[2]
                  color_name = main.get_Color_Name(r,g,b,csv).lower()
              target_count = target_count - 1
              target_pos   = int(length) * (target_count/total_count)
              #print("color_name",color_name)
              #print(width,2+start_pix,5+start_pix,target_count,str(target_pos))
              if color_name != "yellow"  and color_name != "mustard" and color_name  != "dandelion" and color_name  != "aureolin" and color_name !="titanium yellow":
                  break;                                    
          x1 = start_pix2 - 80
          x2 = start_pix2 - 2
          if x2 >= width:
            x2 = width - 20
            
          if 2+start_pix <= 902 and 5+start_pix <= 905:
              target_img_frag = image[560:18+560,x1:x2] #Q20  
              plt.imshow(target_img_frag)      
              plt.title("target_img_frag")                  
              #print(start_pix,2+start_pix,5+start_pix)
              
              
          start_pix  = start_pix  - round(width*14/945)
          start_pix2 = start_pix2 - 10
          if start_pix < 14:
             start_pix = 1
             break

      print("truncation position: ", str(int(round(target_pos,0))))
              
############################################################################################################################    
    def detection_(self,img,colors_csv):

      #color code
      index = ["color","color_name","hex","R","G","B"]
      csv=pd.read_csv(colors_csv, names=index, header=None)

      # image position
       #data=pytesseract.image_to_boxes(img)
       #print(data)

      ksize=(5,5)
      min_threshold=75
      max_threshold=200
      lang='eng'

      #pytesseract_options = " --psm 4 "

      image = cv2.imread(img)
      rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      gray      = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
      blurred   = cv2.GaussianBlur(gray, ksize, 0)
      edged     = cv2.Canny(blurred, min_threshold, max_threshold)
      
      # Get image dimensions
      height, width, _ = rgb_image.shape
      total_count = 0  # 첫 번째 칸 포함
      prev_color = ""
      start_pix = 20
      #for k in range(int((975+20)/20)+1): # ori
      for k in range(width):  # Loop over X-axis (Base Length)
          #img_frag = image[280:18+280, 2+start:20+start] #20Q
          #img_frag = image[306:18+306, 2+start:20+start]
          #img_frag = image[530:10+530, 2+start_pix:20+start_pix] 
          img_frag               = image[530:10+530,2+start_pix:12+start_pix] 
          rgb_image_img_frag     = rgb_image[530:10+530,2+start_pix:12+start_pix]
          pixels_tmp = eval((np.array2string(cv2.cvtColor(img_frag, cv2.COLOR_BGR2RGB)).replace("[[","[").replace("]]","]").replace(" ",",").replace(",,",",").replace(",,",",").replace("[,","[")))
          pixels=[pixels_tmp[x] for x in range(len(pixels_tmp)) if not(pixels_tmp[x] in pixels_tmp[:x])]
          color_name= ""
          for a in pixels:
              c = main.listToString(a).replace(" ","").replace("[","").replace("]","")
              r = c.split(",")[0]
              g = c.split(",")[1]
              b = c.split(",")[2]
              color_name = main.get_Color_Name(r,g,b,csv).lower()
          if color_name == "white":
              break;
          if color_name != prev_color:
              total_count += 1
              prev_color = color_name
          #print("Detecting pixel color: ",color_name,total_count)
          #start_pix = start_pix -2 + 20
          start_pix = start_pix + 14
      #print("total pixel count: ", total_count)
      
      target_pos   = 0
      real_pos     = 0
      total_count2 = 0
      start_pix    = 20
      start_pix2   = 20
      for j in range(width):          
         
          img_frag               = image[530:10+530,2+start_pix:12+start_pix] 
          rgb_image_img_frag     = rgb_image[530:10+530,2+start_pix:12+start_pix]
          pixels_tmp = eval((np.array2string(cv2.cvtColor(img_frag, cv2.COLOR_BGR2RGB)).replace("[[","[").replace("]]","]").replace(" ",",").replace(",,",",").replace(",,",",").replace("[,","[")))
          pixels=[pixels_tmp[x] for x in range(len(pixels_tmp)) if not(pixels_tmp[x] in pixels_tmp[:x])]
          color_name= ""
          for a in pixels:
              c = main.listToString(a).replace(" ","").replace("[","").replace("]","")
              r = c.split(",")[0]
              g = c.split(",")[1]
              b = c.split(",")[2]
              color_name = main.get_Color_Name(r,g,b,csv).lower()
         
          if color_name != prev_color:
            total_count2 += 1
            prev_color = color_name
                  
          img_frag2               = image[280:18+280, 2+start_pix2:5+start_pix2] #Q20
          rgb_image_img_frag2     = rgb_image[280:18+280, 2+start_pix2:5+start_pix2] #Q20
          
          pixels_tmp2 = eval((np.array2string(cv2.cvtColor(img_frag2, cv2.COLOR_BGR2RGB)).replace("[[","[").replace("]]","]").replace(" ",",").replace(",,",",").replace(",,",",").replace("[,","[")))
          pixels2=[pixels_tmp2[x] for x in range(len(pixels_tmp2)) if not(pixels_tmp2[x] in pixels_tmp2[:x])]
          color_name2= ""
          for a in pixels2:
              c = main.listToString(a).replace(" ","").replace("[","").replace("]","")
              r = c.split(",")[0]
              g = c.split(",")[1]
              b = c.split(",")[2]
              color_name2 = main.get_Color_Name(r,g,b,csv).lower()          
          plt.imshow(rgb_image_img_frag2)      
          plt.title("rgb_image_img_frag2")
          plt.show() 
         
          real_pos = total_count2 / (int(total_count)/length)
          #if real_pos > 10:
          #    real_pos += real_pos + 5 -2
          real_pos = round(real_pos,2)
          #print("color_name",color_name,total_count2, total_count, real_pos)
          if color_name == "yellow"  or color_name == "mustard" or color_name  == "dandelion":
              break;
          print("color_name",color_name,total_count2, total_count, real_pos)
          
          start_pix  = start_pix + 14
          #start_pix = start_pix -2 + 20
          start_pix2 = start_pix + 20
          
          x1 =  2+start_pix2
          x2 = 80+start_pix2
          if x2 >= width:
              x2 = width - 20
          target_img_frag = image[560:18+560,x1:x2] #Q20
          #target_img_frag = image[560:18+560, 2+start_pix2:80+start_pix2] #Q20
          #target_img_frag = image[560:18+560, 2+start_pix:20+start_pix]

          #print(width,x1,x2)
          #print(width,str(2+start_pix2),str(80+start_pix2))

          plt.imshow(target_img_frag)      
          plt.title("target_img_frag")
          plt.show()

          gray      = cv2.cvtColor(target_img_frag,cv2.COLOR_BGR2GRAY)
          blurred   = cv2.GaussianBlur(gray, ksize, 0)

          text = pytesseract.image_to_string(gray, lang='kor+eng')
          text = text.replace("-"," ").replace("."," " )

          pos_list=[]
          splits = text.split()
          for split in splits:
              if len(split) > 3:
                 split = split[0:3]
              if split.isnumeric():
                pos_list.append(int(split))
            
          pos_list.sort(reverse=True)
          pos_1st=0
          pos_2nd=0
          c=0
          for a in pos_list:
            if c==0:
             pos_1st=a
            if c==1:
             pos_2nd=a
            c=c+1
            
            interval=round((int(pos_1st)-int(pos_2nd))/2)
            target_pos = int(pos_2nd) + interval
            if interval>=50:
             target_pos = int(pos_1st)
            #print("target pos:", str(target_pos))

      print("final target pos:", str(target_pos))
############################################################################################################################
    def __init__(self):
       pass
############################################################################################################################
    def main(self):

       colors_csv="colors.csv"

       start_time = datetime.now()
       
       main = Main()

       warnings.filterwarnings('ignore')

       parser = argparse.ArgumentParser(description='MICROBIOME PixelCut (gtphrase@inu.ac.kr, gtphrase@naver.com')
       parser.add_argument('image' ,type=str,help='image files')
       parser.add_argument('len' ,type=str,help='fastq read length(cycle)')

       args     = parser.parse_args(sys.argv[1:])
       img_file = args.image
       length   = args.len 
       
       main.detection(img_file,colors_csv,length)
       end_time = datetime.now()
       elapsed = end_time - start_time

       #print("Total time:", elapsed)

if __name__ == '__main__':
   #main()
   main = Main()
   main.main()

