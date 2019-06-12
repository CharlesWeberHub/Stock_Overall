# encoding:utf-8

import datetime
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
from hmmlearn.hmm import GaussianHMM

import Strategy_Engine
import Translator

file = open('intraday_1min_0700.HKG.csv', 'r')
DATA_LENGTH=500



timestamp = list()
open = list()
high = list()
low = list()
close = []
volume = list()
sign_list=[0,0,0,0]  #初始的四个数据点不会产生购买信号


weight_list=[0.05,0.15,0.1,0.2,0.5]

for c in file.readlines():
    c = c.strip('\n')
    c_array = c.split(",")
    timestamp.append(c_array[0])
    open.append(c_array[1])
    high.append(c_array[2])
    low.append(c_array[3])
    close.append(c_array[4])
    volume.append(c_array[5])

timestamp = timestamp[1:]
open = open[1:]
high = high[1:]
low = low[1:]
close = close[1:]
volume = volume[1:]

open = [float(i) for i in open]
high = [float(i) for i in high]
low = [float(i) for i in low]
close = [float(i) for i in close]
volume = [float(i) for i in volume]

# 翻转数组
def getTheReverseArray(list_1):
    N = len(list_1)
    for i in range(int(len(list_1) / 2)):
        list_1[i], list_1[N - i - 1] = list_1[N - i - 1], list_1[i]
    return list_1


close = getTheReverseArray(close)
timestamp = getTheReverseArray(timestamp)
volume = getTheReverseArray(volume)


diff = np.diff(close)

# 得到最终长度的测试数据
timestamp = timestamp[1:1+DATA_LENGTH]
close = close[1:1+DATA_LENGTH]
volume = volume[1:1+DATA_LENGTH]

for index in range(len(close)):

    if index<=len(close)-5:
        cut_close=close[index:index+5]
        sign_list.append(Strategy_Engine.tendency_monitor(cut_close, weight_list))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot_date(timestamp, close, '-')

#将操作信号转成单一切换的信号
act_sign_list=Translator.position_state_translate(sign_list)

#将操作信号变换指示颜色
indicate_list=Translator.color_translate(act_sign_list)

ax.scatter(timestamp,close,c = indicate_list,marker = 'o')

#print('state_list_len:'+str(state_list))

#画操作信号散点图



plt.title('HSBC 0005.hk  '+str(DATA_LENGTH)+ 'minutes data')
plt.show()


print('finish()')
