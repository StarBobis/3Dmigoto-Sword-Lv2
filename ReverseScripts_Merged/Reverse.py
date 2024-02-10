# Reverse scripts used to parse merged.ini automatically and reverse back every single mod in it to .ib and .vb format.
from ReverseScripts_Merged.Util import *

# Before you start to read the code you should know:
# everything is open source if you learn reverse engineering and work hard,
# it's simple but with a lot of annoying data structure.
# but any complicated or hard thing in the world is combined with the simplest minimum single data structure
# so there is nothing difficult if you keep learn them one by one, work hard and work smart is a simple way to success.
# what stop and limit you is your imagination or fear of possible fact reality instead of lack of power.


def go_fuck_the_mod(file_path):
    merged_ini = MergedInI(file_path)
    # (1) Parse CommandList to find all resource replace.
    merged_ini.parse_command_list()
    # (2) Parse TextureOverride and match resource replace.
    merged_ini.parse_texture_override()
    # (3) Process TextureOverride's active resource replace.
    merged_ini.process_active_resource_replace()
    # (4) Parse CycleKey.
    merged_ini.parse_key_variables()
    # (5) Parse Resource.
    merged_ini.parse_resource()
    # (6) Process resource's format and type.
    merged_ini.process_resources()
    # (7) Process every single combination of swap var.
    merged_ini.process_cycle_key_combination()
    # (8) Parse mod and output (click into it and go into next level abstract.)
    merged_ini.parse_mod_and_output()


if __name__ == "__main__":
    target_merged_ini_path = r"C:\Users\Administrator\Desktop\SabakuNoYouseiDishia\Script.ini"
    # target_merged_ini_path = r"C:\Users\Administrator\Desktop\Nahida\merged.ini"
    go_fuck_the_mod(target_merged_ini_path)









