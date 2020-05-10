#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 09:10:01 2020

@author: linmiepii
"""
import pandas as pd
from publicFunc import data_read as dr
from publicFunc import plot_function as pf
import sqlite3

#dr.highpowerBI_table_create()
    
###########################################
#
#   data pre-processing
#
###########################################

root_dir = 'preProcess/'
df = dr.multi_log2csv(root_dir, fm_version='v.03',test_mod='fan_pressure_test',fan_motor = True, is_to_db=False)  


# process_result = whole_range_df
# process_result['D3F2RPM'] = process_result['D3F2RPM'].apply(lambda x: x/1000.)
# process_result = process_result[['D3F2PWM','D3F2RPM','oven_pre', 'fan_motor']]

# X = process_result[process_result.fan_motor == True]
# Y = process_result[process_result.fan_motor == False]

# X = X.iloc[:,1].values
# Y = Y.iloc[:,1].values
# process_result = process_result.groupby('oven_pre').mean()
# process_result = process_result.reset_index()
# process_result.pivot(index='fan_motor', columns='oven_pre', values='D3F2RPM')


# import statsmodels.api as sm
# ttest_6kg = sm.stats.ttest_ind(X, Y)



###########################################
#
#   read from csv
#
###########################################

#root_dir = ''
#df_list = dr.multi_pd_read_csv(root_dir, power_index)  
#whole_range_df = pd.concat([df for df in df_list])
#whole_range_df = whole_range_df.reset_index(drop=True)

###########################################
#
#   read from sql
#
###########################################

conn = sqlite3.connect('Trial.db')
whole_range_df = pd.read_sql(sql='SELECT * FROM trial WHERE test_id LIKE "%2020_04_24%"', con = conn)
print(dr.test_profile_get(whole_range_df))
dr.describe_stats(whole_range_df)

# WHERE test_id LIKE "%2020_05_06%"
###########################################
#
#   Plot
#
###########################################

lineplot_scripts = {
    # 'dut_temp':['date_time','D1T1','D2T1','D3T1','D4T1'],
    # 'dut1_with_PWM':['date_time','D1T1','D1H1PWM','D1F1PWM','OVEN1'],
    # 'dut2_with_PWM':['date_time','D2T1','D2H1PWM','D2F1PWM','OVEN1'],
    # 'dut3_with_PWM':['date_time','D3T1','D3H1PWM','D3F1PWM','OVEN1'],
    # 'dut4_with_PWM':['date_time','D4T1','D4H1PWM','D4F1PWM','OVEN1'],
    # 'BIB_temp':['date_time','BIB1','BIB2','BIB3','BIB4','BIB5','BIB6','BIB7','BIB8','BIB9']

    # 'pressure_RPM':['oven_pre','D3F2RPM']
    }

distplot_scripts = {
    # 'dut_temp':['date_time','D1T1','D2T1','D3T1','D4T1'],
    # 'heater_PWM':['D1H1PWM','D2H1PWM','D3H1PWM','D4H1PWM'],
    # 'fan_PWM':['D1F1PWM','D2F1PWM','D3F1PWM','D4F1PWM']
    }

scatterplot_scripts = {
    # 'dut_temp':['date_time','D1T1','D2T1','D3T1','D4T1'],
    # 'pressure_RPM':['oven_pre', 'D3F2RPM','D3F2PWM'],
    # 'PWM_RPM':['D3F2PWM','oven_pre', 'D3F2RPM']
    } 

query_test = list(pd.unique(whole_range_df['test_id']))

grp_result_df_list = []
for test_id in query_test:
    ind_result = whole_range_df[whole_range_df.test_id == test_id]
    ind_result = ind_result.iloc[-250:, :]
    grp_result_df_list.append(ind_result)
    
grp_result = pd.concat(grp_result_df_list, axis = 0, ignore_index = True)

for test_id in query_test:
    ind_result = whole_range_df[whole_range_df.test_id == test_id]
    ind_result = ind_result.iloc[:, :][ind_result.index % 1 == 0]
    
    for key in lineplot_scripts.keys():
        drawing_data = ind_result[lineplot_scripts[key]]
        pf.classic_lineplot(test_id, key, drawing_data)
        
    for key in distplot_scripts.keys():
        drawing_data = ind_result[distplot_scripts[key]]
        pf.classic_distplot(test_id, key, drawing_data)
        
    for key in scatterplot_scripts.keys():
            drawing_data = ind_result[scatterplot_scripts[key]]
            pf.classic_scatterplot(test_id, key, drawing_data)
            
boxplot_scripts = {
    # 'dut_temp_power':['power','D1T1','D2T1','D3T1','D4T1'],
    # 'dut_temp_firmware':['fw_version','D1T1','D2T1','D3T1','D4T1'],
    # 'dut_temp_pressure':['oven_pre','D1T1','D2T1','D3T1','D4T1'],
    
    # 'X_RPM_fanMotor':['fan_motor','D3F2RPM'],
    # 'X_RPM_pressure':['oven_pre','D3F2RPM']
    }   

barplot_scripts = {
    # 'duts_pwm_power':['power','D1H1PWM','D2H1PWM','D3H1PWM','D4H1PWM'],
    # 'duts_pwm_pressure':['oven_pre','D1H1PWM','D2H1PWM','D3H1PWM','D4H1PWM']
    }

for key in boxplot_scripts.keys():
    drawing_data = grp_result[boxplot_scripts[key]]
    pf.classic_boxplot(key, drawing_data)
    
for key in barplot_scripts.keys():
    drawing_data = grp_result[barplot_scripts[key]]
    drawing_data = drawing_data.groupby(drawing_data.columns[0]).mean()
    drawing_data = drawing_data.reset_index()
    pf.classic_barplot(key, drawing_data)

           




