"""train.py这个程序是把B组的训练集train_X.csv和我的train_50.csv拿来跑这些模型：
    随机森林、svm、xgboost、lightgbm
    都没有调参
    跑出来性别2类、年龄11类分类的错误率，和性别+年龄22类的log_loss"""

import pandas as pd


"""自己的,是train_50
    train_001
    train_002
    ...
    train_007"""
from sklearn.model_selection import train_test_split
data = pd.read_csv('train_007.csv')
X = data.drop(['device', 'target', 'age'], axis=1, inplace=False)
# Y = data['target']
data['combine'] = data['target']*11 + data['age']
Y = data['combine']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=666)
# Y_test = pd.Series(Y_test)
# print(Y_test.value_counts())
from sklearn import metrics
""" target就是性别(gender)，忘记改了"""
"""
   性别有2类，瞎猜猜对的概率(正确率)是0.5，      错误率是0.5
  年龄有11类，瞎猜猜对的概率(正确率)是1/11=0.09，错误率是0.91
"""
# from sklearn.ensemble import forest
# clf = forest.RandomForestClassifier()
# clf.fit(X_train, Y_train)
# Y_pred = clf.predict(X_test)
# Y_pred = pd.Series(Y_pred)
# print(Y_pred.value_counts())
# print(1 - metrics.accuracy_score(Y_test, Y_pred))   #错误率： gender: 0.38506666666666667
#                                                              #  age: 0.8526666666666667
# pro_pred = clf.predict_proba(X_test)
# print(metrics.log_loss(Y_test, pro_pred))    # 对数损失函数logloss: # gender: 0.9008140993504244
#                                                                       # age: 11.64369360139354
# # 随机森林得出的特征排名
# imp = pd.DataFrame({'feature': X.columns, 'importance': clf.feature_importances_})
# imp = imp.sort_values(['importance'], ascending=False).reset_index(drop=True)
# print(imp)
#
# from sklearn import svm
# clf = svm.SVC()
# clf.fit(X_train, Y_train)
# Y_pred = clf.predict(X_test)
# print(1 - metrics.accuracy_score(Y_pred, Y_test))     # gender: 0.35386666666666666
#                                                       #    age: 0.8432
#
# import lightgbm as lgb
# clf = lgb.LGBMClassifier()
# clf.fit(X_train, Y_train)
# Y_pred = clf.predict(X_test)
"""对比真实值和预测值，发现同样是女性的预测结果不好，但是lightgbm好于xgboost
1    9699
2    5301

1    14319
2      681     增加两个特征后为699 

按0.2比例拆分训练集时：
1    9413
2     587"""
# Y_pred = pd.Series(Y_pred)
# print(Y_pred.value_counts())
# print(1 - metrics.accuracy_score(Y_test, Y_pred))   # gender: 0.3496666666666667
#                                                          #  age: 0.8079333333333334
# print(metrics.confusion_matrix(Y_test, Y_pred))
# imp = pd.DataFrame({'feature': X.columns, 'importance': clf.feature_importances_})
# imp = imp.sort_values(['importance'], ascending=False).reset_index(drop=True)
# print(imp)
"""
lightbgm给出的性别分类的特征排名
              feature  importance
0           favor_app         266       一共2044个取值
1           totaltime         164
2           brand_num         155
3     avg_uesd_perday         143
4             numapps         138
5           mu_offset         132
6        mu_offset_cl         112
7             kurt_cl         106
8                kurt         105
9                skew         100
10         st_freq PM          96
11            skew_cl          95
12    st_freq nosleep          95
13    cl_freq nosleep          88
14  st_freq breakfast          87
15         st_freq AM          82
16  cl_freq breakfast          80
17         cl_freq AM          78
18     st_freq dinner          77
19      st_freq lunch          76
20      cl_freq lunch          74
21          opentimes          74
22              sigma          69
23      st_freq night          67
24     cl_freq dinner          65
25         cl_freq PM          57
26           sigma_cl          56
27      cl_freq night          48
28             has_33          34
29        f_label_big          28
30              has_4          23
31      f_label_small          20
32             has_26          18
33              has_2          17
34              has_8          17
35             has_12          15
36             has_28          10
37              has_1           7
38              has_5           7
39             has_30           5
40              has_0           3
41             has_18           3
42             has_35           3
43              has_3           2
44             has_37           1
45              has_9           1
46             has_13           1
47              has_6           0
48             has_25           0
49             has_29           0       
train_002.csv中得分为0的特征：
70              has_6           0
71              has_9           0
72             has_20           0
73             has_25           0
74             has_15           0
75             has_29           0
76             has_37           0"""
# pro_pred = clf.predict_proba(X_test)
# print(metrics.log_loss(Y_test, pro_pred))           # gender: 0.6361159465753837
                                                    # age: 2.1507906677447988
