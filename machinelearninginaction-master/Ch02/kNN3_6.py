from numpy import *
import numpy as np
import operator
import pandas as pd


def create_dataset():
    """

    :return: group, labels
    """
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

def classify0(in_x, dataset, labels, k):
    """
    :param in_x: 一个新的数据
    :param dataset: 数据集x
    :param labels: 数据集y
    :param k: Neighbors
    :return: 数据离得最近的k的点中标记次数最多的label
    """
    dataset_size = dataset.shape[0]
    diff_mat = tile(in_x, (dataset_size, 1)) - dataset
    sq_diff_mat = diff_mat ** 2
    sq_distances = sq_diff_mat.sum(axis=1)
    distances = sq_distances ** 0.5
    sorted_dist_indicies = np.argsort(distances)

    class_count = {}
    for i in range(k):
        voteILabel = labels[sorted_dist_indicies[i]]
        class_count[voteILabel] = class_count.get(voteILabel, 0) + 1
    sorted_class_count = sorted(class_count.items(),
                                key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]

def file_to_matrix(filename):
    #
    fr = open(filename)
    array_lines = fr.readlines()
    num_lines = len(array_lines)
    return_mat = zeros((num_lines, 3))
    df = pd.read_csv(filename, header=None, sep='\t')
    class_label_vector = []
    for i in range(num_lines):
        return_mat[i] = df.iloc[i, :3]
        class_label_vector.append(int(df.iloc[i, -1]))

    return return_mat, class_label_vector

def auto_norm(dataset):
    min_vals = dataset.min(0) # 选取到每列的最小值
    max_vals = dataset.max(0)
    ranges = max_vals - min_vals
    norm_dataset = zeros(shape(dataset))
    m = dataset.shape[0]
    norm_dataset = dataset - tile(min_vals, (m,1)) # tile函数
    norm_dataset = norm_dataset / tile(ranges, (m,1))
    return norm_dataset, ranges, min_vals

def dating_class_test():
    hot_ratio = 0.10
    dating_datamat, dating_labels = file_to_matrix('/Users/weizheng/PycharmProjects/machinelearninginaction-master/Ch02/datingTestSet2.txt')
    norm_mat, ranges, min_vals = auto_norm(dating_datamat)
    m = norm_mat.shape[0]
    num_test_vecs = int(m*hot_ratio)
    error_count = 0.0
    for i in range(num_test_vecs):
        classifier_result = classify0(norm_mat[i,:], norm_mat[num_test_vecs:m,:],
                                      dating_labels[num_test_vecs:m],3)
        print("the classifier came back with: %d, the real answer is: %d" % (classifier_result, dating_labels[i]))
        if (classifier_result != dating_labels[i]): error_count += 1.0
    print ("The total error rate is %f" % (error_count/float(num_test_vecs)))

def classify_person():
    result_list = ['not at all', 'in small doses', 'in large doses']
    percent_tats = float(input("percentage of time spent playing video games?"))
    ff_miles = float(input("frequent flier miles earned per year?"))
    ice_cream = float(input("liters of ice cream consumed per year?"))
    dataing_datamat, dating_labels = file_to_matrix('/Users/weizheng/PycharmProjects/machinelearninginaction-master/Ch02/datingTestSet2.txt')
    norm_mat, ranges, min_vals = auto_norm(dataing_datamat)
    in_arr = array([ff_miles, percent_tats, ice_cream])
    classifier_result = classify0((in_arr - min_vals)/ranges, norm_mat, dating_labels, 3)
    print("You will probably like this person: ", result_list[classifier_result - 1])

classify_person()