"""
击剑训练部位配置

定义编号部位（1-7）攻击的训练要求和中文名称。
"""

from typing import Dict, List
from dataclasses import dataclass

@dataclass
class TrainingArea:
    """训练部位数据类"""
    name: str  # 中文名称
    description: str  # 训练要求描述
    command_prefix: str  # 命令前缀

# 编号部位配置
POSITION_CONFIG = {
    1: TrainingArea(
        name="一部位",
        description="目标：第一部位。要求：精确攻击第一部位。",
        command_prefix="攻击一部位"
    ),
    2: TrainingArea(
        name="二部位",
        description="目标：第二部位。要求：精确攻击第二部位。",
        command_prefix="攻击二部位"
    ),
    3: TrainingArea(
        name="三部位",
        description="目标：第三部位。要求：精确攻击第三部位。",
        command_prefix="攻击三部位"
    ),
    4: TrainingArea(
        name="四部位",
        description="目标：第四部位。要求：精确攻击第四部位。",
        command_prefix="攻击四部位"
    ),
    5: TrainingArea(
        name="五部位",
        description="目标：第五部位。要求：精确攻击第五部位。",
        command_prefix="攻击五部位"
    ),
    6: TrainingArea(
        name="六部位",
        description="目标：第六部位。要求：精确攻击第六部位。",
        command_prefix="攻击六部位"
    ),
    7: TrainingArea(
        name="七部位",
        description="目标：第七部位。要求：精确攻击第七部位。",
        command_prefix="攻击七部位"
    )
}

# 训练流程模板
TRAINING_TEMPLATES = {
    "start": "开始{area_name}训练，{description}",
    "ready": "准备开始，保持注意。",
    "attack": "{command_prefix}！",
    "recover": "还原，准备下一次攻击。",
    "area_complete": "{area_name}训练完成。",
    "all_complete": "全部训练结束，恭喜完成训练。"
}

# 部位解析工具函数
def parse_positions_string(positions_str: str) -> List[int]:
    """
    将逗号分隔的位置字符串转换为位置列表
    例如: "1,3,5" -> [1, 3, 5]
    """
    try:
        positions = []
        for pos_str in positions_str.split(','):
            pos_str = pos_str.strip()
            if not pos_str:
                continue
            pos = int(pos_str)
            positions.append(pos)
        return positions
    except ValueError:
        raise ValueError(f"无效的位置格式: {positions_str}. 请使用逗号分隔的数字，例如: 1,3,5")

def validate_positions(positions: List[int]) -> bool:
    """
    验证位置列表是否有效
    - 每个位置必须在1-7之间
    - 不能有重复的位置
    """
    if not positions:
        raise ValueError("必须指定至少一个训练部位")

    for pos in positions:
        if not (1 <= pos <= 7):
            raise ValueError(f"位置编号必须在1-7之间，得到: {pos}")

    if len(set(positions)) != len(positions):
        raise ValueError("不能指定重复的训练部位")

    return True

def get_position_config(position: int) -> TrainingArea:
    """获取指定位置的配置"""
    if position not in POSITION_CONFIG:
        raise ValueError(f"不支持的位置: {position}. 支持的位置: 1-7")
    return POSITION_CONFIG[position]

def get_position_names(positions: List[int]) -> List[str]:
    """获取位置列表对应的中文名称列表"""
    return [POSITION_CONFIG[pos].name for pos in positions]