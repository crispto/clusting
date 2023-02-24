import numpy as np
from visual import plot_data, prepare_data
def get_data():
    k = [[3,4,3,2,1],[4,3,5,1,1],[3,5,3,3,3],[2,1,3,3,2],[1,1,3,2,3]]
    return np.array(k)

def cal_similarity(data):
    row, col = np.shape(data)
    s = np.zeros((row, row))
    for i in range(row):
        for j in range(row):
            if i != j:
                s[i][j] = -1 *np.sqrt(np.square(data[i,:] - data[j,:]).sum())
    mini_num = np.min(s)
    for i in range(row):
        s[i][i] = mini_num
    return s

                    

def  affinity(s_mat, max_iter = 200, damp = 0.5, max_convergence_iter= 15, close_thre = 1.0, crite_sample_rate= 1.0):
    """
    s_mat 是相似度矩阵
    """
    s = s_mat[:,:] # preference
    row, col = np.shape(s)
    assert(row == col)
    r = np.zeros((row, col))
    r_new = np.zeros((row, col))
    a = np.zeros((row, col))
    a_new = np.zeros((row, col))
    
    c = np.zeros((row, col))
    crite = np.apply_along_axis(np.max, 1, c)

    max_tmp1 = np.zeros((row, col)) # middle result
    c_tmp = np.zeros((row, col)) # middle result for compare
    iter_num = 0
    no_change_count = 0

    def is_close(d1, d2, thre):
        
        for i in range(len(d1)):
            if (abs(d1[i] - d2[i]) > thre):
                return False
        return True 

    def find_top2(row_vec):
        top1_index, top2_index = 0, 0
        for i in range(len(row_vec)):
            if row_vec[i] >= row_vec[top1_index]:
                top2_index = top1_index
                top1_index = i
        if top1_index == 0:
            top2_index, _ = find_top2(row_vec[1:])
            top2_index+=1

        return top1_index, top2_index
    while(1):
        if iter_num >= max_iter:
            print("over max iter")
            break
        if no_change_count >= max_convergence_iter:
            print("clusing success!")
            break
        iter_num+=1
        #update r 
        a_plus_s = a + s
        max_and_second_max = np.apply_along_axis(find_top2, 1, a_plus_s) #get max and second max number
        for i in range(row):
            for k in range(row):
                if k == max_and_second_max[i][0]:
                    max_tmp1[i][k] = a_plus_s[i][max_and_second_max[i][1]]
                else:
                    max_tmp1[i][k] = a_plus_s[i][max_and_second_max[i][0]]
        r_new = s - max_tmp1 # equation 1

        r = damp * r + (1-damp)*r_new # 阻尼
        # equation 2 
        for k in range(col):
            one_vec = r[:, k]
            v = [one_vec[i] for i in range(row) if i != k and one_vec[i] > 0 ]
            a_new[k][k] =  np.sum(v)
           
        # equation 3 
        for i in range(row):
            for k in range(col):
                if  i == k:
                    continue
                one_vec = r[:, k]
                v= [one_vec[j] for j  in range(row) if j != k and j != i and one_vec[j] > 0]
                tmp = r[k][k] + np.sum(v)
                if tmp < 0:
                    a_new[i][k] = tmp
                else:
                    a_new[i][k] = 0

        a = damp *a + (1-damp) *a_new # 阻尼
        # equation 4
        c_tmp = r + a
        crite_new = np.apply_along_axis(np.max, 1, c_tmp)
        # updated
        if not is_close(crite_new, crite, close_thre):
            c = c_tmp
            crite = crite_new
            no_change_count = 0
        else:
            no_change_count += 1
        if (iter_num % 20 == 0):
            print("iter_num: {}, crite: {}\n".format(iter_num, crite.T))
    """
    ter_num: 40, crite: [ 332.86757208 1018.2111493   341.87726824  342.93175844    3.31115455
    4.49263823    4.49823305   53.59163621  381.50256586   30.30504531
   29.67660134   36.55419564   36.5528782    34.8132065    30.37200374
  126.57439581   37.30265728   32.58616105   31.27250351   66.33391136
  129.60979484  417.55808076  129.5219754   127.89488225   31.09449961
   30.29273713   28.06028914   28.58754099   28.67915103   29.04115124
   28.28686602   36.52039506   24.43905025   25.9138526    31.70470689
   26.63367793   29.09702608]
    """
    #output,需要再做一次相近和合并
    keys = []
    vals = []
    for x in crite:
        find =False
        for i, y in enumerate(i,v):
            if y-crite_sample_rate < x and x < y +crite_sample_rate:
                find = True
        





    se = {}
    for i, x in enumerate(set(crite)):
        se[x] = i
    v = [0 for i in range(len(crite))]

    for i in range(len(crite)):
        v[i] = se[crite[i]]
    return v

        




    

if __name__ == "__main__":
    d = prepare_data("raw_data.txt")
    s = cal_similarity(np.array(d))
    label = affinity(s, close_thre=4.)
    print("clutering result: {}, len: {}".format(label, len(label)))
    plot_data(d, label)

