""" 我上一次分享在群里发了ana.py和train_50.csv
    ana.py这个程序是用来生成最初的50个特征的train_50.csv训练集文件，
    写得非常乱，我自己都看不下去了，这哪个zz写的？
    train_50.csv用lightgbm做22分类的log_loss是2.801
    我想把这个log_loss降低，所以要做一些新的特征，再合并到train_50.csv里面来
    做新特征的程序文件是step2.py"""
import pandas as pd
import numpy as np
import itertools
import pprint

start_close = pd.read_csv('deviceid_package_start_close.tsv', sep='\t', header=None)
start_close.columns = ['device', 'app', 'start', 'close']
#
# tmp1 = pd.DataFrame(start_close['device'])
# tmp1['gap'] = (start_close['close'] - start_close['start'])/1000
# tmp1.to_csv('开关表中所有开关时间的秒数差.csv')
# print(gapmean)                  # 7689233.43994
#
# deviceid_brand = pd.read_csv('deviceid_brand.tsv', sep='\t', header=None)
# deviceid_packages = pd.read_csv('deviceid_packages.tsv', sep='\t', header=None)
# deviceid_test = pd.read_csv('deviceid_test.tsv', sep='\t', header=None)
# deviceid_train = pd.read_csv('deviceid_train.tsv', sep='\t', header=None)
# package_label = pd.read_csv('package_label.tsv', sep='\t', header=None)
#
# print(7689233/60)
# print(7689233/3600)
#
#
# 统计每台设备上的app数目
# packages = pd.read_csv('deviceid_packages.tsv', sep='\t', header=None)
# packages.columns = ['device', 'apps']
# apps = packages['apps']
# apps = apps.apply(lambda x: x.split(','))
# numapps = apps.apply(lambda x: len(x))
# numapps = pd.DataFrame({'numapps': numapps})
# packages = pd.concat([packages, numapps], axis=1)
# packages = pd.DataFrame(packages)
# packages.to_csv('numapps.csv')
# with pd.option_context('display.float_format', lambda x: '%.3f' % x):
#     print(start_close.describe())
#                       2                 3
# count      36720940.000      36720940.000
# mean  1489081459549.199 1489089148782.905
# std     22214672578.950   22054559373.389
# min           50988.000         59970.000
# 25%   1488864885959.000 1488865682275.500
# 50%   1489490768269.000 1489491372663.000
# 75%   1490185881235.750 1490186457468.750
# max   2136676365305.000 2136677153179.000
#
# def gethour(start):
#     GMT_hour = int(start/3600000) % 24
#     if GMT_hour <= 15:
#         return GMT_hour + 8
#     else:
#         return GMT_hour - 16
# starthour = pd.DataFrame(start_close['device'])
# starthour['chour'] = start_close['close'].apply(lambda x: gethour(x))
# starthour.to_csv('all_close_hour.csv')

#
# def getunixsecond(start):
#     return int(start/1000)
# import time
# print(time.time())
# import datetime
# print(datetime.datetime.now())
# print(gethour(int(time.time())*1000))
# print(deviceid_brand.describe())
#                                        0       1             2
# count                              72554   72550         72517
# unique                             72554    1134          2943
# top     80a3fdcaed624d6e30bdd3381de25c9b  Xiaomi  HM NOTE 1LTE
# freq                                   1   14074          2055
# with pd.option_context('display.float_format', lambda x: '%.3f' % x):
    # print(deviceid_train.describe())
