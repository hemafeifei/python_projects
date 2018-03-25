'''
Created on March 25, 2018
 Machine Learing in Action
@author: Wei
'''
import numpy as np

def load_dataset(file_name):
    data_mat = []
    label_mat = []
    fr = open(file_name)
    for line in fr.readlines():
        line_arr = line.strip().split('\t')
        data_mat.append([float(line_arr[0]), float(line_arr[1])])
        label_mat.append(float(line_arr[2]))
    return data_mat, label_mat


def select_j_rand(i, m):
    j = 1
    while (j == i):
        j = int(np.random.uniform(0, m))
    return j


def clip_alpha(aj, H, L):
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj


def smo_simple(data_mat_in, class_labels, C, toler, max_iter):
    data_matrix = np.mat(data_mat_in)
    label_mat = np.mat(class_labels).transpose()
    b =0
    m, n = np.shape(data_matrix)
    alphas = np.mat(np.zeros((m, 1)))
    iter = 0
    while (iter < max_iter):
        alpha_pairs_changed = 0
        for i in range(m):
            f_Xi = float(np.multiply(alphas, label_mat).T*(data_matrix*data_matrix[i, :].T)) + b
            Ei = f_Xi - float(label_mat[i])
            if ((label_mat[i]*Ei < - toler) and (alphas[i] < C)) or ((label_mat[i]*Ei > toler) and (alphas[i]>0)):
                j = select_j_rand(i, m)
                f_Xj = float(np.multiply(alphas, label_mat).T*(data_matrix*data_matrix[j, :].T)) + b
                Ej = f_Xj - float(label_mat[j])
                alpha_i_old = alphas[i].copy()
                alpha_j_old = alphas[j].copy()
                if (label_mat[i] != label_mat[j]):
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])

                if L == H:
                    print("L==H")
                    continue
                eta = 2.0 * data_matrix[i, :]* data_matrix[j, :].T - data_matrix[i, :]*data_matrix[i, :].T - \
                    data_matrix[j, :]*data_matrix[j, :].T
                if eta >= 0:
                    print("eta>=0")
                    continue

                alphas[j] -= label_mat[j]*(Ei -Ej)/eta
                alphas[j] = clip_alpha(alphas[j], H, L)
                if (abs(alphas[j] - alpha_j_old) < 0.00001):
                    print("j not moving enough")
                    continue

                alphas[i] += label_mat[j]*label_mat[i]*(alpha_j_old - alphas[j])
                b1 = b - Ei - label_mat[i]*(alphas[i] - alpha_i_old)*data_matrix[i, :]*data_matrix[i, :].T - \
                    label_mat[j]*(alphas[j] - alpha_j_old)* data_matrix[i, :]*data_matrix[j, :].T
                b2 = b - Ej - label_mat[i]*(alphas[i] - alpha_i_old)*data_matrix[i, :]*data_matrix[j, :].T - \
                    label_mat[j]*(alphas[j] - alpha_j_old)*data_matrix[j, :]*data_matrix[j, :].T

                if (0 < alphas[i]) and (C > alphas[i]):
                    b = b1
                elif (0 < alphas[j]) and ( C > alphas[j]):
                    b = b2
                else:
                    b = (b1 + b2)/2.0
                alpha_pairs_changed += 1
                print("iter %d i: %d, pairs changed %d" % (iter, i, alpha_pairs_changed))

        if (alpha_pairs_changed == 0):
            iter += 1
        else:
            iter = 0
        print("iteration number: %d" % iter)
    return b, alphas