# import xgboost as xgb
# clf = xgb.XGBClassifier()
# clf.fit(X_train, Y_train)
# Y_pred = clf.predict(X_test)
# Y_pred = pd.Series(Y_pred)
# print(Y_pred.value_counts())
"""看预测出来的男女数目、比例
1    14732
2      268  可见女性的精确率是相当的低"""
# print(1 - metrics.accuracy_score(Y_test, Y_pred))       # gender: 0.3511333333333333
                                                         #age: 0.8067333333333333
# imp = pd.DataFrame({'feature': X.columns, 'importance': clf.feature_importances_})
# imp = imp.sort_values(['importance'], ascending=False).reset_index(drop=True)
# print(imp)
"""xgboost给出的性别分类的特征排名
              feature  importance
0           favor_app    0.151248
1           totaltime    0.079295
2             numapps    0.057269
3           brand_num    0.055800
4           mu_offset    0.052863
5     st_freq nosleep    0.045521
6              has_33    0.035242
7     cl_freq nosleep    0.033774
8     avg_uesd_perday    0.030837
9                skew    0.029369
10         st_freq PM    0.029369
11      st_freq night    0.027900
12  st_freq breakfast    0.026432
13       mu_offset_cl    0.026432
14               kurt    0.022026
15           sigma_cl    0.022026
16              has_8    0.022026
17            kurt_cl    0.022026
18         cl_freq AM    0.019090
19      cl_freq lunch    0.019090
20              has_4    0.019090
21              sigma    0.017621
22  cl_freq breakfast    0.016153
23         st_freq AM    0.016153
24             has_26    0.016153
25             has_12    0.013216
26          opentimes    0.011747
27            skew_cl    0.010279
28        f_label_big    0.010279
29             has_28    0.010279
30      f_label_small    0.008811
31     st_freq dinner    0.007342
32         cl_freq PM    0.007342
33      cl_freq night    0.005874
34      st_freq lunch    0.005874
35              has_1    0.004405
36              has_2    0.004405
37     cl_freq dinner    0.004405
38              has_5    0.002937
39             has_30    0.000000
40             has_29    0.000000
41             has_25    0.000000
42             has_18    0.000000
43              has_6    0.000000
44              has_9    0.000000
45             has_37    0.000000
46              has_3    0.000000
47             has_35    0.000000
48              has_0    0.000000
49             has_13    0.000000   """
# pro_pred = clf.predict_proba(X_test)
# print(metrics.log_loss(Y_test, pro_pred))               # gender: 0.6368297130599618
                                                        # age: 2.154465679160754
""" 性别+年龄的22分类，预测结果的对数损失函数"""
import lightgbm as lgb
clf = lgb.LGBMClassifier()
clf.fit(X_train, Y_train)
pro_pred = clf.predict_proba(X_test)
print(metrics.log_loss(Y_test, pro_pred))               # 2.8057400786697557
                                                        # train_002: 2.7869898480279254

imp = pd.DataFrame({'feature': X.columns, 'importance': clf.feature_importances_})
imp = imp.sort_values(['importance'], ascending=False).reset_index(drop=True)
with pd.option_context('display.max_rows', None, 'display.max_columns', 100):
    print(imp)


# import xgboost as xgb
# clf = xgb.XGBClassifier()
# clf.fit(X_train, Y_train)
# pro_pred = clf.predict_proba(X_test)
# print(metrics.log_loss(Y_test, pro_pred))               # 2.7887004455884297
"""逻辑回归暴露出了一个严重问题：预测的性别全是男性1
    没有学习到女性的特征"""
# from sklearn.linear_model import LogisticRegression
# clf = LogisticRegression()
# clf.fit(X_train, Y_train)
# Y_pred = clf.predict(X_test)
# Y_pred = pd.Series(Y_pred)
# print(Y_pred.value_counts())
# print(1 - metrics.accuracy_score(Y_test, Y_pred))
              # 原本训练集中性别2占0.34914
