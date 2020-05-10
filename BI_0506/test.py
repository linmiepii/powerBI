#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 20:47:01 2020

@author: linmiepii
"""


import pandas as pd
from publicFunc import data_read as dr
from publicFunc import plot_function as pf
import sqlite3
import os
#dr.highpowerBI_table_create()
    
###########################################
#
#   data pre-processing
#
###########################################

import numpy as np

columns = list('abcde')
matrix = np.random.rand(5,5)

matrix = pd.DataFrame.from_dict(dict(zip(columns, matrix)))
c = list(matrix.columns)

count = 0

for i in c:
    count += 1
    print(count)
