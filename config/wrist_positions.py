"""
手腕动作配置 - 直劈训练模式的手腕动作要求
按部位区分不同的手腕转动方式
"""

# 手腕动作配置 - 按部位区分
WRIST_POSITIONS = {
    "3": {
        "name": "三部位",
        "wrist_action": "手腕转动，手掌心朝下",
        "guidance": "手腕转动使手掌心朝下"
    },
    "4": {
        "name": "四部位",
        "wrist_action": "手腕转动，手掌朝上",
        "guidance": "手腕转动使手掌朝上"
    },
    "5": {
        "name": "五部位",
        "wrist_action": "手腕转动，大拇指朝上",
        "guidance": "手腕转动使大拇指朝上"
    }
}

# 攻击类型配置
ATTACK_TYPES = {
    "stationary": {
        "name": "原地",
        "description": "原地直劈"
    },
    "lunge": {
        "name": "弓步",
        "description": "弓步直劈"
    }
}

# 直劈训练语音模板
STRAIGHT_CUT_TEMPLATES = {
    "segment_start": "开始{target_area}{attack_type}直劈训练。",
    "action_guidance": "{wrist_guidance}，保持手臂与肩膀平行，手臂不要往下掉。",
    "count": "{count}！",
    "hold": "保持...",
    "return_position": "归位。",
    "reminder": "保持手臂不要往下掉，注意动作稳定性。",  # 每20个数
    "segment_complete": "{target_area}{attack_type}训练完成。",
    "all_complete": "全部直劈训练结束，恭喜完成训练。"
}

from typing import List, Dict

def get_straight_cut_combination_summary(attack_types: List[str], target_areas: List[str], attack_count: int) -> Dict:
    """
    获取直劈训练组合的摘要信息

    Args:
        attack_types: 攻击类型列表
        target_areas: 目标部位列表
        attack_count: 每个组合的攻击次数

    Returns:
        包含摘要信息的字典
    """
    total_combinations = len(attack_types) * len(target_areas)
    total_attacks = total_combinations * attack_count

    # 估算命令数量：每个攻击大约需要3-4个命令（数字、保持、归位）
    estimated_commands_per_attack = 3.5
    base_commands = total_combinations * 2  # 每个组合的开始和结束命令
    attack_commands = total_attacks * estimated_commands_per_attack

    estimated_total_commands = int(base_commands + attack_commands + (total_attacks // 20) * 2)  # 加上提醒命令

    return {
        "total_combinations": total_combinations,
        "total_attacks": total_attacks,
        "estimated_commands_count": estimated_total_commands,
        "combination_details": [
            f"{WRIST_POSITIONS[area]['name']}{attack_type}"
            for attack_type in attack_types
            for area in target_areas
        ]
    }