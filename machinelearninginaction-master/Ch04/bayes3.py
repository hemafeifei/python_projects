from numpy import *

def load_dataset():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    class_vec = [0, 1, 0, 1, 0, 1]  # 1 is abusive, 0 not
    return postingList, class_vec

def create_vocab_list(dataset):
    # 创建一个空集
    vocab_set = set([])
    for document in dataset:
        # 创建两个集合的并集
        vocab_set = vocab_set | set(document)
    return list(vocab_set)

def set_of_word2vec(vocab_list, input_set):
    # 创建一个所有元素都为0的向量
    return_vec = [0] * len(vocab_list)
    for word in input_set:
        if word in vocab_list:
            return_vec[vocab_list.index(word)] = 1
        else:
            print("the word : %s is not in my vocabulary!" % word)
    return return_vec

def train_NB0(train_matrix, train_category):
    """
    :param train_matrix: 每短话经过字典矢量化后的适量
    :param train_category: 每段话对应的类别
    :return: 
    """
    num_train_docs = len(train_matrix)
    num_words = len(train_matrix[0])
    # 带有侮辱性倾向的文本的概率
    p_abusive = sum(train_category)/float(num_train_docs)
    p0_num = zeros(num_words)
    p1_num = zeros(num_words)
    p0_denom = 2.0
    p1_denom = 2.0
    for i in range(num_train_docs):
        if train_category[i] == 1:
            p1_num += train_matrix[i]
            p1_denom += sum(train_matrix[i])
        else:
            p0_num += train_matrix[i]
            p0_denom += sum(train_matrix[i])
    p1_vec = log(p1_num/p1_denom)
    p0_vec = log(p0_num/p0_denom)
    return p0_vec, p1_vec, p_abusive

def classify_NB(vec2classify, p0_vec, p1_vec, p_class1):
    """
    
    :param vec2classify: 
    :param p0_vec: 
    :param p1_vec: 
    :param p_class1: 
    :return: 
    """
    p1 = sum(vec2classify * p1_vec) + log(p_class1)
    p0 = sum(vec2classify * p0_vec) + log(1.0 - p_class1)
    if p1 > p0:
        return 1
    else:
        return 0

def test_NB():
    list_posts, list_classes = load_dataset()
    my_vocablist = create_vocab_list(list_posts)
    train_mat = []
    for post_indoc in list_posts:
        train_mat.append(set_of_word2vec(my_vocablist,post_indoc))
    p0v, p1v, pAb = train_NB0(array(train_mat), array(list_classes))
    test_entry = ['love', 'my', 'dalmation']
    this_doc = array(set_of_word2vec(my_vocablist, test_entry))
    print(test_entry, "classified as :", classify_NB(this_doc, p0v, p1v, pAb))
    test_entry2 = ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
    this_doc2 = array(set_of_word2vec(my_vocablist, test_entry2))
    print(test_entry2, "classified as :", classify_NB(this_doc2, p0v, p1v, pAb))
