from statsmodels.stats.weightstats import DescrStatsW
import numpy as np


#0是保持不变，1是买进，2是卖出
STATE=[0,1,2]


#返回股票交易动作状态
def tendency_monitor(close_price_list,weight_list):
    #计算五个时间点的加权标准差，计算分钟间的增长率（斜率）
    weighted_stats = DescrStatsW(close_price_list, weights=weight_list)
    weighted_stats.mean  # 加权平均
    weighted_std=weighted_stats.std  # 加权标准差

    std = np.std(close_price_list, ddof=1)

    # if(weighted_std>0.2):
    #     print(weighted_std)
    #     print(std)
    #print(std)
    #print(str(close_price_list) + '\n')

    #计算五个点之间的差值
    diff = np.diff(close_price_list)

    #判断加权标准差，在交易成本的幅度范围内则不作考虑，返回0状态

    if diff[0]>0 and diff[1]>0 and diff[2]>0 and diff[3]>0:

        #斜率均为正，一次比一次大，则买进
        if (diff[0]<diff[1]<diff[2]<diff[3]):
            return STATE[1]

        #斜率均为正，一次比一次小，则卖出
        if (diff[0]>diff[1]>diff[2]>diff[3]):
            return STATE[2]

    if diff[0] < 0 and diff[1] < 0 and diff[2] < 0 and diff[3] < 0:

        #斜率均为负，一次比一次小，则卖出
        if (diff[0]>diff[1]>diff[2]>diff[3]):
            return STATE[2]

        #斜率均为负，一次比一次大，则买进
        if (diff[0]<diff[1]<diff[2]<diff[3]):
            return STATE[1]

    std_4 = np.std(close_price_list[0:4], ddof=1)
    mean_4=np.mean(close_price_list[0:4])
        #前四个点加权标准差，后一个点计算偏离标准差
    if((close_price_list[4]-mean_4)>std_4+0.05):
        # 如果往上偏，则买进
        return STATE[1]

    elif((close_price_list[4]-mean_4)<-std_4-0.05):
        # 如果往下偏，则卖出
        return STATE[2]


    # std_3 = np.std(close_price_list[0:3], ddof=1)
    # mean_3=np.mean(close_price_list[0:3])
        #前三个点加权标准差，后两个点计算偏离标准差
            #如果往上偏，则买进
            #如果往下偏，则卖出

    #如果以上都没有触发，则加权拟合曲线，上升买，下降卖(程度判定)

    x=[1,2,3,4,5]
    func_param = np.polyfit(x, close_price_list, 1)
    func_formula=np.poly1d(func_param)

    if(func_param[0]>0.045):
        return STATE[1]

    if(func_param[0]<-0.045):
        return STATE[2]

    return STATE[0]