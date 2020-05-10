# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 13:57:28 2020

@author: jasonlin3
"""
import seaborn as sns
import matplotlib.pyplot as plt
from publicFunc import sns_para_set as ss
import pandas as pd
###########################################
#
#   繪圖Function
#
###########################################
  
def classic_boxplot(file_name, data):
    data= pd.melt(data, 
                  id_vars=data.columns[0], 
                  value_vars=list(data.columns[1:]),
                  var_name='group', 
                  value_name='value'
                  )
    ss.Seaborn_Style()
    fig = plt.figure(figsize=(10,6), dpi = 80, facecolor = 'white') 
    ax = fig.add_subplot(111)
    ss.boxplot_Figure_Style()
    ss.boxplot_Axis_Style(ax)
    sns.boxplot(x='group', y='value', data = data , hue=data.columns[0])
    
    # sns.violinplot(x="group", y="value", data=data,hue=data.columns[0])
    fig.savefig('figure/boxplot_' + file_name +'.png')
    plt.show()
    
def classic_distplot(test_id, file_name, data):
    ss.Seaborn_Style()
    fig = plt.figure(figsize=(6,4), dpi = 80, facecolor = 'white') 
    ax = fig.add_subplot(111)
    ss.distplot_Figure_Style()
    ss.distplot_Axis_Style(ax)
    for item in data.columns:       
        sns.distplot(a = data[item], hist=False, label = item)
    
   
    plt.title(test_id, fontsize=12)
    # plt.legend(loc='upper right')    
    fig.savefig('figure/' + test_id +'distplot_' + file_name  + ".png")     
    plt.show()    
def classic_lineplot(test_id,file_name, data):
    data= pd.melt(data,
        id_vars = [data.columns[0]],
        value_vars= data.columns[1:],
        var_name='group',
        value_name = 'value'
        )
    ss.Seaborn_Style()
    fig = plt.figure(figsize=(12,6), dpi = 80, facecolor = 'white') 
    ax = fig.add_subplot(111)
    ss.lineplot_Figure_Style()
    ss.lineplot_Axis_Style(ax)
    plt.title(test_id, fontsize=12)
    plt.xticks(rotation=45)
    sns.lineplot( x= data.columns[0] , y= 'value', hue = 'group', data= data)
    
    fig.savefig('figure/' + test_id +'lineplot_' + file_name + '_'+test_id+'.png') 
    
    
def classic_scatterplot(test_id, file_name, data):
    data= pd.melt(data,
        id_vars = [data.columns[0]],
        value_vars= data.columns[1:],
        var_name='group',
        value_name = 'value'
        )
    ss.Seaborn_Style()
    fig = plt.figure(figsize=(12,6), dpi = 80, facecolor = 'white') 
    ax = fig.add_subplot(111)
    ss.lineplot_Figure_Style()
    ss.lineplot_Axis_Style(ax)
    plt.title(test_id, fontsize=12)
    sns.scatterplot( x= data.columns[0] , y= 'value', hue = 'group', data= data)
    fig.savefig('figure/' + test_id +'lineplot_' + file_name + '_'+test_id+'.png') 
    

def classic_barplot(file_name, data):
    ss.Seaborn_Style()
    fig = plt.figure(figsize=(12,6), dpi = 80, facecolor = 'white') 
    data= pd.melt(data,
                id_vars = data.columns[0],
                value_vars= data.columns[1:],
                var_name='group',
                value_name = 'value'
                )
    sns.barplot(x="group", y="value", hue = data.columns[0], data=data) 
    fig.savefig('figure/barplot_heatPWM.png')


