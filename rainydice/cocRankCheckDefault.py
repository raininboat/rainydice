# -*- coding: utf-8 -*-

file = '''\
# -*- coding: utf-8 -*-
#检定规则判定模块
cocRankCheck={
    # 每组为一种大成功、大失败判定规则
    # text 为该组的解释信息
    # critical 为大成功判定表达式   （返回T/F）
    # fumble 为大失败判定表达式     （返回T/F）
    # result 为检定所得结果，skill_val 为当前技能值（成功率）
    0: {
        'text' : '0 :规则书\\n出1大成功\\n不满50出96 - 100大失败，满50出100大失败',
        'critical' : lambda result,skill_val : result == 1,
        'fumble' : lambda result,skill_val : skill_val<50 and result>=96 and result <= 100 or skill_val>=50 and result == 100 
    },
    1: {
        'text' : '1 :不满50出1大成功，满50出1 - 5大成功\\n不满50出96 - 100大失败，满50出100大失败',
        'critical' : lambda result,skill_val : skill_val<50 and result == 1 or skill_val >= 50 and result >= 1 and result <= 5,
        'fumble' : lambda result,skill_val : skill_val<50 and result >= 96 and result <= 100 or skill_val >= 50 and result == 100 
    },
    2: {
        'text' : '2 :出1 - 5且 <= 成功率大成功\\n出100或出96 - 99且 > 成功率大失败',
        'critical' : lambda result,skill_val : result>=1 and result <= 5 and result <= skill_val,
        'fumble' : lambda result,skill_val : result>=96 and result <= 100 and result > skill_val 
    },
    3: {
        'text' : '3 :出1 - 5大成功\\n出96 - 100大失败',
        'critical' : lambda result,skill_val : result >= 1 and result <= 5,
        'fumble' : lambda result,skill_val : result >= 96 and result <= 100  
    },
    4: {
        'text' : '4 :出1 - 5且 <= 十分之一大成功\\n不满50出 >= 96 + 十分之一大失败，满50出100大失败(全部使用整除)',
        'critical' : lambda result,skill_val : result >= 1 and result <= 5 and result <= skill_val//10,
        'fumble' : lambda result,skill_val : skill_val < 50 and result >= 96+skill_val//10 and result <= 100 or skill_val >= 50 and result == 100 
    },
    5: {
        'text' : '5 :出1 - 2且 < 五分之一大成功\\n不满50出96 - 100大失败，满50出99 - 100大失败(全部使用整除)',
        'critical' : lambda result,skill_val : result >= 1 and result <= 2 and result <= skill_val//5,
        'fumble' : lambda result,skill_val : skill_val<50 and result>=96 and result <= 100 or skill_val>=50 and result == 100 
    },
    6: {
        'text' : '6 :出1 - 5 且 < 1 + 二十分之一大成功\\n出96 - 100且 >= 96 +二十分之一大失败(全部使用整除)',
        'critical' : lambda result,skill_val : result >= 1 and result <= 5 and result <= 1+skill_val//20 or result == 1,
        'fumble' : lambda result,skill_val : result>=96 and result <= 100 and result >= 96 + skill_val//20 or result ==100 
    },

}'''
#检定规则判定模块
cocRankCheck={
    # 每组为一种大成功、大失败判定规则
    # text 为该组的解释信息
    # critical 为大成功判定表达式   （返回T/F）
    # fumble 为大失败判定表达式     （返回T/F）
    # result 为检定所得结果，skill_val 为当前技能值（成功率）
    0: {
        'text' : '0 :规则书\n出1大成功\n不满50出96 - 100大失败，满50出100大失败',
        'critical' : lambda result,skill_val : result == 1,
        'fumble' : lambda result,skill_val : skill_val<50 and result>=96 and result <= 100 or skill_val>=50 and result == 100 
    },
    1: {
        'text' : '1 :不满50出1大成功，满50出1 - 5大成功\n不满50出96 - 100大失败，满50出100大失败',
        'critical' : lambda result,skill_val : skill_val<50 and result == 1 or skill_val >= 50 and result >= 1 and result <= 5,
        'fumble' : lambda result,skill_val : skill_val<50 and result >= 96 and result <= 100 or skill_val >= 50 and result == 100 
    },
    2: {
        'text' : '2 :出1 - 5且 <= 成功率大成功\n出100或出96 - 99且 > 成功率大失败',
        'critical' : lambda result,skill_val : result>=1 and result <= 5 and result <= skill_val,
        'fumble' : lambda result,skill_val : result>=96 and result <= 100 and result > skill_val 
    },
    3: {
        'text' : '3 :出1 - 5大成功\n出96 - 100大失败',
        'critical' : lambda result,skill_val : result >= 1 and result <= 5,
        'fumble' : lambda result,skill_val : result >= 96 and result <= 100  
    },
    4: {
        'text' : '4 :出1 - 5且 <= 十分之一大成功\n不满50出 >= 96 + 十分之一大失败，满50出100大失败(全部使用整除)',
        'critical' : lambda result,skill_val : result >= 1 and result <= 5 and result <= skill_val//10,
        'fumble' : lambda result,skill_val : skill_val < 50 and result >= 96+skill_val//10 and result <= 100 or skill_val >= 50 and result == 100 
    },
    5: {
        'text' : '5 :出1 - 2且 < 五分之一大成功\n不满50出96 - 100大失败，满50出99 - 100大失败(全部使用整除)',
        'critical' : lambda result,skill_val : result >= 1 and result <= 2 and result <= skill_val//5,
        'fumble' : lambda result,skill_val : skill_val<50 and result>=96 and result <= 100 or skill_val>=50 and result == 100 
    },
    6: {
        'text' : '6 :出1 - 5 且 < 1 + 二十分之一大成功\n出96 - 100且 >= 96 +二十分之一大失败(全部使用整除)',
        'critical' : lambda result,skill_val : result >= 1 and result <= 5 and result <= 1+skill_val//20 or result == 1,
        'fumble' : lambda result,skill_val : result>=96 and result <= 100 and result >= 96 + skill_val//20 or result ==100 
    },

}

def create_cocRankCheck(path):
    with open(path, 'w', encoding = 'utf-8') as rankcheck:
        rankcheck.write(file)
    return cocRankCheck
