# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 13:55:50 2020

@author: jasonlin3
"""
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
###########################################
#
#   繪圖參數設定
#
###########################################

def Seaborn_Style():
    style = ('white','dark','whitegrid','darkgrid','ticks')
    context = ('notebook','paper','talk','poster')
    palette = ('pastel','muted','dark','bright','colorblind','dark')
    sns.set_style(style[3])
    sns.set_context(context[0])
    sns.set_palette(palette[4])
#    sns.despine(offset=10, trim=True)
    sns.despine(offset=10)
    sns.despine(bottom=True)

def lineplot_Figure_Style():
    plt.tight_layout()
    plt.title('lineplot', fontsize=12)
#    plt.ylim(20.,120.)
    plt.yticks(fontsize=10)
    plt.xticks(fontsize=10)
    plt.yticks(np.arange(90,110, step=5))

def lineplot_Axis_Style(ax):
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=9)) 
    ax.yaxis.set_minor_locator(plt.MultipleLocator(1)) 
    #ax.xaxis.set_minor_locator(AutoMinorLocator()) 
    ax.xaxis.grid(True, which='major') #x坐标轴的网格使用主刻度
    ax.yaxis.grid(True, which='minor') #y坐标轴的网格使用次刻度
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
def boxplot_Figure_Style():
    plt.tight_layout()
    plt.title('boxplot', fontsize=12)
#    plt.ylim(103.,118.)
    plt.yticks(fontsize=10)
    plt.xticks(fontsize=10)
#    plt.yticks(np.arange(90,110, step=5))
    
def boxplot_Axis_Style(ax):
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=3)) 
    ax.yaxis.set_minor_locator(plt.MultipleLocator(1)) 
    #ax.xaxis.set_minor_locator(AutoMinorLocator()) 
    ax.xaxis.grid(True, which='major') #x坐标轴的网格使用主刻度
    ax.yaxis.grid(True, which='minor') #y坐标轴的网格使用次刻度
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    
def distplot_Figure_Style():
    plt.tight_layout()
    plt.title('kde distribution', fontsize=12)
#    plt.ylim(0.,3.)
    plt.yticks(fontsize=10)
    plt.xticks(fontsize=10)
    
#    plt.yticks(np.arange(90,110, step=5))
    
def distplot_Axis_Style(ax):
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=3)) 
    ax.yaxis.set_minor_locator(plt.MultipleLocator(1)) 
    #ax.xaxis.set_minor_locator(AutoMinorLocator()) 
    ax.xaxis.grid(True, which='major') #x坐标轴的网格使用主刻度
    ax.yaxis.grid(True, which='minor') #y坐标轴的网格使用次刻度
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')