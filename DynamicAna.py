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

if __name__ == '__main__':
    dir_name = "./Data/DynamicAna/"
    anchor_file_name = dir_name+"anchor-location (1).csv"

    beacon_sets = np.loadtxt(anchor_file_name,delimiter=',')

    control_points = np.loadtxt(dir_name+"Six-Control-Point.csv",delimiter=',')

    plt.figure()
    plt.title("beacon and control points")

    plt.plot(beacon_sets[:,0],beacon_sets[:,1],'r*',label = 'anchor')
    plt.plot(control_points[:,0],control_points[:,1],'b+',label='control points')

    plt.legend()
    plt.grid()
    plt.show()