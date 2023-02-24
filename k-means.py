from visual import prepare_data, plot_data_dynamic,plot_data
import matplotlib.pyplot as plt
import random
import math
import numpy as np 


def my_range(x_min, x_max):
    sub = x_max - x_min
    v = random.random()
    return v * sub + x_min

def el_dis(x, y):
    k = (x[0] -y[0])**2 + (x[1] - y[1]) **2 
    return math.sqrt(k)

def k_means_cluster(k, arr):
    """
    聚类算法
    """
    x_vec = [x[0] for x in arr]
    y_vec =[x[1] for x in arr]
    x_min, x_max = min(x_vec), max(x_vec)
    y_min, y_max = min(y_vec), max(y_vec)

    # 开始的随机中心
    mean_p = [(my_range(x_min, x_max), my_range(y_min, y_max)) for i in range(k)]

    cluster_indic = [0 for i in range(len(arr))]  # 存储arr 一行数据属于哪个簇
    dist_mat_tmp = [[0 for i in range(len(mean_p))] for j in range(len(arr))] # 存储 点到不同簇中心的距离

    def cal_dis(arr, mean_p):
        for i, p in enumerate(arr):
            for j,  m_p in enumerate(mean_p):
                dist_mat_tmp[i][j] = el_dis(p, m_p)

    def update_cluster_indic():
        """
        把点归类到自己最近的簇里
        """
        change = False
        for i,  point_to_all_mean in enumerate(dist_mat_tmp):
            min_ind = 0
            for ind in range(len(point_to_all_mean)):
                if point_to_all_mean[ind] < point_to_all_mean[min_ind]:
                    min_ind = ind
                    # 如果点最近的簇改变了， 则更新 
            if cluster_indic[i] != min_ind:
                change = True
                cluster_indic[i] = min_ind
        return change

    def update_mean_points():
        """
        更新质心
        """
        for ind in range(len(mean_p)):
            points_id_vec = [i for i, p in enumerate(cluster_indic) if  p ==ind]
            if (len(points_id_vec) == 0):
                continue
            x_sum = np.array([float(arr[k][0]) for k in points_id_vec], dtype=float)
            y_sum = np.array([float(arr[k][1]) for k in points_id_vec], dtype=float)
            mean_p[ind] = (np.average(x_sum), np.average(y_sum))
   
    updated = True
    while(updated):
        cal_dis(arr, mean_p)
        updated = update_cluster_indic()
        if updated:
            update_mean_points()
    return cluster_indic


if __name__ == "__main__":
    d = prepare_data("raw_data.txt")
    # fig = plt.figure()
    # plt.ion()
    # plot_data_dynamic(d, indic, fig)
    # for i in range(3, 10, 1):
    indic =  k_means_cluster(9, d)

    indic2 = list(set(indic))
    print("category number %d" % len(indic2))
    plot_data(d, indic, name="pic-%d" %100)


