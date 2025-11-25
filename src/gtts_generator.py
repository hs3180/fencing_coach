"""
Google TTS备用语音生成模块

当EdgeTTS不可用时使用Google Text-to-Speech服务。
"""

import asyncio
from pathlib import Path
from typing import List, Optional
import tempfile
import time
from gtts import gTTS
import io

class GTTSGenerator:
    """Google TTS语音生成器"""

    def __init__(self, lang: str = 'zh'):
        """
        初始化Google TTS生成器

        Args:
            lang: 语言代码，默认为中文
        """
        self.lang = lang
        self.temp_dir = Path(tempfile.gettempdir()) / "fencing_trainer_gtts"
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
            output_path = self.temp_dir / f"gtts_{hash(text) % 1000000}.mp3"

        try:
            # gTTS是同步的，在线程池中运行以避免阻塞
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._generate_sync, text, output_path)
            return output_path
        except Exception as e:
            raise RuntimeError(f"Google TTS生成失败: {text[:20]}... - {str(e)}")

    def _generate_sync(self, text: str, output_path: Path):
        """同步生成音频文件"""
        try:
            # 创建gTTS对象
            tts = gTTS(text=text, lang=self.lang, slow=False)

            # 生成音频到内存
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)

            # 保存到文件
            with open(output_path, 'wb') as f:
                mp3_fp.seek(0)
                f.write(mp3_fp.read())

        except Exception as e:
            raise RuntimeError(f"gTTS生成失败: {str(e)}")

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
            for file in self.temp_dir.glob("gtts_*.mp3"):
                file.unlink()
        except Exception:
            pass  # 忽略清理错误

    def get_temp_file_path(self, identifier: str) -> Path:
        """获取临时文件路径"""
        return self.temp_dir / f"gtts_{identifier}.mp3"

async def test_gtts():
    """测试Google TTS功能"""
    generator = GTTSGenerator()
    try:
        text = "测试Google语音生成功能"
        audio_path = await generator.generate_audio(text)
        print(f"音频文件已生成: {audio_path}")
        print(f"文件大小: {audio_path.stat().st_size} bytes")

        # 清理测试文件
        audio_path.unlink()
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_gtts())