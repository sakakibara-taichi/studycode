#fileを読み込んで入力としてpredictorを作成する、出力を別のfileに出力をしてみる

import chainer
import chainer.functions as F
import chainer.links as L
from chainer import training
from chainer.training import extensions
from numpy.random import *
import numpy as np
from chainer import serializers
import csv
from learnerT1 import MultiRegression
import pandas as pd



# 乱数で入力を作成(25380×時間数Δの配列)
# test = randint(0,15,size = 25380)
# test = test.astype(np.float32)
# test=test.reshape(1,25380)
# print(test)
# print(test.shape)
# correct = np.random.randint(1,15,(1,282))
# correct = correct.astype(np.float32)
#print(type(test))



# CSVをdataframeとして読み込む
df = pd.read_csv("loc241t1k30p3T6.csv")
df = df.iloc[:,1:]
# numpy配列に変更
data = df.as_matrix()
# print(type(test))
# print(test.shape)
data = data.astype(np.float32)
test,correct = np.split(data,[data.shape[1]-241],axis=1)
print("done!!")

# なんちゃってmodelを作成する
# Network definition
# class MLP(chainer.Chain):

#     def __init__(self, n_units, n_out):
#        super(MLP, self).__init__()
#        with self.init_scope():
#            # the size of the inputs to each layer will be inferred            self.l1 = L.Linear(None, n_units)  # n_in -> n_units
#             self.l1 = L.Linear(None, n_units)
#             self.l2 = L.Linear(None, n_units)  # n_units -> n_units
#             self.l3 = L.Linear(None, n_out)  # n_units -> n_out

#     def __call__(self, x):
#         h1 = F.relu(self.l1(x))
#         h2 = F.relu(self.l2(h1))
#         return self.l3(h2)
#         print(self.l3(h2))
# #中間層ノード数210、出力層ノード数210
# model = MLP(38070,282)




# 学習済modelを更新する
# modelをロードする時、先にmodelの枠組みを用意してから重みなどをロードしてから始める
# セーブした時の構成のmodelを作る
model = MultiRegression(7230,241)
chainer.serializers.load_npz("T6mymodel2500.npz", model)




x = test
# .dataでnumpy配列の形式にしている？
output = model(x).data
#print(output)
#loss = F.mean_absolute_error(output, correct)

T = 360
z = 0
for a in range(0, T-1) :
    for b in range(0, 240):
        if correct[a,b] != 0:
            y = abs(correct[a,b]-output[a,b])/correct[a,b]
            z = z + y
        else:
            pass

MAPE = 100*z/(T*241)


# print("出力")
# print(output)
# print("正解")
# print(correct)
print(MAPE)

#print(output)
#整数表示に丸めている
# output = output.astype(np.int32)
#print(output.shape)

# dataframeに変換している→CSVに書き込むには必要な作業
# df = pd.DataFrame(output)
# print(df)
# print(type(df))
# df.to_csv("C:/Users/theta/Dropbox/study_B4/output/output_demo/output_demo.csv")
# print("dataframe to csv success")
