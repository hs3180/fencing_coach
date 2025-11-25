"""
CLI处理器模块

处理命令行参数解析、验证和用户交互。
"""

import argparse
import sys
from pathlib import Path
from typing import Optional
from config.wrist_positions import ATTACK_TYPES

class CLIHandler:
    """CLI处理器"""

    def __init__(self):
        """初始化CLI处理器"""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """创建命令行参数解析器"""
        parser = argparse.ArgumentParser(
            description="击剑居家训练语音口令生成器",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
使用示例:
  # 直劈训练
  python fencing_trainer.py --mode stationary,lunge --position 3,4,5 --count 10 --output straight_cut.mp3
  python fencing_trainer.py --mode stationary --position 3 --count 5 -o basic_straight.mp3
            """
        )

        # 直劈训练模式参数组
        straight_cut_group = parser.add_argument_group('直劈训练模式')
        straight_cut_group.add_argument(
            "--mode",
            type=str,
            help="训练模式：stationary(原地),lunge(弓步)，逗号分隔"
        )

        straight_cut_group.add_argument(
            "--position",
            type=str,
            help="目标位置：3,4,5，逗号分隔"
        )

        # 可选参数
        parser.add_argument(
            "-c", "--count",
            type=int,
            default=5,
            help="每个部位/组合的攻击次数 (默认: 5)"
        )

        parser.add_argument(
            "-i", "--interval",
            type=float,
            default=2.0,
            help="攻击口令之间的间隔时间(秒) (默认: 2.0)"
        )

        parser.add_argument(
            "-o", "--output",
            type=str,
            default="fencing_training.mp3",
            help="输出音频文件名 (默认: fencing_training.mp3)"
        )

        parser.add_argument(
            "--voice",
            choices=["chinese", "chinese_male"],
            default="chinese_male",
            help="语音类型 (默认: chinese_male)"
        )

        parser.add_argument(
            "--no-silence",
            action="store_true",
            help="不在命令间插入静音"
        )

        parser.add_argument(
            "--verbose",
            action="store_true",
            help="显示详细输出信息"
        )

        return parser

    def parse_arguments(self, args: Optional[list] = None) -> dict:
        """
        解析命令行参数

        Args:
            args: 参数列表，如果为None则使用sys.argv

        Returns:
            解析后的参数字典
        """
        parsed_args = self.parser.parse_args(args)

        # 智能检测训练模式
        mode = self._infer_training_mode(parsed_args)

        # 检测参数冲突
        conflicts = self._detect_parameter_conflicts(parsed_args)
        if conflicts:
            print("参数冲突:")
            for conflict in conflicts:
                print(f"  - {conflict}")
            sys.exit(1)

        # 直劈训练模式
        config = {
            "mode": "straight-cut"
        }

        # 验证其他参数
        validation_errors = self._validate_arguments(parsed_args, mode)
        if validation_errors:
            print("参数错误:")
            for error in validation_errors:
                print(f"  - {error}")
            sys.exit(1)

        # 添加通用参数
        config.update({
            "attack_count": parsed_args.count,
            "interval": parsed_args.interval,
            "output_path": Path(parsed_args.output),
            "voice": parsed_args.voice,
            "include_silence": not parsed_args.no_silence,
            "verbose": parsed_args.verbose
        })

        # 添加直劈模式专用参数
        if mode == "straight-cut":
            config.update({
                "attack_types": self._parse_attack_types(parsed_args.mode),
                "target_areas": self._parse_target_areas(parsed_args.position)
            })

        return config

    def _parse_attack_types(self, attack_type_str: str) -> list:
        """
        解析攻击类型参数

        Args:
            attack_type_str: 攻击类型字符串，如 "stationary" 或 "stationary,lunge"

        Returns:
            攻击类型列表
        """
        if not attack_type_str:
            return ["stationary"]  # 默认原地直劈

        attack_types = [at.strip() for at in attack_type_str.split(",")]

        # 验证攻击类型
        for at in attack_types:
            if at not in ATTACK_TYPES:
                raise ValueError(f"不支持的攻击类型: {at}。支持的类型: {', '.join(ATTACK_TYPES.keys())}")

        return attack_types

    def _parse_target_areas(self, target_areas_str: str) -> list:
        """
        解析目标部位参数

        Args:
            target_areas_str: 目标部位字符串，如 "3" 或 "3,4,5"

        Returns:
            目标部位列表
        """
        if not target_areas_str:
            return ["3", "4", "5"]  # 默认所有部位

        target_areas = [ta.strip() for ta in target_areas_str.split(",")]

        # 验证目标部位
        valid_areas = ["3", "4", "5"]
        for ta in target_areas:
            if ta not in valid_areas:
                raise ValueError(f"不支持的目标部位: {ta}。支持的部位: {', '.join(valid_areas)}")

        return target_areas

    def _infer_training_mode(self, args) -> str:
        """
        智能检测训练模式
        只支持直劈训练模式
        """
        has_attack_type = bool(args.mode)
        has_target_areas = bool(args.position)

        if has_attack_type or has_target_areas:
            return "straight-cut"
        else:
            raise ValueError(
                "必须指定训练参数。\n\n"
                "直劈训练：--mode stationary --position 3,4,5\n\n"
                "使用 --help 查看详细用法和更多示例。"
            )

    def _detect_parameter_conflicts(self, args) -> list:
        """
        检测参数冲突
        """
        errors = []
        # 当前只有直劈训练模式，没有参数冲突
        return errors

    def _validate_arguments(self, args, mode: str) -> list:
        """
        验证参数的有效性

        Args:
            args: 解析后的参数对象
            mode: 训练模式

        Returns:
            错误信息列表
        """
        errors = []

        # 验证攻击次数（直劈训练）
        if not (1 <= args.count <= 50):
            errors.append("直劈训练攻击次数必须在1-50之间")

        # 验证间隔时间（直劈训练最小间隔2秒）
        if not (2.0 <= args.interval <= 10.0):
            errors.append("直劈训练间隔时间必须在2.0-10.0秒之间")

        # 验证直劈训练模式的特定参数
        if not args.mode:
            errors.append("直劈训练需要 --mode 参数（如：stationary 或 lunge）")

        if not args.position:
            errors.append("直劈训练需要 --position 参数（如：3,4,5）")

        # 验证输出路径
        output_path = Path(args.output)
        if output_path.exists() and not output_path.is_file():
            errors.append("输出路径已存在且不是文件")

        # 验证输出目录是否存在
        output_dir = output_path.parent
        if not output_dir.exists():
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                errors.append(f"无法创建输出目录: {output_dir}")

        return errors

    def print_training_summary(self, config: dict, summary: dict):
        """
        打印训练摘要信息

        Args:
            config: 配置字典
            summary: 训练摘要字典
        """
        print("=== 训练配置 ===")

        print("训练模式: 直劈训练")
        attack_names = [ATTACK_TYPES[at]["name"] for at in config["attack_types"]]
        from config.wrist_positions import WRIST_POSITIONS
        area_names = [WRIST_POSITIONS[ta]["name"] for ta in config["target_areas"]]
        print(f"攻击类型: {', '.join(attack_names)}")
        print(f"目标部位: {', '.join(area_names)}")
        print(f"攻击次数: {config['attack_count']} 次/组合")

        print(f"间隔时间: {config['interval']} 秒")
        print(f"语音类型: {config['voice']}")
        print(f"输出文件: {config['output_path']}")
        print(f"包含静音: {'是' if config['include_silence'] else '否'}")

        print("\n=== 训练内容 ===")
        print(f"训练组合: {len(config['attack_types'])} × {len(config['target_areas'])} = {len(config['attack_types']) * len(config['target_areas'])} 个组合")
        print(f"总攻击次数: {summary['total_attacks']} 次")
        print(f"预估命令数: {summary['estimated_commands_count']} 个")

    def print_progress(self, current: int, total: int, description: str = "处理中"):
        """
        打印进度信息

        Args:
            current: 当前进度
            total: 总数
            description: 描述信息
        """
        percentage = (current / total) * 100 if total > 0 else 0
        bar_length = 30
        filled_length = int(bar_length * current // total) if total > 0 else 0
        bar = '█' * filled_length + '-' * (bar_length - filled_length)

        print(f"\r{description}: |{bar}| {percentage:.1f}% ({current}/{total})", end='', flush=True)

        if current == total:
            print()  # 完成时换行

    def print_success(self, output_path: Path, duration: float):
        """
        打印成功信息

        Args:
            output_path: 输出文件路径
            duration: 音频时长
        """
        print("\n=== 生成完成 ===")
        print(f"输出文件: {output_path}")
        print(f"音频时长: {duration:.1f} 秒")
        print(f"文件大小: {output_path.stat().st_size / 1024:.1f} KB")

def test_cli_handler():
    """测试CLI处理器"""
    handler = CLIHandler()

    # 测试参数解析
    test_args = [
        "--positions", "1,3,5",
        "--count", "3",
        "--interval", "2.5",
        "--output", "test_training.mp3"
    ]

    try:
        config = handler.parse_arguments(test_args)
        print("参数解析成功:")
        for key, value in config.items():
            print(f"  {key}: {value}")
    except SystemExit:
        print("参数解析失败")

if __name__ == "__main__":
    test_cli_handler()