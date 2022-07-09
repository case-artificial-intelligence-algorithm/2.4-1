#!/usr/bin/env python3
#coding=utf-8

# Apriori算法用于解决频繁项集挖掘问题，并返回关联规则

import pandas as pd

# 读取数据
def load_data_set():
    data = []
    DataSet = pd.read_excel('data_set.xlsx')  # 读取三元组
    i = 0

    while i < len(DataSet):
        line = DataSet['ITEM'][i]
        d = line.strip().split(',')
        data.append(d)
        i += 1

    return data

def create_C1(data_set):
    C1 = set()  # 创建空集
    for t in data_set:
        for item in t:
            item_set = frozenset([item])    # frozenset()函数将列表转换为集合
            C1.add(item_set)    #
    return C1

def is_apriori(Ck_item, Lksub1):
    """
    判断是否为频繁项集
    :param Ck_item: 候选项集
    :param Lksub1: Lk-1频繁项集
    :return: 是否为频繁项集
    """
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lksub1:
            return False
    return True

def create_Ck(Lksub1, k):
    """
    创建第k个候选项集的集合
    :param Lksub1: # Lk-1频繁项集
    :param k: 项集中最大的项的长度
    :return: Ck 频繁项集
    """
    Ck = set()
    len_Lksub1 = len(Lksub1) # Lk-1的长度
    list_Lksub1 = list(Lksub1)
    for i in range(len_Lksub1):
        for j in range(1, len_Lksub1):
            l1 = list(list_Lksub1[i])
            l2 = list(list_Lksub1[j])
            l1.sort()
            l2.sort()
            if l1[0:k - 2] == l2[0:k - 2]:  # 前k-2项相同时,将两个集合合并
                Ck_item = list_Lksub1[i] | list_Lksub1[j]
                if is_apriori(Ck_item, Lksub1): # 判断是否为频繁项集
                    Ck.add(Ck_item) # 添加到Ck
    return Ck


def generate_Lk_by_Ck(data_set, Ck, min_support, support_data):
    """
    :param data_set: 数据集
    :param Ck: 项集
    :param min_support: 最小支持度
    :param support_data: 候选项目的支持度
    :return: Lk 候选项集
    """
    Lk = set() # 记录候选项集
    item_count = {} # 记录项集的频率

    for t in data_set: # 计算项集的频率
        for item in Ck:
            if item.issubset(t):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1

    t_num = float(len(data_set))

    for item in item_count:
        if (item_count[item] / t_num) >= min_support:   # 记录所有满足条件的项集
            Lk.add(item)
            support_data[item] = item_count[item] / t_num
    return Lk


def generate_L(data_set, k, min_support):
    """
    产生频繁项集
    :param data_set: 数据集
    :param k: 项集中最大的项的长度
    :param min_support: 最小支持度
    :return: L,support_data  L为频繁项集，support_data为频繁项集的支持度
    """
    C1 = create_C1(data_set)
    support_data = {}
    L1 = generate_Lk_by_Ck(data_set, C1, min_support, support_data) # 第一个频繁项集
    Lksub1 = L1.copy()
    L = [] # 频繁项集列表
    L.append(Lksub1)

    for i in range(2, k + 1):
        Ci = create_Ck(Lksub1, i) # 第i个频繁项集
        Li = generate_Lk_by_Ck(data_set, Ci, min_support, support_data) # 第i个频繁项集
        Lksub1 = Li.copy()
        L.append(Lksub1)
    return L, support_data


def generate_rules(L, support_data, min_conf):
    """
    :param L: 频繁项集
    :param support_data: 频繁项集的支持度
    :param min_conf: 最小置信度
    :return: rules_list 包含频繁项集的规则
    """
    big_rule_list = [] # 存储所有的关联规则
    sub_set_list = [] # 存储所有的频繁项集
    for i in range(0, len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):  # 如果频繁项集中的某个项集已经在之前的频繁项集中出现，则跳过
                    conf = support_data[freq_set] / \
                        support_data[freq_set - sub_set]
                    big_rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= min_conf and big_rule \
                        not in big_rule_list:   # 如果置信度大于最小置信度，则添加到关联规则列表
                        big_rule_list.append(big_rule)
            sub_set_list.append(freq_set)

    return big_rule_list


def solution():
    data = load_data_set()  # 加载数据集
    L, support_data = generate_L(data, k=3, min_support=0.2) # 产生频繁项集
    big_rules_list = generate_rules(L, support_data, min_conf=0.7)  # 产生关联规则
    print("关联规则: ")
    for item in big_rules_list:
        print(item[0], "=>", item[1], "置信度: ", item[2])


if __name__ == '__main__':
    solution()
