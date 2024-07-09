from typing import List, Tuple
import json

# 解析JSON文件
def parse_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 分类任务
def categorize_tasks(tasks: dict) -> Tuple[List[dict], List[dict]]:
    fix_time_plans = []
    loop_plans = []

    for task in tasks.values():
        if task['type'] == 'fix_time':
            fix_time_plans.append(task)
        elif task['type'] == 'loop':
            loop_plans.append(task)

    return fix_time_plans, loop_plans

# 主函数，解析schedule.json
def parse_schedule(file_path: str) -> Tuple[List[dict], List[dict]]:
    schedule = parse_json(file_path)
    return categorize_tasks(schedule)