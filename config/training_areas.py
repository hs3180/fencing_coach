"""
击剑训练部位配置

定义三部位、四部位、五部位攻击的训练要求和中文名称。
"""

from typing import Dict, List
from dataclasses import dataclass

@dataclass
class TrainingArea:
    """训练部位数据类"""
    name: str  # 中文名称
    description: str  # 训练要求描述
    command_prefix: str  # 命令前缀

# 训练部位配置
TRAINING_AREAS = {
    "三部位": {
        "头部": TrainingArea(
            name="头部",
            description="目标：对方头顶部位。要求：手臂充分伸直，注意击打时机和准确性。",
            command_prefix="攻击头部"
        ),
        "躯干": TrainingArea(
            name="躯干",
            description="目标：对方胸部和腹部。要求：注意步法配合，保持身体平衡。",
            command_prefix="攻击躯干"
        ),
        "手臂": TrainingArea(
            name="手臂",
            description="目标：对方前臂或手部。要求：动作快速准确，避免过早暴露意图。",
            command_prefix="攻击手臂"
        )
    },
    "四部位": {
        "头部": TrainingArea(
            name="头部",
            description="目标：对方头顶部位。要求：手臂充分伸直，注意击打时机和准确性。",
            command_prefix="攻击头部"
        ),
        "胸前": TrainingArea(
            name="胸前",
            description="目标：对方胸前区域。要求：注意步法跟进，保持攻击角度。",
            command_prefix="攻击胸前"
        ),
        "腰侧": TrainingArea(
            name="腰侧",
            description="目标：对方腰部侧面。要求：利用步法创造攻击机会，注意防守转换。",
            command_prefix="攻击腰侧"
        ),
        "手臂": TrainingArea(
            name="手臂",
            description="目标：对方前臂或手部。要求：动作快速准确，避免过早暴露意图。",
            command_prefix="攻击手臂"
        )
    },
    "五部位": {
        "头部": TrainingArea(
            name="头部",
            description="目标：对方头顶部位。要求：手臂充分伸直，注意击打时机和准确性。",
            command_prefix="攻击头部"
        ),
        "胸前": TrainingArea(
            name="胸前",
            description="目标：对方胸前区域。要求：注意步法跟进，保持攻击角度。",
            command_prefix="攻击胸前"
        ),
        "腰侧": TrainingArea(
            name="腰侧",
            description="目标：对方腰部侧面。要求：利用步法创造攻击机会，注意防守转换。",
            command_prefix="攻击腰侧"
        ),
        "后背": TrainingArea(
            name="后背",
            description="目标：对方后背区域。要求：把握时机，利用对手转身瞬间攻击。",
            command_prefix="攻击后背"
        ),
        "手臂": TrainingArea(
            name="手臂",
            description="目标：对方前臂或手部。要求：动作快速准确，避免过早暴露意图。",
            command_prefix="攻击手臂"
        )
    }
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

# 支持的训练模式
SUPPORTED_MODES = ["三部位", "四部位", "五部位"]

def get_training_areas(mode: str) -> Dict[str, TrainingArea]:
    """获取指定训练模式的部位配置"""
    if mode not in SUPPORTED_MODES:
        raise ValueError(f"不支持的训练模式: {mode}. 支持的模式: {SUPPORTED_MODES}")
    return TRAINING_AREAS[mode]

def get_area_names(mode: str) -> List[str]:
    """获取指定训练模式的所有部位名称"""
    return list(get_training_areas(mode).keys())

def validate_training_mode(mode: str) -> bool:
    """验证训练模式是否有效"""
    return mode in SUPPORTED_MODES