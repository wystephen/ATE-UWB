# -*- coding:utf-8 -*-
# Created by steve @ 17-9-22 下午1:33
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

import math


import matplotlib.pyplot as plt

class ParticalFilter2D:
    '''
    particle filter , with only velocity ,orientation, and position(x,y).
    '''
    def __init__(self,particle_num=200,
                 observation_sigma=0.5,
                 noise_sigma = [0.1,10.0/180.0 * np.pi]):
        '''

        :param particle_num:
        :param observation_sigma: confidence for observation value(x,y)
        '''
        self.particle_num_ = particle_num

        self.p_state = np.zeros([self.particle_num_,4])

        self.p_cov = np.ones([self.particle_num_,1])
        self.p_cov /= float(self.particle_num_)

        self.observation_sigma_ = observation_sigma
        self.noise_sigma_ = noise_sigma

    def initial_filter(self,initial_state):
        '''

        :param initial_state:
        :return:
        '''

        self.p_state[:,0] = initial_state[0]
        self.p_state[:,1] = initial_state[1]

        self.p_state[:,2:] = np.random.normal(0.0,
                                              self.noise_sigma_,
                                              size=(self.particle_num_,2))

    def update_state(self,observation_pose,dt=0.5):

        # add noise and update state
        self.p_state[:,2] += np.random.normal(0.0,self.noise_sigma_[0],
                                               size = (self.particle_num_))
        self.p_state[:,3] += np.random.normal(0.0,self.noise_sigma_[1],
                                              size= self.particle_num_)
        # for i in range(self.particle_num_):
        #     while self.p_state[i,3] < -np.pi or
        #     if (self.p_state[i,3]

        # self.p_state[:,0] += dt * (self.p_state[:,2]*np.sin(self.p_state[:,3]))
        # self.p_state[:,1] += dt * (self.p_state[:,3]*np.cos(self.p_state[:,3]))
        self.p_state[:,0] += dt * self.p_state[:,2]
        self.p_state[:,1] += dt * self.p_state[:,3]



        # evaluate and compute state
        out_pose = np.zeros(2)
        for i in range(self.particle_num_):
            score = self.normal_pdf(np.linalg.norm(self.p_state[i,:2]-observation_pose),
                    0.0,
                    self.observation_sigma_) + 1e-10

            self.p_cov[i] *= (score+0.0000001)

            # out_pose += self.p_cov[i] * self.p_state[i,:2]
        plt.figure()
        plt.plot(self.p_cov)
        plt.show()
        # out_pose /= self.p_cov.sum()
        self.p_cov /= np.sum(self.p_cov)
        # print(self.p_cov)
        for i in range(self.particle_num_):
            out_pose += self.p_cov[i] * self.p_state[i,:2]


        # resample
        beta = np.zeros_like(self.p_cov)
        for i in range(self.particle_num_):
            if i == 0:
                beta[i] = self.p_cov[i]
            else:
                beta[i] = beta[i-1] + self.p_cov[i]

        tmp_sample_vector = self.p_state * 1.0
        tmp_cov_vecotr = self.p_cov * 1.0

        rnd_score = np.random.uniform(0.0,1.0,self.p_cov.shape)

        for i in range(self.particle_num_):
            index = 0
            while rnd_score[i] > 0.00001 and index < self.particle_num_-1:
                rnd_score -= tmp_cov_vecotr[index]
                index += 1
            self.p_state[i,:] = tmp_sample_vector[index,:]
            self.p_cov[i] = tmp_cov_vecotr[index]

        self.p_cov /= self.p_cov.sum()



        # output
        return out_pose


    def normal_pdf(self,x,miu,sigma):

        para1 = 1.0/(np.sqrt(2.0 * np.pi)*sigma)
        para2 = (x-miu)**2.0 / 2.0 / sigma /sigma

        return para1 * np.exp(-para2)






