# -*- coding:utf-8 -*-
# Created by steve @ 17-9-26 下午4:26
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

# import statmodels.api as sm

import os

list  # __getitem__

if __name__ == '__main__':
    # TODO:Never use it before change the way of save error and std..
    dir_name = "./Data/SignalAna/"
    anchor_sets_file_name = dir_name + "anchor-location.csv"
    data_dir = dir_name + "data/"

    beacon_sets = np.loadtxt(anchor_sets_file_name, delimiter=',')
    print(beacon_sets)

    points = 0
    for file_name in os.listdir(data_dir):
        if '.csv' in file_name:
            points += 1
    test_point_sets = np.zeros([points, 3])
    test_point_name = list()

    points = 0
    for file_name in os.listdir(data_dir):
        if '.csv' in file_name:
            print("filename :", data_dir + file_name)
            tmp_data = np.genfromtxt(data_dir + file_name,
                                     delimiter=',',
                                     filling_values=-1000.0)

            tag_pose = np.zeros(3)
            tag_pose[0] = float(file_name.split('-')[1])
            tag_pose[1] = float(file_name.split('-')[2].split('.csv')[0])
            tag_pose[2] = 1.7
            test_point_sets[points, :] = tag_pose
            test_point_name.append(file_name.split('.csv')[0])
            points += 1

            real_distance = np.zeros(beacon_sets.shape[0])

            # plot error
            plt.figure()
            for i in range(beacon_sets.shape[0]):
                real_distance[i] = np.linalg.norm(
                    beacon_sets[i, :] - tag_pose
                )
                plt.plot((tmp_data[:, i] - real_distance[i]),
                         '.',
                         label='A' + str(i))
            plt.grid()
            plt.legend()
            plt.title(file_name)
            plt.ylim(-3.0, 3.0)
            plt.savefig(data_dir + file_name.split('.csv')[0].split('T105-')[1] + 'error' + '.jpg', dpi=1000)
            # plt.show()

            # plot real and data
            plt.figure()
            for i in range(beacon_sets.shape[0]):
                plt.plot(tmp_data[:, i], '.', label='A' + str(i))

            plt.grid()
            plt.legend()
            plt.title(file_name + 'measurement')
            plt.ylim(0.0, np.max(tmp_data))
            plt.savefig(data_dir + file_name.split('.csv')[0].split('T105-')[1] + 'measurement' + '.jpg', dpi=1000)

            errandcov = np.zeros([beacon_sets.shape[0], 2])
            # plt.figure()
            for i in range(beacon_sets.shape[0]):
                normal_list = np.where(tmp_data[:, i] > 0.0)
                # print('normal_list', normal_list)
                tmp_col_data = tmp_data[normal_list[0], i]
                # plt.plot(tmp_col_data,'r-',label=str(i))
                errandcov[i, 0] = np.mean(tmp_col_data - real_distance[i])
                errandcov[i, 1] = np.std(tmp_col_data - real_distance[i])
            np.savetxt(dir_name + file_name.split('.csv')[0] + 'errandcov.txt',
                       errandcov,
                       delimiter=',')

            # plt.show()



            print(real_distance)

    plt.figure()
    plt.title("Anchor and test points")
    plt.plot(beacon_sets[:, 0], beacon_sets[:, 1], 'r*', label='anchor')
    for i in range(beacon_sets.shape[0]):
        plt.text(beacon_sets[i, 0], beacon_sets[i, 1], 'A' + str(i))
    plt.plot(test_point_sets[:, 0], test_point_sets[:, 1], 'b*', label='test points')
    for i in range(test_point_sets.shape[0]):
        plt.text(test_point_sets[i, 0], test_point_sets[i, 1],
                 test_point_name[i])
    plt.grid()
    plt.legend()
    plt.savefig(dir_name + 'plane_show.jpg',dpi=1000)
