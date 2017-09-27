# -*- coding:utf-8 -*-
# Created by steve @ 17-9-27 下午8:16
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


import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

import particlefilter

if __name__ == '__main__':
    dir_name = "./Data/DynamicAna/"
    anchor_file_name = dir_name+"anchor-location (1).csv"

    beacon_sets = np.loadtxt(anchor_file_name,delimiter=',')

    control_points = np.loadtxt(dir_name+"Six-Control-Point.csv",delimiter=',')

    observation_value = np.genfromtxt(dir_name+"T105-move-round1.csv",
                                      delimiter=',',
                                      filling_values=-10.0)

    plt.figure()
    plt.title("beacon and control points")
    plt.plot(beacon_sets[:,0],beacon_sets[:,1],'r*',label = 'anchor')
    plt.plot(control_points[:,0],control_points[:,1],'b+',label='control points')
    plt.legend()
    plt.grid()


    plt.figure()
    plt.grid()
    plt.title("range ")
    for i in range(observation_value.shape[0]):
        plt.plot(observation_value[:,i], label = str(i))
    plt.legend()


    res_pose = np.zeros([observation_value.shape[0],3])
    pf = particlefilter.ParticalFilter2D(300, 3.5, [0.00601, 0.00601])
    pf.initial_filter(res_pose[0, :])

    for i in range(observation_value.shape[0]):
        print("i:",i)

        res_pose[i, :] = pf.update_state_range(observation_value[i,:],0.5)



    plt.show()