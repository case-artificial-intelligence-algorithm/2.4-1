#!/usr/bin/env python3

from my_solution import solution


# 测试用例
def test_solution():

    # 正确答案
    correct_solution_rule = set([(frozenset({'E'}), frozenset({'B'}), 1.0), (frozenset({'E'}), 
    frozenset({'A'}), 1.0), (frozenset({'D'}), frozenset({'B'}), 1.0), (frozenset({'E', 'B'}), 
    frozenset({'A'}), 1.0), (frozenset({'E', 'A'}), frozenset({'B'}), 1.0), (frozenset({'E'}), 
    frozenset({'B', 'A'}), 1.0)])

    # 程序求解结果
    result_rule = solution()
    assert result_rule == correct_solution_rule

