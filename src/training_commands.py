"""
训练命令生成模块

生成击剑训练的完整语音命令序列。
"""

from typing import List, Dict
from pathlib import Path
import tempfile
from config.wrist_positions import (
    WRIST_POSITIONS, ATTACK_TYPES, STRAIGHT_CUT_TEMPLATES, get_straight_cut_combination_summary
)



class StraightCutCommandGenerator:
    """直劈训练命令生成器"""

    def __init__(self, attack_types: List[str], target_areas: List[str]):
        """
        初始化直劈命令生成器

        Args:
            attack_types: 攻击类型列表 ['stationary', 'lunge']
            target_areas: 目标部位列表 ['3', '4', '5']
        """
        self.attack_types = attack_types
        self.target_areas = target_areas
        self.combinations = [
            (attack_type, target_area)
            for attack_type in attack_types
            for target_area in target_areas
        ]

    def generate_all_commands(self, count: int) -> List[str]:
        """
        生成所有组合的训练命令

        Args:
            count: 每个组合的攻击次数

        Returns:
            完整命令文本列表
        """
        all_commands = []

        # 生成所有组合的训练
        for attack_type, target_area in self.combinations:
            segment_commands = self._generate_segment_commands(
                target_area, attack_type, count
            )
            all_commands.extend(segment_commands)

        # 全部训练结束
        all_commands.append(STRAIGHT_CUT_TEMPLATES["all_complete"])

        return all_commands

    def _generate_segment_commands(self, target_area: str, attack_type: str, count: int) -> List[str]:
        """
        生成单个组合的训练命令

        Args:
            target_area: 目标部位 ('3', '4', '5')
            attack_type: 攻击类型 ('stationary', 'lunge')
            count: 攻击次数

        Returns:
            命令文本列表
        """
        commands = []
        wrist_config = WRIST_POSITIONS[target_area]
        attack_config = ATTACK_TYPES[attack_type]

        # 开始本段训练
        start_command = STRAIGHT_CUT_TEMPLATES["segment_start"].format(
            target_area=wrist_config["name"],
            attack_type=attack_config["name"]
        )
        commands.append(start_command)

        # 动作指导
        guidance_command = STRAIGHT_CUT_TEMPLATES["action_guidance"].format(
            wrist_guidance=wrist_config["guidance"]
        )
        commands.append(guidance_command)

        # 计数序列
        for i in range(1, count + 1):
            commands.append(STRAIGHT_CUT_TEMPLATES["count"].format(count=i))
            commands.append(STRAIGHT_CUT_TEMPLATES["hold"])
            commands.append(STRAIGHT_CUT_TEMPLATES["return_position"])

            # 每20次提醒
            if i % 20 == 0:
                commands.append(STRAIGHT_CUT_TEMPLATES["reminder"])

        # 本段训练完成
        complete_command = STRAIGHT_CUT_TEMPLATES["segment_complete"].format(
            target_area=wrist_config["name"],
            attack_type=attack_config["name"]
        )
        commands.append(complete_command)

        return commands

    def get_training_summary(self, attack_count: int) -> Dict:
        """
        获取训练摘要信息

        Args:
            attack_count: 每个组合的攻击次数

        Returns:
            训练摘要字典
        """
        return get_straight_cut_combination_summary(
            self.attack_types, self.target_areas, attack_count
        )

    def validate_attack_count(self, attack_count: int) -> bool:
        """
        验证攻击次数是否合理

        Args:
            attack_count: 攻击次数

        Returns:
            是否有效
        """
        return 1 <= attack_count <= 50


# 工厂模式方法
def create_command_generator(config: Dict):
    """
    根据配置创建相应的命令生成器

    Args:
        config: 配置字典，包含模式等信息

    Returns:
        命令生成器实例
    """
    if config["mode"] == "straight-cut":
        return StraightCutCommandGenerator(
            config["attack_types"],
            config["target_areas"]
        )
    else:
        return TrainingCommandGenerator(config["positions"])

def test_command_generator():
    """测试命令生成器"""

    print("=== 测试传统位置训练 ===")
    # 测试多位置训练
    generator = TrainingCommandGenerator([1, 3, 5])

    print("训练摘要:")
    summary = generator.get_training_summary(attack_count=3)
    for key, value in summary.items():
        print(f"  {key}: {value}")

    print("\n命令序列 (前10个):")
    commands = generator.generate_full_training_commands(attack_count=2)
    for i, command in enumerate(commands[:10], 1):
        print(f"  {i:2d}. {command}")
    print(f"  ... (共{len(commands)}个命令)")

    print("\n=== 测试直劈训练 ===")
    # 测试直劈训练
    straight_generator = StraightCutCommandGenerator(
        attack_types=["stationary", "lunge"],
        target_areas=["3", "4", "5"]
    )

    print("训练摘要:")
    straight_summary = straight_generator.get_training_summary(attack_count=5)
    for key, value in straight_summary.items():
        print(f"  {key}: {value}")

    print("\n命令序列 (前15个):")
    straight_commands = straight_generator.generate_all_commands(count=5)
    for i, command in enumerate(straight_commands[:15], 1):
        print(f"  {i:2d}. {command}")
    print(f"  ... (共{len(straight_commands)}个命令)")

def test_straight_cut_generator():
    """测试直劈命令生成器"""
    print("=== 直劈训练命令生成器测试 ===")

    # 测试单一组合
    generator = StraightCutCommandGenerator(
        attack_types=["stationary"],
        target_areas=["3"]
    )

    print("\n单一组合测试 (3部位原地直劈, 3次):")
    commands = generator.generate_all_commands(count=3)
    for i, command in enumerate(commands, 1):
        print(f"{i:2d}. {command}")

    print(f"\n总命令数: {len(commands)}")

    # 测试多个组合
    multi_generator = StraightCutCommandGenerator(
        attack_types=["stationary", "lunge"],
        target_areas=["3", "4"]
    )

    print("\n=== 多组合测试 ===")
    summary = multi_generator.get_training_summary(attack_count=2)
    print("训练摘要:")
    for key, value in summary.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_command_generator()