# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 20:25:24 2022

@author: Mario Fernández Ruiz
"""

import pandas as pd
import datetime as dt
import warnings 
from datetime import datetime
import time as TIME 
warnings.filterwarnings('ignore')



#OLD-FUNCTIONS------------------------------------------------------------
def sum_hour(hour,minute):
    hora = hour[0:2]
    minuto = hour[2:4]
    segundo = hour[4:6]
    hora1 = dt.timedelta(hours = int(hora), minutes = int(minuto), seconds = int(segundo))
    hora_suma = dt.timedelta(minutes=int(minute))
    suma = hora1+hora_suma
    
    #Si segundo es >=30 se añade un minuto
    #BUENA IDEA ??????????????????????????????????????????
    if (int(segundo)>=30):
        suma = suma + dt.timedelta(minutes=1)
    #---------------------------------------------------
    
    split = str(suma).rsplit(":")
    new_minuto=split[1]
    if (len(split[0])<=1):
        new_hora = "0"+split[0]
    else:
        new_hora = split[0]
        
    resultado = new_hora + new_minuto
    return resultado


def obtain_predictions_OLD(txt): #txt is the name of the txt file (so you should add .txt)
    path='C:/Users/Usuario/Desktop/e-Callisto/NeuralNetwork/Predictions/'
    file = open(path+txt)
    rows = file.readlines()
    prediction_list = []
    for i in range(len(rows)):
        cols = rows[i].rsplit()
        if (not len(rows[i])<=1):
            day = rows[i].rsplit()[1].rsplit("_")[3]
            base_hour = rows[i].rsplit()[1].rsplit("_")[4]
            minute_to_sum = rows[i].rsplit()[1].rsplit("_")[5].rsplit("-")[1][0:2]
            hour = sum_hour(base_hour, minute_to_sum)    
            if (("SI" in rows[i].rsplit()[3]) or ("ASSAerupcion" in rows[i].rsplit()[3])):
                prediction=True
            else:
                prediction=False

            run=cols[1].rsplit("/")[3].rsplit("-",1)[0]
            fourplet = [day,hour,prediction,run]
            prediction_list.append(fourplet)
    return prediction_list

def obtain_metrics_OLD(ID,txt): #Given txt file of predictions (name including '.txt') and ID of a CALLISTO station
#it returns a list with [day, time, TN/FP/TP/FN] for each prediction in the file
#To decide TN/FP/TP/FN, obtain_interval_bursts(ID) function is used
#TN: prediction is Negative, obtain_interval_bursts doesn't contain that time
#FP: prediction is Positive, obtain_interval_bursts doesn't contain that time
#TP: prediction is Positive, obtain_interval_bursts does contain that time
#FN: prediction is Negative, obtain_interval_bursts does contain that time
    burst_time_list = obtain_interval_bursts(ID)  
    prediction_list = obtain_predictions_OLD(txt) #ESTA ES LA UNICA DIFERENCIA

    pdPred=pd.DataFrame(prediction_list)
    day=pdPred[0][0]
    pdBursts=pd.DataFrame(burst_time_list)
    pdBursts=pdBursts.loc[(pdBursts[0]==prediction_list[0][0])]
    pdBursts=pdBursts.loc[(pdBursts[1]==prediction_list[0][1])]

    metrics_list = []
    pdPred=pd.DataFrame(prediction_list)
    for i in range(len(prediction_list)): 
        day=pdPred[0][i]
        hour=pdPred[1][i]
        pdBursts=pd.DataFrame(burst_time_list)
        pdBursts=pdBursts.loc[(pdBursts[0]==prediction_list[i][0])]
        pdBursts=pdBursts.loc[(pdBursts[1]==prediction_list[i][1])]
        if (prediction_list[i][2]==False and len(pdBursts)<=0):
            metric="TN"
        elif (prediction_list[i][2]==False and len(pdBursts)>0):
            metric="FN"
        elif (prediction_list[i][2]==True and len(pdBursts)<=0):
            metric="FP"
        else:
            metric="TP"

        run = pdPred[3][i]
        fourplet = [day, hour, metric, run]
        metrics_list.append(fourplet)        
    return metrics_list




#-------------------------------------------------------------------------




































#AUX FUNCTIONS--------------------------------------------------------------------------------
def round_hour(hour): #aux function: given time in format 'HHMMSS' it returns 'HHMM' rounded
    segundo = hour[4:6]
    time = datetime.strptime(hour, "%H%M%S")

    #If SS >=30 we add 1 minute. GOOD IDEA?????
    if (int(segundo)>=30): time = time + dt.timedelta(minutes=1)
    #---------------------------------------------------
    
    time = str(time)
    new_time = time[11:13]+time[14:16]
    return new_time

def sum_minute(hour,plus): #given time in format 'HHMM' and an integer (+-) i returns the sum of time plus integer.
    time = datetime.strptime(hour, "%H%M") + dt.timedelta(minutes=plus)
    time = str(time)
    new_time = time[11:13]+time[14:16]
    return new_time
#------------------------------------------------------------------------------------------------






#BASE FUNCTIONS---------------------------------------------------------------------------------
#There are only 2 diff paths (but in many functions): paths for predictions (txt/csv) & paths for bursts.csv

def obtain_predictions(txt): #Given txt file of predictions (name including '.txt') 
#it returns a list with [day, time, Positive/Negative, FITS] for each prediction in the file
    path='C:/Users/Usuario/Desktop/e-Callisto/NeuralNetwork/Predictions/' #Edit
    file = open(path+txt)
    rows = file.readlines()
    prediction_list = []
    for i in range(len(rows)):
        cols = rows[i].rsplit()
        if (not len(rows[i])<=1):
            day = cols[1].rsplit("_")[3]
            hour = cols[1].rsplit("_")[4]
            hour = round_hour(hour)
            if (("SI" in cols[3]) or ("ASSAerupcion" in cols[3])):
                prediction=True
            else:
                prediction=False
            
            if i%15 == 0:
                run = cols[1].rsplit("/")[3].rsplit(".")[0] + ".fit.gz"
            fourplet = [day,hour,prediction, run]
            prediction_list.append(fourplet)
    return prediction_list

def obtain_predictions_threshold(txt,th): #Same as above, but Pos/Neg is decided with a threshold
#True if -according to pred file- prob(Positive) >= th (Threshold)
    path='C:/Users/Usuario/Desktop/e-Callisto/NeuralNetwork/Predictions/' #Edit
    file = open(path+txt)
    rows = file.readlines()
    prediction_list = []
    for i in range(len(rows)):
        cols = rows[i].rsplit()
        if (not len(rows[i])<=1):
            day = cols[1].rsplit("_")[3]
            hour = cols[1].rsplit("_")[4]
            hour = round_hour(hour)
            if th <= 50:                
                if (("SI" in cols[3]) or ("ASSAerupcion" in cols[3]) or (float(cols[4][0:len(cols[4])-1])<=(100-th))):
                    prediction=True
                else:
                    prediction=False
            else:
                tr_check = float(cols[4][0:len(cols[4])-1])
                if ("SI" in cols[3]) and (tr_check>=th):
                    prediction=True
                else:
                    prediction=False
                    
            if i%15 == 0:
                run = cols[1].rsplit("/")[3].rsplit(".")[0] + ".fit.gz"
            fourplet = [day,hour,prediction, run]
            prediction_list.append(fourplet)
    return prediction_list

def obtain_interval_bursts(ID): #Given ID of a CALLISTO station it returns a
#list of [date,time] for every minute with a burst in the given station (according to e-Callisto reports)
#csv with this information is needed ... To implement (having it auto)
    path='C:/Users/Usuario/Desktop/e-Callisto/CallistoReports/' #Edit
    bursts = pd.read_csv(path+'CallistoEvents.csv', encoding= 'unicode_escape')
    bursts = bursts.dropna() #Remove NA
    burstsID = bursts[bursts.Obs.str.contains(ID)]
    burstsID['Year'] = burstsID['Year'].astype('str')
    burstsID['Month'] = burstsID['Month'].astype('str')
    burstsID['Day'] = burstsID['Day'].astype('str')
    burstTimeList = []
    for i in burstsID.index: 
        year = burstsID["Year"][i]
        if (len(burstsID["Month"][i])==1):
            month = "0"+burstsID["Month"][i]
        else:
            month = burstsID["Month"][i]
        if (len(burstsID["Day"][i])==1):
            day = "0"+burstsID["Day"][i]
        else:
            day = burstsID["Day"][i]
            
        date = year+month+day        
        begin = burstsID["Begin"][i]
        end = burstsID["End"][i]
        if len(end)>4:
            end = end[0:4]
        elif end=='????':
            end = '2359'
        k = begin
        
        
        while (k<=end):
            duplex = [date,k]
            burstTimeList.append(duplex)
            if (k[1:4]=="959"):
                k = str(int(k[0])+1)+"000"
            elif (k[2:4]=="59"):
                k = k[0]+str(int(k[1])+1)+"00"
            elif (k[3]=="9"):
                k = k[0:2]+str(int(k[2])+1)+"0"                
            else:
                k = k[0:3]+str(int(k[3])+1)
        
    return burstTimeList

def obtain_beginEnd_bursts(ID): #Given ID of a CALLISTO station it returns a
#list of [date,begin,end] for every burst in the given station (according to e-Callisto reports)
#csv with this information is needed ... To implement (having it auto)
    path='C:/Users/Usuario/Desktop/e-Callisto/CallistoReports/'    #Edit
    bursts = pd.read_csv(path+'CallistoEvents.csv', encoding= 'unicode_escape')
    bursts = bursts.dropna() #quitamos los NA que hay por errores en los reports
    #burstsID = bursts.loc[(bursts.Obs == ID)]
    burstsID = bursts[bursts.Obs.str.contains(ID)]
    burstsID['Year'] = burstsID['Year'].astype('str')
    burstsID['Month'] = burstsID['Month'].astype('str')
    burstsID['Day'] = burstsID['Day'].astype('str')
    burstTimeList = []
    for i in burstsID.index: 
        year = burstsID["Year"][i]
        if (len(burstsID["Month"][i])==1):
            month = "0"+burstsID["Month"][i]
        else:
            month = burstsID["Month"][i]
        if (len(burstsID["Day"][i])==1):
            day = "0"+burstsID["Day"][i]
        else:
            day = burstsID["Day"][i]
            
        date = year+month+day        
        begin = burstsID["Begin"][i]
        end = burstsID["End"][i]
        
        triplex = [date,begin,end]
        burstTimeList.append(triplex)        
    return burstTimeList

def obtain_beginEnd_bursts_wo_parenthesis(ID): #Version of above for only "not-in-brakets bursts" in reports
    path='C:/Users/Usuario/Desktop/e-Callisto/CallistoReports/'    #Edit
    bursts = pd.read_csv(path+'CallistoEvents.csv', encoding= 'unicode_escape')
    bursts = bursts.dropna() #quitamos los NA que hay por errores en los reports
    #burstsID = bursts.loc[(bursts.Obs == ID)]
    burstsID = bursts[bursts.Obs.str.contains(ID)]
    burstsID = burstsID[burstsID.Obs.str.startswith(burstsID["Obs"][burstsID.index[0]][0])]
    burstsID['Year'] = burstsID['Year'].astype('str')
    burstsID['Month'] = burstsID['Month'].astype('str')
    burstsID['Day'] = burstsID['Day'].astype('str')
    burstTimeList = []
    for i in burstsID.index: 
        year = burstsID["Year"][i]
        if (len(burstsID["Month"][i])==1):
            month = "0"+burstsID["Month"][i]
        else:
            month = burstsID["Month"][i]
        if (len(burstsID["Day"][i])==1):
            day = "0"+burstsID["Day"][i]
        else:
            day = burstsID["Day"][i]
            
        date = year+month+day        
        begin = burstsID["Begin"][i]
        end = burstsID["End"][i]
        
        triplex = [date,begin,end]
        burstTimeList.append(triplex)      
    return burstTimeList


def obtain_beginEnd_bursts_parenthesis(ID): #Version of above for only "bursts in brakets" in reports
    path='C:/Users/Usuario/Desktop/e-Callisto/CallistoReports/'    #Edit
    bursts = pd.read_csv(path+'CallistoEvents.csv', encoding= 'unicode_escape')
    bursts = bursts.dropna() #quitamos los NA que hay por errores en los reports
    #burstsID = bursts.loc[(bursts.Obs == ID)]
    burstsID = bursts[bursts.Obs.str.contains(ID)]
    burstsID = burstsID[burstsID.Obs.str.startswith("(")]
    burstsID['Year'] = burstsID['Year'].astype('str')
    burstsID['Month'] = burstsID['Month'].astype('str')
    burstsID['Day'] = burstsID['Day'].astype('str')
    burstTimeList = []
    for i in burstsID.index: 
        year = burstsID["Year"][i]
        if (len(burstsID["Month"][i])==1):
            month = "0"+burstsID["Month"][i]
        else:
            month = burstsID["Month"][i]
        if (len(burstsID["Day"][i])==1):
            day = "0"+burstsID["Day"][i]
        else:
            day = burstsID["Day"][i]
            
        date = year+month+day        
        begin = burstsID["Begin"][i]
        end = burstsID["End"][i]
        
        triplex = [date,begin,end]
        burstTimeList.append(triplex)        
    return burstTimeList

def obtain_metrics(ID,txt): #Given txt file of predictions (name including '.txt') and ID of a CALLISTO station
#it returns a list with [day, time, TN/FP/TP/FN] for each prediction in the file
#To decide TN/FP/TP/FN, obtain_interval_bursts(ID) function is used
#TN: prediction is Negative, obtain_interval_bursts doesn't contain that time
#FP: prediction is Positive, obtain_interval_bursts doesn't contain that time
#TP: prediction is Positive, obtain_interval_bursts does contain that time
#FN: prediction is Negative, obtain_interval_bursts does contain that time
    burst_time_list = obtain_interval_bursts(ID)  
    prediction_list = obtain_predictions(txt)

    pdPred=pd.DataFrame(prediction_list)
    day=pdPred[0][0]
    pdBursts=pd.DataFrame(burst_time_list)
    pdBursts=pdBursts.loc[(pdBursts[0]==prediction_list[0][0])]
    pdBursts=pdBursts.loc[(pdBursts[1]==prediction_list[0][1])]

    metrics_list = []
    pdPred=pd.DataFrame(prediction_list)
    for i in range(len(prediction_list)): 
        day=pdPred[0][i]
        hour=pdPred[1][i]
        pdBursts=pd.DataFrame(burst_time_list)
        pdBursts=pdBursts.loc[(pdBursts[0]==prediction_list[i][0])]
        pdBursts=pdBursts.loc[(pdBursts[1]==prediction_list[i][1])]
        if (prediction_list[i][2]==False and len(pdBursts)<=0):
            metric="TN"
        elif (prediction_list[i][2]==False and len(pdBursts)>0):
            metric="FN"
        elif (prediction_list[i][2]==True and len(pdBursts)<=0):
            metric="FP"
        else:
            metric="TP"

        run = pdPred[3][i]
        fourplet = [day, hour, metric, run]
        metrics_list.append(fourplet)        
    return metrics_list


def obtain_metrics_threshold(ID,txt,th): #Same as above, but Pos/Neg of predictions is decided with a threshold
#True if -according to pred file- prob(Positive) >= th (Threshold)
    burst_time_list = obtain_interval_bursts(ID)  
    prediction_list = obtain_predictions_threshold(txt, th)

    pdPred=pd.DataFrame(prediction_list)
    day=pdPred[0][0]
    pdBursts=pd.DataFrame(burst_time_list)
    pdBursts=pdBursts.loc[(pdBursts[0]==prediction_list[0][0])]
    pdBursts=pdBursts.loc[(pdBursts[1]==prediction_list[0][1])]

    metrics_list = []
    pdPred=pd.DataFrame(prediction_list)
    for i in range(len(prediction_list)): 
        day=pdPred[0][i]
        hour=pdPred[1][i]
        pdBursts=pd.DataFrame(burst_time_list)
        pdBursts=pdBursts.loc[(pdBursts[0]==prediction_list[i][0])]
        pdBursts=pdBursts.loc[(pdBursts[1]==prediction_list[i][1])]
        if (prediction_list[i][2]==False and len(pdBursts)<=0):
            metric="TN"
        elif (prediction_list[i][2]==False and len(pdBursts)>0):
            metric="FN"
        elif (prediction_list[i][2]==True and len(pdBursts)<=0):
            metric="FP"
        else:
            metric="TP"
        
        run = pdPred[3][i]
        fourplet = [day,hour,metric,run]
        metrics_list.append(fourplet)     
    return metrics_list

def DiffRuns(metrics):  #Given a metrics list (or subset) it returns a list with the name of all different FITS files
    runList = []
    for i in metrics.index:
        run = metrics[3][i]
        if (run not in runList):
            runList.append(run)
    return runList
#--------------------------------------------------------------------------------






#AUX FOR CONF. MATRIX---------------------------------------------------------------
def obtain_FP_times(metrics_list): #FP time min by min
    pdMetrics=pd.DataFrame(metrics_list)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    FP_list = pdMetrics.loc[(pdMetrics[2]=="FP")]
    return FP_list

def obtain_Pdef_times_min(metrics_list): #TP+FN times min by min (ordered crono.)
    pdMetrics=pd.DataFrame(metrics_list)
    FN_list = pdMetrics.loc[(pdMetrics[2]=="FN")]
    TP_list = pdMetrics.loc[(pdMetrics[2]=="TP")]
    Pdef_list = pd.concat([FN_list, TP_list], axis=0)
    Pdef_list = Pdef_list.sort_index()
    return Pdef_list

def n_runs(times): #Given the result of previous functions (times min by min) it returns the number of 
#15 minutes runs for those times
    if (len(times)==0):
        return 0
    elif (len(times)==1):
        return 1
    
    count=1
    for i in range(len(times)-1):
        if (times.iloc[i,0]==times.iloc[i+1,0] and int(times.iloc[i,1])//15==int(times.iloc[i+1,1])//15):
            count=count
        else:
            count=count+1      
    return count
#------------------------------------------------------------------------------------






#PDEF-------------------------------------------------------------------------------------------------------
#Assign TP/FN to every burst in the e-Callisto report we are working with----------------------------
def obtain_Pdef_times(metrics_list,ID):
    pdMetrics=pd.DataFrame(metrics_list)
    bursts = obtain_beginEnd_bursts(ID)
    pdBursts = pd.DataFrame(bursts)
    pdBursts = pdBursts.loc[(pdBursts[0]>=metrics_list[0][0])]
    pdBursts = pdBursts.loc[(pdBursts[0]<=metrics_list[len(metrics_list)-1][0])]
    
    Pdef_list = []
    for i in pdBursts.index:
        date = pdBursts[0][i]
        begin = pdBursts[1][i]
        end = pdBursts[2][i]
        metric_burst = pdMetrics.loc[(pdMetrics[0]==pdBursts[0][i])] #Select day
        if (len(metric_burst)<=0):
            continue
        try:
            metric_burst = metric_burst.loc[(metric_burst[1]>=sum_minute(pdBursts[1][i],-1))] #Select >= begin-1min 
            metric_burst = metric_burst.loc[(metric_burst[1]<=sum_minute(pdBursts[2][i],1))] #Select <= end+1min
        except:
            continue
        metric_burst_TP = metric_burst.loc[(metric_burst[2]=="TP")] #Select Positives
        metric_burst_FP = metric_burst.loc[(metric_burst[2]=="FP")] #In case is out by 1 min
        metric_burst = pd.concat([metric_burst_TP, metric_burst_FP], axis=0)
        if (len(metric_burst)<=0): #If 0 positives
            metric = "FN"
        else:
            metric = "TP"
        Pdef_list.append([date,begin,end,metric])

    return Pdef_list


#Same as above, but only for "not-in-brackets bursts" in CALLISTO reports
def Pdef_wo_parenthesis(metrics_list,ID):
    pdMetrics=pd.DataFrame(metrics_list)
    bursts = obtain_beginEnd_bursts_wo_parenthesis(ID)
    pdBursts = pd.DataFrame(bursts)
    pdBursts = pdBursts.loc[(pdBursts[0]>=metrics_list[0][0])]
    pdBursts = pdBursts.loc[(pdBursts[0]<=metrics_list[len(metrics_list)-1][0])]
    
    Pdef_list = []
    for i in pdBursts.index:
        date = pdBursts[0][i]
        begin = pdBursts[1][i]
        end = pdBursts[2][i]
        metric_burst = pdMetrics.loc[(pdMetrics[0]==pdBursts[0][i])] #Select day
        if (len(metric_burst)<=0):
            continue
        try:
            metric_burst = metric_burst.loc[(metric_burst[1]>=sum_minute(pdBursts[1][i],-1))] #Select >= begin-1min 
            metric_burst = metric_burst.loc[(metric_burst[1]<=sum_minute(pdBursts[2][i],1))] #Select <= end+1min
        except:
            continue
        metric_burst_TP = metric_burst.loc[(metric_burst[2]=="TP")] #Select Positives
        metric_burst_FP = metric_burst.loc[(metric_burst[2]=="FP")] #In case is out by 1 min
        metric_burst = pd.concat([metric_burst_TP, metric_burst_FP], axis=0)
        if (len(metric_burst)<=0): #If 0 positives
            metric = "FN"
        else:
            metric = "TP"
        Pdef_list.append([date,begin,end,metric])

    return Pdef_list


#Same as above, but only for "bursts in brackets" in CALLISTO reports
def Pdef_parenthesis(metrics_list,ID):
    pdMetrics=pd.DataFrame(metrics_list)
    bursts = obtain_beginEnd_bursts_parenthesis(ID)
    pdBursts = pd.DataFrame(bursts)
    pdBursts = pdBursts.loc[(pdBursts[0]>=metrics_list[0][0])]
    pdBursts = pdBursts.loc[(pdBursts[0]<=metrics_list[len(metrics_list)-1][0])]
    
    Pdef_list = []
    for i in pdBursts.index:
        date = pdBursts[0][i]
        begin = pdBursts[1][i]
        end = pdBursts[2][i]
        metric_burst = pdMetrics.loc[(pdMetrics[0]==pdBursts[0][i])] #Select day
        metric_burst = metric_burst.loc[(metric_burst[1]>=pdBursts[1][i])] #Select > begin
        metric_burst = metric_burst.loc[(metric_burst[1]<=pdBursts[2][i])] #Select < end
        metric_burst = metric_burst.loc[(metric_burst[2]=="TP")] #Select Positives
        if (len(metric_burst)<=0): #If 0 positives
            metric = "FN"
        else:
            metric = "TP"
        Pdef_list.append([date,begin,end,metric])

    return Pdef_list
#----------------------------------------------------------------------------------------------------





#CONF. MATRIX FUNCTIONS---------------------------------------------------------------------------------
def obtain_confusion_matrix(metrics_list, ID): #Given metrics list and ID of a CALLISTO station
#it returns the confusion matrix (results)
    Pdef_times = obtain_Pdef_times(metrics_list, ID)
    pdPdef=pd.DataFrame(Pdef_times)
    
    n_FP = n_runs(obtain_FP_times(metrics_list))
    n_TN = len(metrics_list)/15 - n_runs(obtain_FP_times(metrics_list)) - n_runs(obtain_Pdef_times_min(metrics_list))    
    
    if (len(pdPdef)>0): #In case there are any events
        n_TP = len(pdPdef.loc[(pdPdef[3]=="TP")])
        n_FN = len(pdPdef.loc[(pdPdef[3]=="FN")])
    else:
        n_TP = 0
        n_FN = 0
    
    confusion_matrix = {"TN": n_TN, "FP": n_FP, "TP": n_TP, "FN": n_FN}
    return confusion_matrix

#Same as above, but only for "not-in-brackets bursts" in CALLISTO reports
def obtain_confusion_matrix_wo_parenthesis(metrics_list,ID): 
    Pdef_times = Pdef_wo_parenthesis(metrics_list, ID)
    pdPdef=pd.DataFrame(Pdef_times)
    
    n_FP = n_runs(obtain_FP_times(metrics_list))
    n_TN = len(metrics_list)/15 - n_runs(obtain_FP_times(metrics_list)) - n_runs(obtain_Pdef_times_min(metrics_list))    
    
    if (len(pdPdef)>0): #In case there are any events
        n_TP = len(pdPdef.loc[(pdPdef[3]=="TP")])
        n_FN = len(pdPdef.loc[(pdPdef[3]=="FN")])
    else:
        n_TP = 0
        n_FN = 0
    
    confusion_matrix = {"TN": n_TN, "FP": n_FP, "TP": n_TP, "FN": n_FN}
    return confusion_matrix


def obtain_confusion_matrix_percentage(cm): #Given a confusion matrix it returns the rates
    TN_rate = round(cm["TN"]/(cm["TN"] + cm["FP"]),4)*100
    if cm["TP"] + cm["FN"] == 0:
        TP_rate = 0
        FN_rate = 0
    else:
        TP_rate = round(cm["TP"]/(cm["TP"] + cm["FN"]),4)*100
        FN_rate = round(cm["FN"]/(cm["TP"] + cm["FN"]),4)*100
    FP_rate = round(cm["FP"]/(cm["TN"] + cm["FP"]),4)*100
    
    confusion_matrix = {"TN rate": TN_rate, "FP rate": FP_rate, "TP rate": TP_rate, "FN rate": FN_rate}
    return confusion_matrix
#----------------------------------------------------------------------------------------------------








#REDUCED SAMPLE & FN RATE--------------------------------------------------------------------------------------
def obtain_performance(metrics_list, ID): #Given a metrics_list and the ID of a given e-Callisto station, 
#it returns [sample_reduction, FN_rate]
#sample_reduction: proportion of predicted Positives (so, those needed to check)
#FN_rate: proportion of missed actual bursts
    #First, we compute FN_rate
    Pdef_times = obtain_Pdef_times(metrics_list, ID)
    pdPdef=pd.DataFrame(Pdef_times)
    if (len(pdPdef)>0): #In case there are no events
        n_TP = len(pdPdef.loc[(pdPdef[3]=="TP")])
        n_FN = len(pdPdef.loc[(pdPdef[3]=="FN")])
    else:
        n_TP = 0
        n_FN = 0    
    FN_rate = round(n_FN/(n_TP + n_FN),4)*100
    
    #Next, we compute sample_reduction
    runsALL = pd.DataFrame(metrics_list)             
    runsFP = runsALL.loc[(runsALL[2]=="FP")]   
    runsTP = runsALL.loc[(runsALL[2]=="TP")]
    runsFPTP = pd.concat([runsFP, runsTP], axis=0)
    diffRunsALL=DiffRuns(runsALL)
    diffRunsFPTP=DiffRuns(runsFPTP)
    
    ####NUEVO
    diffRunsFP=DiffRuns(runsFP)
    diffRunsTP=DiffRuns(runsTP)
    ####
    
    sample_reduction = round(len(diffRunsFPTP)/len(diffRunsALL),4)*100
    
    #Ad-hoc para TFM
    performance = {"Sample Reduction": sample_reduction, "FN rate": FN_rate,
                   "Bursts detected by model": n_TP, "Bursts in reports": n_TP + n_FN,
                   "No. Runs involved": len(diffRunsALL), "Positive Runs": len(diffRunsFPTP),
                   #"RSFtrue": round(len(diffRunsTP)/len(diffRunsALL),4)*100,
                   #"RSFfalse": round(len(diffRunsFP)/len(diffRunsALL),4)*100}
                   "RSFtrue": round(len(diffRunsTP)/len(diffRunsFPTP),4)*100,
                   "RSFfalse": round(len(diffRunsFP)/len(diffRunsFPTP),4)*100}
    
    
    #performance = [sample_reduction, FN_rate]
    
    return performance

#To implement a threshold use a metrics_list with a threshold already implemented.
#-----------------------------------------------------------------------------------------------------------





#REDUCED SAMPLE & FN RATE--------------------------------------------------------------------------------------
def obtain_performance_wo_brkts(metrics_list, ID): #Given a metrics_list and the ID of a given e-Callisto station, 
#it returns [sample_reduction, FN_rate]
#sample_reduction: proportion of predicted Positives (so, those needed to check)
#FN_rate: proportion of missed actual bursts
    #First, we compute FN_rate
    Pdef_times = Pdef_wo_parenthesis(metrics_list, ID)
    pdPdef=pd.DataFrame(Pdef_times)
    if (len(pdPdef)>0): #In case there are no events
        n_TP = len(pdPdef.loc[(pdPdef[3]=="TP")])
        n_FN = len(pdPdef.loc[(pdPdef[3]=="FN")])
    else:
        n_TP = 0
        n_FN = 0    
    FN_rate = round(n_FN/(n_TP + n_FN),4)*100
    
    #Next, we compute sample_reduction
    runsALL = pd.DataFrame(metrics_list)             
    runsFP = runsALL.loc[(runsALL[2]=="FP")]   
    runsTP = runsALL.loc[(runsALL[2]=="TP")]
    runsFPTP = pd.concat([runsFP, runsTP], axis=0)
    diffRunsALL=DiffRuns(runsALL)
    diffRunsFPTP=DiffRuns(runsFPTP)
    
    ####NUEVO
    diffRunsFP=DiffRuns(runsFP)
    diffRunsTP=DiffRuns(runsTP)
    ####
    
    sample_reduction = round(len(diffRunsFPTP)/len(diffRunsALL),4)*100
    
    #Ad-hoc para TFM
    performance = {"Sample Reduction": sample_reduction, "FN rate": FN_rate,
                   "Bursts detected by model": n_TP, "Bursts in reports": n_TP + n_FN,
                   "No. Runs involved": len(diffRunsALL), "Positive Runs": len(diffRunsFPTP),
                   #"RSFtrue": round(len(diffRunsTP)/len(diffRunsALL),4)*100,
                   #"RSFfalse": round(len(diffRunsFP)/len(diffRunsALL),4)*100}
                   "RSFtrue": round(len(diffRunsTP)/len(diffRunsFPTP),4)*100,
                   "RSFfalse": round(len(diffRunsFP)/len(diffRunsFPTP),4)*100}
    
    
    #performance = [sample_reduction, FN_rate]
    
    return performance

#To implement a threshold use a metrics_list with a threshold already implemented.
#-----------------------------------------------------------------------------------------------------------








#MAIN--------------------------------------------------------------------------------------------------
ID = "Australia-ASSA"
#ID = "HUMAIN"

txt = "ASSA_2021.txt"


performance_th = []
for k in range(1,20):
    th = k*5
    metrics_list = obtain_metrics_threshold(ID, txt, th)
    
    performance = obtain_performance(metrics_list,ID)
    performance_th.append([th,performance]) 


"""
th=50

