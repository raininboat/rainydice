# Rainy Dice 跑团机器人

本插件适用于仑质编写的[OlivOS青果核心交互栈](https://github.com/OlivOS-Team/OlivOS)，内容有参考仑质的[OlivaDice(DIXE)](https://github.com/lunzhiPenxil/Dice)<br>
## 插件仓库位置:
>`正式库`：[github](https://github.com/raininboat/rainydice)<br>
>`备份库`：[gitee](https://gitee.com/thunderain_zhou/rainydice)
&nbsp;
## 当前完成的功能列表
- `.st` 技能设置指令 包含：.st show / del / clr / name (设置当前人物卡名称）/  标准半自动人物卡的st输入 / .st 技能 +-表达式
- `.r` 投掷指令 包含正常带括号的四则运算    (符合骰娘标准实现，详见【骰娘指令标准.txt】，未进行大规模测试，可能有bug！)
- `.ra` 检定指令 含bp（奖励骰惩罚骰）h（暗骰） 不含#多轮检定     (未符合骰娘标准实现，未来需重构)
- `.nn` 设置用户名称
- `.sc` 理智检定
- `.setcoc` 房规设置
- `.ti` / `.li` 疯狂症状
- `.en` 幕间成长检定(未进行测试)
- `.log` 跑团记录
> 目前跑团记录基本实现已经完成，文件通过smtp邮件发送至`qq邮箱`中，tg等其他平台暂未适配，由于染色目前是通过正文html实现的，有概率被拦截为垃圾邮件，如未获取，请尝试在垃圾邮件中寻找或自行联系master
&nbsp;

## 下一步将要实现的功能
- `.log` 跑团记录
- `.ra` 指令重构
- 多人物卡
&nbsp;

## 未来准备实现的内容
（咕咕咕咕咕咕了）
### _标准骰娘功能_
* `.admin` 群管指令
* `.help` 帮助文档
* `.draw` 抽卡
* 。。。
### _特色功能_
- `.combat` 战斗轮提醒
- 。。。
&nbsp;

## 最后

>由于本人马上就要进入高三，这一年应该没多少时间进行更新（咕咕咕预告），如果有人愿意在此基础上进行更新改造都欢迎，最后如果真有事情要联系至此邮箱(虽然我不一定有时间看)：thunderain_zhou@163.com
