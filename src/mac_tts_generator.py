"""
macOS系统TTS生成模块

使用macOS内置的say命令进行中文语音合成。
"""

import asyncio
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional

class MacTTSGenerator:
    """macOS TTS语音生成器"""

    def __init__(self, voice: str = "Ting-Ting"):
        """
        初始化macOS TTS生成器

        Args:
            voice: 语音名称，默认为Ting-Ting（中文女声）
        """
        self.voice = voice
        self.temp_dir = Path(tempfile.gettempdir()) / "fencing_trainer_mac"
        self.temp_dir.mkdir(exist_ok=True)

    async def generate_audio(self, text: str, output_path: Optional[Path] = None) -> Path:
        """
        生成单个文本的音频文件

        Args:
            text: 要合成的文本
            output_path: 输出文件路径，如果为None则使用临时文件

        Returns:
            生成的音频文件路径
        """
        if output_path is None:
            output_path = self.temp_dir / f"mac_tts_{hash(text) % 1000000}.aiff"

        try:
            # 使用say命令生成AIFF文件
            cmd = [
                "say",
                "-v", self.voice,
                "-o", str(output_path),
                text
            ]

            # 在线程池中运行命令以避免阻塞
            loop = asyncio.get_event_loop()

            def run_command():
                return subprocess.run(cmd, capture_output=True, text=True, check=True)

            result = await loop.run_in_executor(None, run_command)

            # 转换为MP3格式
            mp3_path = output_path.with_suffix('.mp3')
            await self._convert_to_mp3(output_path, mp3_path)

            # 删除临时的AIFF文件
            output_path.unlink()

            return mp3_path

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"macOS TTS生成失败: {text[:20]}... - {e.stderr if e.stderr else str(e)}")
        except Exception as e:
            raise RuntimeError(f"macOS TTS生成失败: {text[:20]}... - {str(e)}")

    async def _convert_to_mp3(self, input_path: Path, output_path: Path):
        """将AIFF文件转换为MP3格式"""
        try:
            cmd = [
                "ffmpeg",
                "-i", str(input_path),
                "-codec:a", "mp3",
                "-b:a", "192k",
                "-y",  # 覆盖输出文件
                str(output_path)
            ]

            loop = asyncio.get_event_loop()

            def run_command():
                return subprocess.run(cmd, capture_output=True, text=True, check=True)

            result = await loop.run_in_executor(None, run_command)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"音频转换失败: {e.stderr if e.stderr else str(e)}")

    async def generate_multiple_audio(self, texts: List[str]) -> List[Path]:
        """
        批量生成多个文本的音频文件

        Args:
            texts: 文本列表

        Returns:
            生成的音频文件路径列表
        """
        tasks = []
        for text in texts:
            task = self.generate_audio(text)
            tasks.append(task)

        return await asyncio.gather(*tasks)

    def cleanup_temp_files(self):
        """清理临时文件"""
        try:
            for file in self.temp_dir.glob("mac_tts_*.aiff"):
                file.unlink()
            for file in self.temp_dir.glob("mac_tts_*.mp3"):
                file.unlink()
        except Exception:
            pass  # 忽略清理错误

    def get_temp_file_path(self, identifier: str) -> Path:
        """获取临时文件路径"""
        return self.temp_dir / f"mac_tts_{identifier}.mp3"

    def list_available_voices(self):
        """列出可用的语音"""
        try:
            result = subprocess.run(["say", "-v", "?"],
                                  capture_output=True, text=True)
            print("可用的语音:")
            print(result.stdout)
        except Exception as e:
            print(f"获取语音列表失败: {e}")

async def test_mac_tts():
    """测试macOS TTS功能"""
    generator = MacTTSGenerator()
    try:
        text = "测试macOS语音生成功能"
        audio_path = await generator.generate_audio(text)
        print(f"音频文件已生成: {audio_path}")
        print(f"文件大小: {audio_path.stat().st_size} bytes")

        # 清理测试文件
        audio_path.unlink()
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_mac_tts())