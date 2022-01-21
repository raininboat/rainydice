# Rainy Dice 跑团机器人

***注意！本插件目前处在开发迭代状态，存储结构不保证与未来版本通用！***

本插件适用于仑质编写的[OlivOS青果核心交互栈](https://github.com/OlivOS-Team/OlivOS)，内容有参考仑质的[OlivaDice(DIXE)](https://github.com/lunzhiPenxil/Dice)
<br>

## 插件仓库位置:
>`正式库`：[github](https://github.com/raininboat/rainydice)<br>
>`备份库`：[gitee](https://gitee.com/thunderain_zhou/rainydice)
<br>

## 插件依赖第三方库
- `psutil` OlivOS 本体也在使用，无需重复安装
- `python-docx` 使用指令 `pip install python-docx` 下载安装
- `sqlite3`
- 。。。*(其他想到再写)*

- - -

## 当前已完成的功能列表
### _标准跑团功能_
- `.st` 技能设置指令 包含：.st show / del / clr / name (设置当前人物卡名称）/  标准半自动人物卡的st输入 / .st 技能 +-表达式
- `.r` 投掷指令 包含正常带括号的四则运算    (符合骰娘标准实现，详见【骰娘指令标准.txt】，未进行大规模测试，可能有bug！)
- `.ra` 检定指令 含bp（奖励骰惩罚骰）h（暗骰） 不含#多轮检定     (未符合骰娘标准实现，未来需重构)
- `.nn` 设置用户名称
- `.sc` 理智检定
- `.coc(6|7)(d) (个数)` 新coc人物卡做成（COC 6版7版简略、详细人物卡做成）
- `.setcoc` 房规设置
- `.ti` / `.li` 疯狂症状
- `.en` 幕间成长检定(未进行测试)
- `.log` 跑团记录
- `.draw` 抽卡
> 目前跑团记录基本实现已经完成，文件通过smtp邮件发送至`qq邮箱`中，tg等其他平台暂未适配，目前可通过html渲染生成邮件正文，或生成docx文档等方式进行渲染，其中使用html发送正文有很大概率被拦截为***垃圾邮件***，如未获取，请尝试在垃圾邮件中寻找或自行联系master
<br>

### _其他功能_
- `.system status` 查看当前系统状态
- `.system restart` 重启 OlivOS 框架 *(需要 bot admin 或 master 权限)*
- 防撤回（默认关闭）
> 群聊使用 `.recall on` 打开后，消息撤回时自动通过回复该消息的方式显示出来；使用 `.recall off` 再次关闭
<br>

- - -
## 下一步将要实现的功能
- `.ra` 指令重构
- `.st` 中的**多人物卡**实现
- `.dnd` 随机人物卡
- `.name` 随机姓名 
<br>

- - -
## 未来准备实现的内容
~~（咕咕咕咕咕咕了）~~

### _标准骰娘功能_
* `.admin` 群管指令
* `.help` 帮助文档
* 。。。

### _特色功能_
- `.combat` 战斗轮提醒
- 。。。

### _其他计划内容_ ***可能有变动，只是作为计划先行罗列***
- 使用内存数据库作为运行时数据存储、读取形式
- 优化指令匹配模块

- - -
## 配置存储文件
所有配置文件和存储的信息都在 ./plugin/data/rainydice 目录中，其中:
- /log: 跑团记录，单个跑团记录的目录生成为 `log_[平台]_[群号]_[时间]`
- /temp: dice临时记录内容，可以删除，下次运行重新生成
- /PublicDeck: 所有外置牌堆 其中 `default.json` 为默认内置牌堆，自动生成

### conf/bot.json 具体配置：
```jsonc
{
    "email": {
        "enabled": true,                // 是否开启email模块
        "host": "smtp.exmail.qq.com",   // email服务商的smtp服务器（在官方帮助文档中寻找）
        "password": "xxxxx",            // 授权码（自行查看邮件运营商帮助文档，开启smtp服务）
        "port": 465,                    // smtp服务器端口
        "ssl": true,                    // 是否开启ssl
        "useraddr": "noreply@mail.rainydice.cn"     // 具体邮箱账号
    },
    "log": {                            // log 文件渲染方式，原生txt文档默认生成
        "csv": false,                   // csv 版本(也就是sql存储的原生表格信息) 默认关闭
        "doc": true,                    // docx 版本，染色文件 默认开启
        "html": false                   // html 开启后邮件正文使用html文档做染色文件，容易被判定为垃圾邮件 默认关闭
    },
    "name": "本机器人",                 // Rainy Dice 机器人名称
    "qq_admin": [
        0                               // qq 平台dice管理员
    ],
    "qq_master": 0,                     // qq 平台dice所有者
    "telegram_admin": [
        222,
        321
    ],
    "telegram_master": 123
}
```
### conf/rankcheck.py 具体配置：
该文件为机器人所有检定大成功大失败判断（村规设置）<br>
默认文件:
```python
cocRankCheck = {
    # 每组为一种大成功、大失败判定规则
    # text 为该组的解释信息
    # critical 为大成功判定表达式   （返回T/F）
    # fumble 为大失败判定表达式     （返回T/F）
    # result 为检定所得结果，skill_val 为当前技能值（成功率）

    # 这里是自定义规则的编号，也是指令.setcoc 后面连接的数字
    # -1: {
    #       # 这里是房规的解释文本，用于生成.help setcoc内容和setcoc设置后的回应内容中具体规则描述部分
    #     'text' : '出1 - 5 且 < 1 + 二十分之一大成功\n出96 - 100且 >= 96 +二十分之一大失败(全部使用整除)',
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
```
## 最后

>由于本人高三，这一年应该没多少时间进行更新（咕咕咕预告），如果有人愿意在此基础上进行更新改造都欢迎，最后如果真有事情要联系至此邮箱(虽然我不一定有时间看)：thunderain_zhou@163.com
