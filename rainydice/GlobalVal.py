class GlobalVal(object):
    def getHelpDoc(self,key='') : # 最大子串不会先不做了，现在只是自动把&关联项转换完毕
        if key in self.HelpDoc:
            temp = self.HelpDoc[key]
            if temp[0] == '&':
                newKey = temp[1:]
                temp = self.getHelpDoc(key=newKey)
            return temp
        else:
            return ''
        
    def getGlobalMsg(self,key=''):
        if key in self.GlobalMsg:
            temp = self.GlobalMsg[key]
            if temp[0] == '&':
                newKey = temp[1:]
                temp = self.getGlobalMsg(key=newKey)
            return temp
        else:
            return ''
    # 所有指令开始符号（只有这些会匹配）
    Command_Start_Sign = ('.','。','/')
    GlobalMsg = {
        'BotMsg' : 'RainyDice by Rainy Zhou\n测试版',
        'InputErr' : '请认真核对输入的内容！',
        'GroupCmdErr':'[Command_Name]只能在群聊中使用',
        'SkillUnsetErr' : '[Skill_Name]技能值未设定！\n请先使用 .st 进行设定',
        'rdReply' : '[User_Name]进行投掷:\n[DiceExp]=[Result]',
        'raReply' : '[User_Name]进行[Skill_Name]检定:\nD100 = [Result] / [Skill_Val] [Rank]',
        'rbpReply' : '[User_Name]进行[Skill_Name]检定:\nD100 = [rdResult] [[Sign]骰:[ROLL_List]] = [Result] / [Skill_Val] [Rank]',
        'rhGroupReply' : '[User_Name]进行了一次暗骰',
        'rhPrivateReply' : '在群聊[[Group_Name]]([Group_ID])中,你进行投掷：D100 = [Result]',
        'scReply' : '[User_Name]进行理智检定:\nD100 = [Roll_Result] / [Old_San] [Rank]\n理智损失: [San_Lose_Expression] = [San_Lose_Result] ',
        'stDelReply' : '已将[User_Name]的技能【Skill_Name】删除',
        'stChangeReply' : '已记录[User_Name]的属性变化:\n[Skill_Name]：[Skill_Val][Change_Expression]=[Skill_Val]+([Change_Result])=[Skill_Val_Result]',
        
        
    }
    GlobalVal = {
        'rankName' : ["【未知情况】","大成功","极难成功","困难成功","成功","失败","大失败"]
    }
    HelpDoc = {
        'ra' : 'ra/rc帮助信息',
        'rc' : '&ra',
        'sc' : 'sc帮助信息',
        'rd' : 'rd帮助信息'
    }