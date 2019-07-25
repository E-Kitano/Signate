# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 19:43:34 2019

@author: calpi
"""

#seabornが日本語に対応するように設定する。
import matplotlib as mpl
print(mpl.matplotlib_fname())

#可視化をしてみる。
import seaborn as sns
#ヒストグラム
sns.distplot(train['y'])
#散布図
sns.jointplot('temperature','y',data=train)

#カテゴリごとにデータを見る。
sns.stripplot('week','y',data=train)


train.columns
