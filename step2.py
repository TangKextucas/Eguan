import pandas as pd
import numpy as np
"""加2：大写品牌+型号一共的3000多个,作为一个特征
        大写品牌一共2000多个,作为一个特征"""
# br = pd.read_csv('deviceid_brand.tsv', sep='\t', header=None)
# br.columns = ['device', 'brand', 'version']
# br.dropna(inplace=True)
# br['brand_up'] = br['brand'].apply(lambda x: str(x).upper())
# br['b_v'] = br['brand_up'] + '_' + br['version']
# from sklearn.preprocessing import LabelEncoder
# le_b_v = LabelEncoder()
# b_v = br['b_v'].unique()
# b_v_num = le_b_v.fit_transform(b_v)
# transbv = {}
# for i in range(len(b_v)):
#     transbv[b_v[i]] = b_v_num[i]
# br['b_v_num'] = br['b_v'].apply(lambda x: transbv[x])
# le_b = LabelEncoder()
# b = br['brand_up'].unique()
# b_num = le_b_v.fit_transform(b)
# transb = {}
# for i in range(len(b)):
#     transb[b[i]] = b_num[i]
# br['b_num'] = br['brand_up'].apply(lambda x: transb[x])
# br.index = br['device']
# br.drop(['device', 'brand', 'version', 'brand_up', 'b_v'], axis=1, inplace=True)
# data = pd.read_csv('train_50.csv')
# data.index = data['device']
# data.drop(['Unnamed: 0', 'device'], axis=1, inplace=True)
# data = data.join([br])
# data.fillna({'b_num': data['b_num'].mode()[0], 'b_v_num': data['b_v_num'].mode()[0]}, inplace=True)
# data.to_csv('train_001.csv')
"""处理打开时间
    对于一个人所有的打开时间，看是否在同一个1秒、10秒、30秒、60秒之内打开了多次，统计这个次数"""
# start_close = pd.read_csv('deviceid_package_start_close.tsv', sep='\t', header=None)
# start_close.columns = ['device', 'app', 'start', 'close']
# minute = []
# thirty = []
# tensec = []
# onesec = []
# st = start_close['start'].values
# for i in range(len(start_close['start'])):
    # minute.append(int(st[i]/60000))
    # thirty.append(int(st[i]/30000))
    # tensec.append(int(st[i]/10000))
    # onesec.append(int(st[i]/1000))
# start_close['minute'] = minute
# start_close['thirty'] = thirty
# start_close['tensec'] = tensec
# start_close['onesec'] = onesec
# start_close.drop(['app', 'start', 'close'], axis=1, inplace=True)
# dev = []
# isrush_1 = []
# isrush_10 = []
# isrush_30 = []
# isrush_60 = []
# d = dict(list(start_close.groupby(['device'])))
# for i in d.keys():
#     dev.append(i)
#     isrush_1.append(len(d[i]['onesec']) - len(set(list(d[i]['onesec']))))
    # isrush_10.append(len(d[i]['tensec']) - len(set(list(d[i]['tensec']))))
    # isrush_30.append(len(d[i]['thirty']) - len(set(list(d[i]['thirty']))))
    # isrush_60.append(len(d[i]['minute']) - len(set(list(d[i]['minute']))))

