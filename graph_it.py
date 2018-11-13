# -*-coding:utf-8 -*-
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import functions_lib as fl

def importance_array(W):
    I = []
    for i in range(1,len(W)):
        row = []
        for j in range(1,len(W[0])):
            row.append(fl.importance_of_the_block(i,j,W))
        I.append(row)
    return np.array((I))

def security_array(W):
    S = []
    for i in range(1,len(W)):
        row = []
        for j in range(1,len(W[0])):
            row.append(fl.security_of_the_block(i,j,W))
        S.append(row)
    return np.array((S))

def block_array(W,n):
    B = []
    for i in range(1,len(W)):
        row = []
        for j in range(1,len(W[0])):
            row.append(fl.blocks_on_view_part(i,j,W,n))
        B.append(row)
    return np.array((B))

#下面代码改编自matplotlib的官方Gallery中Creating annotated heatmaps的
# A simple categorical heatmap
def graph_importance(W):
    fig, ax = plt.subplots()
    im = ax.imshow(importance_array(W))
    ax.set_xticks(np.arange(len(W[0]-1)))
    ax.set_yticks(np.arange(len(W)-1))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
    fig.tight_layout()
    plt.show()

def graph_security_index(W):
    fig, ax = plt.subplots()
    im = ax.imshow(security_array(W))
    ax.set_xticks(np.arange(len(W[0]-1)))
    ax.set_yticks(np.arange(len(W)-1))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
    fig.tight_layout()
    plt.show()

def graph_whether_blocked(W,n):
    fig, ax = plt.subplots()
    im = ax.imshow(block_array(W,n))
    ax.set_xticks(np.arange(len(W[0]-1)))
    ax.set_yticks(np.arange(len(W)-1))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
    fig.tight_layout()
    plt.show()