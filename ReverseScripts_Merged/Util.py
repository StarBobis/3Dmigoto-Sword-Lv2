# Python's design problem: All class must have __init__ to initialize their attributes
# if you don't do it ,when you call ClassName(), it will use the last one created
# every new () way created will be a reference type which will reference the last one created.
# see https://docs.python.org/3/reference/datamodel.html#classes
# Classes are callable. These objects normally act as factories for new instances of themselves,
# but variations are possible for class types that override __new__().
# The arguments of the call are passed to __new__() and,
# in the typical case, to __init__() to initialize the new instance.

# Nico: keep these class as simple as you can, only expand it when you really need it.

# python's design problem:
# if you pass a class's instance as a Dict's value or add into List
# it will be a reference type instead a new copy one.
# to fix it we need to manually copy a new one.
# this is very important since we use classes to abstract type.
import copy

import os.path

# for generate combination.
import itertools


def print_line_break():
    print("-----------------------------------------------------------------------")


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
        self.resource_replace_line = ""
        self.condition_list = []

    def show(self):
        print("resource_replace_line: " + self.resource_replace_line)
        for condition in self.condition_list:
            condition.show()


class TextureOverride:
    Name = ""
    Hash = ""
    ActiveCondition = None
    CommandList = []

    def __init__(self):
        self.Name = None
        self.Hash = None
        self.ActiveCondition = None
        self.CommandList = []

    ResourceReplaceList = []
    ActiveResourceReplaceList = []


class CycleKey:
    Key = ""
    VarName = ""
    VarValues = []

    def __init__(self):
        self.Key = ""
        self.VarName = ""
        self.VarValues = []

    def show(self):
        print("[Key]: " + self.Key)
        print("[VarName]: " + self.VarName)
        print("[VarValues]: " + str(self.VarValues))


class Resource:
    Name = ""
    Format = ""
    Stride = ""
    FileName = ""

    # Type can be Container,IB,VB,Texture
    Type = ""

    def __init__(self):
        self.Name = ""
        self.Type = ""
        self.Format = ""
        self.Stride = ""
        self.FileName = ""

    def show(self):
        print("[Name]: " + self.Name)
        print("[Type]: " + self.Type)
        print("[Format]: " + self.Format)
        print("[Stride]: " + self.Stride)
        print("[FileName]: " + self.FileName)


