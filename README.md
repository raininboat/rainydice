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
- 。。。

- - -

## 当前已完成的功能列表
### _标准跑团功能_
- `.st` 技能设置指令 包含：.st show / del / clr / name (设置当前人物卡名称）/  标准半自动人物卡的st输入 / .st 技能 +-表达式
- `.r` 投掷指令 包含正常带括号的四则运算    (符合骰娘标准实现，详见【骰娘指令标准.txt】，未进行大规模测试，可能有bug！)
- `.ra` 检定指令 含bp（奖励骰惩罚骰）h（暗骰） 不含#多轮检定     (未符合骰娘标准实现，未来需重构)
- `.nn` 设置用户名称
- `.sc` 理智检定
- `.setcoc` 房规设置
- `.ti` / `.li` 疯狂症状
- `.en` 幕间成长检定(未进行测试)
- `.log` 跑团记录
> 目前跑团记录基本实现已经完成，文件通过smtp邮件发送至`qq邮箱`中，tg等其他平台暂未适配，目前可通过html渲染生成邮件正文，或生成docx文档等方式进行渲染，其中使用html发送正文有很大概率被拦截为***垃圾邮件***，如未获取，请尝试在垃圾邮件中寻找或自行联系master
<br>

### _其他功能_
- `.system state` 查看当前系统状态
- 防撤回（默认关闭）
> 群聊使用 `.recall on` 打开后，消息撤回时自动通过回复该消息的方式显示出来；使用 `.recall off` 再次关闭
<br>

- - -
## 下一步将要实现的功能
- `.ra` 指令重构
- `.st` 中的**多人物卡**实现
- `.draw` 抽卡
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
### conf/bot.json 具体配置：
```json
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
## 最后

>由于本人马上就要进入高三，这一年应该没多少时间进行更新（咕咕咕预告），如果有人愿意在此基础上进行更新改造都欢迎，最后如果真有事情要联系至此邮箱(虽然我不一定有时间看)：thunderain_zhou@163.com
