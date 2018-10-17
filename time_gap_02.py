"""
这个程序只读取了打开关闭行为这一张表，
不需要再改动，也不需要再注释哪些代码，
拿来直接运行，直接生成一个表，表中包含69个和时间段有关的特征，并且以deviceid作为index
这些特征是：
打开、关闭次数按照小时分布的均值偏移、标准差、峰度、偏度：(8个)
'mu_offset', 'sigma', 'skew', 'kurt', 'mu_offset_cl', 'sigma_cl', 'skew_cl', 'kurt_cl'
在24小时的每一个小时打开的平均次数(这个平均是指总次数除以天数)：(24个)
'st_open0','st_open1', 'st_open2', 'st_open3', 'st_open4', 'st_open5', 'st_open6',
'st_open7', 'st_open8', 'st_open9', 'st_open10', 'st_open11',
'st_open12', 'st_open13', 'st_open14', 'st_open15', 'st_open16',
'st_open17', 'st_open18', 'st_open19', 'st_open20', 'st_open21',
'st_open22', 'st_open23'
在一天中6个时间段的打开的平均次数：(6个)
st_freq nosleep', 'st_freq breakfast',
'st_freq AM', 'st_freq lunch', 'st_freq PM', 'st_freq night',
在一天中7个时间段的关闭的平均次数：(7个)
'cl_freq nosleep','cl_freq breakfast', 'cl_freq AM', 'cl_freq lunch',
'cl_freq PM','cl_freq dinner', 'cl_freq night'
每小时打开之后的平均使用时间：(24个）
'0_time' '1_time' '2_time' '3_time' '4_time' '5_time' '6_time' '7_time'
 '8_time' '9_time' '10_time' '11_time' '12_time' '13_time' '14_time'
 '15_time' '16_time' '17_time' '18_time' '19_time' '20_time' '21_time'
 '22_time' '23_time'
我的笔记本：联想小新Air
操作系统：Windows 10 家庭中文版
内存：4G
CPU：Intel(R) Core(TM) m3- -6Y30 CPU @ 0.90GHz 1.51 GHz × 4
第一次运行这个程序花费5分钟多一点
"""
import pandas as pd
import numpy as np
import math
import gc
gc.disable()
"""
和之前的代码最大的不同就是增加了这个gc，它的作用是清理掉中间变量占用的内存，防止内存不足(之前多次碰到这种问题)
首先把gc关掉，如果一直开着，它就会一直监控着内存变化，这个监控也是会消耗资源的，所以先关掉
当你要清除中间变量a的时候，就再打开，清理之后又马上关掉
gc.enable()   打开垃圾回收功能
del a         清理a
gc.collect()  清空垃圾回收站
gc.disable()  关闭垃圾回收功能
"""

"""读取打开关闭行为的数据表，名字记为start_close"""
start_close = pd.read_csv('deviceid_package_start_close.tsv', sep='\t', header=None)
start_close.columns = ['device', 'app', 'start', 'close']
gc.enable()
del start_close['app']
gc.collect()
gc.disable()
"""计算每个device的使用天数，最后求平均的时候用"""
grouped = start_close.groupby(['device'])
days = grouped.max()['close'] - grouped.min()['start']
gc.enable()
del grouped
gc.collect()
gc.disable()
days = days.map(lambda x: math.ceil(x/86400000))
days = pd.DataFrame(days, columns=['days'])
"""
gethour函数：根据精确到毫秒数的UNIX时间戳，求这个时间戳对应的时刻在一天当中是第几个小时(0到23)
首先得到格林尼治时间的小时数
因为时差的存在，要把它转换成北京时间的小时数
"""
def gethour(unix_time):
    # GMT_hour = int(unix_time/3600000) % 24
    """
    如果上一行报错：ValueError:cannot convert float NaN to integer
    就把上一行改成     """
    x = unix_time/3600000
    x = 0 if (x != x) else int(x)
    GMT_hour = x % 24

    if GMT_hour <= 15:
        return GMT_hour + 8
    else:
        return GMT_hour - 16
"""求打开关闭表中所有打开和关闭时间的小时数，以及使用时长，做成一个新的表hour，并且对应到每一个device"""
hour = pd.DataFrame(start_close['device'])
hour['st'] = start_close['start'].apply(lambda x: gethour(x))
hour['cl'] = start_close['close'].apply(lambda x: gethour(x))
hour['use'] = start_close.eval('(close-start)/1000')
"""OK，现在我们只需要小时数hour这个表，所以之前的start_close可以清理掉了"""
gc.enable()
del start_close
gc.collect()
gc.disable()
"""
sortedDictValues函数的作用是，把值为0的键也加进来，键一共有24个，对应0到23点钟，值是每一个小时打开的次数
比如说有一个人7点打开1次，8点打开2次，12点打开3次，18点打开4次，其他时间没有打开
counter函数求出的一天的打开次数分布就是adict={7:1, 8:2, 12:3, 18:4}
这个函数就把adict变成{1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:1, 8:2, 9:0, 10:0, 11:0, 12:3, 13:0, 14:0, 15:0, 16:0, 17:0, 18:4,
                19:0, 20:0, 21:0, 22:0, 23:0}
这里假设adict是不包含打开次数为0的小时数的分布，而dis是完整的包含24个小时的键的分布          
"""
def sortedDictValues(adict):
    keys = list(adict.keys())
    keys.sort()
    dis = {key: adict[key] if key in keys else 0 for key in range(24)}
    return dis
