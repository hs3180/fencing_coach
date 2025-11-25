"""
训练命令生成模块

生成击剑训练的完整语音命令序列。
"""

from typing import List, Dict
from pathlib import Path
import tempfile
from config.training_areas import (
    get_training_areas, get_area_names, TRAINING_TEMPLATES
)

class TrainingCommandGenerator:
    """训练命令生成器"""

    def __init__(self, training_mode: str):
        """
        初始化训练命令生成器

        Args:
            training_mode: 训练模式 ("三部位", "四部位", "五部位")
        """
        self.training_mode = training_mode
        self.training_areas = get_training_areas(training_mode)
        self.area_names = get_area_names(training_mode)

    def generate_area_commands(self, area_name: str, attack_count: int) -> List[str]:
        """
        生成单个部位的训练命令序列

        Args:
            area_name: 部位名称
            attack_count: 攻击次数

        Returns:
            命令文本列表
        """
        area_config = self.training_areas[area_name]
        commands = []

        # 1. 训练要求说明
        start_command = TRAINING_TEMPLATES["start"].format(
            area_name=area_name,
            description=area_config.description
        )
        commands.append(start_command)

        # 2. 准备开始
        commands.append(TRAINING_TEMPLATES["ready"])

        # 3. 训练口令
        for i in range(attack_count):
            # 攻击命令
            attack_command = TRAINING_TEMPLATES["attack"].format(
                command_prefix=area_config.command_prefix
            )
            commands.append(attack_command)

            # 如果不是最后一次攻击，添加还原命令
            if i < attack_count - 1:
                commands.append(TRAINING_TEMPLATES["recover"])

        # 4. 结束提示
        complete_command = TRAINING_TEMPLATES["area_complete"].format(
            area_name=area_name
        )
        commands.append(complete_command)

        return commands

    def generate_full_training_commands(self, attack_count: int) -> List[str]:
        """
        生成完整训练的命令序列

        Args:
            attack_count: 每个部位的攻击次数

        Returns:
            完整命令文本列表
        """
        all_commands = []

        # 生成总开始命令
        all_commands.append(f"开始{self.training_mode}直刺训练，请大家做好准备。")

        # 为每个部位生成训练命令
        for i, area_name in enumerate(self.area_names):
            # 生成当前部位的命令
            area_commands = self.generate_area_commands(area_name, attack_count)
            all_commands.extend(area_commands)

            # 如果不是最后一个部位，添加休息命令
            if i < len(self.area_names) - 1:
                all_commands.append("休息一下，准备下一个部位的训练。")

        # 添加总结束命令
        all_commands.append(TRAINING_TEMPLATES["all_complete"])

        return all_commands

    def get_training_summary(self, attack_count: int) -> Dict:
        """
        获取训练摘要信息

        Args:
            attack_count: 每个部位的攻击次数

        Returns:
            训练摘要字典
        """
        total_commands = len(self.area_names) * attack_count
        total_areas = len(self.area_names)

        return {
            "training_mode": self.training_mode,
            "total_areas": total_areas,
            "area_names": self.area_names,
            "attack_count_per_area": attack_count,
            "total_attack_commands": total_commands,
            "estimated_commands_count": total_commands + total_areas * 4 + 2  # 包括开始、结束、准备等命令
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
    # 测试四部位训练
    generator = TrainingCommandGenerator("四部位")

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