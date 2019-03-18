# -*- coding: utf-8 -*-
"""
Spyder Editor

@author redburning
"""

import os
import time
import json
import pandas as pd
from fbprophet import Prophet
from multiprocessing import Pool



def excludeQLV(data, qlv_file):
    qlv_data = pd.read_csv(qlv_file, stype = str)
    qlv = list(qlv_data['qlv'])
    data = data[~data['measure_point_no'].isin(qlv)]
    return data   
   

def get_assemble_data(data, assemble_no):
    assemble_data = data[data['assembly_no'] == assemble_no]
    return assemble_data


def get_stage_data(data, stage_no):
    stage_data = data[data['stage'] == stage_no]
    return stage_data


def direction_transform(data):
    data = data.dropna(subset = ['direction'])
    direction = list(data['direction'])
    ipetype = list(data['ipetype'])
    for index in range(len(direction)):
        if direction[index] == 'X/Y/Z':
            direction[index:index + 3] = ['X', 'Y', 'Z']
            index += 3
        elif (direction[index] == 'X/1' or direction[index] == 'Y/1' or direction[index] == 'Z/1') and ipetype[index] == 'FPT':
            direction[index] = 'A'
        elif (direction[index] == 'X/1' or direction[index] == 'Y/1' or direction[index] == 'Z/1') and (ipetype[index] == 'BPT' or ipetype[index] == 'KPT'):
            direction[index] = 'B'
        elif direction[index] == '2002/3/4':
            direction[index:index + 3] = ['2', '3', '4']
            index += 3
        elif direction[index] == '2/3/4':
            direction[index:index + 3] = ['2', '3', '4']
            index += 3
        elif direction[index] == '2/4':
            direction[index:index + 2] = ['2', '4']
            index += 2
    data['direction'] = direction
    
    return data



def get_limits(assemble_no):
    _format = '.csv'
    
    file_path = './upper_lower_limits/' + str(assemble_no) + '_lower_upper' + _format
    
    data = pd.read_csv(file_path)
    lower_dict = {}
    upper_dict = {}
    key = list(data['key'])
    lower = list(data['lower'])
    upper = list(data['upper'])
    for index in range(len(data)):
        if (str(lower[index]) != 'nan' and str(upper[index]) != 'nan'):
            lower_dict[key[index]] = lower[index]
            upper_dict[key[index]] = upper[index]
    return lower_dict, upper_dict




def parallel_analysis(assemble_name, assemble_data, current_folder):
    
    _format = '.csv'
    assemble_folderpath = current_folder + os.path.sep + assemble_name
    if not os.path.exists(assemble_folderpath):
        os.makedirs(assemble_folderpath)
        
    point_predicted_folderpath = assemble_folderpath + os.path.sep + 'points_predicted'
    if not os.path.exists(point_predicted_folderpath):
        os.makedirs(point_predicted_folderpath)
    
    point_unpredicted_folderpath = assemble_folderpath + os.path.sep + 'points_unpredicted'
    if not os.path.exists(point_unpredicted_folderpath):
        os.makedirs(point_unpredicted_folderpath)
        
    point_notfindlimits_folderpath = assemble_folderpath + os.path.sep + 'points_notfindlimits'
    if not os.path.exists(point_notfindlimits_folderpath):
        os.makedirs(point_notfindlimits_folderpath)
    
    assemble_data['key'] = assemble_data['stage'] + '-' + assemble_data['measure_point_no'] + '-' + assemble_data['direction']
    assemble_data = assemble_data[['key', 'measure_time_date', 'deviation']]
    
    assemble_data['deviation'] = assemble_data['deviation'].astype(float)
        
    periods = 30
    point_unpredicted = pd.DataFrame(columns = ['point_no'])
    point_notfindlimits = pd.DataFrame(columns = ['point_no'])
    lower_dict, upper_dict = get_limits(assemble_name)
    for point in assemble_data.groupby(['key']):
        point_name = point[0]
        point_data = point[1]
        if point_name in lower_dict.keys() and point_name in upper_dict.keys():
            training_data = point_data[['measure_time_date', 'deviation']]
            training_data = training_data.sort_values(['measure_time_date'])
            training_data.columns = ['ds', 'y']
            
            if len(training_data) > 20:
                
                prophet = Prophet()
                prophet.fit(training_data)
                future = prophet.make_future_dataframe(freq = 'D', periods = periods, include_history = False)
                forecasts = prophet.predict(future)
                
                forecasts = forecasts[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
                
                training_data.columns = ['ds', 'yhat']
                          
                temp_data = training_data.groupby(['ds']).mean()
                df_res = pd.DataFrame(columns = ['ds', 'yhat', 'yhat_lower', 'yhat_upper'])
                df_res['ds'] = list(temp_data.index)
                df_res['yhat'] = list(temp_data['yhat'])
                
                
                df_res['yhat_lower'] = 0
                df_res['yhat_upper'] = 0
                
                df_res = df_res.append(forecasts, ignore_index = True)               
                
                
                lower = lower_dict[point_name]
                upper = upper_dict[point_name]
                df_res['lower'] = lower
                df_res['upper'] = upper
                
                point_predicted_savepath = point_predicted_folderpath + os.path.sep + point_name + _format
                df_res.to_csv(point_predicted_savepath, index = False)
            
            else:
                point_unpredicted = point_unpredicted.append({'point_no' : point_name}, ignore_index = True)
        else:
            point_notfindlimits = point_notfindlimits.append({'point_no' : point_name}, ignore_index = True)
            
    point_unpredicted_savepath = point_unpredicted_folderpath + os.path.sep + 'point_unpredicted' + _format
    point_unpredicted.to_csv(point_unpredicted_savepath, index = False)
    
    point_notfindlimits_savepath = point_notfindlimits_folderpath + os.path.sep + 'point_notfindlimits' + _format
    point_notfindlimits.to_csv(point_notfindlimits_savepath, index = False)
    
    

def do_analysis(data, current_folder):
    
    thread_no = config['threads_no']
    pool = Pool(processes = thread_no)
    
    for assemble in data.groupby(['assembly_no']):
        
        assemble_name = assemble[0]
        assemble_data = assemble[1]
        
        pool.apply_async(parallel_analysis, (assemble_name, assemble_data, current_folder, ))
        
    pool.close()
    pool.join()
        
        



if __name__ == '__main__':
    
    fjson = open('config.json')
    config = json.loads(fjson.read())
    
    starttime = time.time()
    f = open('running records.txt', 'w')
    
    path = config['awk_data_path']
    
    data = pd.read_csv(path, dtype = str) 
    
    data['measure_time_date'] = pd.to_datetime(data.measure_time_date, format = '')    
    
    f.write('direction transform...' + '\n')
    data = direction_transform(data)
    
    
    f.write('processing data of all stages...' + '\n')
    
    stage_all_folder = config['result_path'] + 'Stage All'
    
    if not os.path.exists(stage_all_folder):
        os.makedirs(stage_all_folder)
    do_analysis(data, stage_all_folder)   
    
    stages = pd.Series(data['stage'])
    stage_counts = stages.value_counts()
    
    
    for stage_name in stage_counts.index:
        
        f.write('processing data of stage ' + stage_name + '\n')
        
        stage_folder = config['result_path'] + stage_name
        
        if not os.path.exists(stage_folder):
            os.makedirs(stage_folder)
        stage_data = get_stage_data(data, stage_name)
        do_analysis(stage_data, stage_folder)
    
    
        
    endtime = time.time()
    f.write('finished. use time(s):' + str(endtime - starttime) + '\n')
    f.close()
    
    fjson.close()