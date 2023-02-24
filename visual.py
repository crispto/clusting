import matplotlib.pyplot as plt
import json


# 归类 cluster 输出的 label id, 一般不需要
def trans_code(label_data):
    print("len label_data", len(label_data))
    q = list(set(label_data))
    q_map = {q[i]: i for i in range(len(q))}
    v = [q_map[k] for k in label_data]
    return v 


def plot_data(data, labels, name="pic"):
    """
    绘图，data 为聚类输入， labels 为聚类输出的 label 数组
    """
    colors = 'bgrcmyk'
    markers = 'ov^<>s*hH+'
    for i, p in enumerate(data):
        id = labels[i]
        c = markers[id//(len(colors))]
        color = colors[id % (len(colors))]
        plt.plot(p[0], p[1], c, color=color)
    plt.savefig("%s.png" %name)

def plot_data_dynamic(data, labels, fig):
    fig.clf()
    colors = 'bgrcmyk'
    markers = 'ov^<>s*hH+'
    for i, p in enumerate(data):
        id = labels[i]
        c = markers[id//(len(colors))]
        color = colors[id % (len(colors))]
        plt.plot(p[0], p[1], c, color=color)
        plt.pause(0.2)

def prepare_label(filepath):
    """
    parse label file 
    """
    f = open(filepath, 'r')
    data = []
    for line in f.readlines():
        data.append(int(line))
    return data

def prepare_data(filepath):
    """
    parse raw data file 
    """
    raw_f = open(filepath, 'r')
    raw_data = []
    for line in raw_f.readlines():
        q = line.split()
        raw_data.append([float(x) for x in q])
    return raw_data

if __name__ == "__main__":
    label_path = "label.txt"
    raw_path = "raw_data.txt"




    label_data = prepare_label(label_path)
    raw_data = prepare_data(raw_path)

    print("label_data: ", label_data)
    label_data_encode = trans_code(label_data)
    print("label: ", label_data_encode)
    plot_data(raw_data, label_data_encode)