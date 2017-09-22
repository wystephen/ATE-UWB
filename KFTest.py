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
    file = open('./Data/Point.txt','r')

    all_linex = file.readlines()

    src_pose = np.zeros([len(all_linex),2])
    src_index = 0

    for line_str in all_linex:

        result = re.findall('\d{1,3}\.{0,1}\d{1,2}',line_str.split(' ')[0])
        print(result)

        src_pose[src_index,0] = float(result[0])
        src_pose[src_index,1] = float(result[1])
        src_index += 1



    res_pose = src_pose * 1.0
    pf = particlefilter.ParticalFilter2D(2000,0.5,0.01)
    pf.initial_filter(res_pose[0,:])

    for i in range(src_pose.shape[0]):
        res_pose[i,:] = pf.update_state(src_pose[i,:])



    plt.figure()
    plt.grid(True)
    plt.plot(src_pose[:,0],src_pose[:,1],'r-+')
    plt.plot(res_pose[:,0],res_pose[:,1],'b-+')
    plt.show()





