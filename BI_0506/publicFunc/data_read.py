# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 10:11:53 2020

@author: jasonlin3
"""

import os
import pandas as pd
import sqlite3
from colorama import Fore ,Style
 

###########################################
#
#   Sqlite configuration
#
###########################################
def highpowerBI_table_create():
    conn = sqlite3.connect('D:/BI/BIttt.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS test (
          date time ,
          D1p float,
          ppp int
            );
    ''')

def test_dict_get(root_dir):
    
    files= os.listdir(root_dir) #得到資料夾下的所有檔名稱
    pre_test_list = []
    
    for file in files:
        if not file.startswith('.'):
            test_id= '_'.join(file.split('_')[2:])
            if test_id not in pre_test_list:
                pre_test_list.append(test_id)       
            else:
                pass
    
    
    test_list = []
    all_test_file = []
    for test_id in pre_test_list:
        test_id_file = ['noFile', 'noFile','noFile']
        for file in files:
            if test_id in file:
                if 'ATC_BIBLog' in file:
                    test_id_file[1] = file
                elif 'ATC_OVENLog' in file:
                    test_id_file[2] = file
                else:
                    test_id_file[0] = file
        if 'noFile' in test_id_file:
            print(f'{Fore.RED} {test_id} {Style.RESET_ALL} is short of file \n')
        else:
            test_list.append(test_id)
            all_test_file.append(test_id_file)
        
        
    return test_list, dict(zip(test_list, all_test_file))   

def multi_log2csv(root_dir, fm_version=None, test_mod='full-control',fan_motor=True, is_to_db=False):
    '''
    

    Parameters
    ----------
    root_dir : string
        test file dir
    fm_version : string, optional
        DESCRIPTION. The default is None.
    test_mod : string, optional
        DESCRIPTION. [ 'full-control','dissipation-capability', 'other' ] \n
        The default is 'full-control'. 
    is_to_db : bool, optional
        DESCRIPTION. if data will go to DB  \n
        The default is False.

    Returns
    -------
    None.

    '''
   
    test_list, test_dict = test_dict_get(root_dir) 
    
    for test_id in test_list: #遍歷資料夾   
        BIB_log = []
        OVEN_log=[]
        log=[]
        datas = []
        for i, file in enumerate(test_dict[test_id]):
            f = open(root_dir + file, encoding="ISO-8859-1"); #開啟檔案   
            if i ==0:
                datas =log
            elif i==1:
                datas = BIB_log
            else:
                datas =OVEN_log
                    
            for line in f:
                data = line.split(' ') 
                datas.append(data)
       
                
        df_log = pd.DataFrame(log)[[0,1,2,10,15,18,24,28,34,38,44,48,56,61,64,70,74,80,84,90,94,102,107,110,116,120,126,130,136,140,148,153,156,162,166,172,176,182,186]]
        df_BIB_log =pd.DataFrame(BIB_log)[[10,14,18,22,26,30,34,38,42]]
        df_OVEN_log=pd.DataFrame(OVEN_log)[[10,14,18,22,26,30,34]]
        
      
#0 1 2 time 
#dut1  power: 10  T1: 15  T2:  18  H1PWM:24  H2PWM:28   F1PWM: 34  F2PWM  38   F!RPM: 44   F2RPM:  48
#dut2  power: 56  T1: 61  T2:  64  H1PWM:70  H2PWM:74   F1PWM: 80  F2PWM: 84   F1RPM: 90   F2RPM:  94
#dut3  power: 102 T1: 107 T2: 110  H1PWM:116 H2PWM:120  F1PWM: 126 F2PWM: 130  F1RPM: 136  F2RPM: 140
#dut4  power: 148 T1:153  T2: 156  H1PWM:162 H2PWM:166  F1PWM: 172 F2PWM: 176  F1RPM: 182  F2RPM: 186     
#        
#BIB   T1:10  T2:14  T3:18  T4:22  T5:26   T6:30  T7:34  T8:38  T9:42
#oven  kg:10  T1:14  T2:18  T3:22  T4:26   T5:30  T6:34 
                
        df_log.columns= ['date', 'MN', 'time',\
                          'D1p', 'D1T1', 'D1T2','D1H1PWM', 'D1H2PWM','D1F1PWM','D1F2PWM','D1F1RPM','D1F2RPM',\
                          'D2p', 'D2T1', 'D2T2','D2H1PWM', 'D2H2PWM','D2F1PWM','D2F2PWM','D2F1RPM','D2F2RPM',\
                          'D3p', 'D3T1', 'D3T2','D3H1PWM', 'D3H2PWM','D3F1PWM','D3F2PWM','D3F1RPM','D3F2RPM',\
                          'D4p', 'D4T1', 'D4T2','D4H1PWM', 'D4H2PWM','D4F1PWM','D4F2PWM','D4F1RPM','D4F2RPM']
        df_BIB_log.columns =['BIB1','BIB2','BIB3','BIB4','BIB5','BIB6','BIB7','BIB8','BIB9']
        df_OVEN_log.columns=['oven_pre','OVEN1','OVEN2','OVEN3','OVEN4','OVEN5','OVEN6']
        concat_df = pd.concat([df_log, df_BIB_log,df_OVEN_log], axis = 1)
        concat_df['date_time'] = concat_df.apply(lambda x: convert_to_datetime(x['date'],x['MN'],x['time']), axis=1)
        concat_df  = concat_df.drop(columns = ['date','MN','time'])
        concat_df['fw_version']=fm_version
        concat_df['test_id'] = test_id
        concat_df['test_mod'] = test_mod
        concat_df['fan_motor'] = fan_motor
        
        type_convert_col = ['D1p', 'D1T1', 'D1T2','D1H1PWM', 'D1H2PWM','D1F1PWM','D1F2PWM','D1F1RPM','D1F2RPM',\
                          'D2p', 'D2T1', 'D2T2','D2H1PWM', 'D2H2PWM','D2F1PWM','D2F2PWM','D2F1RPM','D2F2RPM',\
                          'D3p', 'D3T1', 'D3T2','D3H1PWM', 'D3H2PWM','D3F1PWM','D3F2PWM','D3F1RPM','D3F2RPM',\
                          'D4p', 'D4T1', 'D4T2','D4H1PWM', 'D4H2PWM','D4F1PWM','D4F2PWM','D4F1RPM','D4F2RPM',\
                              'BIB1','BIB2','BIB3','BIB4','BIB5','BIB6','BIB7','BIB8','BIB9',\
                                  'oven_pre','OVEN1','OVEN2','OVEN3','OVEN4','OVEN5','OVEN6']
              
        concat_df[type_convert_col] = concat_df[type_convert_col].astype(float)

        duts_power_on = detect_power_on(concat_df) 
        if duts_power_on:
            concat_df = data_trim(concat_df, duts_power_on)
        
        concat_df = cal_power(concat_df, duts_power_on)  
        
        
##############################################

        

        # concat_df['D3F2PWM_shift'] = concat_df['D3F2PWM'].shift(periods = 1, fill_value = 0)
        # concat_df['mark'] = concat_df.apply(lambda x: section_detect(x['D3F2PWM'],x['D3F2PWM_shift']), axis = 1)
        # start_mark = list(concat_df[concat_df.mark == True].index)
        # end_mark = list(concat_df[concat_df.mark == False].index)
        
        # section_mark_pair = {}
        # for i, (start, end) in enumerate(zip(start_mark, end_mark)):
        #     section_mark_pair.update( {i : [start+5, end-1]} )
        
        # condition = [(True, 7),(False, 7),(False, 7),(False, 7),
        #               (False, 6),(True, 6),(True, 5),(True, 5),
        #               (True, 5),(True, 4),(True, 3),(True, 3),
        #               (True, 3),(True, 2),(True, 1),(True, 1),
        #               (True, 1),(True, 0),]
        
        # df_list = []
        # for i in section_mark_pair.keys():
        #     trim_data = concat_df.iloc[section_mark_pair[i][0]:section_mark_pair[i][1], :]
        #     trim_data['fan_motor'] = condition[i][0]
        #     trim_data['oven_pre'] = condition[i][1]
        #     trim_data = trim_data.drop(columns = ['D3F2PWM_shift', 'mark'])
        #     df_list.append(trim_data)
                  
        # concat_df = pd.concat(df_list, axis = 0)
        # concat_df['D3F2RPM'] = concat_df['D3F2RPM'].apply(lambda x: x/1000.)
    
    
##############################################            
    
        # concat_df.to_csv(test_id+'.csv', encoding ='utf-8', index=False)
        # print(test_id + '.csv output is done')
        
        if is_to_db  == True:
            conn = sqlite3.connect('BI.db')
            concat_df.to_sql('experiment', conn, if_exists='append', index=False)
            print(f'{Fore.GREEN}{test_id}{Style.RESET_ALL} to highpowerBI_db is done \n')
        else:
            conn = sqlite3.connect('Trial.db')
            concat_df.to_sql('trial', conn, if_exists='append', index=False)
            print(test_id + ' to trial_db is done \n')


def section_detect(cell_1, cell_2):
    if cell_1 != 0 and cell_2 == 0:
        return True
    elif cell_1 == 0 and cell_2 != 0:
        return False
    else:
        return None

def detect_power_on(concat_df):
    power_list = ['D1p','D2p','D3p','D4p']
    duts_power_on = []
    for i in power_list:
        single_dut_power = concat_df[i].mean()
        if single_dut_power != 0.:
            duts_power_on.append(i)
    print('power on : ', duts_power_on)
    return duts_power_on 

    
def data_trim(concat_df, duts_power_on):

    dut_power_off_index = []
    dut_power_on_index = []
    for i in duts_power_on:
        dut_power_off_index.append(concat_df[concat_df[i] != 0].index[-10])
        dut_power_on_index.append(concat_df[concat_df[i] != 0].index[1])
    
    index_end = min(dut_power_off_index)
    index_start = max(dut_power_on_index)
    return concat_df.iloc[index_start:index_end,:]

def cal_power(concat_df, duts_power_on):    
    sum_dut_power = 0.
    for i in duts_power_on:
        single_dut_power = concat_df[i].mean()
        sum_dut_power = sum_dut_power + single_dut_power

    concat_df['power'] = int(sum_dut_power / (len(duts_power_on)+ 1.234e-56)) 
    return  concat_df   

import datetime
def convert_to_datetime(date,MN,time):
    if MN=='¤W¤È':
        return datetime.datetime.strptime(date+' '+time,'%Y/%m/%d %H:%M:%S')
    elif MN=='¤U¤È':
        time_lst = time.split(':')
        hour_val  = time_lst[0]
        if hour_val=='12':
            return datetime.datetime.strptime(date+' '+time,'%Y/%m/%d %H:%M:%S')
        else:
            time_lst[0] = str(int(hour_val)+12)
            time = ':'.join(time_lst)
            return datetime.datetime.strptime(date+' '+time,'%Y/%m/%d %H:%M:%S')
        
def describe_stats(df):
    test_id_list = df['test_id'].unique()
    for test_id in test_id_list:
        print(test_id)
        print('\n')     
        describe = df[df.test_id == test_id][['D1T1','D2T1','D3T1','D4T1']].describe().transpose()
        describe['diff'] = describe.apply(lambda x: x['max'] - x['min'], axis =1)
        print (describe)
        print('\n')
        
def test_profile_get(df):
    test_id_list = pd.unique(df['test_id'])
    test_profile = {}
    for test_id in test_id_list:
        test = df[df.test_id == test_id]
        oven_pre = pd.unique(test['oven_pre'])
        power = pd.unique(test['power'])
        fan_motor = pd.unique(test['fan_motor'])
        fw_version = pd.unique(test['fw_version'])
        test_mod = pd.unique(test['test_mod'])
        profile = {test_id:[oven_pre,power,fan_motor,fw_version,test_mod]}
        test_profile.update(profile)
    test_profile = pd.DataFrame.from_dict(test_profile, orient = 'index')
    test_profile.columns = ['oven pressure', 'power', 'fan_motor','fw_version', 'test_mod']
    return test_profile