metrics = obtain_metrics_threshold(ID, txt, th)
burst_intervals = obtain_Pdef_times(metrics, ID)
cm = obtain_confusion_matrix(metrics,ID)
cm_rates = obtain_confusion_matrix_percentage(cm)
burst_intervals_wo = Pdef_wo_parenthesis(metrics, ID)
cm_wo = obtain_confusion_matrix_wo_parenthesis(metrics, ID)
cm_wo_rates = obtain_confusion_matrix_percentage(cm_wo)
print(cm)
print(cm_rates)
"""

"""
th=75

metrics = obtain_metrics_threshold(ID, txt, th)
burst_intervals = obtain_Pdef_times(metrics, ID)
cm = obtain_confusion_matrix(metrics,ID)
cm_rates = obtain_confusion_matrix_percentage(cm)
burst_intervals_wo = Pdef_wo_parenthesis(metrics, ID)
cm_wo = obtain_confusion_matrix_wo_parenthesis(metrics, ID)
cm_wo_rates = obtain_confusion_matrix_percentage(cm_wo)
print(cm)
print(cm_rates)
"""

#------------------------------------------------------------------------------------------









#Discarded Functions--------------------------------------------------------------------
""" REDUNDANT (We use metrics_list directly as argument insted of ID,txt) (cm instead of ID,txt in last case)
def obtain_FN_times(ID,txt):
    metrics_list = obtain_performance(ID, txt)
    pdMetrics=pd.DataFrame(metrics_list)
    FN_list = pdMetrics.loc[(pdMetrics[2]=="FN")]
    return FN_list
