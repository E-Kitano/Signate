# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 19:43:34 2019

@author: calpi
"""


#可視化をしてみる。
import seaborn as sns
import matplotlib.pyplot as plt
import os
os.chdir("C:\\Users\\KUSER2\\Documents\\@kitano\\業務外\\勉強\\Lunchbox\\chart\\y")
import datetime

#yについて探索
os.chdir("C:\\Users\\KUSER2\\Documents\\@kitano\\業務外\\勉強\\Lunchbox\\chart\\y")
sns.set()
plt.hist(train['y'])
plt.title("yのヒストグラム")
plt.savefig("yのヒストグラム")

datetime.datetime.strptime(train['datetime'],'%y%m%d')

plt.plot(train['datetime'],train['y'])
plt.title("yの時系列")
plt.xlabel("datetime")
plt.ylabel("売上")
plt.savefig("yの時系列")

train.dtypes
datetime_train['datetime']
train.head()
#散布図
#sns.jointplot('temperature','y',data=train)

#カテゴリごとにデータを見る。
#sns.stripplot('week','y',data=train)
#plt.show()