class MergedInI:
    FilePath = ""
    FileLocationFolder = ""
    LineList = [""]

    # 仅在CommandList中解析出来的ResourceReplace字典
    # CommandList名称，ResourceReplaceList
    CommandListResourceReplaceDict = {}

    TextureOverrideList = [TextureOverride()]

    CycleKeyList = [CycleKey()]

    ResourceList = [Resource()]
    ResourceDict = {}

    VarCombinationDictList = []

    def __init__(self, file_path):
        self.FilePath = file_path
        self.FileLocationFolder = os.path.dirname(self.FilePath)
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

    def parse_command_list(self):
        # 是否处于commandlist部分
        flag_in_commandlist_section = False
        # 是否处于if部分
        flag_in_if_section = False

        # 用于判断我们在第几层if
        if_level_count = 0

        # 资源替换和条件列表的字典
        # 每个资源替换可以有多个条件列表
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
                if_level_count = 0
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
                    print("[End] if section")
                    # end时必须清除当前等级的condition
                    # 等级下降
                    if_level_count = if_level_count - 1
                    print("[Level Decrease] to " + str(if_level_count))

                    # 移除当前层级的condition
                    print("Remove current level condition:" + tmp_condition.ConditionStr + " from [condition_dict]")
                    condition_dict.pop(tmp_condition.ConditionLevel)
                    print("[condition_dict] after remove size: " + str(len(condition_dict)))

                    # end时，必须把当前tmp_condition设为字典中上一个等级的condition
                    if if_level_count > 0:
                        print("Set [tmp_condition] to level " + str(if_level_count) + "'s condition.")
                        tmp_condition = condition_dict.get(if_level_count)


                if line.startswith("if"):
                    flag_in_if_section = True
                    if_level_count = if_level_count + 1
                    print("[Start] if section, current level: " + str(if_level_count))
                    print("[Generate new Condition]: ")
                    tmp_condition = Condition()
                    tmp_condition.ConditionStr = line[2:len(line)]
                    tmp_condition.ConditionLevel = if_level_count
                    tmp_condition.Positive = True
                    tmp_condition.show()
                    condition_dict[tmp_condition.ConditionLevel] = copy.copy(tmp_condition)
                    print("Add it into Condition Dict!")
                    print_line_break()

                # 处理else if模式
                if line.startswith("elseif"):
                    print("[Detect] else if section.")
                    print("[Generate new Condition]: ")
                    tmp_condition = Condition()
                    tmp_condition.ConditionStr = line[2:len(line)]
                    tmp_condition.ConditionLevel = if_level_count
                    tmp_condition.Positive = True
                    tmp_condition.show()
                    condition_dict[tmp_condition.ConditionLevel] = copy.copy(tmp_condition)
                    print("Add it into Condition Dict!")
                    print_line_break()

                # 需要额外判断是否处于else模式
                if line.startswith("else") and not line.startswith("elseif"):
                    tmp_condition.Positive = False
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

    def parse_texture_override(self):
        # Clean before we start to parse:
        self.TextureOverrideList.clear()

        print_line_break()
        print("[Start to parse TextureOverride section]")

        is_in_textureoverride = False

        tmp_texture_override = TextureOverride()

        for line in self.LineList:
            if line.startswith("[") and line.endswith("]") and is_in_textureoverride:
                print("[End] TextureOverride section")
                is_in_textureoverride = False
                print("Add into TextureOverrideList")
                self.TextureOverrideList.append(copy.copy(tmp_texture_override))
                print("Clean and make a new tmp_texture_override")
                tmp_texture_override = TextureOverride()

            if line.startswith("[textureoverride") and not is_in_textureoverride:
                print("[Start] TextureOverride section")
                is_in_textureoverride = True

                print("[Initialize] tmp_texture_override object")
                tmp_texture_override = TextureOverride()
                tmp_texture_override.Name = line[1:len(line) - 1]
                print("TextureOverride Name: " + tmp_texture_override.Name)

            if is_in_textureoverride and line.startswith("hash="):
                tmp_texture_override.Hash = line[5:len(line)]
                print("[Detect] hash : " + tmp_texture_override.Hash)

            if is_in_textureoverride and line.startswith("run=commandlist"):
                tmp_command = line[4:len(line)]
                tmp_texture_override.CommandList.append(tmp_command)
                print("[Detect] command :" + tmp_command)
            if is_in_textureoverride and line.startswith("$") and line.find("=") != -1:
                tmp_texture_override.ActiveCondition = line
                print("[Detect] active condition: " + tmp_texture_override.ActiveCondition)

        # if we still in texture override section after parse,then manually quit.
        if is_in_textureoverride:
            print("[End] TextureOverride section")
            print("Add into TextureOverrideList")
            self.TextureOverrideList.append(copy.copy(tmp_texture_override))

        print_line_break()
        print("[Start to match resource replace]")
        for texture_override in self.TextureOverrideList:
            print("[Match] texture override name: " + texture_override.Name)
            print(len(texture_override.CommandList))

            all_resource_replace_list = []
            for command in texture_override.CommandList:
                print("Command: " + command)
                resource_replace_list = self.CommandListResourceReplaceDict.get(command)

                if resource_replace_list is None:
                    # print(command + " can't match any resource replace.")
                    continue
                print("resource_replace_list size: " + str(len(resource_replace_list)))
                # [Python design problem], the for resource_replace in resource_replace_list
                # will happen before print("texture_override.ResourceReplaceList size: "
                # + str(len(texture_override.ResourceReplaceList)))
                # this happened if you change textureoverride's attribute in a for structure
                # So we have to use a new list to load and manually fill it back.
                for resource_replace in resource_replace_list:
                    all_resource_replace_list.append(resource_replace)
                    resource_replace.show()
            texture_override.ResourceReplaceList = copy.copy(all_resource_replace_list)

            print_line_break()
        print("[Match resource replace over]")
        print_line_break()

    def process_active_resource_replace(self):
        print("[Start to active resource replace by active condition]")
        for texture_override in self.TextureOverrideList:
            if texture_override.ActiveCondition != "" and texture_override.ActiveCondition is not None:
                print("TextureOverride Name: " + texture_override.Name)
                print("ActiveCondition: " + texture_override.ActiveCondition)
                active_var_splits = texture_override.ActiveCondition.split("=")
                var_name = active_var_splits[0]
                var_value = active_var_splits[1]

                # First we need to find is our active condition really effect resource replace?
                find_active = False
                for resource_replace in texture_override.ResourceReplaceList:
                    for condition in resource_replace.condition_list:
                        condition_str_split = condition.ConditionStr.split("==")
                        condition_var_name = condition_str_split[0]
                        if condition_var_name == var_name:
                            find_active = True
                            break
                    if find_active:
                        break

                # if active condition is not in condition list,we think all resource replace work.
                if not find_active:
                    print("the active condition in TextureOverride is not match any in resource list"
                          " so we use default ResourceReplaceList")
                    print(len(texture_override.ResourceReplaceList))
                    texture_override.ActiveResourceReplaceList = copy.copy(texture_override.ResourceReplaceList)
                    break

                activated_resource_replace_list = []
                # else we need to find which resource replace is activated by our active condition.
                for resource_replace in texture_override.ResourceReplaceList:
                    if len(resource_replace.condition_list) == 0:
                        # in merged.ini can not without condition.
                        print("Error: no condition list for " + resource_replace.resource_replace_line)
                        exit(1)

                    print("resource_replace name: " + resource_replace.resource_replace_line)

                    # if there is any condition match with outside active condition,
                    # we think entire resource_replace is been activated.
                    resource_replace_activated = False
                    for condition in resource_replace.condition_list:
                        condition_str_split = condition.ConditionStr.split("==")
                        condition_var_name = condition_str_split[0]
                        condition_var_value = condition_str_split[1]

                        if condition_var_name == var_name:
                            print("Meet active var: " + var_name)
                            print("VarName: " + var_name + " VarValue: " + var_value)
                            print("condition_var_name: " + condition_var_name + " condition_var_value: "
                                  + condition_var_value + " Positive: " + str(condition.Positive))
                            if condition.Positive and condition_var_value == var_value:
                                print("Active!")
                                print_line_break()
                                resource_replace_activated = True
                                break
                    if resource_replace_activated:
                        activated_resource_replace_list.append(resource_replace)
                    else:
                        print("resource_replace_activated is false ,this resource is not activated")

                texture_override.ActiveResourceReplaceList = activated_resource_replace_list
            else:
                # if there is no active condition, it will be active by default without other condition.
                print("there is no active condition in TextureOverride so we use default ResourceReplaceList")
                texture_override.ActiveResourceReplaceList = texture_override.ResourceReplaceList

        print_line_break()
        # don't uncomment these annoying code unless you are testing
        # print("Show test result: ")
        # for texture_override in self.TextureOverrideList:
        #     if texture_override.Name == "textureoverridenahidaposition":
        #         for resource_replace in texture_override.ActiveResourceReplaceList:
        #             resource_replace.show()
        #         print(len(texture_override.ActiveResourceReplaceList))

    def parse_key_variables(self):
        print_line_break()
        is_in_key_section = False
        self.CycleKeyList = []
        tmp_cycle_key = CycleKey()

        for line in self.LineList:
            if line.startswith("[") and line.endswith("]") and is_in_key_section:
                is_in_key_section = False
                print("[End] key section")
                self.CycleKeyList.append(copy.copy(tmp_cycle_key))
                tmp_cycle_key = CycleKey()

            if line.startswith("[key") and not is_in_key_section:
                is_in_key_section = True
                print("[Start] key section")

            if is_in_key_section:
                if line.startswith("key="):
                    tmp_cycle_key.Key = line[4:len(line)]
                    print("[Detect] key: " + tmp_cycle_key.Key)

                if line.startswith("$") and line.find("=") != -1 and line.find(",") != -1:
                    print("[Detect] cycle var")
                    line_split = line.split("=")
                    var_name = line_split[0]
                    var_values = line_split[1]
                    tmp_cycle_key.VarName = var_name
                    tmp_cycle_key.VarValues = var_values.split(",")

        # manually quit if no more content in ini.
        if is_in_key_section:
            print("[End] key section")
            self.CycleKeyList.append(copy.copy(tmp_cycle_key))

        # show
        for cycle_key in self.CycleKeyList:
            cycle_key.show()

    def parse_resource(self):
        is_in_resource_section = False

        tmp_resource = Resource()

        for line in self.LineList:

            if line.startswith("[") and line.endswith("]") and is_in_resource_section:
                is_in_resource_section = False
                print("[End] resource section")
                self.ResourceList.append(copy.copy(tmp_resource))
                tmp_resource = Resource()

            if line.startswith("[resource") and not is_in_resource_section:
                is_in_resource_section = True
                tmp_resource.Name = line[1:len(line) -1 ]
                print("[Start] resource section")
                print("Resource Name: " + tmp_resource.Name)

            if is_in_resource_section:
                if line.startswith("format="):
                    tmp_resource.Format = line[7:len(line)]
                    print("[Detect] format : " + tmp_resource.Format)
                if line.startswith("stride="):
                    tmp_resource.Stride = line[7:len(line)]
                    print("[Detect] stride : " + tmp_resource.Stride)
                if line.startswith("filename="):
                    tmp_resource.FileName = line[9:len(line)]
                    print("[Detect] filename : " + tmp_resource.FileName)

        if is_in_resource_section:
            self.ResourceList.append(copy.copy(tmp_resource))
            print("[End] resource section")
        print_line_break()
        # for resource in self.ResourceList:
        #     resource.show()

    def process_resources(self):
        print_line_break()
        # TODO 路径重置、类型设置、加入字典供后续使用
        for resource in self.ResourceList:
            # 1.set type
            if resource.FileName == "":
                # A simple empty resource used to store or recover things.
                resource.Type = "Container"
            else:

                if resource.Stride != "":
                    resource.Type = "VB"
                else:
                    if resource.Format != "":
                        resource.Type = "IB"
                    else:
                        resource.Type = "Texture"

            if resource.Type == "":
                print("[Warning] Unknown Type")

            if resource.FileName.startswith("."):
                resource.FileName = self.FileLocationFolder + resource.FileName[1:len(resource.FileName)]

            resource.show()
            # then put it into dict, {name:resource}
            self.ResourceDict[resource.Name] = copy.copy(resource)

    def process_cycle_key_combination(self):
        # list all possible combination of variable to make a mod.
        var_values_list = []
        var_name_list = []
        all_combinations = []
        for cycle_key in self.CycleKeyList:
            var_values = cycle_key.VarValues
            var_values_list.append(cycle_key.VarValues)
            var_name_list.append(cycle_key.VarName)

        all_combinations = list(itertools.product(*var_values_list))
        # add into dict
        for combination_list in all_combinations:
            tmp_var_name_value_dict = {}
            for i in range(len(combination_list)):
                var_name = var_name_list[i]
                var_value = combination_list[i]
                print("var_name: " + var_name + " var_value: " + var_value)
                tmp_var_name_value_dict[var_name] = var_value
            print_line_break()
            self.VarCombinationDictList.append(copy.copy(tmp_var_name_value_dict))

        # print(self.VarCombinationDictList)
    def parse_mod_and_output(self):
        for var_combination_dict in self.VarCombinationDictList:
            # 对于每种可能的变量取值，我们都进行mod拼装然后输出
            print_line_break()
            print("Not work yet, i will finish these later.")
            print_line_break()
            # TODO 获取TextureOverrideIB，转换成R32_UINT进行输出，同时记录最大值和最小值