def obtain_FP_times(ID,txt):
    metrics_list = obtain_performance(ID, txt)
    pdMetrics=pd.DataFrame(metrics_list)
    FP_list = pdMetrics.loc[(pdMetrics[2]=="FP")]
    return FP_list
def obtain_TP_times(ID,txt):
    metrics_list = obtain_performance(ID, txt)
    pdMetrics=pd.DataFrame(metrics_list)
    TP_list = pdMetrics.loc[(pdMetrics[2]=="TP")]
    return TP_list
def obtain_Pdef_times(ID,txt):
    metrics_list = obtain_performance(ID, txt)
    pdMetrics=pd.DataFrame(metrics_list)
    Pdef_list = pdMetrics.loc[(pdMetrics[2]=="FN" or pdMetrics[2]=="TP")]
    return Pdef_list

def obtain_confusion_matrix(ID,txt):
    metrics_list = obtain_metrics(ID, txt)
    Pdef_times = obtain_Pdef_times(metrics_list, ID)
    pdPdef=pd.DataFrame(Pdef_times)
    
    #n_FP = len(pdMetrics.loc[(pdMetrics[2]=="FP")])
    n_FP = n_runs(obtain_FP_times(metrics_list))
    n_TN = len(metrics_list)/15 - n_runs(obtain_FP_times(metrics_list)) - n_runs(obtain_Pdef_times_min(metrics_list))    
    
    if (len(pdPdef)>0): #In case there are any events
        n_TP = len(pdPdef.loc[(pdPdef[3]=="TP")])
        n_FN = len(pdPdef.loc[(pdPdef[3]=="FN")])
    else:
        n_TP = 0
        n_FN = 0
       
    confusion_matrix = {"TN": n_TN, "FP": n_FP, "TP": n_TP, "FN": n_FN}
    return confusion_matrix

