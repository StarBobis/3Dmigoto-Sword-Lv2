# Reverse scripts used to parse merged.ini automatically and reverse back every single mod in it.
# (everything is open source if you learn reverse engineering and work hard)


# python problem: if you pass a class instance as a Dict's value or put into List
# it will be a reference type instead a new copy one.
# to fix it we need to manually copy a new one.
# this is very important since we use classes to abstract type.
import copy


class CommandList:
    pass


class MigotoPresent:
    ConstantCommandList = []


class MigotoKey:
    EffectCondition = ""
    Key = ""
    Type = ""
    ConstantsDict = {}
    ConstantCommandList = []


class MigotoStructure:
    # var name and it's possible value eg: {"swapwar":[0,1]}
    ConstantDict = {}
    #
    MigotoKeyList = []


class Condition:
    ConditionStr = ""
    ConditionLevel = 0
    Positive = True

    def __init__(self):
        self.ConditionStr = ""
        self.ConditionLevel = 0
        self.Positive = True

    def show(self):
        print("[Condition]ConditionStr: " + self.ConditionStr)
        print("[Condition]ConditionLevel: " + str(self.ConditionLevel))
        print("[Condition]Positive: " + str(self.Positive))


class ResourceReplace:
    # 原始的资源替换格式
    resource_replace_line = ""
    # 条件列表 Condition()
    condition_list = []

    def __init__(self):
        # 这里很奇怪，必须在init里面手动初始化，否则第二次使用构造方法创建对象时，值会沿用上一次的
        self.resource_replace_line = ""
        self.condition_list = []

    def show(self):
        print("resource_replace_line: " + self.resource_replace_line)
        for condition in self.condition_list:
            condition.show()


