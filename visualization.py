# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 19:43:34 2019

@author: calpi
"""

#seabornが日本語に対応するように設定する。
import matplotlib as mpl
import matplotlib.pyplot as plt
#可視化をしてみる。
import seaborn as sns
#とりあえず一時しのぎで設定してみる


#ヒストグラム
sns.distplot(train['y'])
#散布図
sns.jointplot('temperature','y',data=train)

#カテゴリごとにデータを見る。
sns.stripplot('week','y',data=train)
plt.show()

train.columns