def obtain_confusion_matrix_percentage(ID,txt):
    cm = obtain_confusion_matrix(ID, txt)
        
    TN_rate = round(cm["TN"]/(cm["TN"] + cm["FP"]),4)*100
    TP_rate = round(cm["TP"]/(cm["TP"] + cm["FN"]),4)*100
    FN_rate = round(cm["FN"]/(cm["TP"] + cm["FN"]),4)*100
    FP_rate = round(cm["FP"]/(cm["TN"] + cm["FP"]),4)*100
    
    confusion_matrix = {"TN rate": TN_rate, "FP rate": FP_rate, "TP rate": TP_rate, "FN rate": FN_rate}
    return confusion_matrix
"""



""" DESCARTADO POR AHORA / TODAS LAS FUNCIONES PARA DAR RESULTADO EN BASE A BURST/QUIET INTERVALS

def obtain_Pdef_times_union(metrics_list):
    pdMetrics=pd.DataFrame(metrics_list)
    FN_list = pdMetrics.loc[(pdMetrics[2]=="FN")]
    TP_list = pdMetrics.loc[(pdMetrics[2]=="TP")]
    Pdef_list = pd.concat([FN_list, TP_list], axis=0)
    Pdef_list = Pdef_list.sort_index()
        
    if (Pdef_times.shape[0]>0):
        date=Pdef_times.iloc[0,0]
        begin=Pdef_times.iloc[0,1]
        end=begin
        if (Pdef_times.iloc[0,2]=='FN'):
            metric="FN"
        else:
            metric='TP'
        
        to_append=[date,begin,end,metric]
    Pdef_list2=[]
    
    
    iterator=1
    while iterator <= len(Pdef_times)-1:
        if (Pdef_times.index[iterator]!=Pdef_times.index[iterator-1]+1):
            Pdef_list2.append(to_append)
            #to_append=[date,begin,end,metric]
            date=date=Pdef_times.iloc[iterator,0]
            begin=Pdef_times.iloc[iterator,1]
            end=begin
            if (Pdef_times.iloc[iterator,2]=='FN'):
                metric='FN'
            else:
                metric='TP'
            to_append=[date,begin,end,metric]
            
        elif (Pdef_times.index[iterator]==Pdef_times.index[iterator-1]+1 and Pdef_times.iloc[iterator,2]=='TP'):
            end=Pdef_times.iloc[iterator,1]
            metric='TP'
            to_append=[date,begin,end,metric]
            
        elif (Pdef_times.index[iterator]==Pdef_times.index[iterator-1]+1 and Pdef_times.iloc[iterator,2]=='FN'):
            end=Pdef_times.iloc[iterator,1]
            to_append=[date,begin,end,metric]
        
        iterator = iterator+1
    if (Pdef_times.shape[0]>0):
        Pdef_list2.append(to_append)
        
    return Pdef_list2

