# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 09:29:27 2021

@author: Mario Fernández Ruiz
"""

import urllib
from bs4 import BeautifulSoup
import requests
from astropy.io import fits
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib import cm
from os import mkdir
from os import remove
import os
import time as TIME 
import glob
import datetime as dt
from datetime import datetime
from pathlib import Path


#AUX FUNCTIONS------------------------------------------------------------------------------------------------
def sum1day(iterator):
    new_iterator = datetime.strptime(iterator, "%Y/%m/%d")+dt.timedelta(days=1)
    new_iterator = str(new_iterator)[0:10].replace("-","/")
    return new_iterator

def listFD2(url, ID, focus_code):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser') #Devuelve todo el contenido de una página en formato html
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').startswith(ID) and node.get('href').endswith(focus_code+'.fit.gz')]

def sumMinute(namePNG, minute):
    time = namePNG.rsplit("_")[2]
    newTime = datetime.strptime(time, "%H%M%S") + dt.timedelta(minutes=minute)
    newTime = str(newTime).rsplit()[1]
    newTime = newTime.rsplit(":")[0] + newTime.rsplit(":")[1] + newTime.rsplit(":")[2]
    new_namePNG = namePNG.rsplit("_")[0]+"_"+namePNG.rsplit("_")[1]+"_"+newTime +"_"+namePNG.rsplit("_")[3]
    return new_namePNG
#--------------------------------------------------------------------------------------------------------------





#MAIN FUNCTIONS-------------------------------------------------------------------------------------------------
def fullIntervalImages(begin, end, ID, focus_code): #end after begin please
    begin_wo_bars = begin.replace("/", "") #To remove '/' in date
    end_wo_bars = end.replace("/", "") #To remove '/' in date
    iterator = begin
    
    path = 'C:/Users/Usuario/Desktop/e-Callisto/NeuralNetwork'
    nombreCarpeta_txt = ID+'_'+begin_wo_bars+'-'+end_wo_bars+'_'+focus_code
    file = open(path+'/txt/' + nombreCarpeta_txt +'.txt', "w")  #Creates a .txt with the path of all images in DIGITS (to use the model)
    
    while(iterator != sum1day(end)): 
        url = 'http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/'+iterator+'/'
        L = listFD2(url, ID, focus_code)
        iterator_wo_bars = iterator.replace("/", "") #To remove '/' in date
        nombreCarpeta = ID+'_'+iterator_wo_bars+'_'+focus_code
        
        if not os.path.exists(Path(path+nombreCarpeta+'/')):
            mkdir(path+nombreCarpeta+'/') #Creates a file where images will be
                
        for i in range (len(L)):
            try:
                myfile = L[i].rsplit('/', 1)[1]
                namePNG= myfile.rsplit(".")[0]
                myurl = url + myfile
                urllib.request.urlretrieve(myurl,myfile) 
                    
                hdu   = fits.open(myfile)
                data  = hdu[0].data.astype(np.float32)
                freqs = hdu[1].data['Frequency'][0] # extract frequency axis
                time  = hdu[1].data['Time'][0] # extract time axis
                hdu.close()

    #------------------------------------------------------------------------------
                plt.figure(figsize=(4.6,4.72)) #Exact numbers for the images to be 256x256px
                plt.axis('off')
                extent = (time[0], time[-1], freqs[-1], freqs[0])
                avg =  data.mean(axis=1, keepdims=True)  # calculate average
                bgs = data - avg  # subtract average
                plt.imshow(bgs, aspect = 'auto', extent = extent, cmap=cm.CMRmap, vmin=0,vmax=12) #values for vmin and vmax are selected to get the best contrast
                
            #After some observation these have been considered to be the best ranges for freq for every observatory
                if (ID=='Australia-ASSA'):
                    plt.ylim((25,80)) # y-axis limits in MHz
                elif (ID=='BIR'):
                    plt.ylim((20,87))
                elif (ID=='SWISS-Landschlacht'):
                    plt.ylim((18,84))
                elif (ID=='SWISS-HEITERSWIL'):
                    plt.ylim((45,80.8))
                #elif (ID=='GLASGOW'): #GLASGOW limit is all range
                      
                for j in range (15):
                    plt.xlim((j*60,60+j*60))
                    plt.savefig(path+nombreCarpeta+'/'+sumMinute(namePNG, j)+".png",bbox_inches='tight', pad_inches=0.0)
                    file.write("/data/"+nombreCarpeta+'/'+sumMinute(namePNG, j)+".png 0" + '\n')
                plt.clf()  
                plt.close()
                
            except:
                continue
        iterator = sum1day(iterator)     
    file.close()
    
    
    #Comment this part if you want to keep FITS files
    fileList = glob.glob('*.fit.gz') ##### remove all downloaded fit.gz files ... in working directory JBG
    for filePath in fileList:
        try:
            remove(filePath)
        except:
            print("Error while deleting file : ", filePath)
    




    


#MAIN---------------------------------------------------------------------------------------
#fullIntervalImages("2014/01/01", "2014/01/31", 'BIR','01')
#fullIntervalImages("2014/02/01", "2014/02/28", 'BIR','01')
#fullIntervalImages("2014/03/01", "2014/03/31", 'BIR','01')
#fullIntervalImages("2014/04/01", "2014/04/30", 'BIR','01')
#fullIntervalImages("2014/05/01", "2014/05/31", 'BIR','01')
#fullIntervalImages("2014/06/01", "2014/06/30", 'BIR','01')
#fullIntervalImages("2014/07/01", "2014/07/31", 'BIR','01')
#fullIntervalImages("2014/08/01", "2014/08/31", 'BIR','01')
#fullIntervalImages("2014/09/01", "2014/09/30", 'BIR','01')
#fullIntervalImages("2014/10/01", "2014/10/31", 'BIR','01')
#fullIntervalImages("2014/11/01", "2014/11/30", 'BIR','01')
#fullIntervalImages("2014/12/01", "2014/12/31", 'BIR','01')

start = TIME.time()
fullIntervalImages("2022/02/02", "2022/02/02", 'Australia-ASSA','62')
end = TIME.time()
  
timeElapsed = end-start   
print("Time elapsed running has been: " + str(timeElapsed/60) + ' minutes')

"""
start = time.time()
#for i in range(1,31):
#    if i<10:
#        fullDayImages('2021/11/0' + str(i),'SWISS-Landschlacht','62')
#    else:
#        fullDayImages('2021/11/' + str(i),'SWISS-Landschlacht','62') 
   