class MergedInI:
    FilePath = ""
    LineList = [""]

    # 仅在CommandList中解析出来的ResourceReplace字典
    # CommandList名称，ResourceReplaceList
    CommandListResourceReplaceDict = {}

    def __init__(self, file_path):
        self.FilePath = file_path
        self.LineList = []
        with open(self.FilePath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                # make sure everything is lower case and remove every space and line break.
                line = line.strip()
                line = line.lower()
                line = line.replace(" ", "")
                line = line.replace("\r", "")
                line = line.replace("\n", "")
                self.LineList.append(line)

    def parse_ini_structure(self):
        flag_texture_override = False

        # 需要列出所有可能执行到的路径

        for line in self.LineList:
            print("Original Line: " + line)
            if line.startswith("[textureoverride"):
                print("Detect TextureOverride:")

            if flag_texture_override and line.startswith("$"):
                print("Detect activate var: ")



    def parse_command_list(self):
        flag_in_commandlist_section = False
        flag_in_if_section = False
        flag_in_else_section = False
        # 用于判断我们在第几层if
        if_count = 0

        # 资源替换和条件列表的字典
        # 每个资源替换可以满足多个条件列表
        tmp_resource_replace_list = []

        # 这里需要管理一个Condition字典
        condition_dict = {}
        tmp_condition = Condition()

        # 暂时的commandlist名称
        tmp_commandlist_name = ""
        for line in self.LineList:
            # CommandList End
            if line.startswith("[") and line.endswith("]") and flag_in_commandlist_section:
                flag_in_commandlist_section = False
                if_count = 0
                print("[End] CommandList Section")

                print(type(tmp_resource_replace_list))

                self.CommandListResourceReplaceDict[tmp_commandlist_name] = tmp_resource_replace_list
                print("Add [tmp_resource_replace_list] to [CommandListResourceReplaceDict]")

                print("Set [tmp_resource_replace_list] to empty")
                tmp_resource_replace_list = []
                print("-----------------------------------------------------------")

            # CommandList Start
            if line.startswith("[commandlist") and line.endswith("]") and not flag_in_commandlist_section:
                print("[Start] CommandList Section")
                flag_in_commandlist_section = True

                # 获取[]内完整commandlist名称
                tmp_commandlist_name = line[1:len(line) - 1]
                print("[CommandList Name]: " + tmp_commandlist_name)

            if flag_in_commandlist_section:
                if line.startswith("endif"):
                    # 只有在第一层时遇到了endif才能退出if模式
                    flag_in_if_section = False
                    flag_in_else_section = False
                    print("[End] if section")
                    # end时必须清除当前等级的condition
                    # 等级下降
                    if_count = if_count - 1
                    print("[Level Decrease] to " + str(if_count))

                    # end时，必须把当前tmp_condition设为字典中上一个等级的condition
                    if if_count > 0:
                        print("Set [tmp_condition] to level " + str(if_count) + "'s condition.")
                        tmp_condition = condition_dict.get(if_count)

                if line.startswith("if"):
                    flag_in_if_section = True
                    if_count = if_count + 1
                    print("[Start] if section, current level: " + str(if_count))
                    print("[Generate new Condition]: ")
                    tmp_condition = Condition()
                    tmp_condition.ConditionStr = line[2:len(line)]
                    tmp_condition.ConditionLevel = if_count
                    tmp_condition.Positive = True
                    tmp_condition.show()
                    condition_dict[tmp_condition.ConditionLevel] = copy.copy(tmp_condition)
                    print("Add it into Condition Dict!")

                # 需要额外判断是否处于else模式
                if line.startswith("else"):
                    tmp_condition.Positive = False
                    flag_in_else_section = True
                    print("[Detect] else section.")
                    print("Change current level's condition's positive to False and add it into Condition dict")
                    tmp_condition.show()
                    condition_dict[tmp_condition.ConditionLevel] = copy.copy(tmp_condition)

                if flag_in_if_section:
                    # 在if 格式下判断是否有资源替换
                    if line.find("=resource") != -1:
                        print("[Detect] ResourceReplace: " + line)
                        tmp_resource_replace = ResourceReplace()
                        tmp_resource_replace.resource_replace_line = line

                        print("tmp_resource_replace.condition_list current size: " + str(len(tmp_resource_replace.condition_list)))

                        print("Set condition_dict size: " + str(len(condition_dict.values())))
                        for condition in condition_dict.values():
                            print("[Add] condition into [tmp_resource_replace] and show ")
                            condition.show()
                            tmp_resource_replace.condition_list.append(copy.copy(condition))

                            # 这里再次查看为什么会这样
                            # tmp_resource_replace.condition_list[0].show()

                            print("tmp_resource_replace.condition_list current size: " + str(len(tmp_resource_replace.condition_list)))
                        # 然后放到临时的resource列表
                        print("Add it into [tmp_resource_replace_list]")
                        tmp_resource_replace_list.append(copy.copy(tmp_resource_replace))
                        # tmp_resource_replace_list[0].condition_list[0].show() 到这里仍然是正常的

                        # 然后移除
                        print("Remove current level condition:" + tmp_condition.ConditionStr + " from [condition_dict]")
                        condition_dict.pop(tmp_condition.ConditionLevel)
                        print("[condition_dict] after remove size: " + str(len(condition_dict)))


        # 这里因为我们已经结束了，如果没有检测到新的[]，就默认结束CommandList
        if flag_in_commandlist_section:
            print("[End] CommandList Section")
            print(type(tmp_resource_replace_list))
            self.CommandListResourceReplaceDict[tmp_commandlist_name] = tmp_resource_replace_list
            print("Add [tmp_resource_replace_list] to [CommandListResourceReplaceDict]")
            print("-----------------------------------------------------------")

        print("[CommandList Parse Over.]")
        for commandlist_name in self.CommandListResourceReplaceDict.keys():
            print("CommandList name: " + commandlist_name)
            # print(type(self.CommandListResourceReplaceDict[commandlist_name]))
            for resource_replace in self.CommandListResourceReplaceDict[commandlist_name]:
                resource_replace.show()
                # print(len(resource_replace.condition_list))
            print("-----------------------------------------------------------")




    def parse_buffer_files(self):
        pass

    def output_model_files(self):
        pass


if __name__ == "__main__":
    merged_ini = MergedInI(r"C:\Users\Administrator\Desktop\SabakuNoYouseiDishia\Script.ini")
    # merged_ini.parse_ini_structure()
    merged_ini.parse_command_list()

    # merged_ini.parse_buffer_files()
    # merged_ini.output_model_files()







