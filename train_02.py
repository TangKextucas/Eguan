"""最新训练集是train_007，
    用lightgbm跑性别+年龄22类的log_loss
    以及性别+年龄22类的特征，我解释了每一个特征是什么意思
    没有调参
    训练集测试集拆分比例是0.2，随机种子是666"""

import pandas as pd
from sklearn.model_selection import train_test_split
data = pd.read_csv('train_007.csv')
X = data.drop(['device', 'target', 'age'], axis=1, inplace=False)
data['combine'] = data['target']*11 + data['age']
Y = data['combine']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=666)
from sklearn import metrics

""" 性别+年龄的22分类，预测结果的对数损失函数"""
import lightgbm as lgb
clf = lgb.LGBMClassifier()
clf.fit(X_train, Y_train)
pro_pred = clf.predict_proba(X_test)
print(metrics.log_loss(Y_test, pro_pred))

""" 性别+年龄的22分类，预测结果的特征排名"""
imp = pd.DataFrame({'feature': X.columns, 'importance': clf.feature_importances_})
imp = imp.sort_values(['importance'], ascending=False).reset_index(drop=True)
with pd.option_context('display.max_rows', None, 'display.max_columns', 100):
    print(imp)

"""程序跑出来的结果在特征排名.txt里面，我解释了每一个特征的含义"""
