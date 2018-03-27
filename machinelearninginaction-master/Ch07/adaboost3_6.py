from numpy import *


def load_simpdata():
    datamat = matrix([[1., 2.1],
                     [2., 1.1],
                     [1.3, 1.],
                     [1., 1.],
                     [2., 1.]])
    class_labels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return datamat, class_labels


def stump_classify(data_matrix, dimen, thresh_val, thressh_ineq):
    ret_array = ones((shape(data_matrix)[0], 1))
    if thressh_ineq == 'lt':
        ret_array[data_matrix[:, dimen] <= thresh_val] = -1.0
    else:
        ret_array[data_matrix[:, dimen] > thresh_val] = -1.0
    return ret_array


def build_stump(data_arr, class_labels, D):
    data_matrix = mat(data_arr)
    label_mat = mat(class_labels).T
    m, n = shape(data_matrix)
    num_steps = 10.0
    best_stump = {}
    best_class_est = mat(zeros((m, 1)))
    min_error = inf
    for i in range(n):
        range_min = data_matrix[:, i].min()
        range_max = data_matrix[:, i].max()
        step_size = (range_max-range_min)/num_steps
        for j in range(-1, int(num_steps)+1):
            for inequal in ['lt', 'gt']:
                thresh_val = (range_min + float(j) * step_size)
                predicted_vals = stump_classify(data_matrix, i, thresh_val, inequal)
                err_arr = mat(ones((m, 1)))
                err_arr[predicted_vals == label_mat] = 0
                weighted_error = D.T*err_arr
                print("split: dim %d, thresh %.2f, thresh inequal: %s, the weighted error"
                      "is % .3f" % (i, thresh_val, inequal, weighted_error))
                if weighted_error < min_error:
                    min_error = weighted_error
                    best_class_est = predicted_vals.copy()
                    best_stump['dim'] = i
                    best_stump['thresh'] = thresh_val
                    best_stump['ineq'] = inequal
    return best_stump, min_error, best_class_est


def adaboost_train(data_arr, class_labels, num_iter=40):
    weak_class_arr = []
    m = data_arr.shape[0]
    D = mat(ones((m, 1))/m)
    agg_class_est = mat(ones((m, 1)))

    for i in range(num_iter):
        best_stump, error, class_est = build_stump(data_arr, class_labels, D)
        print("D:", D.T)
        alpha = float(0.5*log((1.0 - error)/max(error, 1e-16)))
        best_stump['alpha'] = alpha
        weak_class_arr.append(best_stump)
        print("class_est: ", class_est.T)

        expon = multiply(-alpha*mat(class_labels).T, class_est)
        D = multiply(D, exp(expon))
        D = D/D.sum()
        agg_class_est += alpha*class_est
        print("agg_class_est: ", agg_class_est.T)

        agg_errors = multiply(sign(agg_class_est) != mat(class_labels).T, ones((m, 1)))
        error_rate = agg_errors.sum()/m
        print("total error: ", error_rate, "\n")

        if error_rate == 0:
            break
    return weak_class_arr


def ada_classify(data_to_classify, classifier_arr):
    data_matrix = mat(data_to_classify)
    m = shape(data_matrix)[0]
    agg_class_est = mat(zeros((m, 1)))
    for i in range(len(classifier_arr)):
        class_est = stump_classify(data_matrix, classifier_arr[i]['dim'],
                                   classifier_arr[i]['thresh'],
                                   classifier_arr[i]['ineq'])
        agg_class_est += classifier_arr[i]['alpha']*class_est
        print(agg_class_est)
    return sign(agg_class_est)


# 加载第4章马疝病数据
def load_dataset(path):
    num_feature = len(open(path).readline().split('\t'))
    data_mat = []
    label_mat = []
    fr = open(path)
    for line in fr.readlines():
        line_arr = []
        cur_line = line.strip().split('\t')
        for i in range(num_feature - 1):
            line_arr.append(float(cur_line[i]))
        data_mat.append(line_arr)
        label_mat.append(float(cur_line[-1]))
    return mat(data_mat), label_mat

