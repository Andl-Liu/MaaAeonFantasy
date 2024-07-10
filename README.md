<div align="center">

# MaaAeonFantasy

</div>

本程序是依赖于[MaaFramework](https://github.com/MaaXYZ/MaaFramework)、针对游戏《星神少女》的自动测试程序。目前还在早期开发阶段，存在很多问题，如果遇到bug请带着debug文件夹下的maa.log进行反馈。

> **MaaFramework** 是基于图像识别技术、运用 [MAA](https://github.com/MaaAssistantArknights/MaaAssistantArknights) 开发经验去芜存菁、完全重写的新一代自动化黑盒测试框架。
> 低代码的同时仍拥有高扩展性，旨在打造一款丰富、领先、且实用的开源库，助力开发者轻松编写出更好的黑盒测试程序，并推广普及。


## 目前已实现的功能

- 领取冥河探索收益
- 领取任务派遣奖励
- 进行任务派遣
- 进行祭祀
- 银河铁道登车
- 银河铁道赞助
- cg活动每日免费币
- cg活动收菜
- 和使徒交谈
- 每日斗技场
- 每日星神再会
- 每日皇者争锋
- 每日免费造型召唤
- 每日免费星空轮回
- 领取每日任务奖励
- 买空公会商店
- 领取体力补给
- 每日诸神回归

## 使用说明

[点击此处下载](https://github.com/Andl-Liu/MaaAeonFantasy/releases)

### 如果想单独执行某些脚本任务
- 请根据自己的系统下载对应版本的压缩包。比如`Windows(x86)`用户请下载`MaaAeonFantasy-win-x86_64-vXXX.zip`
- 解压后运行`MaaPiCli.exe`即可

### 如果想要定时或循环执行执行某些脚本任务
请下载`MaaAeonFantasy_schedule_vXXX.zip`,目前只支持windows系统
#### 使用前的准备：
- 请确保电脑中有`python`环境，如果没有请先安装`python-3.12.4-amd64.exe`，具体过程可参考[此处](https://blog.csdn.net/weixin_65158585/article/details/128487634)。
- 如果是第一次使用，请先运行`install.bat`

#### 使用方法：
- 需要`mumu模拟器12`
- 主页需要有星神少女的图标
- 请将模拟器的分辨率调为`1280*720`
- 打开`start.bat`
- 等待命令行窗口显示选择模拟器，输入mumu模拟器对应的编号并按回车
- 等待程序继续执行
- 如果命令行窗口显示"是否补偿执行某一个计划"，请按需要输入"y"(执行)或"n"(不执行)，并按回车

#### 如何自定义定时执行计划和循环执行计划：
- 打开文件夹`assets\resource\base`下的文件`schedule.json`
- 按需要进行编辑

#### 如何自定义再会星神：
- 打开文件夹`assets\resource\base\pipeline`下的文件`meet_task.json`
- 找到"进行再会1_sub"、"进行再会2_sub"和"进行再会3_sub"，将其中的"expected"后的值改成自己需要的星神名称
- 比如"expected": "阿波罗"，就是和阿波罗进行再会
- 该名字需要和星神再会界面的名称保持一致
- 默认再会星神阿波罗、泊瑟芬、修普诺斯

## 鸣谢

本项目由 **[MaaFramework](https://github.com/MaaXYZ/MaaFramework)** 强力驱动！

感谢以下开发者对本项目作出的贡献:

<a href="https://github.com/Andl-Liu/MaaAeonFantasy/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Andl-Liu/MaaAeonFantasy&max=1000" />
</a>

