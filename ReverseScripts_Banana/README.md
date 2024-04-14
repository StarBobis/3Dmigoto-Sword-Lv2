# Usage
Banana is designed to manually reverse a single mod,it's a little hard to use
, but it can work on every type of mod,the only thing you need to do is figure out
how to config these ini files and know something about your target mod's d3d11 element attributes.

# POC
这个是逆向Mod的POC，学习意义大于实际使用意义。

# 使用说明
Banana脚本是用来手动逆向单个Mod的，虽然很多配置在源码里写死了，而且用起来也很麻烦，
但是使用得当可以逆向任意Mod，其教育意义远大于实际意义，毕竟用Python开源出来就是为了教会别人核心原理，不然发布个.exe就完了。
主要使用方法是先配置global_config.ini到指定游戏的指定配置，然后在对应的配置的preset.ini里修改对应参数，然后运行ReverseToModel。
如果这里面缺少你所需要逆向的游戏类型，你需要手动添加对应的配置文件夹，填写对应的vertex_attr.ini里的内容，然后在global_config.ini里切换并测试。

在逆向后可以使用SplitToBuffer.py将模型分割回去，不过分割后可能需要额外的TANGENT修复，以及COLOR修复，这部分代码已经Deprecated了，仅供参考。
# 鸣谢
Banana脚本从构思到编写花费的时间只用了几个小时，后面也只是偶尔用到时才会缝补一些代码，难免有bug和疏漏，欢迎指正。

关于逆向是否道德的问题，各有立场，各有各的利益相关，各有各的价值观，我们每个人都在为实现理想中的世界而努力，无需多言。
如果人与人都能够相互理解，那么世界上就不会有那么多的战争了，更多的时候是即使互相能够理解，也无法改变我们自己的利益立场。
逆向模型的本质就是让除了作者之外的人也能修改Mod的模型，在这一点上，AGMG的规则和制度是完全站在Mod作者的利益上考虑的，
虽然可以理解，但是失去了Mod社区的开源精神，失去了言论自由、失去了行为自由，也就失去了灵魂。
最终失去了Mod创作的初衷，变成了为金钱而创造色情Mod，垄断模型资源的的资本奴隶。

在这里特别感谢SilentNightSound以及AGMG社区的几位@Tool Developer，从他们身上学到了很多技术，
AGMG社区掌握了大量基础的3Dmigoto和d3d11相关技术，对于Shader Hacker来说是一个有意思的地方。
虽然大部分核心技术都被GateKeep了，不过如果自己深入研究d3d11文档的话还是能够复现的，所以获益良多，非常感谢。
总之，AGMG是一个适合初学者的地方，在我入门Mod学习时给了我很多帮助，但是随着学习逐渐深入，
特别是当你掌握了3Dmigoto的核心技术，而立场和思想又和他们不同时，就触碰到了AGMG社区的基本利益，这也是我退出的核心原因。

其次感谢所有一直支持我的粉丝，逆向技术是把双刃剑，因为这个讨厌我的人很多，因为这个喜欢我的人也很多，不过我不在乎，技术是自由的。
果然时间会让人显示出他的真实面貌，让我能够分辨出哪些是朋友，哪些是伪装的敌人，哪些是真正的敌人。

最后，向开源精神和自由主义致敬。