#             1         2
# count 50000.000 50000.000
# mean      1.354     5.622
# std       0.478     2.481
# min       1.000     0.000
# 25 %      1.000     4.000
# 50 %      1.000     6.000
# 75 %      2.000     7.000
# max       2.000    10.000
# print(deviceid_packages.describe())
#
# print(package_label.describe())
#                                        0      1      2
# count                              10368  10368  10368
# unique                             10368     45    288
# top     294b017acedad2b1ee90131cd04ac276   系统工具     其它
# freq                                   1   1005    640
#
# start_close.drop(['app', 'close'], axis=1, inplace=True)
# tmp2 = start_close.groupby(['device']).count()
# tmp2 = pd.DataFrame(tmp2)
# tmp2.to_csv('开关表中每一台设备上所有app总的打开次数.csv')
# #
# #
# start_close['gap'] = (start_close['close'] - start_close['start'])/1000
# start_close.drop(['start', 'close'], axis=1, inplace=True)
# people = dict(list(start_close.groupby(['device'])))
# device_list = []
# app_list = []
# gap_list = []
# for k1 in people.keys():
#     people[k1].drop(['device'], axis=1, inplace=True)
#     j = dict(list(people[k1].groupby(['app'])))
#     for k2 in j.keys():
#         gap_list.append(np.sum(j[k2]['gap']))
#         app_list.append(k2)
#         device_list.append(k1)
# timeall = pd.DataFrame({'device': device_list, 'app': app_list, 'totaltime': gap_list})
# timeall.to_csv('each_app_used_time_on_device_001.csv')
# #
# # 获得每台设备上安装的app的大小类别
#
# 直接把这些大小类别做一个Labelencoder
# deviceid_packages.columns = ['device', 'applist']
# package_label.columns = ['app', 'label_big', 'label_small']
# label_big_unique = list(package_label['label_big'].unique())
# label_small_unique = list(package_label['label_small'].unique())
# from sklearn.preprocessing import LabelEncoder
# le1 = LabelEncoder()
# le2 = LabelEncoder()
# label_big_unique_numeric = le1.fit_transform(label_big_unique)
# label_small_unique_numeric = le2.fit_transform(label_small_unique)
#
# num_dict_label_big = {}
# num_dict_label_small = {}
# for i in range(len(label_big_unique)):
#     num_dict_label_big[label_big_unique[i]] = label_big_unique_numeric[i]
# for i in range(len(label_small_unique)):
#     num_dict_label_small[label_small_unique[i]] = label_small_unique_numeric[i]
# package_label['label_big_num'] = package_label['label_big'].apply(lambda x: num_dict_label_big[x])
# package_label['label_small_num'] = package_label['label_small'].apply(lambda x: num_dict_label_small[x])
# #
# # with pd.option_context('display.max_rows', None, 'display.max_columns', 100):
# #     print(package_label.head(60))
# #
# app_label_big_dict = {}
# app_label_small_dict = {}
# for row in package_label.itertuples(index=True, name='Pandas'):
#     key = getattr(row, 'app')
#     value_big = getattr(row, 'label_big_num')
#     value_small = getattr(row, 'label_small_num')
#     app_label_big_dict[key] = value_big
#     app_label_small_dict[key] = value_small
# def f_big(applist):
#     ans = []
#     for i in applist.split(','):
#         if i in app_label_big_dict.keys():
#             ans.append(app_label_big_dict[i])
#         else:
#             ans.append(-999)
#     return ans
# def f_small(applist):
#     ans = []
#     for i in applist.split(','):
#         if i in app_label_small_dict.keys():
#             ans.append(app_label_small_dict[i])
#         else:
#             ans.append(-999)
#     return ans
# def g_big(app):
#     ans = 0
#     if app in app_label_big_dict.keys():
#         ans = app_label_big_dict[app]
#     else:
#         ans = -999
#     return ans
# def g_small(app):
#     ans = 0
#     if app in app_label_small_dict.keys():
#         ans = app_label_small_dict[app]
#     else:
#         ans = -999
#     return ans
# #
# deviceid_packages['label_big_num'] = deviceid_packages['applist'].apply(lambda x: f_big(x))
# deviceid_packages['label_small_num'] = deviceid_packages['applist'].apply(lambda x: f_small(x))
# deviceid_packages.drop(['applist'], axis=1, inplace=True)

# deviceid_packages.to_csv('label of apps on each device.csv')
# 现在这个就是数值化之后的类别了