"""getmu函数：求这个分布的均值"""
def getmu(dis):
    a = list(dis.values())
    N = np.sum(a)
    ans = np.sum(i*a[i] for i in range(24))
    return ans/N
"""getsigma函数：求这个分布的标准差"""
def getsigma(dis):
    a = list(dis.values())
    onestd = np.std(a)
    return onestd
"""getskew函数：求这个分布的偏度系数"""
def getskew(dis):
    a = list(dis.values())
    a = pd.Series(a)
    return a.skew()
"""getkurt函数：求这个分布的峰度度系数"""
def getkurt(dis):
    a = list(dis.values())
    a = pd.Series(a)
    return a.kurt()
"""
getBriefDis函数：把原本的24个小时的分布，变成按照7个大的时间段区间的分布，统计每个时间段有多少打开次数(累加起来)
比如
dis = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:1, 8:2, 9:0, 10:0, 11:0, 12:3, 13:0, 14:0, 15:0, 16:0, 17:0, 18:4,
                19:10, 20:5, 21:0, 22:0, 23:0}
求得的
dis_brief = {'nosleep': 0, 'breakfast': 1, 'AM': 2, 'lunch': 3, 'PM': 0, 'dinner': 4, 'night': 15}
"""
def getBriefDis(dis):
    dis_brief = {'nosleep': 0, 'breakfast': 0, 'AM': 0, 'lunch': 0, 'PM': 0, 'dinner': 0, 'night': 0}
    for i in range(0, 5):
        dis_brief['nosleep'] += dis[i]
    for i in range(5, 8):
        dis_brief['breakfast'] += dis[i]
    for i in range(8, 12):
        dis_brief['AM'] += dis[i]
    for i in range(12, 14):
        dis_brief['lunch'] += dis[i]
    for i in range(14, 18):
        dis_brief['PM'] += dis[i]
    for i in range(18, 19):
        dis_brief['dinner'] += dis[i]
    for i in range(19, 24):
        dis_brief['night'] += dis[i]
    return dis_brief

from collections import Counter
"""
首先说一下counter函数的作用，它给一个Series中的所有元素出现的次数做一个统计，返回一个键是元素，值是元素出现次数的字典
比如说一个人所有的打开行为是a = [7,13,8,13,8,19,7,13,7]
那么Counter(a) = {7: 3, 13: 3, 8: 2, 19: 1}
7点打开3次，13点打开3次，8点打开2次，19点打开1次
下面这两句是求所有人的打开、关闭行为的时间分布的总的均值，作为基准线
"""
basemu_st = getmu(sortedDictValues(Counter(hour['st'])))
basemu_cl = getmu(sortedDictValues(Counter(hour['cl'])))

"""求每小时打开之后的平均使用时间"""
use_time_hour = hour.pivot_table('use', index='device', columns='st', aggfunc='sum')
use_time_hour = use_time_hour.join(days)
for i in range(24):
    use_time_hour[i] = use_time_hour[i]/use_time_hour['days']
use_time_hour.drop(['days'], axis=1, inplace=True)
use_time_hour.columns = use_time_hour.columns.map(lambda x: str(x) + '_time')

tmp = dict(list(hour.groupby(['device'])))
"""
解释一下上面这一句：把hour表按照device分组，得到一个字典叫tmp，字典的
键：device
值：每一个device对应的所有打开和关闭行为的小时数(是原表的子表)

OK, 现在有了tmp，不需要hour了，清理掉hour            """
gc.enable()
del hour
gc.collect()
gc.disable()

device_list = []
dev_dis_st = {}
dev_dis_cl = {}
"""
由tmp来求这一个列表和两个字典
device_list：原来的表中device保持原有的顺序排列的列表
dev_dis_st：键是device，值是这个device的打开时间的分布(也是一个字典) 
dev_dis_cl：键是device，值是这个device的关闭时间的分布(也是一个字典)
length：所有device的数目
"""

for k in tmp.keys():
    device_list.append(k)
    dev_dis_st[k] = sortedDictValues(Counter(tmp[k]['st']))
    dev_dis_cl[k] = sortedDictValues(Counter(tmp[k]['cl']))
length = len(device_list)
"""OK, tmp不需要了，清理掉"""
gc.enable()
del tmp
gc.collect()
gc.disable()

