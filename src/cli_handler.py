"""
CLI处理器模块

处理命令行参数解析、验证和用户交互。
"""

import argparse
import sys
from pathlib import Path
from typing import Optional
from config.training_areas import parse_positions_string, validate_positions, get_position_names

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
  python fencing_trainer.py --positions 1,3,5 --count 5 --interval 2 --output training.mp3
  python fencing_trainer.py -p 3 --count 3 --interval 1.5 -o position3.mp3
  python fencing_trainer.py --positions 1,2,3,4,5,6,7 --count 2 -o all_positions.mp3
            """
        )

        # 必需参数
        parser.add_argument(
            "-p", "--positions",
            type=str,
            required=True,
            help="训练部位 (1-7)，逗号分隔。例如: 1 或 1,3,5 或 1,2,3,4,5,6,7"
        )

        # 可选参数
        parser.add_argument(
            "-c", "--count",
            type=int,
            default=5,
            help="每个部位的攻击次数 (默认: 5)"
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
            default="chinese",
            help="语音类型 (默认: chinese)"
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

        # 解析和验证位置参数
        try:
            positions = parse_positions_string(parsed_args.positions)
            validate_positions(positions)
        except ValueError as e:
            print(f"位置参数错误: {e}")
            sys.exit(1)

        # 验证其他参数
        validation_errors = self._validate_arguments(parsed_args)
        if validation_errors:
            print("参数错误:")
            for error in validation_errors:
                print(f"  - {error}")
            sys.exit(1)

        return {
            "positions": positions,
            "position_names": get_position_names(positions),
            "attack_count": parsed_args.count,
            "interval": parsed_args.interval,
            "output_path": Path(parsed_args.output),
            "voice": parsed_args.voice,
            "include_silence": not parsed_args.no_silence,
            "verbose": parsed_args.verbose
        }

    def _validate_arguments(self, args) -> list:
        """
        验证参数的有效性

        Args:
            args: 解析后的参数对象

        Returns:
            错误信息列表
        """
        errors = []

        # 验证攻击次数
        if not (1 <= args.count <= 20):
            errors.append("攻击次数必须在1-20之间")

        # 验证间隔时间
        if not (0.5 <= args.interval <= 10.0):
            errors.append("间隔时间必须在0.5-10.0秒之间")

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
        print(f"训练部位: {', '.join(config['position_names'])}")
        print(f"攻击次数: {config['attack_count']} 次/部位")
        print(f"间隔时间: {config['interval']} 秒")
        print(f"语音类型: {config['voice']}")
        print(f"输出文件: {config['output_path']}")
        print(f"包含静音: {'是' if config['include_silence'] else '否'}")

        print("\n=== 训练内容 ===")
        print(f"训练部位: {', '.join(summary['position_names'])}")
        print(f"总攻击命令: {summary['total_attack_commands']} 个")
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