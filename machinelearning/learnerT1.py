# learner_phaze1_v3はtrainの関数でトレーニングしている
# leaner_phaze1_v2はtrainer.runを実行しているが上手くいかなかった
from __future__ import print_function
import argparse
import chainer
from chainer import Chain, Variable
import chainer.functions as F
import chainer.links as L
from chainer import training
from chainer.training import extensions
from chainer import serializers
from numpy.random import *
import numpy as np
import pandas as pd
import time


# Network definition
#重回帰のクラスを作成
class MultiRegression(Chain):
    def __init__(self, n_units, n_out):
        #super(MultiRegression, self).__init__()
        super().__init__()
        with self.init_scope():
            # the size of the inputs to each layer will be inferred
            #中間層が２層の構造
            self.l1 = L.Linear(None, n_units)  # n_in -> n_units
            self.l2 = L.Linear(None, n_units)  # n_units -> n_units
            self.l3 = L.Linear(None, n_out)  # n_units -> n_out

    def __call__(self, x):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        return self.l3(h2)

def normal_equation(test, train1):
    xs2 = np.hstack((np.ones((test.shape[0], 1), "f"), test))
    theta = np.linalg.inv(xs2.T.dot(xs2)).dot(xs2.T).dot(train1)
    return theta

#正規化をしている
def normalize(test, train1):
    # xmeans = np.mean(test, axis = 0)
    # # print("xmeans = " + np.array_str(xmeans))
    # xstds  = np.std(test, axis = 0)
    # # print("xstds = " + np.array_str(xstds))
    # ymean = np.mean(train1)
    # # print("ymean = %f" % ymean)
    # ystd  = np.std(train1)
    # # print("ystd = %f" % ystd)
    # nxs = (test - xmeans) / xstds
    # nys = (train1 - ymean) / ystd
    # return nxs, nys, xmeans, xstds, ymean, ystd

    xmax = np.max(test)
    xmin = np.min(test)
    x1 = np.ones_like(test)
    ymax = np.max(train1)
    ymin = np.min(train1)
    y1 = np.ones_like(train1)

    nxs = (test - xmin * x1)/(xmax - xmin)
    nys = (train1 - ymin * y1)/(ymax - ymin)
    return nxs, nys, xmax, xmin, ymax, ymin


def denormalize_params(nW, nb, xmeans, xstds, ymean, ystd):
    W = ystd / xstds * nW
    b = ymean - (sum(ystd / xstds * xmeans * nW) + ystd * nb)
    return W, b

#学習させている
def train(model, test, train1, xmeans, xstds, ymean, ystd):
    # test = Variable(test)
    # train1 = Variable(train1)

    alpha = 0.5
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(model)
    start_time = time.time()
    
    #100回学習させている
    for i in range(2500):
        # grad(勾配)を初期化している！！重要！！
        model.l3.zerograds()
        model.l2.zerograds()
        model.l1.zerograds()
        print("=== Epoch %d ===" % (i + 1))
        yp = model(train1)
        # print("OK")
        print(yp.shape)
        # 形式がわからない→test,trainを同じ形にしないと動作しない
        loss = F.mean_squared_error(yp, test)
        # print("OK1")
        loss.backward()
        # print("model.l1.W.data = %s" % np.array_str(model.l1.W.data))
        # print("model.l1.W.grad = %s" % np.array_str(model.l1.W.grad))
        # print("model.l1.b.data = %s" % np.array_str(model.l1.b.data))
        # print("model.l1.b.grad = %s" % np.array_str(model.l1.b.grad))
        print("loss = %f" % loss.data)
        # print("")
        optimizer.update()
        # return model.l1.W.data[0], model.l1.b.data[0]
        # W, b = denormalize_params(model.l1.W.data[0], model.l1.b.data[0], xmeans, xstds, ymean, ystd)
        if (i+1)%500 ==0:
            serializers.save_npz("T1mymodel{0:04d}.npz".format(i+1), model)
            # f.write('TIME: '+str(time.time()-start)
            nowtime = time.time()
            duration = time.time() - start_time
            # print("TIME = ")
            # print(duration)
            # print("")
            f = open('T1time.txt','a')
            f.write('TIME'+str(i+1)+ '=' + str(duration)+'\n')
        # return W,b
    print("end")

def main():
    #パラメータを与えている
    parser = argparse.ArgumentParser(description='Chainer example: MNIST')
    parser.add_argument('--batchsize', '-b', type=int, default=100,
                        help='Number of images in each mini-batch')
    parser.add_argument('--epoch', '-e', type=int, default=2500,
                        help='Number of sweeps over the dataset to train')
    parser.add_argument('--frequency', '-f', type=int, default=-1,
                        help='Frequency of taking a snapshot')
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help='GPU ID (negative value indicates CPU)')
    parser.add_argument('--out', '-o', default='result',
                        help='Directory to output the result')
    parser.add_argument('--resume', '-r', default='',
                        help='Resume the training from snapshot')
    parser.add_argument('--unit', '-u', type=int, default=1000,
                        help='Number of units')
    parser.add_argument('--noplot', dest='plot', action='store_false',
                        help='Disable PlotReport extension')
    args = parser.parse_args()

    print('GPU: {}'.format(args.gpu))
    print('# unit: {}'.format(args.unit))
    print('# Minibatch-size: {}'.format(args.batchsize))
    print('# epoch: {}'.format(args.epoch))
    print('')

    model = MultiRegression(7230,241)

    df = pd.read_csv("loc241t6k30p3T1.csv")
    # df = pd.read_csv("data2/loc241t5k180p1T6_kai.csv")
    df = df.iloc[:,1:]
    data = df.as_matrix()
    data=data.astype(np.float32)
    train1,test = np.split(data,[data.shape[1]-241],axis=1)

    #test = np.random.randint(1,15,(5,1050))
    #test = test.astype(np.float32)

    # print(type(test))
    # print(test.shape)
    # print(test)

    #train1 = np.random.randint(1,15,(5,210))
    #train1 = train1.astype(np.float32)

    # print(type(train1))
    # print(train1.shape)
    # print(train1)

    nxs, nys, xmax, xmin, ymax, ymin = normalize(test, train1)
    train(model,nxs, nys, xmax, xmin, ymax, ymin)
    # W, b = denormalize_params(nW, nb, xmeans, xstds, ymean, ystd)

    # serializers.save_npz("mymodel.npz", model)
    print("npz save success")

if __name__ == '__main__':
    main()