# 分析一下品牌和型号
# deviceid_brand.columns = ['device', 'brand_big', 'brand_small']
# deviceid_brand['brand_big_up'] = deviceid_brand['brand_big'].apply(lambda x: str(x).upper())
# # 描述频率
# key_list = list(deviceid_brand['brand_big_up'])
# from collections import Counter
# print(Counter(key_list))
# 'XIAOMI': 14074, 'SAMSUNG': 12736, 'HUAWEI': 9967, 'OPPO': 6401, 'VIVO': 4919, 'HONOR': 3972,
# 'COOLPAD': 3764, 'LENOVO': 2877, 'ZTE': 1692,   # 做这3个的系列
#  'MEIZU': 897, 'GIONEE': 834, 'SONY': 803,
#
# tmp = dict(list(deviceid_brand.groupby(['brand_big_up'])))
# mydict = {'COOLPAD', 'LENOVO', 'ZTE'}
# mydf = pd.DataFrame()
# mydf = pd.concat([tmp['COOLPAD'], tmp['LENOVO'], tmp['ZTE']], axis=0)
# print(mydf.head())
# 暂时放一下
#
# # 每个人对应每台设备(deviceid)
# # 1.每个人使用时间最长的APP以及这个app的类别
# total = pd.read_csv('each app used time on each device.csv')
# print(total.index)
# print(total.columns)
# RangeIndex(start=0, stop=765698, step=1)
# Index(['Unnamed: 0', 'device', 'app', 'totaltime'], dtype='object')
# total.drop(['Unnamed: 0'], axis=1, inplace=True)
# 用python引擎读取带有中文名或中文路径的文件，不推荐这个做法，因为速度慢而且占内存，最好直接用英文命名文件
# print(total.head())
# group_device = dict(list(total.groupby(['device'])))
# dev = list(group_device.keys())
# f_label_big = []
# f_label_sma = []
# for k in dev:
#     v = group_device[k]
#     v = v.sort_values(['totaltime'], ascending=False).reset_index(drop=True)
#     favorapp = v.loc[0, ]['app']
# # todo
#     if g_big(favorapp) == 32:
#         if len(v.index) < 2:
#             f_label_big.append(32)
#             f_label_sma.append(g_small(favorapp))
#         else:
#             secapp = v.loc[1, ]['app']
#             f_label_big.append(g_big(secapp))
#             f_label_sma.append(g_small(secapp))
#     else:
#         f_label_big.append(g_big(favorapp))
#         f_label_sma.append(g_small(favorapp))
# ans = pd.DataFrame({'device': dev, 'f_label_b': f_label_big, 'f_label_s': f_label_sma})
# ans.to_csv('label_of_favorite_app.csv')

# app_totaltime_dict = {}
# for row in total.itertuples(index=True, name='Pandas'):
#     key = getattr(row, 'totaltime')
#     value = getattr(row, 'app')
#     app_totaltime_dict[key] = value
#
# fu = total.groupby(['device']).max()
# fu = pd.DataFrame(fu)
# fu.drop(['app'], axis=1, inplace=True)
# # with pd.option_context('display.max_rows', None, 'display.max_columns', 100):
# #     print(fu.head(20))
# fu['favorapp'] = fu['totaltime'].apply(lambda x: app_totaltime_dict[x])
# fu['f_lable_big'] = fu['favorapp'].apply(lambda x: g_big(x))
# fu['f_label_small'] = fu['favorapp'].apply(lambda x: g_small(x))
# fu.drop(['totaltime'], axis=1, inplace=True)
# with pd.option_context('display.max_rows', None, 'display.max_columns', 100):
#     print(fu.head(20))
# fu.to_csv('label_of_favorite_app.csv')
# 2.每个人按照一天中时间段分开，每个时间段玩了多少次，以及这个频次时间分布的均值偏移(相对于总体人群)、标准差、偏度、峰度
from collections import Counter
# starthour = pd.read_csv('all_start_hour.csv')
# starthour = pd.read_csv('all_close_hour.csv')



