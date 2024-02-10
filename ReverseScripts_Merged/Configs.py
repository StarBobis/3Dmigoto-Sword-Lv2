# Python's design problem: All class must have __init__ to initialize their attributes
# if you don't do it ,when you call ClassName(), it will use the last one created
# every new () way created will be a reference type which will reference the last one created.

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
