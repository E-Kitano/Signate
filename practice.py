# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 23:16:26 2019

@author: Eri
"""

# 練習
# SIGNATE お弁当の需要予測
import os
os.chdir("C:\\Users\\calpi\\OneDrive\\Documents\\kitano\\signate\\Lunchbox")
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import sklearn
import re
import pandas_profiling
profile = train.profile_report()
profile.to_file(output_file="output.html")
sns.set(font="IPAexGothic",style="white")

train = pd.read_csv("./data/train.csv")
test = pd.read_csv("./data/test.csv")
sample = pd.read_csv("./data/sample.csv",header=None)
print("Data Shapes")
print("Train:",train.shape, "Test:",test.shape, "Sample:",sample.shape)


sample
train.index = pd.to_datetime(train["datetime"])
train.head(50)
######################################

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

#　忠鉢さんのqiitaのマネ

# 売上がどうなってるのか確認
plt.plot(train['y'])
# データの概要把握
# 行,列
train.shape
# 訓練データとテストデータの基本統計量を把握
train.describe(include="all").T
test.describe(include="all").T
#view_stats(train)
train[0:30,:]
train["remarks"].values


########################################
# まずは自分たちで最低限の処理をしたものをやってみる。

# 前処理①　欠損値の数確認。
# 欠損地の数確認。
train.isnull().sum()
# 欠損地の割合
train.isnull().sum() / len(train)

#　関数づくりは挫折
#def null調べ(df):
#   for i in df.columns:
#       print(i)
#       print("null数:" + str(df[df.columns[i]].isnull().sum()))

# nameの確認
# 回数の確認。二回以上が25品目、一回が131品目。2回以上は約16%だけ。
menu = train[['y','name']].groupby('name').count()
# menuを行名に
menu['name'] = menu.index
menu.index = list(range(len(menu)))
#.sort_values(by='y',ascending=False)

# orとなっている部分を整理。2個だけかい。
#double = menu[menu['name'].str.contains('or')]
#double_db = pd.DataFrame({'y':[1,2,1],
#                         'name':pd.Categorical(["酢豚","カレー","鶏のレモンペッパー"])})
#menu_ap = menu.append(double_db)
#menu_best = menu_ap[~ menu_ap['name'].str.contains('or')]

# 辞書作り
# リストなら繰り返しできる。

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

train_pre = generate_food(data=train,genre="meat")
train_pre = generate_food(data=train_pre,genre="fish")
train_pre = generate_food(data=train_pre,genre="rice")

train_pre.head(10)
train_pre[['name','food']]

a = 'onaka'
if a == "onaka":
    print(a)

# それ以外はその他
train.loc[train.isnull().any(axis=1),"food"] = 'その他'

# foodの欠損値がいくらか
train.isnull().sum()
train[train.isnull().any(axis=1)]

# paydayに0を入れる
#train['payday'] = train['payday'].fillna(0)

# remarksの」処理。remarksがあるかないかで変わるか。
# どうやら「お楽しみメニュー」の人気が高い。
#train[['remarks','y']].groupby('remarks').count()
#train_remarks = train[train['remarks'].notnull()]
#train_Notremarks = train[train['remarks'].isnull()]
#train_Notremarks['y'].loc[150:207].mean()
#train_remarks['y'].mean()
#train_remarks[['y','remarks']]

# remarksに特記事項なしと入れる
#train['remarks'] = train['remarks'].fillna("特記事項なし") 

# eventの処理。
#train[['event','y']].groupby('event').count()
#train_event = train[train['event'].notnull()]
#train_Notevent = train[train['event'].isnull()]
#train_event.query('event == "ママの会"')
#train_event.query('event.str.contains("キャリア")',engine='python')
#train_Notevent['y']

# eventを除く
#train.drop(columns = 'event').head(10)

# weatherの処理
#train[['y','weather']].groupby('weather').mean()
# 薄曇りをくもりに
#data_removeColumns['weather'] = data_removeColumns['weather'].replace('薄曇','曇')

# kcal
#train[['y','name','kcal']].groupby(['name','kcal']).count()
#train[train['kcal'].isnull()]

###########################################
###########################################
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
    return data
    

train = pre(train)
train.tail(10)

############################################
############################################

# 可視化

# 売上がどうなってるのか確認
plt.plot(train['y'])
# ヒストグラムを描いてみる

