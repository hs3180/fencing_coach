"""
TTS语音生成模块

使用EdgeTTS进行中文语音合成，生成训练口令的音频文件。
"""

import asyncio
import edge_tts
import tempfile
import os
from pathlib import Path
from typing import List, Optional
from config.voices import VOICE_CONFIG, DEFAULT_VOICE

class TTSGenerator:
    """TTS语音生成器"""

    def __init__(self, voice_name: str = DEFAULT_VOICE):
        """
        初始化TTS生成器

        Args:
            voice_name: 语音配置名称
        """
        self.voice_config = VOICE_CONFIG.get(voice_name, VOICE_CONFIG[DEFAULT_VOICE])
        self.temp_dir = Path(tempfile.gettempdir()) / "fencing_trainer"
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
            output_path = self.temp_dir / f"tts_{hash(text) % 1000000}.mp3"

        try:
            communicate = edge_tts.Communicate(
                text,
                self.voice_config["voice"],
                rate=self.voice_config["rate"],
                volume=self.voice_config["volume"],
                pitch=self.voice_config["pitch"]
            )
            await communicate.save(str(output_path))
            return output_path
        except Exception as e:
            raise RuntimeError(f"TTS生成失败: {text[:20]}... - {str(e)}")

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
            for file in self.temp_dir.glob("tts_*.mp3"):
                file.unlink()
        except Exception:
            pass  # 忽略清理错误

    def get_temp_file_path(self, identifier: str) -> Path:
        """获取临时文件路径"""
        return self.temp_dir / f"tts_{identifier}.mp3"

async def test_tts():
    """测试TTS功能"""
    generator = TTSGenerator()
    try:
        text = "测试语音生成功能"
        audio_path = await generator.generate_audio(text)
        print(f"音频文件已生成: {audio_path}")
        print(f"文件大小: {audio_path.stat().st_size} bytes")

        # 清理测试文件
        audio_path.unlink()
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_tts())