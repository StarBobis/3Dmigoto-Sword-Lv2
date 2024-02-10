# Python's design problem: All class must have __init__ to initialize their attributes
# if you don't do it ,when you call ClassName(), it will use the last one created
# every new () way created will be a reference type which will reference the last one created.
# see https://docs.python.org/3/reference/datamodel.html#classes
# Classes are callable. These objects normally act as factories for new instances of themselves,
# but variations are possible for class types that override __new__().
# The arguments of the call are passed to __new__() and,
# in the typical case, to __init__() to initialize the new instance.

# Nico: keep these class as simple as you can, only expand it when you really need it.


def print_line_break():
    print("-----------------------------------------------------------------------")


def generate_combinations(lists, current_combination, all_combinations):
    if not lists:
        all_combinations.append(current_combination)
        return

    current_list = lists[0]
    remaining_lists = lists[1:]

    for item in current_list:
        new_combination = current_combination + [item]
        generate_combinations(remaining_lists, new_combination, all_combinations)



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