def Ndef_times(metrics_list,ID): #Se podría crear una funcion con solo sin paréntesis
#Fallo que tiene: No se da información sobre días sin bursts. No lo veo importante por ahora.
    Pdef_times = obtain_Pdef_times_union(metrics_list)
    pdMetrics=pd.DataFrame(metrics_list)
    if len(Pdef_times)<=0:
        print("There are no bursts")
        return []
    
    Ndef_list=[]
    if Pdef_times[0][1]!='0000':
        date_begin=Pdef_times[0][0]
        hour_begin='0000'
        hour_end=sum_minute(Pdef_times[0][1],-1)
        metric_burst = pdMetrics.loc[(pdMetrics[0]==date_begin)] 
        metric_burst = metric_burst.loc[(metric_burst[1]>=hour_begin)] #Select > begin
        metric_burst = metric_burst.loc[(metric_burst[1]<=hour_end)] #Select < end
        metric_burst = metric_burst.loc[(metric_burst[2]=="FP")] #Select Positives
        if (len(metric_burst)<=0): #If 0 positives
            metric = "TN"
        else:
            metric = "FP"
        Ndef_list.append([date_begin,hour_begin,hour_end,metric])
    
    for i in range(len(Pdef_times)-1):
        if Pdef_times[i][0]==Pdef_times[i+1][0]:
            date_begin = Pdef_times[i][0]
            hour_begin = sum_minute(Pdef_times[i][2],1)
            hour_end = sum_minute(Pdef_times[i+1][1],-1)
            metric_burst = pdMetrics.loc[(pdMetrics[0]==date_begin)] 
            metric_burst = metric_burst.loc[(metric_burst[1]>=hour_begin)] #Select > begin
            metric_burst = metric_burst.loc[(metric_burst[1]<=hour_end)] #Select < end
            metric_burst = metric_burst.loc[(metric_burst[2]=="FP")] #Select Positives
            if (len(metric_burst)<=0): #If 0 positives
                metric = "TN"
            else:
                metric = "FP"
            Ndef_list.append([date_begin,hour_begin,hour_end,metric])
        else:
            date_begin = Pdef_times[i][0]
            hour_begin = sum_minute(Pdef_times[i][2],1)
            hour_end = '2359'
            metric_burst = pdMetrics.loc[(pdMetrics[0]==date_begin)] 
            metric_burst = metric_burst.loc[(metric_burst[1]>=hour_begin)] #Select > begin
            metric_burst = metric_burst.loc[(metric_burst[1]<=hour_end)] #Select < end
            metric_burst = metric_burst.loc[(metric_burst[2]=="FP")] #Select Positives
            if (len(metric_burst)<=0): #If 0 positives
                metric = "TN"
            else:
                metric = "FP"
            Ndef_list.append([date_begin,hour_begin,hour_end,metric])
            date_begin = Pdef_times[i+1][0]
            hour_begin = '0000'
            hour_end = sum_minute(Pdef_times[i+1][1],-1)
            metric_burst = pdMetrics.loc[(pdMetrics[0]==date_begin)] 
            metric_burst = metric_burst.loc[(metric_burst[1]>=hour_begin)] #Select > begin
            metric_burst = metric_burst.loc[(metric_burst[1]<=hour_end)] #Select < end
            metric_burst = metric_burst.loc[(metric_burst[2]=="FP")] #Select Positives
            if (len(metric_burst)<=0): #If 0 positives
                metric = "TN"
            else:
                metric = "FP"
            Ndef_list.append([date_begin,hour_begin,hour_end,metric])
            
        
    if Pdef_times[len(Pdef_times)-1][2]=='2359':
        return Ndef_list
    
    date_begin=Pdef_times[len(Pdef_times)-1][0]
    hour_begin=sum_minute(Pdef_times[len(Pdef_times)-1][2],1)
    hour_end='2359'
    metric_burst = pdMetrics.loc[(pdMetrics[0]==date_begin)] 
    metric_burst = metric_burst.loc[(metric_burst[1]>=hour_begin)] #Select > begin
    metric_burst = metric_burst.loc[(metric_burst[1]<=hour_end)] #Select < end
    metric_burst = metric_burst.loc[(metric_burst[2]=="FP")] #Select Positives
    if (len(metric_burst)<=0): #If 0 positives
        metric = "TN"
    else:
        metric = "FP"
    Ndef_list.append([date_begin,hour_begin,hour_end,metric])
    return Ndef_list

def obtain_intervals(ID, txt):
    metrics = obtain_metrics(ID, txt)
    burst_intervals = obtain_Pdef_times(metrics, ID)
    quiet_intervals = Ndef_times(metrics, ID)
    intervals = burst_intervals + quiet_intervals 
    intervals = pd.DataFrame(intervals)
    intervals = intervals.sort_values([0,2])
    return intervals

def obtain_cm_intervals(ID,txt):
    intervals = obtain_intervals(ID, txt)
    
    if (len(intervals)==0):
        n_TN = 0
        n_FP = 0
        n_TP = 0
        n_FN = 0
    else:    
        n_TN = len(intervals.loc[(intervals[3]=="TN")])
        n_FP = len(intervals.loc[(intervals[3]=="FP")])
        n_TP = len(intervals.loc[(intervals[3]=="TP")])
        n_FN = len(intervals.loc[(intervals[3]=="FN")])

    confusion_matrix = {"TN": n_TN, "FP": n_FP, "TP": n_TP, "FN": n_FN}
    return confusion_matrix
"""