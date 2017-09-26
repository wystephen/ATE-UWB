# -*- coding:utf-8 -*-
# Created by steve @ 17-9-22 上午8:24
'''
                   _ooOoo_ 
                  o8888888o 
                  88" . "88 
                  (| -_- |) 
                  O\  =  /O 
               ____/`---'\____ 
             .'  \\|     |//  `. 
            /  \\|||  :  |||//  \ 
           /  _||||| -:- |||||-  \ 
           |   | \\\  -  /// |   | 
           | \_|  ''\---/''  |   | 
           \  .-\__  `-`  ___/-. / 
         ___`. .'  /--.--\  `. . __ 
      ."" '<  `.___\_<|>_/___.'  >'"". 
     | | :  `- \`.;`\ _ /`;.`/ - ` : | | 
     \  \ `-.   \_ __\ /__ _/   .-` /  / 
======`-.____`-.___\_____/___.-`____.-'====== 
                   `=---=' 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
         佛祖保佑       永无BUG 
'''

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import re

import particlefilter

if __name__ == '__main__':
    file = open('./Data/Point.txt', 'r')

    all_linex = file.readlines()

    src_pose = np.zeros([len(all_linex), 2])
    src_index = 0

    for line_str in all_linex:
        result = list()
        # result = re.findall('\d{1,3}\.{0,1}\d{0,2}',line_str.split(' ')[0])
        # print(result,line_str)
        result.append(line_str.split(':')[1].split(',')[0])
        result.append(line_str.split(',')[1].split(' ')[0])

        src_pose[src_index, 0] = float(result[0])
        src_pose[src_index, 1] = float(result[1])
        src_index += 1

    res_pose = src_pose * 1.0
    pf = particlefilter.ParticalFilter2D(300, 2.5, [0.051, 0.051])
    pf.initial_filter(res_pose[0, :])

    for i in range(100):
        print("i:",i)

        res_pose[i, :] = pf.update_state(src_pose[i, :], dt=0.5)

    np.savetxt('test_data.txt', src_pose)

    plt.figure()
    plt.grid(True)
    plt.plot(src_pose[:100, 0], src_pose[:100, 1], 'r-+')
    plt.plot(res_pose[:100, 0], res_pose[:100, 1], 'b-+')
    for i in range(100):
        plt.plot([src_pose[i,0],res_pose[i,0]],
        [src_pose[i,1],res_pose[i,1]],'y-')

    plt.figure()
    plt.plot(src_pose[:, 0], 'r-*')
    plt.plot(src_pose[:, 1], 'b-*')
    plt.show()
