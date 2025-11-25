"""
训练命令生成模块

生成击剑训练的完整语音命令序列。
"""

from typing import List, Dict
from pathlib import Path
import tempfile
from config.training_areas import (
    POSITION_CONFIG, get_position_config, TRAINING_TEMPLATES
)

class TrainingCommandGenerator:
    """训练命令生成器"""

    def __init__(self, positions: List[int]):
        """
        初始化训练命令生成器

        Args:
            positions: 要训练的位置列表 [1, 3, 5]
        """
        self.positions = sorted(positions)  # 排序确保一致性
        self.position_configs = {pos: get_position_config(pos) for pos in self.positions}

    def generate_position_commands(self, position: int, attack_count: int) -> List[str]:
        """
        生成单个位置的训练命令序列

        Args:
            position: 位置编号
            attack_count: 攻击次数

        Returns:
            命令文本列表
        """
        position_config = self.position_configs[position]
        commands = []

        # 1. 训练要求说明
        start_command = TRAINING_TEMPLATES["start"].format(
            area_name=position_config.name,
            description=position_config.description
        )
        commands.append(start_command)

        # 2. 准备开始
        commands.append(TRAINING_TEMPLATES["ready"])

        # 3. 训练口令
        for i in range(attack_count):
            # 攻击命令
            attack_command = TRAINING_TEMPLATES["attack"].format(
                command_prefix=position_config.command_prefix
            )
            commands.append(attack_command)

            # 如果不是最后一次攻击，添加还原命令
            if i < attack_count - 1:
                commands.append(TRAINING_TEMPLATES["recover"])

        # 4. 结束提示
        complete_command = TRAINING_TEMPLATES["area_complete"].format(
            area_name=position_config.name
        )
        commands.append(complete_command)

        return commands

    def generate_full_training_commands(self, attack_count: int) -> List[str]:
        """
        生成完整训练的命令序列

        Args:
            attack_count: 每个位置的攻击次数

        Returns:
            完整命令文本列表
        """
        all_commands = []
        position_names = [self.position_configs[pos].name for pos in self.positions]

        # 生成总开始命令
        if len(self.positions) == 1:
            all_commands.append(f"开始{position_names[0]}直刺训练，请大家做好准备。")
        else:
            all_commands.append(f"开始{','.join(position_names)}直刺训练，请大家做好准备。")

        # 为每个位置生成训练命令
        for i, position in enumerate(self.positions):
            # 生成当前位置的命令
            position_commands = self.generate_position_commands(position, attack_count)
            all_commands.extend(position_commands)

            # 如果不是最后一个位置，添加休息命令
            if i < len(self.positions) - 1:
                all_commands.append("休息一下，准备下一个部位的训练。")

        # 添加总结束命令
        all_commands.append(TRAINING_TEMPLATES["all_complete"])

        return all_commands

    def get_training_summary(self, attack_count: int) -> Dict:
        """
        获取训练摘要信息

        Args:
            attack_count: 每个位置的攻击次数

        Returns:
            训练摘要字典
        """
        position_names = [self.position_configs[pos].name for pos in self.positions]
        total_commands = len(self.positions) * attack_count
        total_positions = len(self.positions)

        return {
            "positions": self.positions,
            "position_names": position_names,
            "total_positions": total_positions,
            "attack_count_per_position": attack_count,
            "total_attack_commands": total_commands,
            "estimated_commands_count": total_commands + total_positions * 4 + 2  # 包括开始、结束、准备等命令
        }

    def validate_attack_count(self, attack_count: int) -> bool:
        """
        验证攻击次数是否合理

        Args:
            attack_count: 攻击次数

        Returns:
            是否有效
        """
        return 1 <= attack_count <= 20

def test_command_generator():
    """测试命令生成器"""
    # 测试多位置训练
    generator = TrainingCommandGenerator([1, 3, 5])

    print("=== 训练摘要 ===")
    summary = generator.get_training_summary(attack_count=3)
    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\n=== 命令序列 ===")
    commands = generator.generate_full_training_commands(attack_count=2)
    for i, command in enumerate(commands, 1):
        print(f"{i:2d}. {command}")

    print(f"\n总命令数: {len(commands)}")

if __name__ == "__main__":
    test_command_generator()