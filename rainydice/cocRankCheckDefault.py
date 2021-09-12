# -*- coding: utf-8 -*-
'''
   ___  ___   _____  ____  __
  / _ \/ _ | /  _/ |/ /\ \/ /
 / , _/ __ |_/ //    /  \  / 
/_/|_/_/ |_/___/_/|_/   /_/  
                             
    COC 大成功失败判定模板（村规）

    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @ 注意！请勿修改本文件中的判断逻辑和内容！                  @
    @ 如需自定义村规请修改 data/rainydice/conf/rankcheck.py   @
    @ 本文件仅为生成判断文件的默认模板                         @
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

'''

# 此处为写入文件的内容
file = '''\
# -*- coding: utf-8 -*-
"""
   ___  ___   _____  ____  __
  / _ \/ _ | /  _/ |/ /\ \/ /
 / , _/ __ |_/ //    /  \  / 
/_/|_/_/ |_/___/_/|_/   /_/  
                             
    COC 大成功失败判定（村规）

    请在 cocRankCheck 中添加新键值对以完成自定义判定逻辑
    下文中已存在的 0 ~ 6 为自带的 7 种检定模式
    如需增加可以在下方自定义
"""
#检定规则判定模块
cocRankCheck={
    # 每组为一种大成功、大失败判定规则
    # text 为该组的解释信息
    # critical 为大成功判定表达式   （返回T/F）
    # fumble 为大失败判定表达式     （返回T/F）
    # result 为检定所得结果，skill_val 为当前技能值（成功率）

    # 这里是自定义规则的编号，也是指令.setcoc 后面连接的数字
    # -1: {
    #       # 这里是房规的解释文本，用于生成.help setcoc内容和setcoc设置后的回应内容中具体规则描述部分
    #     'text' : '出1 - 5 且 < 1 + 二十分之一大成功\\n出96 - 100且 >= 96 +二十分之一大失败(全部使用整除)',
    #
    #       # 这是大成功判定逻辑，如需修改仅需改变 lambda result,skill_val : 后方表达式内容 为真则大成功
    #     'critical' : lambda result,skill_val : result >= 1 and result <= 5 and result <= 1+skill_val//20 or result == 1,
    #
    #       # 这是大失败判定逻辑，如需修改仅需改变 lambda result,skill_val : 后方表达式内容 为真则大失败
    #     'fumble' : lambda result,skill_val : result>=96 and result <= 100 and result >= 96 + skill_val//20 or result ==100
    #
    #       # 如果大成功大失败判定同时为真，则返回大成功
    # },

    0: {
        'text' : '规则书\\n出1大成功\\n不满50出96 - 100大失败，满50出100大失败',
        'critical' : lambda result,skill_val : result == 1,
        'fumble' : lambda result,skill_val : skill_val<50 and result>=96 and result <= 100 or skill_val>=50 and result == 100 
    },
    1: {
        'text' : '不满50出1大成功，满50出1 - 5大成功\\n不满50出96 - 100大失败，满50出100大失败',
        'critical' : lambda result,skill_val : skill_val<50 and result == 1 or skill_val >= 50 and result >= 1 and result <= 5,
        'fumble' : lambda result,skill_val : skill_val<50 and result >= 96 and result <= 100 or skill_val >= 50 and result == 100 
    },
    2: {
        'text' : '出1 - 5且 <= 成功率大成功\\n出100或出96 - 99且 > 成功率大失败',
        'critical' : lambda result,skill_val : result>=1 and result <= 5 and result <= skill_val,
        'fumble' : lambda result,skill_val : result>=96 and result <= 100 and result > skill_val 
    },
    3: {
        'text' : '出1 - 5大成功\\n出96 - 100大失败',
        'critical' : lambda result,skill_val : result >= 1 and result <= 5,
        'fumble' : lambda result,skill_val : result >= 96 and result <= 100  
    },
    4: {
        'text' : '出1 - 5且 <= 十分之一大成功\\n不满50出 >= 96 + 十分之一大失败，满50出100大失败(全部使用整除)',
        'critical' : lambda result,skill_val : result >= 1 and result <= 5 and result <= skill_val//10,
        'fumble' : lambda result,skill_val : skill_val < 50 and result >= 96+skill_val//10 and result <= 100 or skill_val >= 50 and result == 100 
    },
    5: {
        'text' : '出1 - 2且 < 五分之一大成功\\n不满50出96 - 100大失败，满50出99 - 100大失败(全部使用整除)',
        'critical' : lambda result,skill_val : result >= 1 and result <= 2 and result <= skill_val//5,
        'fumble' : lambda result,skill_val : skill_val<50 and result>=96 and result <= 100 or skill_val>=50 and result == 100 
    },
    6: {
        'text' : '出1 - 5 且 < 1 + 二十分之一大成功\\n出96 - 100且 >= 96 +二十分之一大失败(全部使用整除)',
        'critical' : lambda result,skill_val : result >= 1 and result <= 5 and result <= 1+skill_val//20 or result == 1,
        'fumble' : lambda result,skill_val : result>=96 and result <= 100 and result >= 96 + skill_val//20 or result ==100 
    },

}
'''
# 默认模板
cocRankCheck={
    # 每组为一种大成功、大失败判定规则
    # text 为该组的解释信息
    # critical 为大成功判定表达式   （返回T/F）
    # fumble 为大失败判定表达式     （返回T/F）
    # result 为检定所得结果，skill_val 为当前技能值（成功率）
    0: {
        'text' : '规则书\n出1大成功\n不满50出96 - 100大失败，满50出100大失败',
        'critical' : lambda result,skill_val : result == 1,
        'fumble' : lambda result,skill_val : skill_val<50 and result>=96 and result <= 100 or skill_val>=50 and result == 100 
    },
    1: {
        'text' : '不满50出1大成功，满50出1 - 5大成功\n不满50出96 - 100大失败，满50出100大失败',
        'critical' : lambda result,skill_val : skill_val<50 and result == 1 or skill_val >= 50 and result >= 1 and result <= 5,
        'fumble' : lambda result,skill_val : skill_val<50 and result >= 96 and result <= 100 or skill_val >= 50 and result == 100 
    },
    2: {
        'text' : '出1 - 5且 <= 成功率大成功\n出100或出96 - 99且 > 成功率大失败',
        'critical' : lambda result,skill_val : result>=1 and result <= 5 and result <= skill_val,
        'fumble' : lambda result,skill_val : result>=96 and result <= 100 and result > skill_val 
    },
    3: {
        'text' : '出1 - 5大成功\n出96 - 100大失败',
        'critical' : lambda result,skill_val : result >= 1 and result <= 5,
        'fumble' : lambda result,skill_val : result >= 96 and result <= 100  
    },
    4: {
        'text' : '出1 - 5且 <= 十分之一大成功\n不满50出 >= 96 + 十分之一大失败，满50出100大失败(全部使用整除)',
        'critical' : lambda result,skill_val : result >= 1 and result <= 5 and result <= skill_val//10,
        'fumble' : lambda result,skill_val : skill_val < 50 and result >= 96+skill_val//10 and result <= 100 or skill_val >= 50 and result == 100 
    },
    5: {
        'text' : '出1 - 2且 < 五分之一大成功\n不满50出96 - 100大失败，满50出99 - 100大失败(全部使用整除)',
        'critical' : lambda result,skill_val : result >= 1 and result <= 2 and result <= skill_val//5,
        'fumble' : lambda result,skill_val : skill_val<50 and result>=96 and result <= 100 or skill_val>=50 and result == 100 
    },
    6: {
        'text' : '出1 - 5 且 < 1 + 二十分之一大成功\n出96 - 100且 >= 96 +二十分之一大失败(全部使用整除)',
        'critical' : lambda result,skill_val : result >= 1 and result <= 5 and result <= 1+skill_val//20 or result == 1,
        'fumble' : lambda result,skill_val : result>=96 and result <= 100 and result >= 96 + skill_val//20 or result ==100 
    },

}

def create_cocRankCheck(path):
    with open(path, 'w', encoding = 'utf-8') as rankcheck:
        rankcheck.write(file)
    return cocRankCheck