# rush = pd.DataFrame({'rush_1': isrush_1}, index=dev)
# print(rush['rush_1'].value_counts())
# print(rush['rush_10'].value_counts())
# print(rush['rush_60'].value_counts())
# print(rush['rush_60'].value_counts())
# data = pd.read_csv('train_004.csv')
# data.index = data['device']
# data.drop(['device'], axis=1, inplace=True)
# data = data.join([rush])
# data.fillna({'rush_1': -999}, inplace=True)
# data.to_csv('train_005.csv')
"""24小时每小时打开次数"""
# dis = pd.read_csv('tmp_time_24_distri.csv')
# print(dis.columns)
# dis.index = dis['device']
# dis.drop(['Unnamed: 0', 'device'], axis=1, inplace=True)
# data = pd.read_csv('train_005.csv')
# data.index = data['device']
# data.drop(['device'], axis=1, inplace=True)
# data = data.join([dis])
# data.to_csv('train_006.csv')
"""不区分deviceid，对所有deviceid的所有打开行为，统计打开次数最多的app"""
# start_close = pd.read_csv('deviceid_package_start_close.tsv', sep='\t', header=None)
# start_close.columns = ['device', 'app', 'start', 'close']
# print(start_close['app'].value_counts().head(40))
"""
输出结果：
1896072db9ce6406febfc17f681c2086    12050342
07e967d75aab2f6a52c558695a572a7c     3557203
8d2448133beb3422f0f638bacf8f7051     1287254
e29eb7083bdf54af48352ffa979fc830     1153291
4b58ecb20fe0d5e7a823b7d95911166d      817326
6d0125a3f13a454c98b9841e4ef96b1a      635441
97d0422a3317b1929926dc90cda4fc53      589070
200cf557b3703944f1f68af08484d2bd      545693
3570fa5e14faf9b3126b9deea90c21d5      524154
0b0816ff97e9a3e5501ed2dcb4a0d66e      521415
b6bcc9662526fb3fdcac16c577e49813      479507
58e96a6325c839e07269513fc9ba9811      456010
2338f5519ae89cb819360870c849ac62      407721
86f9f299cdbc8e2a19fed1712f522c49      385886
e4fb97b00004709730e13c588d457350      365837
ad96c9503da1f8ef626838d75e69fb26      339967
6509b19bd37433de13cba04063f879ed      285001
90cb852cf345e04d508fe03f74089183      276273
ecf4f0ab94f5a4083ef581584c82debd      276231
4dee8fb18b5af024c012c77d21983f89      260074
4c0931dd33d2f7e088955a929c8da9d9      237310
43afea5a44582df0b76771e2892029fe      226691
039be717f253f7b10ed1ce405de08b9f      223131
0995e7526bf406557d1e55c9f650a2b5      214593
9e9ff523f0448879c6cd521495fd758d      201076
02bce1b62f5f5626621faa3cf7425529      199691
616120feb399049e89585756e0cfc4d1      197089
d977dd0e10adc6311525d4351fbf9c84      172045
793037657df0b898fc5202b167272370      168078
37de3dfb9d3bc0a2264adf8802fef726      167514
                                      ...
93eaaaaaff5d94fad78d8ae5e7824e58           1
fd657c565eb9d23f38f7a4cd2294f8c9           1
9834e765553b02e518f2763815fc599e           1
9bf2d95a85d761a875e0c20b7d825cfd           1
0b779934c8fa4fe3e6580133cef1a473           1
0cdb43384e9f1b2fd3ac19f6347677a5           1
bf64c85de93e1e88eec1df76190f387c           1
7ed4ab235d197dcf3f4b5040fc33d911           1
4e29187d7955e9a0c9f9e5c02c1109bf           1
90171c7c380f0b32b5c41d84dfa6f1cc           1
7f0567794d235124fd5c30c19640cd20           1
e11d299c6303714a25ae2f0546db5889           1
923ceaad3c34a253fcf38fdc7f792974           1
8f0ae55ac717708e4b9f1783a0f1b63b           1
3feeaffdfc6cc7b96728eafe790f1fe7           1
c031218ff8016aa0dd1ce9b47d2e76f8           1
912eeefe8351f8d05bfbe5f7f3400794           1
920b9869a6230884da2d7485442dfe3e           1
28227a9bb2987cb4468e0af5d9f2c672           1
6068cfcd32e82cee4c69b37db9c96724           1
0bf7be2da37c331c0c2e19126088f55e           1
d8533c2811694d8f504183c7c13e826b           1
163aadab37a69442785004e9b735aef1           1
1c4ea3b7ef13c4670811d29709bd5f12           1
4e1cde4cd7787741ecffcccce199ea61           1
12bd445e01d921c374d8b32928f871a1           1
ebc1038e7ac2793feab90a1d87c1414b           1
b181bd4179cf4578fd4836ed266a2c04           1
b0a357a9efe42cfc092c73933e41b581           1
6909e1746863f77aeed0cc7a97f9b979           1
Name: app, Length: 35000, dtype: int64          """
# data = pd.read_csv('train_006.csv')
# print(np.mean(data['numapps']))
# print(data['numapps'].value_counts())
"""
10.55378
5      3640
6      3581
4      3443
7      3358
8      3225
3      3094
9      2871
10     2626
2      2384
11     2327
1      2040
12     2033
13     1876
14     1663
15     1490
16     1281
17     1211
18      971
19      889
20      820
21      683
22      609
23      520
24      465
25      379
26      332
27      272
28      264
29      212
30      180
       ... 
65        3
64        3
69        3 """

# deviceid_p_p = pd.read_csv('deviceid_p_p.csv')
# with pd.option_context('display.max_rows', None, 'display.max_columns', 100):
#     print(deviceid_p_p.head())
# print(deviceid_p_p.columns)
"""
   Unnamed: 0                        deviceid_x  gender  age  deviceid_y  \
0           0  bd86d59afa24a839ce6029d718accb19       1    3      2087.0   
1           1  e7d158c9a8262a35c9cc630a15a9103e       1    5      4261.0   
2           2  97abdc3828448b5acc7428dd307bc635       2    5      3159.0   
3           3  e4dbdbf07c9cff03d79f4872e65742b4       1    4      4261.0   
4           4  6bd4537b2970c5c6ab765c1860b88aa5       1    3      4261.0   

          p  brand_age_n  brand_age_mean  
0  0.064565        247.0        0.071761  
1  0.131822        629.0        0.133574  
2  0.178717        519.0        0.173986  
3  0.131822        585.0        0.156794  
4  0.131822        564.0        0.163858  
Index(['Unnamed: 0', 'deviceid_x', 'gender', 'age', 'deviceid_y', 'p',
       'brand_age_n', 'brand_age_mean'],
      dtype='object')   """