# 字典按键排序, 获得一天的时间频次分布
# def sortedDictValues1(adict):
#     keys = list(adict.keys())
#     keys.sort()
#     dis = {key: adict[key] if key in keys else 0 for key in range(24)}
#     return dis
# def getmu(dis):
#     a = list(dis.values())
#     N = np.sum(a)
#     ans = np.sum(i*a[i] for i in range(24))
#     return ans/N
# def getsigma(dis):
#     a = list(dis.values())
#     onestd = np.std(a)
#     return onestd
# def getskew(dis):
#     a = list(dis.values())
#     a = pd.Series(a)
#     return a.skew()
# def getkurt(dis):
#     a = list(dis.values())
#     a = pd.Series(a)
#     return a.kurt()
# def getBriefDis(dis):
#     dis_brief = {'nosleep': 0, 'breakfast': 0, 'AM': 0, 'lunch': 0, 'PM': 0, 'dinner': 0, 'night': 0}
#     for i in range(0, 5):
#         dis_brief['nosleep'] += dis[i]
#     for i in range(5, 8):
#         dis_brief['breakfast'] += dis[i]
#     for i in range(8, 12):
#         dis_brief['AM'] += dis[i]
#     for i in range(12, 14):
#         dis_brief['lunch'] += dis[i]
#     for i in range(14, 18):
#         dis_brief['PM'] += dis[i]
#     for i in range(18, 19):
#         dis_brief['dinner'] += dis[i]
#     for i in range(19, 24):
#         dis_brief['night'] += dis[i]
#     return dis_brief
# tmp = dict(list(starthour.groupby(['device'])))
# for k in tmp.keys():
#     tmp[k] = sortedDictValues1(Counter(tmp[k]['shour']))

# print(tmp)
# basemu = getmu(sortedDictValues1(Counter(starthour['chour'])))

# device = list(tmp.keys())
# dis = []
# length = len(device)
# for i in range(length):
#     dis.append(tmp[device[i]])
# dis_brief = []
# mean = []
# std = []
# skew = []
# kurt = []
# for i in range(length):
#     dis_brief.append(getBriefDis(dis[i]))
#     mean.append(getmu(dis[i]) - basemu)
#     std.append(getsigma(dis[i]))
#     skew.append(getskew(dis[i]))
#     kurt.append(getkurt(dis[i]))

# ans = pd.DataFrame({'device': device})
# ans = pd.DataFrame({'device': device, 'mu_offset_cl': mean, 'sigma_cl': std, 'skew_cl': skew, 'kurt_cl': kurt})
#
# for i in range(24):
#     cur = []
#     for j in range(length):
#         cur.append(dis[j][i])
#     cur = pd.Series(cur)
    # ans['st_freq ' + i] = cur
    # ans['st_open' + str(i)] = cur
