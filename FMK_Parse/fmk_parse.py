# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 09:29:36 2018

@author: weijie
"""

import time
import os
from scipy.optimize import fsolve
import sympy as sy
import pandas as pd
import json
from math import sqrt, sin, cos


# 这个方向转换仅仅是变换方向，不关心每个方向的偏差值是多少
def direction_transform(data):
    '''
    data_c = data.copy()
    data_c = data_c.dropna(subset = ['direction'])
    data_c = data_c.sort_values(['assembly_no', 'car_no', 'measure_point_no', 'measure_time_date', 'measure_time_time', 'z_standard_low', 'z_standard_upper', 'y_standard_low', 'y_standard_upper', 'x_standard_low', 'x_standard_upper'])
    
    direction = list(data_c['direction'])
    for i in range(len(direction)):
        direction[i] = direction[i][1:-1]
    measure_point = list(data_c['measure_point_no'])
    car_no = list(data_c['car_no'])
    ipetype = list(data_c['ipetype'])
    
    length = len(direction)
    index = 0
    while index < length:
        if (direction[index] == "'X/1'" or direction[index] == "'Y/1'" or direction[index] == "'Z/1'") and ipetype[index] == 'FPT':
            direction[index] = 'A'
            index += 1
        elif (direction[index] == "'X/1'" or direction[index] == "'Y/1'" or direction[index] == "'Z/1'") and (ipetype[index] == 'BPT' or ipetype[index] == 'KPT'):
            direction[index] = 'B'
            index += 1
        elif (direction[index] == "'X/Y/Z'"):
            if (index + 1 < length) and (measure_point[index] == measure_point[index + 1]) and (direction[index] == direction[index + 1]) and (car_no[index] == car_no[index + 1]) and (index + 2 < length) and (measure_point[index] == measure_point[index + 2]) and (direction[index] == direction[index + 2]) and (car_no[index] == car_no[index + 2]):
                direction[index:index + 3] = ['X', 'Y', 'Z']
                index += 3
            else:
                direction[index] = 'X'
                data_c = data_c.append(data_c.iloc[index], ignore_index = True)
                data_c = data_c.append(data_c.iloc[index], ignore_index = True)
                direction.append('Y')
                direction.append('Z')
                index += 1
                print('X/Y/Z direction append finished...')
        elif (direction[index] == "'X/Y'"):
            if (index + 1 < length) and (measure_point[index] == measure_point[index + 1]) and (direction[index] == direction[index + 1]) and (car_no[index] == car_no[index + 1]):
                direction[index: index + 2] = ['X', 'Y']
                index += 2
            else:
                direction[index] = 'X'
                data_c = data_c.append(data_c.iloc[index], ignore_index = True)
                direction.append('Y')
                index += 1
                print('X/Y direction append finished...')
        elif (direction[index] == "'X/Z'"):
            if (index + 1 < length) and (measure_point[index] == measure_point[index + 1]) and (direction[index] == direction[index + 1]) and (car_no[index] == car_no[index + 1]):
                direction[index: index + 2] = ['X', 'Z']
                index += 2
            else:
                direction[index] = 'X'
                data_c = data_c.append(data_c.iloc[index], ignore_index = True)
                direction.append('Z')
                index += 1
                print('X/Z direction append finished...')
        elif (direction[index] == "'Y/Z'"):
            if (index + 1 < length) and (measure_point[index] == measure_point[index + 1]) and (direction[index] == direction[index + 1]) and (car_no[index] == car_no[index + 1]):
                direction[index: index + 2] = ['Y', 'Z']
                index += 2
            else:
                direction[index] = 'Y'
                data_c = data_c.append(data_c.iloc[index], ignore_index = True)
                direction.append('Z')
                index += 1
                print('Y/Z direction append finished...')
        elif (direction[index] == "'2/3/4'"):
            if (index + 1 < length) and (measure_point[index] == measure_point[index + 1]) and (direction[index] == direction[index + 1]) and (car_no[index] == car_no[index + 1]) and (index + 2 < length) and (measure_point[index] == measure_point[index + 2]) and (direction[index] == direction[index + 2]) and (car_no[index] == car_no[index + 2]):
                direction[index: index + 3] = ['2', '3', '4']
                index += 3
            else:
                direction[index] = '2'
                data_c = data_c.append(data_c.iloc[index], ignore_index = True)
                data_c = data_c.append(data_c.iloc[index], ignore_index = True)
                direction.append('3')
                direction.append('4')
                index += 1
                print('2/3/4 direction append finished...')
        elif (direction[index] == "'2/4'"):
            if (index + 1 < length) and (measure_point[index] == measure_point[index + 1]) and (direction[index] == direction[index + 1]) and (car_no[index] == car_no[index + 1]):
                direction[index: index + 2] = ['2', '4']
                index += 2
            else:
                direction[index] = '2'
                data_c = data_c.append(data_c.iloc[index], ignore_index = True)
                direction.append('4')
                index += 1
                print('2/4 direction append finished...')
        else:
            index += 1
    
    data_c['direction'] = direction
    
    return data_c
    '''
    
    data_c = data.copy()
    data_c = data_c.dropna(subset = ['direction_flag'])
    
    direction_flag = list(data_c['direction_flag'])
    ipetype = list(data_c['ipetype'])
    direction_new = []
    
    length = len(direction_flag)
    index = 0
    
    while index < length:
        if (direction_flag[index] == '1') and (ipetype[index] == 'BPT'):
            direction_new.append('B')
            index += 1
        elif (direction_flag[index] == '1') and (ipetype[index] != 'BPT'):
            direction_new.append('A')
            index += 1
        else:
            direction_new.append(direction_flag[index])
            index += 1
            
    data_c['direction'] = direction_new
    
    return data_c






def get_direction_match_data(data, direction):
    
    res = data.copy()
    if direction == 'dx' or direction == 'dX' or direction == 'X':
        res = res[(res['direction_flag'] == 'X') | ((res['direction_flag'] == '1') & (res['direction'] == "'X/1'"))]
    elif direction == 'dy' or direction == 'dY' or direction == 'Y':
        res = res[(res['direction_flag'] == 'Y') | ((res['direction_flag'] == '1') & (res['direction'] == "'Y/1'"))]
    elif direction == 'dz' or direction == 'dZ' or direction == 'Z':
        res = res[(res['direction_flag'] == 'Z') | ((res['direction_flag'] == '1') & (res['direction'] == "'Z/1'"))]
    elif direction == 'A':
        res = res[(res['direction_flag'] == '1') & (res['ipetype'] != 'BPT')]
    elif direction == 'B':
        res = res[(res['direction_flag'] == '1') & (res['ipetype'] == 'BPT')]
        
    return res
    
    



def get_point_difference(data_point_a, data_point_b):
    
    data_res = pd.DataFrame(columns = data_point_a.columns)
    
    if (len(data_point_a) > 0) and (len(data_point_b) > 0):
        name_point_a = data_point_a.iloc[0]['measure_point_no']
        name_point_b = data_point_b.iloc[0]['measure_point_no']
        data_point_a = data_point_a.sort_values(['time'])
        data_point_b = data_point_b.sort_values(['time'])
        
        measure_value_dic = {'dx' : 'x_value', 'dX' : 'x_value', 'dy' : 'y_value', 'dY' : 'y_value', 'dz' : 'z_value', 'dZ' : 'z_value'}
        standard_value_dic = {'dx' : 'x_standard', 'dX' : 'x_standard', 'dy' : 'y_standard', 'dY' : 'y_standard', 'dz' : 'z_standard', 'dZ' : 'z_standard'}
        
        if len(data_point_a) == len(data_point_b):
            deviation_ab = []
            measure_value_ab = []
            standard_value_ab = []
            measure_value_a = list(data_point_a[measure_value_dic[direction_name]])
            measure_value_b = list(data_point_b[measure_value_dic[direction_name]])
            standard_value_a = list(data_point_a[standard_value_dic[direction_name]])
            standard_value_b = list(data_point_b[standard_value_dic[direction_name]])
            for i in range(len(data_point_a)):
                measure_value_ab.append(abs(measure_value_a[i] - measure_value_b[i]))
                standard_value_ab.append(abs(standard_value_a[i] - standard_value_b[i]))
                deviation_ab.append(measure_value_ab[i] - standard_value_ab[i])
            data_res = data_res.append(data_point_a, ignore_index = True)
            
            data_res[measure_value_dic[direction_name]] = measure_value_ab
            data_res[standard_value_dic[direction_name]] = standard_value_ab
            data_res['deviation'] = deviation_ab
        
        else:
            time_list = list(data_point_a['time'])
            carno_list = list(data_point_a['car_no'])
            for i in range(len(data_point_a)):
                time = time_list[i]
                car_no = carno_list[i]
                for j in range(len(data_point_b)):
                    if (data_point_b.iloc[j]['time'] == time) and (data_point_b.iloc[j]['car_no'] == car_no):
                        temp_data = data_point_a.iloc[i].copy()
                        temp_data[measure_value_dic[direction_name]] = abs(data_point_a.iloc[i][measure_value_dic[direction_name]] - data_point_b.iloc[j][measure_value_dic[direction_name]])
                        temp_data[standard_value_dic[direction_name]] = abs(data_point_a.iloc[i][standard_value_dic[direction_name]] - data_point_b.iloc[j][standard_value_dic[direction_name]])
                        temp_data['deviation'] = temp_data[measure_value_dic[direction_name]] - temp_data[standard_value_dic[direction_name]]
                        data_res = data_res.append(temp_data, ignore_index = True)
                        break
        
        data_res['measure_point_no'] = name_point_a + '-' + name_point_b
    else:
        print('abnormal size of two points while calculating difference.')
        
    return data_res



def get_vars_known_according_time_carno(data, time, car_no, direction):
    standard_value_dic = {'X':'x_standard', 'Y':'y_standard', 'Z':'z_standard'}
    for i in range(len(data)):        
        if (data.iloc[i]['time'] == time) and (data.iloc[i]['car_no'] == car_no):
            x = data.iloc[i]['x_value']
            y = data.iloc[i]['y_value']     
            z = data.iloc[i]['z_value']
            
            if x == 0 and y == 0 and z == 0:
                break
            else:
                variable_known.append(float(x))
                variable_known.append(float(y))
                variable_known.append(float(z))
            
            t = data.iloc[i][standard_value_dic[direction]]
            variable_known.append(float(t))
            break
        


def generate_equation(alpha, beta, gamma, tx, ty, tz):
    
    equations = []
    direction_dic = {'X' : 0, 'Y' : 1, 'Z' : 2}
    a = sy.Matrix([[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]])
    b = sy.Matrix([[cos(gamma), -sin(gamma), 0, 0], [sin(gamma), cos(gamma), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    c = sy.Matrix([[cos(beta), 0, sin(beta), 0], [0, 1, 0, 0], [-sin(beta), 0, cos(beta), 0], [0, 0, 0, 1]])
    d = sy.Matrix([[1, 0, 0, 0], [0, cos(alpha), -sin(alpha), 0], [0, sin(alpha), cos(alpha), 0], [0, 0, 0, 1]])
    m = a * b * c * d
    
    for i in range(len(direction_global)):
        direction = direction_global[i]
        index = direction_dic[direction]
        equation = 0
        for k in range(3):
            equation += m[index * 4 + k] * (variable_known[i * 4 + k])            
            
        k += 1
        equation += m[index * 4 + k] * 1
        equation -= variable_known[i * 4 + k]
        equations.append(equation)
        
    return equations
    

    
def f(x):
    alpha = float(x[0])
    beta = float(x[1])
    gamma = float(x[2])
    tx = float(x[3])
    ty = float(x[4])
    tz = float(x[5])
    equations = generate_equation(alpha, beta, gamma, tx, ty, tz)
    return equations


def get_touch_direction():
    
    touch_direction_dic_path = config['touchDirection_dic_path']
    data = pd.read_csv(touch_direction_dic_path)
    touch_direction_dic = {}
    key = list(data['key'])
    direction = list(data['IPE.TouchDirection'])
    for i in range(len(key)):
        touch_direction_dic[key[i]] = direction[i]
        
    return touch_direction_dic





def transform_no_singlepoint_yes(data, assemble_no, point_no, direction_name):    
    
    data_res = data[(data['assembly_no'] == str(assemble_no)) & (data['measure_point_no'] == point_no)]
    data_res = get_direction_match_data(data_res, direction_name)
    data_res = data_res.sort_values(['time'])
    
    return data_res




def transform_no_singlepoint_no(data, assemble_no, point_a, point_b, direction_name):
    
    data_assemble = data[data['assembly_no'] == str(assemble_no)]
    data_point_a = data_assemble[data_assemble['measure_point_no'] == point_a]
    data_point_b = data_assemble[data_assemble['measure_point_no'] == point_b]
    
    data_point_a = get_direction_match_data(data_point_a, direction_name)
    data_point_b = get_direction_match_data(data_point_b, direction_name)
    
    data_res = get_point_difference(data_point_a, data_point_b)
    
    return data_res

    
    


def transform_yes_singlepoint_yes(data, assemble_no, point_no, benchmark_point_name_list, benchmark_point_dir_list, direction_name, dev_correction):
    
    global variable_known
    
    data_assemble = data[data['assembly_no'] == str(assemble_no)]
    data_assemble = data_assemble.sort_values(['time'])
    
    data_point_awk = data_assemble[data_assemble['measure_point_no'] == point_no]
    data_point_awk = get_direction_match_data(data_point_awk, direction_name)
    if len(data_point_awk) == 0:
        print('measure point  ' + str(point_no) + '  not find in awk data')
    
    data_point_0 = data_assemble[data_assemble['measure_point_no'] == benchmark_point_name_list[0]]
    data_point_0 = get_direction_match_data(data_point_0, benchmark_point_dir_list[0])
    #data_point_0 = data_point_0[(data_point_0['direction'].astype(str) == benchmark_point_dir_list[0]) | (data_point_0['direction'].astype(str) == benchmark_point_dir_list[0] + '/1')]
    if len(data_point_0) == 0:
        print('benchmark point  ' + str(benchmark_point_name_list[0]) + ' of measure point  ' + str(point_no) + ' not find in awk data')
    
    data_point_1 = data_assemble[data_assemble['measure_point_no'] == benchmark_point_name_list[1]]
    data_point_1 = get_direction_match_data(data_point_1, benchmark_point_dir_list[1])
    #data_point_1 = data_point_1[(data_point_1['direction'].astype(str) == benchmark_point_dir_list[1]) | (data_point_1['direction'].astype(str) == benchmark_point_dir_list[1] + '/1')]
    if len(data_point_1) == 0:
        print('benchmark point  ' + str(benchmark_point_name_list[1]) + ' of measure point  ' + str(point_no) + ' not find in awk data')
    
    data_point_2 = data_assemble[data_assemble['measure_point_no'] == benchmark_point_name_list[2]]
    data_point_2 = get_direction_match_data(data_point_2, benchmark_point_dir_list[2])
    #data_point_2 = data_point_2[(data_point_2['direction'].astype(str) == benchmark_point_dir_list[2]) | (data_point_2['direction'].astype(str) == benchmark_point_dir_list[2] + '/1')]
    if len(data_point_2) == 0:
        print('benchmark point  ' + str(benchmark_point_name_list[2]) + ' of measure point  ' + str(point_no) + ' not find in awk data')
    
    data_point_3 = data_assemble[data_assemble['measure_point_no'] == benchmark_point_name_list[3]]
    data_point_3 = get_direction_match_data(data_point_3, benchmark_point_dir_list[3])
    #data_point_3 = data_point_3[(data_point_3['direction'].astype(str) == benchmark_point_dir_list[3]) | (data_point_3['direction'].astype(str) == benchmark_point_dir_list[3] + '/1')]
    if len(data_point_3) == 0:
        print('benchmark point  ' + str(benchmark_point_name_list[3]) + ' of measure point  ' + str(point_no) + ' not find in awk data')
    
    data_point_4 = data_assemble[data_assemble['measure_point_no'] == benchmark_point_name_list[4]]
    data_point_4 = get_direction_match_data(data_point_4, benchmark_point_dir_list[4])
    #data_point_4 = data_point_4[(data_point_4['direction'].astype(str) == benchmark_point_dir_list[4]) | (data_point_4['direction'].astype(str) == benchmark_point_dir_list[4] + '/1')]
    if len(data_point_4) == 0:
        print('benchmark point  ' + str(benchmark_point_name_list[4]) + ' of measure point  ' + str(point_no) + ' not find in awk data')    
    
    data_point_5 = data_assemble[data_assemble['measure_point_no'] == benchmark_point_name_list[5]]
    data_point_5 = get_direction_match_data(data_point_5, benchmark_point_dir_list[5])
    #data_point_5 = data_point_5[(data_point_5['direction'].astype(str) == benchmark_point_dir_list[5]) | (data_point_5['direction'].astype(str) == benchmark_point_dir_list[5] + '/1')]
    if len(data_point_5) == 0:
        print('benchmark point  ' + str(benchmark_point_name_list[5]) + ' of measure point  ' + str(point_no) + ' not find in awk data')
    
    
    data_point_0.to_csv('data_point_0.csv', index = False)
    data_point_1.to_csv('data_point_1.csv', index = False)
    data_point_2.to_csv('data_point_2.csv', index = False)
    data_point_3.to_csv('data_point_3.csv', index = False)
    data_point_4.to_csv('data_point_4.csv', index = False)
    data_point_5.to_csv('data_point_5.csv', index = False)
    data_point_awk.to_csv('data_point_awk.csv', index = False)
    
    
    time_list = list(data_point_awk['time'])
    carno_list = list(data_point_awk['car_no'])
    res = pd.DataFrame(columns = data_point_awk.columns)
    
    for index in range(len(time_list)):
        time = time_list[index]
        car_no = carno_list[index]
        
        variable_known = []
        get_vars_known_according_time_carno(data_point_0, time, car_no, benchmark_point_dir_list[0])
        get_vars_known_according_time_carno(data_point_1, time, car_no, benchmark_point_dir_list[1])
        get_vars_known_according_time_carno(data_point_2, time, car_no, benchmark_point_dir_list[2])
        get_vars_known_according_time_carno(data_point_3, time, car_no, benchmark_point_dir_list[3])
        get_vars_known_according_time_carno(data_point_4, time, car_no, benchmark_point_dir_list[4])
        get_vars_known_according_time_carno(data_point_5, time, car_no, benchmark_point_dir_list[5])
        
        if len(variable_known) == 24:
            
            x0 = [0, 0, 0, 0, 0, 0]
            alpha, beta, gamma, tx, ty, tz = fsolve(func = f, x0 = x0)
            
            a = sy.Matrix([[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]])
            b = sy.Matrix([[cos(gamma), -sin(gamma), 0, 0], [sin(gamma), cos(gamma), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
            c = sy.Matrix([[cos(beta), 0, sin(beta), 0], [0, 1, 0, 0], [-sin(beta), 0, cos(beta), 0], [0, 0, 0, 1]])
            d = sy.Matrix([[1, 0, 0, 0], [0, cos(alpha), -sin(alpha), 0], [0, sin(alpha), cos(alpha), 0], [0, 0, 0, 1]])
            m = a * b * c * d
            
            temp_data = data_point_awk.iloc[index].copy()
            x = temp_data['x_value']
            y = temp_data['y_value']
            z = temp_data['z_value']
            res_matrix = m * sy.Matrix([[x], [y], [z], [1]])
            x_ = res_matrix[0]
            y_ = res_matrix[1]
            z_ = res_matrix[2]
            temp_data['x_value'] = x_
            temp_data['y_value'] = y_
            temp_data['z_value'] = z_
            
            res = res.append(temp_data, ignore_index = True)
        
        elif len(variable_known) > 24:
            print('size of variable_known is abnormal, maybe forget to clear global variables.')
        else:
            print('Not enough known variables. variable_known length: ' + str(len(variable_known)))
    
    direction_dic = {'X': 'x_value', 'Y': 'y_value', 'Z': 'z_value', 'dx': 'x_value', 'dX': 'x_value', 'dY': 'y_value', 'dz': 'z_value'}
    assemble_point = str(assemble_no) + '-' + str(point_no)
    if (assemble_point) in dev_correction.keys():
        res[direction_dic[direction_name]] += dev_correction[assemble_point]
        print('error correction finished.')
    
    deviation = []
    x_value = list(res['x_value'])
    x_standard = list(res['x_standard'])
    y_value = list(res['y_value'])
    y_standard = list(res['y_standard'])
    z_value = list(res['z_value'])
    z_standard = list(res['z_standard'])
    direction = list(res['direction'])
    stage = list(res['stage'])
    touch_direction_dic = get_touch_direction()
    
    if direction_name == 'X':
        for i in range(len(res)):
            deviation.append(x_value[i] - x_standard[i])
        res['deviation'] = deviation
    
    elif direction_name == 'Y': 
        for i in range(len(res)):
            deviation.append(y_value[i] - y_standard[i])
        res['deviation'] = deviation
    
    elif direction_name == 'Z': 
        for i in range(len(res)):
            deviation.append(z_value[i] - z_standard[i])
        res['deviation'] = deviation
        
    elif direction_name == 'A' or direction_name == 'B':
        print('direction == A | B')
        for i in range(len(res)):
            point_id = str(assemble_no) + '-' + stage[i] + '-' + str(point_no) 
            v = sqrt((x_value[i] - x_standard[i])**2 + (y_value[i] - y_standard[i])**2 + (z_value[i] - z_standard[i])**2)
            
            if direction[i] == 'X/1' and (point_id in touch_direction_dic.keys() and touch_direction_dic[point_id] == ' +X'):
                if x_value[i] - x_standard[i] > 0:
                    print('direction name = A | B')
                    v = -v
            elif direction[i] == 'X/1' and (point_id in touch_direction_dic.keys() and touch_direction_dic[point_id] == ' -X'):
                if x_value[i] - x_standard[i] < 0:
                    print('direction name = A | B')
                    v = -v
            elif direction[i] == 'Y/1' and (point_id in touch_direction_dic.keys() and touch_direction_dic[point_id] == ' +Y'):
                if y_value[i] - y_standard[i] > 0:
                    print('direction name = A | B')
                    v = -v
            elif direction[i] == 'Y/1' and (point_id in touch_direction_dic.keys() and touch_direction_dic[point_id] == ' -Y'):
                if y_value[i] - y_standard[i] < 0:
                    print('direction name = A | B')
                    v = -v
            elif direction[i] == 'Z/1' and (point_id in touch_direction_dic.keys() and touch_direction_dic[point_id] == ' +Z'):
                if z_value[i] - z_standard[i] > 0:
                    print('direction name = A | B')
                    v = -v
            elif direction[i] == 'Z/1' and (point_id in touch_direction_dic.keys() and touch_direction_dic[point_id] == ' -Z'):
                if z_value[i] - z_standard[i] < 0:
                    print('direction name = A | B')
                    v = -v
            deviation.append(v)
        res['deviation'] = deviation
    
    return res
    
    


def transform_yes_singlepoint_no(data, assemble_no, point_a, point_b, benchmark_point_name_list, benchmark_point_dir_list, direction_name, dev_correction):
    
    data_point_a = transform_yes_singlepoint_yes(data, assemble_no, point_a, benchmark_point_name_list, benchmark_point_dir_list, direction_name, dev_correction)
    data_point_b = transform_yes_singlepoint_yes(data, assemble_no, point_b, benchmark_point_name_list, benchmark_point_dir_list, direction_name, dev_correction)
    
    data_point_a = get_direction_match_data(data_point_a, direction_name)
    data_point_b = get_direction_match_data(data_point_b, direction_name)
    
    res = get_point_difference(data_point_a, data_point_b)
    
    return res



def point_name_split(name):
    name = name.replace('\n', '')
    name = name.replace(' ', '')
    res = name.split('-')
    name_a = res[0]
    name_b = res[1]
    
    return name_a, name_b



def dataformat_transform(data):
    
    data['deviation'] = data['deviation'].astype(float)
    data['x_value'] = data['x_value'].astype(float)
    data['y_value'] = data['y_value'].astype(float)
    data['z_value'] = data['z_value'].astype(float)
    data['x_standard'] = data['x_standard'].astype(float)
    data['y_standard'] = data['y_standard'].astype(float)
    data['z_standard'] = data['z_standard'].astype(float)
    
    return data
    



def get_benchmark_point_info():
    benchmark_point_dir_list = []
    benchmark_point_name_list = []
    
    for dire in str(benckmark_point_dir_1[index]).split('/'):
        if dire != 'nan':
            benchmark_point_dir_list.append(dire)
            benchmark_point_name_list.append(benchmark_point_name_1[index])

    for dire in str(benckmark_point_dir_2[index]).split('/'):
        if dire != 'nan':
            benchmark_point_dir_list.append(dire)
            benchmark_point_name_list.append(benchmark_point_name_2[index])

    for dire in str(benckmark_point_dir_3[index]).split('/'):
        if dire != 'nan':
            benchmark_point_dir_list.append(dire)
            benchmark_point_name_list.append(benchmark_point_name_3[index])

    for dire in str(benckmark_point_dir_4[index]).split('/'):
        if dire != 'nan':
            benchmark_point_dir_list.append(dire)
            benchmark_point_name_list.append(benchmark_point_name_4[index])

    for dire in str(benckmark_point_dir_5[index]).split('/'):
        if dire != 'nan':
            benchmark_point_dir_list.append(dire)
            benchmark_point_name_list.append(benchmark_point_name_5[index])

    for dire in str(benckmark_point_dir_6[index]).split('/'):
        if dire != 'nan':
            benchmark_point_dir_list.append(dire)
            benchmark_point_name_list.append(benchmark_point_name_6[index])
            
    return benchmark_point_dir_list, benchmark_point_name_list;



def dataformat(data):
    dimensional_chain_list = list(data["dimensional_chain"])
    for i in range(len(dimensional_chain_list)):
        dimensional_chain_list[i] = dimensional_chain_list[i].replace("\n","")
        dimensional_chain_list[i] = dimensional_chain_list[i].replace("\r","")
        dimensional_chain_list[i] = dimensional_chain_list[i].replace("?","")
    data["dimensional_chain"] = dimensional_chain_list
    
    for dimensional_chain in data.groupby(["dimensional_chain"]):
        dimensional_chain_name = dimensional_chain[0]
        dimensional_chain_data = dimensional_chain[1]
        
        dimensional_chain_folder_path = config['result_path'] + dimensional_chain_name
        
        if not os.path.exists(dimensional_chain_folder_path):
            os.makedirs(dimensional_chain_folder_path)
        
        for measure_point in dimensional_chain_data.groupby(['measure_point_no']):
            measure_point_name = measure_point[0]
            measure_point_data = measure_point[1]
            measure_point_folder_path = dimensional_chain_folder_path + os.path.sep + measure_point_name + '.csv'
            measure_point_data.to_csv(measure_point_folder_path, index = False)
    
    

def get_dev_correction(path):
    
    dev_corr_data = pd.read_csv(path)
    dev_correction = {}
    for i in range(len(dev_corr_data)):
        key = dev_corr_data.iloc[i]['measure_point_no']
        value = dev_corr_data.iloc[i]['offset']
        dev_correction[key] = value
        
    return dev_correction



if __name__ == '__main__':
    
    starttime = time.time()
    frecord = open('running records.txt', 'w')
    
    fjson = open('config.json')
    config = json.loads(fjson.read())
    
    direction_global = []
    variable_known = []
    
    fmk_dic_path = config['fmk_dic_path']
    awk_data_path = config['awk_data_path']
    
    fmk_dic = pd.read_csv(fmk_dic_path, encoding = 'ANSI')
    
    dev_correction = get_dev_correction(config['dev_correction'])
    
    data_awk = pd.read_csv(awk_data_path, dtype = str)
    #data_awk = direction_transform(data_awk)
    data_awk = dataformat_transform(data_awk)
    
    data_awk['time'] = data_awk['measure_time_date'] + '-' + data_awk['measure_time_time']
    data_awk['dimensional_chain'] = ''
    
    data_fmk = pd.DataFrame(columns = data_awk.columns)
    
    transform_flag = list(fmk_dic['need_transform'])
    single_measure_point = list(fmk_dic['single_point'])
    measure_point_no = list(fmk_dic['measure_point_no'])
    assemble_no = list(fmk_dic['assembly_no'])
    direction = list(fmk_dic['direction'])
    direction_exec = list(fmk_dic['direction_exec'])
    benchmark_point_name_1 = list(fmk_dic['benchmark_point_1'])
    benchmark_point_name_2 = list(fmk_dic['benchmark_point_2'])
    benchmark_point_name_3 = list(fmk_dic['benchmark_point_3'])
    benchmark_point_name_4 = list(fmk_dic['benchmark_point_4'])
    benchmark_point_name_5 = list(fmk_dic['benchmark_point_5'])
    benchmark_point_name_6 = list(fmk_dic['benchmark_point_6'])
    benckmark_point_dir_1 = list(fmk_dic['benchmark_point_1_direction'])
    benckmark_point_dir_2 = list(fmk_dic['benchmark_point_2_direction'])
    benckmark_point_dir_3 = list(fmk_dic['benchmark_point_3_direction'])
    benckmark_point_dir_4 = list(fmk_dic['benchmark_point_4_direction'])
    benckmark_point_dir_5 = list(fmk_dic['benchmark_point_5_direction'])
    benckmark_point_dir_6 = list(fmk_dic['benchmark_point_6_direction'])
    dimensional_chain = list(fmk_dic['dimensional_chain_name'])
    
    for index in range(len(fmk_dic)):
        
        assemble_name = assemble_no[index]
        point_name = measure_point_no[index]
        direction_name = direction[index]
        direction_exec_name = direction_exec[index]
        dimensional_chain_name = dimensional_chain[index]
        if transform_flag[index] == 0:
            if single_measure_point[index] == 0:
                point_name_a, point_name_b = point_name_split(point_name)
                res = transform_no_singlepoint_no(data_awk, assemble_name, point_name_a, point_name_b, direction_name)
                res['direction'] = direction_exec_name
                res['dimensional_chain'] = dimensional_chain_name
                data_fmk = data_fmk.append(res, ignore_index = True)
            
            elif single_measure_point[index] == 1:                
                res = transform_no_singlepoint_yes(data_awk, assemble_name, point_name, direction_name)
                res['direction'] = direction_exec_name
                res['dimensional_chain'] = dimensional_chain_name
                data_fmk = data_fmk.append(res, ignore_index = True)
                
        elif transform_flag[index] == 1:
            benchmark_point_dir_list, benchmark_point_name_list = get_benchmark_point_info()
            direction_global = benchmark_point_dir_list
            
            if single_measure_point[index] == 0:
                point_name_a, point_name_b = point_name_split(point_name)
                res = transform_yes_singlepoint_no(data_awk, assemble_name, point_name_a, point_name_b, benchmark_point_name_list, benchmark_point_dir_list, direction_name, dev_correction)
                res['direction'] = direction_exec_name
                res['dimensional_chain'] = dimensional_chain_name
                data_fmk = data_fmk.append(res, ignore_index = True)
            
            elif single_measure_point[index] == 1:
                res = transform_yes_singlepoint_yes(data_awk, assemble_name, point_name, benchmark_point_name_list, benchmark_point_dir_list, direction_name, dev_correction)
                res['direction'] = direction_exec_name
                res['dimensional_chain'] = dimensional_chain_name
                data_fmk = data_fmk.append(res, ignore_index = True)
        
        print('current progress:' + str(index + 1) + '/' + str(len(fmk_dic)))
        frecord.write('current progress:' + str(index + 1) + '/' + str(len(fmk_dic)) + '\n')
        frecord.flush()    
    
    result_path = config['result_path']
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    
    dataformat(data_fmk)
    data_fmk.to_csv(result_path + 'fmk.csv', index = False)
    
    fjson.close()
    
    endtime = time.time()
    frecord.write('finished. use time(s):' + str(endtime - starttime) + '\n')
    print('finished. use time(s):' + str(endtime - starttime))
    frecord.close()
    
    
    
    
    
    
    
