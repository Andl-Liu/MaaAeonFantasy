# 初始化工具包，提供用户配置路径
# python -m pip install maafw
from maa.resource import Resource
from maa.controller import AdbController
from maa.instance import Instance
from maa.toolkit import Toolkit

from schedule_parser import parse_schedule

import asyncio
import sys
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import List, Dict, Any

resource_path = "assets\\resource\\base"

# 主函数，程序的入口点
async def main():
    # 用户配置目录路径，默认为当前目录
    user_path = "./"
    # 初始化工具包，传入用户配置路径
    Toolkit.init_option(user_path)

    # 加载资源文件
    resource = Resource()
    await resource.load(resource_path)

    # 选择并初始化设备
    device = await select_device()
    controller = AdbController(
        adb_path=device.adb_path,
        address=device.address,
    )
    await controller.connect()

    # 初始化实例，并绑定资源和控制器
    maa_inst = Instance()
    maa_inst.bind(resource, controller)

    # 检查实例是否初始化成功，如果失败则退出
    if not maa_inst.inited:
        print("Failed to init MAA.")
        exit()

    # 进行每日定时任务
    print("Daily task started.")
    await daily_task(maa_inst, resource_path + "\\schedule.json")
        

# 选择并返回一个ADB设备
# 以编号和名称的形式输出device_list, 让用户选择一个device并完成链接
async def select_device():
    # 获取连接的设备列表
    device_list = await Toolkit.adb_devices()
    # 检查设备列表，如果没有设备则退出
    if not device_list:
        print("No ADB device found.")
        exit()
    # 遍历设备列表，打印设备编号和名称
    for i, device in enumerate(device_list):
        print(f"{i}: {device.name}")
    # 获取用户选择的设备编号，判断用户输入是否合法
    while True:
        try:
            choice = int(input("选择一个设备（输入编号并回车）: "))
            if 0 <= choice < len(device_list):
                break
            print("Invalid device number.")
        except ValueError:
            print("Invalid input.")
    # 返回选择的设备
    return device_list[choice]

def watch_for_exit(q: Queue):
    """在单独线程中监听用户输入'exit'，并通过队列通知"""
    for line in sys.stdin:
        if line.strip().lower() == 'exit':
            q.put_nowait(None)  # 放入一个信号值，表示退出
            break

async def daily_task(maa_inst: Instance, schedule_file_path: str):
    """根据schedule.json安排和执行任务"""
    fix_time_plans, loop_plans = parse_schedule(schedule_file_path)
    
    # 创建队列用于监听退出信号
    q = asyncio.Queue()
        
    # 创建一个字典fix_time_dict,key为fix_time_plans中每一项的name,value为false(False代表未执行,True代表已执行)
    fix_time_dict = {plan["name"]: False for plan in fix_time_plans}
    # 创建一个字典loop_dict,key为loop_plans中每一项的name,value为-1(上次执行的时间戳,-1代表未执行)
    loop_dict = {plan["name"]: -1 for plan in loop_plans}
    # 当前日期
    current_date = datetime.now().date()

    # 判断今日已错过的定时计划,让用户选择是否执行
    for plan in fix_time_plans:
        if datetime.strptime(plan["time"], "%H:%M").time() < datetime.now().time():
            print(f"已错过的定时计划 {plan["name"]}.")
            print("是否要补偿执行 (y/n)")
            answer = input()
            if answer == "n":
                print(f"不会补偿执行计划 {plan["name"]}...")
                fix_time_dict[plan["name"]] = True

    while True:
        # 判断日期是否变更,如果变更,将fix_time_dict的值设为False
        if current_date != datetime.now().date():
            current_date = datetime.now().date()
            fix_time_dict = {plan["name"]: False for plan in fix_time_plans}

        # 遍历fix_time_plans
        for plan in fix_time_plans:
            # 判断是否已经执行过
            if fix_time_dict[plan["name"]]:
                continue
            # 获取计划的指定时间(将形如hh:mm的字符串转换为datetime对象)
            plan_time = datetime.strptime(plan["time"], "%H:%M").time()
            # 判断当前时间是否超过了计划的指定时间
            if datetime.now().time() < plan_time:
                continue
            # 循环执行计划中的所有任务
            print(f"Running fix time task {plan["name"]}...")
            fix_time_dict[plan["name"]] = True
            for task in plan["tasks"]:
                await run_task_with_log(maa_inst, task)

        # 遍历loop_plans
        for plan in loop_plans:
            # 如果从未执行,或距离上次执行超过了指定间隔时间,则循环执行计划中的所有任务,否则跳过
            if not (loop_dict[plan["name"]] == -1 or datetime.now() - loop_dict[plan["name"]] >= timedelta(seconds=int(plan["interval"])/1000)):
                continue
            # 循环执行计划中的所有任务
            print(f"Running loop task {plan["name"]}...")
            for task in plan["tasks"]:
                await run_task_with_log(maa_inst, task)
                # 更新loop_dict的值为当前时间戳
                loop_dict[plan["name"]] = datetime.now()

    
# 执行任务,附加日志输出
async def run_task_with_log(maa_inst: Instance, task_name: str):
    print(f"Running task {task_name}...")
    task_detail = await maa_inst.run_task(task_name)
    # 根据任务详情判断任务是否成功
    if task_detail is not None and all(node.run_completed for node in task_detail.node_details):
        print(f"Task {task_name} completed successfully.")
    else:
        print(f"Task {task_name} failed or partially completed.")



if __name__ == "__main__":
    asyncio.run(main())
