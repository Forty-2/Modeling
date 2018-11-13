# -*-coding:utf-8 -*-
'''函数库'''
import numpy as np
import math

def distance_of_the_block(i,j,W):
    '''函数distance返回一个小方块M(i,j)到最近展板(墙)的距离'''
    list_of_d = []
    for q in list(range(1,len(W[1])+1)):
        for p in list(range(1,len(W)+1)):
            #遍历W(i,j)
            if W[p-1][q-1] == 1:
                d1 = (abs(i-p)+abs(j-q))
                d2 = (abs(i+1-p)+abs(j-q))
                d3 = (abs(i-p)+abs(j+1-q))
                d4 = (abs(i+1-p)+abs(j+1-q))
                d = min(d1,d2,d3,d4)
                list_of_d.append(d)
            else:
                pass
    return (min(list_of_d))

def importance_of_the_block(i,j,W):
    '''函数importance返回一个小方块的重要度I(i,j)'''
    if distance_of_the_block(i,j,W) <= 3:
        I = 1
    elif distance_of_the_block(i,j,W)<=7.5:
        I = 0.5
    elif distance_of_the_block(i,j,W)<=11.5:
        I = 0.3
    elif distance_of_the_block(i,j,W) <=15.5:
        I = 0.2
    elif distance_of_the_block(i,j,W) <=23:
        I = 0.1
    else:
        I = 0.05
    return I

def L(p,i,j,n,W):
    '''返回线段上p行对应q值'''
    if n == 1:
        return (p-1)*(j-1)/(i-1)
    elif n == 2:
        return ((p-1)-(i+1))*(j-len(W)+2)/(i-len(W[0])+2)+j+1
    else:
        raise ValueError

def blocks_on_view_part(i,j,W,n):
    '''返回方块的某角是否被挡'''
    #由于是方阵，故连线有一定角度，需考虑到一定的宽度，这就很烦了
    #我们这样定义以缩小误差：四个角未被挡，给他权重1；如果一个角被挡，给他权重0.75；0.5；0.25；0
    #再定义”角被挡“，角的坐标到摄像头的线段L，存在相连两点值为1，且一点在L上，一点在L下
    A = []
    if n == 1:
        for p in range(2,i):
            for q in range(2,j):
                d0 = ((q-1 - L(p,i,j,n,W)))
                if W[p-1][q-1] == 0:
                    A.append(0)
                elif d0 == 0:
                    A.append(1)
                else:
                    d1 = d0*((q+1 - L(p,i,j,n,W))*W[p-1][q])
                    d2 = d0*((q-1 - L(p,i,j,n,W))*W[p-1][q-2])
                    d3 = d0*((q - L(p+1,i,j,n,W))*W[p][q-1])
                    d4 = d0*((q - L(p-1,i,j,n,W))*W[p-2][q-1])
                    d5 = d0*((q+1 - L(p+1,i,j,n,W))*W[p][q])
                    d6 = d0*((q+1 - L(p-1,i,j,n,W))*W[p-2][q])
                    d7 = d0*((q-1 - L(p+1,i,j,n,W))*W[p][q-2])
                    d8 = d0*((q-1 - L(p-1,i,j,n,W))*W[p-2][q-2])
                    if (d1 or d2 or d3 or d4 or d5 or d6 or d7 or d8)< 0:
                        A.append(1)
                    else:
                        A.append(0)
    elif n == 2:
        for p in range(i+1,len(W)-2):
            for q in range(j+1,len(W[0])-2):
                d0 = ((q - L(p,i,j,n,W)))
                if W[p-1][q-1] == 0:
                    A.append(0)
                elif d0 == 0:
                    A.append(1)
                else:
                    d1 = d0*((q+1 - L(p,i,j,n,W))*W[p-1][q])
                    d2 = d0*((q-1 - L(p,i,j,n,W))*W[p-1][q-2])
                    d3 = d0*((q - L(p+1,i,j,n,W))*W[p][q-1])
                    d4 = d0*((q - L(p-1,i,j,n,W))*W[p-2][q-1])
                    d5 = d0*((q+1 - L(p+1,i,j,n,W))*W[p][q])
                    d6 = d0*((q+1 - L(p-1,i,j,n,W))*W[p-2][q])
                    d7 = d0*((q-1 - L(p+1,i,j,n,W))*W[p][q-2])
                    d8 = d0*((q-1 - L(p-1,i,j,n,W))*W[p-2][q-2])
                    if (d1 or d2 or d3 or d4 or d5 or d6 or d7 or d8)< 0:
                        A.append(1)
                    else:
                        A.append(0)
    else:
        raise ValueError
    if int(any(A)) == 1:
        return 0
    else:
        return 1


def wholeness_of_surveillance(i,j,W,n):
    '''返回小方格监控完整度'''
    record = blocks_on_view_part(i,j,W,n)+blocks_on_view_part(i+1,j,W,n)\
        +blocks_on_view_part(i,j+1,W,n)+blocks_on_view_part(i+1,j+1,W,n)
    return (record*0.25)

def angle_to_the_cam(i,j,W,n):
    '''返回方格到摄像头连线与墙的夹角'''
    if n == 1:
        return math.atan((i-0.5)/(j-0.5))
    elif n == 2:
        return math.atan(((i-0.5)-len(W)+1)/((j-0.5)-len(W[0]+1)))
    else:
        raise ValueError

def monitoring_coverage_time(i,j,W,n):
    '''返回每个小方块半周期被两探头监控的时间'''
    #假设每次转完半周期，摄像头停止1s
    if math.pi/6 <= angle_to_the_cam(i,j,W,n) <= math.pi/3:
        return 4.5
    elif 0 <= angle_to_the_cam(i,j,W,n) < math.pi/6:
        return (1+angle_to_the_cam(i,j,W,n)*27/math.pi)
    elif math.pi/3 <= angle_to_the_cam(i,j,W,n) <= math.pi/2:
        return (1+(math.pi/2-angle_to_the_cam(i,j,W,n))*27/math.pi)

def security_of_the_block(i,j,W):
    '''返回小方格M(i,j)的安全系数'''
    m = monitoring_coverage_time(i,j,W,1)*wholeness_of_surveillance(i,j,W,1)+monitoring_coverage_time(i,j,W,2)*wholeness_of_surveillance(i,j,W,2)
    return m

def security_index_of_the_block(i,j,W):
    return security_of_the_block(i,j,W)*importance_of_the_block(i,j,W)

def whole_security_index(W):
    '''返回整体安全系数'''
    s = 0
    for i in range(1,len(W)):
        for j in range(1,len(W[0])):
            s = s + security_index_of_the_block(i,j,W)
    return s

def perfect_solution(W):
    m = 0
    for i in range(1,len(W)):
        for j in range(1,len(W[0])):
            m = m + importance_of_the_block(i,j,W)
    return 10*1*m

def result(W):
    return whole_security_index(W)/perfect_solution(W)