"""统计每个device前40名app的使用时间"""
# start_close = pd.read_csv('deviceid_package_start_close.tsv', sep='\t', header=None, names=['device', 'app', 'start', 'close'], dtype={'device': str, 'app': str, 'start': np.int64, 'close': np.int64})
# start_close['gap'] = (start_close['close'] - start_close['start'])/1000
# start_close['app'] = start_close['app'].astype('|S40')
# start_close.drop(['start', 'close'], axis=1, inplace=True)
topAPP = [
'1896072db9ce6406febfc17f681c2086',
'07e967d75aab2f6a52c558695a572a7c',
'8d2448133beb3422f0f638bacf8f7051',
'e29eb7083bdf54af48352ffa979fc830',
'4b58ecb20fe0d5e7a823b7d95911166d',
'6d0125a3f13a454c98b9841e4ef96b1a',
'97d0422a3317b1929926dc90cda4fc53',
'200cf557b3703944f1f68af08484d2bd',
'3570fa5e14faf9b3126b9deea90c21d5',
'0b0816ff97e9a3e5501ed2dcb4a0d66e',
'b6bcc9662526fb3fdcac16c577e49813',
'58e96a6325c839e07269513fc9ba9811',
'2338f5519ae89cb819360870c849ac62',
'86f9f299cdbc8e2a19fed1712f522c49',
'e4fb97b00004709730e13c588d457350',
'ad96c9503da1f8ef626838d75e69fb26',
'6509b19bd37433de13cba04063f879ed',
'90cb852cf345e04d508fe03f74089183',
'ecf4f0ab94f5a4083ef581584c82debd',
'4dee8fb18b5af024c012c77d21983f89',
'4c0931dd33d2f7e088955a929c8da9d9',
'43afea5a44582df0b76771e2892029fe',
'039be717f253f7b10ed1ce405de08b9f',
'0995e7526bf406557d1e55c9f650a2b5',
'9e9ff523f0448879c6cd521495fd758d',
'02bce1b62f5f5626621faa3cf7425529',
'616120feb399049e89585756e0cfc4d1',
'd977dd0e10adc6311525d4351fbf9c84',
'793037657df0b898fc5202b167272370',
'37de3dfb9d3bc0a2264adf8802fef726',
'f5cbf990604deb427ac48510d86f33e8',
'1cd8e0a97bf3552196f0f60eb3566ac7',
'b82ae67fe7545960b386ae50e3be37a2',
'6a283d0a1b1b98eb16f8941c2804aa1f',
'8c8544b6c129ad4a431be753143ed1c3',
'79eeda5f4c7fd2a0d483dc3d46fa5b3b',
'fc88cfe07a933a0c8624437cc174669d',
'9c1028bb28d1e14b22a05bd6531c3ea9',
'e481bb827fe08b4d4335225f6f125bde',
'91920559406bf05062e3d94c862d5817',
]
"""方法一：重复计算，耗时太久，已放弃"""
# people = dict(list(start_close.groupby(['device'])))
# dev = []
# for d in people.keys():
#     dev.append(d)
# res = pd.DataFrame({'device': dev})
# for i in topAPP:
#     tmp = []
#     for d in people.keys():
#         if i not in people[d]['app'].values:
#             tmp.append(0)
#         else:
#             people[d].drop(['device'], axis=1, inplace=True)
#             tmp.append(int(people[d].groupby(['app']).sum().loc[i]))
#     res[i+'_'+'time'] = tmp
# res.to_csv('top_15_APPs_used_time.csv')
# with pd.option_context('display.max_rows', None, 'display.max_columns', 100):
#     print(res.head())
"""方法二：利用以前跑出来的数据"""
# each = pd.read_csv('each app used time on each device.csv')
# each.drop(['Unnamed: 0'], axis=1, inplace=True)
# people = dict(list(each.groupby(['device'])))
# dev = []
# for d in people.keys():
#     dev.append(d)
# res = pd.DataFrame({'device': dev})
# for i in topAPP:
#     tmp = []
#     for d in people.keys():
#         if i not in people[d]['app'].values:
#             tmp.append(0)
#         else:
#             people[d].index = people[d]['app']
#             tmp.append(int(people[d]['totaltime'].loc[i]))
#     res[i+'_'+'time'] = tmp
#     print(res[i+'_'+'time'].value_counts())

# res.to_csv('top_40_APPs_used_time.csv')
# with pd.option_context('display.max_rows', None, 'display.max_columns', 100):
#     print(res.head())
"""合并"""
# data1 = pd.read_csv('train_006.csv')
# data2 = pd.read_csv('top_40_APPs_used_time.csv')
# data1.index = data1['device']
# data2.index = data2['device']
# data1.drop(['device'], axis=1, inplace=True)
# data1.drop(['st_open18'], axis=1, inplace=True)
# data2.drop(['Unnamed: 0'], axis=1, inplace=True)
# data2.drop(['device'], axis=1, inplace=True)
# data = data1.join([data2])
# data.to_csv('train_007.csv')

