# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 19:51:19 2019

@author: calpi
"""

#　お弁当の予測
# 前処理まとめ

# SIGNATE お弁当の需要予測

#　データ説明
# 目的変数はy:販売数
# datetime:日付
# week:曜日
# soldout:完売したかどうか(0:完売していない,1:完売)
# name:メインメニューの名前
# kcal:おかずのカロリー
# remarks:特記事項
# event:13時開始お弁当持ち込み可の社内イベント
# payday:1:給料日
# weather:天気
# pre..:降水量。ない場合は"-"
# temperature:気温

################################################
import os
os.chdir("C:\\Users\\KUSER2\\Documents\\@kitano\\業務外\\勉強\\Lunchbox")
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import sklearn
import re
#import pandas_profiling
#profile = train.profile_report()
#profile.to_file(output_file="output.html")

sns.set(font="IPAexGothic",style="white")

train = pd.read_csv("./data/train.csv")
test = pd.read_csv("./data/test.csv")
sample = pd.read_csv("./data/sample.csv",header=None)
print("Data Shapes")
print("Train:",train.shape, "Test:",test.shape, "Sample:",sample.shape)


###############################################


def generate_food(data,genre):
    # ジャンルのデータを読む
    file_name = "script/menu/" + genre + ".txt"
    open_file = open(file_name)
    read_file = open_file.read()
    open_file.close()
    # 読み込んだものを','で区切る
    food_genre_list = read_file.split(',')

    # food列にgenreを入れる        
    if genre == 'rice':
        for j in range(len(food_genre_list)):
            data.loc[data['name'].str.endswith(food_genre_list[j]),'food'] = genre
    else:
        for j in range(len(food_genre_list)):
            data.loc[data['name'].str.contains(food_genre_list[j]),'food'] = genre
    return(data)
    
##############################################

# 前処理の関数

# paydayに0を入れ、remarksに特記事項なしと入れる
# event、降水量、kcalを除く
# soldout、paydayに文字を入れる。
def pre(data):
    data_fillna = data.fillna({'payday': 0 , 'remarks': "特記事項なし"})
    data_removeColumns = data_fillna.drop(columns = {'event','precipitation','kcal'})
    data_removeColumns['soldout'] = data_removeColumns['soldout'].replace({0:'残った',1:'完売'})
    data_removeColumns['payday'] = data_removeColumns['payday'].replace({0:'なし',1:'給料日'})
    data = data_removeColumns
    
    data = generate_food(data,genre='meat')
    data = generate_food(data,genre='fish')
    data = generate_food(data,genre='rice')
    data.loc[data.isnull().any(axis=1),'food'] = 'その他'
    data = data.drop('name',axis=1)
    return data



train = pre(train)
train.tail(10)

#次、決定木でモデリング
#extra treesが良い精度出るらしい。