# ans.to_csv('tmp_time_24_distri.csv')
# # print(getmu(sortedDictValues1(Counter(starthour['shour']))))
# # print(getsigma(sortedDictValues1(Counter(starthour['shour'])))/length)
# # ans.to_csv('freq_hour_distribution_of_allapps_open_on_each_device.csv')
# # ans.to_csv('freq_close_hour_distribution_on_each_device.csv')
#
# #
"""看设备有没有安装这些大类别的app"""
# 0          实用工具      17
# 1            视频      38
# 2          母婴亲子      25
# 3            金融      43
# 4            其它      11
# 5          地图导航      16
# 6            教育      22
# 7          摄影摄像      21
# 8          移动购物      33
# 9            资讯      40
# 10         应用管理      19
# 11         移动阅读      34
# 12           汽车      26
# 13           休闲       7
# 14   ACT(动作类游戏)       0
# 15         音频娱乐      44
# 16          浏览器      27
# 17         体育竞技       9
# 18           社交      32
# 19           射击      18
# 20         交通出行       5
# 21         系统工具      36
# 22           竞速      35
# 23         商务办公      15
# 24           生活      31
# 25    SIM(模拟游戏)       2
# 26           旅游      23
# 27         智能硬件      24
# 28           健康      10
# 29           医疗      13
# 30         动漫娱乐      12
# 31         游戏平台      30
# 32    SLG(策略游戏)       3
# 33         视频直播      39
# 34           体育       8
# 35        企业级应用       6
# 36         游戏工具      29
# 37          输入法      41
# 38         游戏媒体      28
# 39  RPG(角色扮演游戏)       1
# 40           美食      37
# 41    TAB(桌面游戏)       4
# 42           房产      20
# 43           通讯      42
# 44           卡牌      14
# nicelabel = {4, 33, 18, 29, 26, 35, 2,
#              0, 5, 3, 1, 25,
#              8, 37, 30, 28, 9, 6, 12, 13}
# step2label = {14, 42, 20, 41, 39, 10, 23, 24, 31, 15, 36, 32, 27, 44, 7, 34, 19, 40, 21, 22, 16, 11, 43, 38, 17}
# biglabel = list(deviceid_packages['label_big_num'])
# deviceid = deviceid_packages['device']
# res = pd.DataFrame(deviceid)
# # for i in nicelabel:
# for i in step2label:
#     th = []
#     for j in range(len(deviceid)):
#         if i in biglabel[j]:
#             th.append(2)
#         else:
#             if -999 in biglabel[j]:
#                 th.append(0)
#             else:
#                 th.append(1)
#     th = pd.Series(th)
#     res['has_' + str(i)] = th
#
# data = pd.read_csv('train_001.csv')
#
# data.index = data['device']
# data.drop(['device'], axis=1, inplace=True)
# res.index = res['device']
# res.drop(['device'], axis=1, inplace=True)
# data = data.join([res])
# data.to_csv('train_002.csv')

#   # 得到每个设备的使用总时长
# apptime = pd.read_csv('each app used time on each device.csv')
# apptime.drop(['Unnamed: 0'], axis=1, inplace=True)
# apptime.index = apptime['device']
# apptime.drop(['device'], axis=1, inplace=True)
# apptime.drop(['app'], axis=1, inplace=True)
# ans = apptime.groupby(['device']).sum()
# ans.to_csv('total_time_of_each_device_used.csv')

# 合并47个特征
# tmp = pd.read_csv('df_total.csv', encoding='gbk')
# tmp.columns = ['device', 'brand']
# tmp.index = tmp['device']
# tmp.drop(['device'], axis=1, inplace=True)
# le3 = LabelEncoder()
# tmp['brand_num'] = le3.fit_transform(tmp['brand'])
# tmp.drop(['brand'], axis=1, inplace=True)

# tmp1 = pd.read_csv('freq_hour_distribution_of_allapps_open_on_each_device.csv')
# tmp1.drop(['Unnamed: 0'], axis=1, inplace=True)
# tmp1.index = tmp1['device']
# tmp1.drop(['device'], axis=1, inplace=True)
#
# tmp2 = pd.read_csv('if device has one of 20 nice labels.csv')
# tmp2.drop(['Unnamed: 0'], axis=1, inplace=True)
# tmp2.index = tmp2['device']
# tmp2.drop(['device'], axis=1, inplace=True)

