#! /usr/bin/env python
# -*- coding:utf-8 -*-
#
# written by taichi sakakibara, 2018/5/26.
""" This program is the simuration of random walk in two-dimentional space.
"""
#ただの4点だけの移動をランダムで行う
import numpy as np
from numpy.random import *#乱数を生成
# from agent import Agent


#classでエージェントの生成したい
# class Agent:
#     def__init__(self,p)    
#     #初期の場所の設定
#     P = np.array([[0,0],[1,0],[0,1],[1,1]]])
    


"""頂点(エリアの大きさ)の定義"""
P = np.array([[0,0],[0,2],[2,2],[2,0]]) #4点それぞれを定義

"""速度を設定"""
#それぞれの場所での速度を定義する
v0 = np.array([[1,0],[0,1]])#左下
v1 = np.array([[1,0],[0,-1]])#左上
v2 = np.array([[-1,0],[0,-1]])#右上
v3 = np.array([[-1,0],[0,1]])#右下


"""userの初期位置を決定する"""
user = ([0,0])
#初期位置を設定するために0~4の乱数を生成
a = randint(4)
user = user + P[a]
print("スタート地点は"+str(user))


"""userの試行"""
for i in range(10):
    #角に到達した時の2択を実行するための乱数
    b = randint(2)
    
    #位置によって処理を行う
    if (user == P[0]).all():#userが[0,0]
        #上か右か選択
        user = user + v0[b]
        vc = v0[b]
    elif (user == P[1]).all():#userが[0,1]
        user = user + v1[b]
        vc = v1[b]
    elif (user == P[2]).all():#userが[1,1]
        user = user + v2[b]
        vc = v2[b]
    elif (user == P[3]).all():#userが[1,0]
        user = user + v3[b]
        vc = v3[b]
    else:                     #userが頂点以外にいる
        user = user + vc     #保持する速度で移動を継続する


    # print(i+1)
    print("vc = " + str(vc))
    print("位置は"+str(user))

