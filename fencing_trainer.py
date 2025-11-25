#!/usr/bin/env python3
"""
击剑居家训练语音口令生成器

主程序入口文件，整合所有模块功能，生成训练音频文件。
"""

import asyncio
import sys
import time
from pathlib import Path
from typing import List

from src.cli_handler import CLIHandler
from src.training_commands import create_command_generator
from src.tts_generator import TTSGenerator
from src.audio_processor import AudioProcessor

class FencingTrainer:
    """击剑训练器主类"""

    def __init__(self, config: dict):
        """
        初始化训练器

        Args:
            config: 配置字典
        """
        self.config = config
        self.cli_handler = CLIHandler()
        self.command_generator = create_command_generator(config)
        self.tts_generator = TTSGenerator(config["voice"])
        self.audio_processor = AudioProcessor()

    async def generate_training_audio(self) -> Path:
        """
        生成训练音频文件

        Returns:
            生成的音频文件路径
        """
        start_time = time.time()

        try:
            # 1. 生成训练命令
            if self.config["verbose"]:
                print("正在生成训练命令...")

            # 根据训练模式生成命令
            if self.config["mode"] == "straight-cut":
                commands = self.command_generator.generate_all_commands(
                    count=self.config["attack_count"]
                )
            else:
                commands = self.command_generator.generate_full_training_commands(
                    self.config["attack_count"]
                )

            total_commands = len(commands)

            if self.config["verbose"]:
                print(f"共生成 {total_commands} 个命令")

            # 2. 生成TTS音频文件
            if self.config["verbose"]:
                print("正在生成语音音频...")

            audio_files = []
            for i, command in enumerate(commands):
                if self.config["verbose"]:
                    self.cli_handler.print_progress(i, total_commands, "生成语音")

                # 生成单个命令的音频
                audio_path = await self.tts_generator.generate_audio(command)
                audio_files.append(audio_path)

            if self.config["verbose"]:
                self.cli_handler.print_progress(total_commands, total_commands, "生成语音")

            # 3. 拼接音频文件
            if self.config["verbose"]:
                print("正在拼接音频文件...")

            output_path = self.config["output_path"]
            self.audio_processor.create_training_audio(
                audio_files,
                output_path,
                self.config["include_silence"]
            )

            # 4. 获取音频时长
            duration = self.audio_processor.get_audio_duration(output_path)

            # 5. 清理临时文件
            if self.config["verbose"]:
                print("正在清理临时文件...")

            self.tts_generator.cleanup_temp_files()

            # 6. 计算总耗时
            elapsed_time = time.time() - start_time

            if self.config["verbose"]:
                print(f"生成完成，耗时: {elapsed_time:.1f} 秒")

            return output_path

        except Exception as e:
            # 清理临时文件
            self.tts_generator.cleanup_temp_files()
            raise RuntimeError(f"音频生成失败: {str(e)}")

    def run(self):
        """运行训练器"""
        try:
            # 获取训练摘要
            summary = self.command_generator.get_training_summary(self.config["attack_count"])
            self.cli_handler.print_training_summary(self.config, summary)

            # 直接开始生成音频（无需确认）
            print("\n开始生成训练音频...")

            # 生成音频
            output_path = asyncio.run(self.generate_training_audio())
            duration = self.audio_processor.get_audio_duration(output_path)

            # 打印成功信息
            self.cli_handler.print_success(output_path, duration)

        except KeyboardInterrupt:
            print("\n\n用户中断操作。")
            sys.exit(1)
        except Exception as e:
            print(f"\n错误: {e}")
            sys.exit(1)

def check_dependencies():
    """检查依赖项是否安装"""
    try:
        import edge_tts
        import ffmpeg
        print("依赖项检查通过。")
        return True
    except ImportError as e:
        print(f"依赖项缺失: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def main():
    """主函数"""
    print("击剑居家训练语音口令生成器 v1.0")
    print("=" * 40)

    # 检查依赖
    if not check_dependencies():
        sys.exit(1)

    # 解析命令行参数
    cli_handler = CLIHandler()
    try:
        config = cli_handler.parse_arguments()
    except SystemExit:
        # argparse会调用sys.exit，我们直接返回
        return

    # 运行训练器
    trainer = FencingTrainer(config)
    trainer.run()

if __name__ == "__main__":
    main()