# tmp3 = deviceid_packages
# tmp3.index = tmp3['device']
# tmp3.drop(['device'], axis=1, inplace=True)
#
# tmp4 = pd.read_csv('total_time_of_each_device_used.csv')
# tmp4.index = tmp4['device']
# tmp4.drop(['device'], axis=1, inplace=True)
# 每台设备平均每天使用时间(秒)
# days = (start_close.groupby(['device']).max()['close'] - start_close.groupby(['device']).min()['start'])/86400000
# days = pd.DataFrame(days, columns=['days'])
# tmp4 = tmp4.join(days)
# tmp4['avg_uesd_perday'] = tmp4['totaltime'] / tmp4['days']
# tmp4.drop(['days'], axis=1, inplace=True)
#
# tmp5 = pd.read_csv('nums_apps_on_device.csv')
# tmp5.drop(['Unnamed: 0'], axis=1, inplace=True)
# tmp5.drop(['apps'], axis=1, inplace=True)
# tmp5.index = tmp5['device']
# tmp5.drop(['device'], axis=1, inplace=True)
#
# tmp6 = pd.read_csv('total_open_times_on_device.csv')
# tmp6.columns = ['device', 'opentimes']
# tmp6.index = tmp6['device']
# tmp6.drop(['device'], axis=1, inplace=True)
#
# tmp7 = pd.read_csv('label_of_favorite_app.csv')     # 最喜欢的app要不要去掉呢？？？
# tmp7.columns = ['device', 'favorapp', 'f_label_big', 'f_label_small']
# tmp7.index = tmp7['device']
# tmp7.drop(['device'], axis=1, inplace=True)
# le4 = LabelEncoder()
# tmp7['favor_app'] = le4.fit_transform(tmp7['favorapp'])
# tmp7.drop(['favorapp'], axis=1, inplace=True)
#
# tmp8 = pd.read_csv('freq_close_hour_distribution_on_each_device.csv')
# tmp8.drop(['Unnamed: 0'], axis=1, inplace=True)
# tmp8.index = tmp8['device']
# tmp8.drop(['device'], axis=1, inplace=True)
#
# tmp9 = pd.read_csv('deviceid_train.tsv', sep='\t', header=None)
# tmp9.columns = ['device', 'target', 'age']
# tmp9.drop(['age'], axis=1, inplace=True)
# tmp9.index = tmp9['device']
# tmp9.drop(['device'], axis=1, inplace=True)

# with pd.option_context('display.max_rows', None, 'display.max_columns', 100):
    # print(tmp.head())
    # print(tmp1.head())
    # print(tmp2.head())
    # print(tmp3.head())
    # print(tmp4.head())
    # print(tmp5.head())
    # print(tmp6.head())
    # print(tmp7.head())
    # print(tmp8.head())
    # print(tmp9.head())
    # print(tmp7['favor_app'].describe())
    # count                                  72727
    # unique                                  2586
    # top         1896072db9ce6406febfc17f681c2086
    # freq                                   20423
    # print(tmp7['favor_app'].value_counts())
    # print(tmp.columns)
    # print(tmp1.columns)
    # print(tmp2.columns)
    # print(tmp3.columns)
    # print(tmp4.columns)
    # print(tmp5.columns)
    # print(tmp6.columns)
    # print(tmp7.columns)
    # print(tmp8.columns)
    # print(tmp9.columns)
# train = tmp9.join([tmp, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7, tmp8])
# train.to_csv('gender_47_classif_num_train.csv')
#
# data = pd.read_csv('gender_47_classification_train.csv', encoding='gbk')
# data = data.fillna('HM')
# print(data.isnull().any())
# print(data.columns)
# print(data.shape)
# print(len(data['device'].unique()))         # 直接按这一列去重算了
# with pd.option_context('display.max_rows', None, 'display.max_columns', 100):
#     print(data['brand'].describe())
# data1 = data
# print(data['target'].value_counts())        # 50348 多的348个怎么来的？

# 1    32543
# 2    17805
# print(data1.isnull().any())

# xtrain,xtest,ytrain,ytest = train_test_split(numDF.drop(['y','target'],axis = 1),
#                                             numDF['target'],train_size = 0.7)
from sklearn.preprocessing import LabelEncoder
# data['']
# data = pd.read_csv('gender_47_classif_num_train.csv')
# cols = data.columns.tolist()
# cols.insert(2, 'age')
# data = data.reindex(columns=cols)
# data['age'] = tmp9['age']
# data.fillna(59, inplace=True)
# data.to_csv('train_52.csv')
# # 然而这两列还是字符串的列表
# data = pd.read_csv('train_52.csv')
# data.drop(['label_big_num'], axis=1, inplace=True)
# data.drop(['label_small_num'], axis=1, inplace=True)
# data.drop(['Unnamed: 0'], axis=1, inplace=True)
# data.to_csv('train_50.csv')
# 最终训练集： train_50.csv