fullDayImages('2022/01/30' ,'Australia-ASSA','62')
    
end = time.time()
timeElapsed = end-start
   
print("Time elapsed running has been: " + str(timeElapsed/60) + ' minutes')
"""




#DISCARDED----------------------------------------------------------------------------------
"""
def fullIntervalImages_1dir(begin, end, nombreCarpeta, ID, focus_code): #end after begin please
    iterator = begin
    
    path = 'C:/Users/Doncel/Desktop/Mario/NeuralNetwork/'
    if not os.path.exists(Path(path+nombreCarpeta+'/')):
        mkdir(path+nombreCarpeta+'/') #Creates a file where images will be
    while(iterator != sum1day(end)): 
        url = 'http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/'+iterator+'/'
        L = listFD2(url, ID, focus_code)
        
        
        for i in range (len(L)):
            myfile = L[i].rsplit('/', 1)[1]
            namePNG= myfile.rsplit(".")[0]
            myurl = url + myfile
            urllib.request.urlretrieve(myurl,myfile) 
                
            hdu   = fits.open(myfile)
            data  = hdu[0].data.astype(np.float32)
            freqs = hdu[1].data['Frequency'][0] # extract frequency axis
            time  = hdu[1].data['Time'][0] # extract time axis
            hdu.close()

    #------------------------------------------------------------------------------
            plt.figure(figsize=(4.6,4.72)) #Exact numbers for the images to be 256x256px
            plt.axis('off')
            extent = (time[0], time[-1], freqs[-1], freqs[0])
            avg =  data.mean(axis=1, keepdims=True)  # calculate average
            bgs = data - avg  # subtract average
            plt.imshow(bgs, aspect = 'auto', extent = extent, cmap=cm.CMRmap, vmin=0,vmax=12) #values for vmin and vmax are selected to get the best contrast
            
            #After some observation these have been considered to be the best ranges for freq for every observatory
            if (ID=='Australia-ASSA'):
                plt.ylim((25,80)) # y-axis limits in MHz
            elif (ID=='BIR'):
                plt.ylim((20,87))
            elif (ID=='SWISS-Landschlacht'):
                plt.ylim((18,84))
            elif (ID=='SWISS-HEITERSWIL'):
                plt.ylim((45,80.8))
            #elif (ID=='GLASGOW'): #GLASGOW no necesita ningun limite
                      
            for j in range (15):
                plt.xlim((j*60,60+j*60))
                plt.savefig(path+nombreCarpeta+'/'+sumMinute(namePNG, j)+".png",bbox_inches='tight', pad_inches=0.0)
            plt.clf()  
            plt.close()
            
        iterator = sum1day(iterator)  
"""