"""
接下来就仅仅依靠6个全局变量：
dev_dis_st, dev_dis_cl, device_list, length, basemu_st, basemu_cl
来做特征，其他变量都清理掉了
"""

"""分开来，首先是打开时间"""

"""
dis这个列表现在表示的意思是：所有的device的打开行为的列表，比如dis[i]就是对应的设备device_list[i]的时间分布
dis[j][13]的意思是device_list[j]这个设备在13点钟打开行为的次数
下面也求了dis_brief，同理
dis_brief[j]['nosleep']的意思是device_list[j]这个设备在熬夜时间(0点到4点)打开行为的次数
"""
dis = []
for i in range(length):
    dis.append(dev_dis_st[device_list[i]])
"""
前面改过之后，device_list[i]是一个设备，tmp是字典，对应的值就是这个设备的打开行为的时间分布
下面这些也是一样的，都变成了列表
比如skew[i]就是dis[i]这个时间分布的偏度系数
"""
dis_brief = []
mean = []
std = []
skew = []
kurt = []
for i in range(length):
    dis_brief.append(getBriefDis(dis[i]))
    mean.append(getmu(dis[i]) - basemu_st)
    std.append(getsigma(dis[i]))
    skew.append(getskew(dis[i]))
    kurt.append(getkurt(dis[i]))
"""建立特征表，以device作为index，和使用天数做合并，合并之后清理掉days"""
ans = pd.DataFrame({'mu_offset': mean, 'sigma': std, 'skew': skew, 'kurt': kurt})
ans.index = device_list
ans = ans.join(days)
gc.enable()
del days
gc.collect()
gc.disable()
"""
下面这段代码把每一个时间段作为一列，每一个时间段的打开次数作为一个特征
其实就是把之前求的两个字典dis和dis_brief展开了
"""
"""先展开24个小时的dis"""
for i in range(24):
    cur = []
    for j in range(length):
        cur.append(dis[j][i])
    ans['st_open' + str(i)] = cur
    ans['st_open' + str(i)] = ans['st_open' + str(i)] / ans['days']
"""
再展开7个时间段的dis_brief，因为dinner时间段就是18点，而上面已经求过每一个小时的(也包括18点)，
所以dinner不用再重复求了，否则是完全无用的特征
"""
for i in ['nosleep', 'breakfast', 'AM', 'lunch', 'PM', 'night']:
    cur_brief = []
    for j in range(length):
        cur_brief.append(dis_brief[j][i])
    ans['st_freq ' + i] = cur_brief
    ans['st_freq ' + i] = ans['st_freq ' + i] / ans['days']
"""OK，清理内存"""
gc.enable()
del cur_brief
gc.collect()
del dis_brief
gc.collect()
del cur
gc.collect()
del dis
gc.collect()
del dev_dis_st
gc.collect()
del mean
gc.collect()
del skew
gc.collect()
del kurt
gc.collect()
del std
gc.collect()
gc.disable()

"""同样的事情，对关闭时间再来做一遍"""

dis = []
for i in range(length):
    dis.append(dev_dis_cl[device_list[i]])
dis_brief = []
mean = []
std = []
skew = []
kurt = []
for i in range(length):
    dis_brief.append(getBriefDis(dis[i]))
    mean.append(getmu(dis[i]) - basemu_cl)
    std.append(getsigma(dis[i]))
    skew.append(getskew(dis[i]))
    kurt.append(getkurt(dis[i]))
ans['mu_offset_cl'] = mean
ans['sigma_cl'] = std
ans['skew_cl'] = skew
ans['kurt_cl'] = kurt
"""
因为做特征排名发现关闭时间的特征普遍弱于打开时间的特征，所以关闭时间就不做24个小时的分布了，只做7个时间段的
"""
for i in ['nosleep', 'breakfast', 'AM', 'lunch', 'PM', 'dinner', 'night']:
    cur_brief = []
    for j in range(length):
        cur_brief.append(dis_brief[j][i])
    ans['cl_freq ' + i] = cur_brief
    ans['cl_freq ' + i] = ans['cl_freq ' + i] / ans['days']
"""OK，清理内存"""
gc.enable()
del cur_brief
gc.collect()
del dis_brief
gc.collect()
del dev_dis_cl
gc.collect()
del dis
gc.collect()
del mean
gc.collect()
del skew
gc.collect()
del kurt
gc.collect()
del std
gc.collect()
gc.disable()
"""最后完成的结果命名为ans，把device拼上去作为index"""
ans = ans.join(use_time_hour)
ans.fillna(0, inplace=True)
ans.insert(0, 'device', ans.index)
gc.enable()
del ans['days']
gc.collect()
gc.disable()
print(ans.tail())
ans.to_csv('time_gap_02.csv')
"""把结果变成csv文件保存到硬盘上，然后清理内存中的ans"""
gc.enable()
del device_list
gc.collect()
del ans
gc.collect()
gc.disable()