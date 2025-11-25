"""
音频处理模块

使用FFmpeg进行音频处理，包括音频拼接、静音插入和MP3编码。
"""

import ffmpeg
import tempfile
import numpy as np
from pathlib import Path
from typing import List, Optional
from config.voices import AUDIO_CONFIG

class AudioProcessor:
    """音频处理器"""

    def __init__(self):
        """初始化音频处理器"""
        self.sample_rate = AUDIO_CONFIG["sample_rate"]
        self.bitrate = AUDIO_CONFIG["bitrate"]
        self.silence_duration = AUDIO_CONFIG["silence_duration"]
        self.area_break_duration = AUDIO_CONFIG["area_break_duration"]

    def generate_silence(self, duration: float, output_path: Path) -> Path:
        """
        生成静音文件

        Args:
            duration: 静音时长(秒)
            output_path: 输出文件路径

        Returns:
            静音文件路径
        """
        try:
            # 生成静音音频
            silence_samples = int(duration * self.sample_rate)
            silence_audio = np.zeros(silence_samples, dtype=np.float32)

            # 使用FFmpeg生成静音文件
            (
                ffmpeg
                .input('pipe:', format='f32le', ac=1, ar=self.sample_rate)
                .output(str(output_path), acodec='mp3', audio_bitrate=self.bitrate)
                .overwrite_output()
                .run(input=silence_audio.tobytes(), capture_stdout=True, capture_stderr=True)
            )
            return output_path
        except Exception as e:
            raise RuntimeError(f"静音文件生成失败: {str(e)}")

    def concatenate_audio_files(self, audio_files: List[Path], output_path: Path) -> Path:
        """
        拼接多个音频文件

        Args:
            audio_files: 音频文件路径列表
            output_path: 输出文件路径

        Returns:
            拼接后的音频文件路径
        """
        if not audio_files:
            raise ValueError("没有音频文件需要拼接")

        try:
            # 创建输入流
            inputs = []
            for audio_file in audio_files:
                inputs.append(ffmpeg.input(str(audio_file)))

            # 拼接音频
            concatenated = ffmpeg.concat(*inputs, v=0, a=1)
            output = ffmpeg.output(concatenated, str(output_path), acodec='mp3', audio_bitrate=self.bitrate)

            try:
                ffmpeg.run(output, overwrite_output=True)
            except ffmpeg.Error as e:
                stderr_output = e.stderr.decode('utf-8') if e.stderr else 'No stderr output'
                raise RuntimeError(f"FFmpeg错误: {stderr_output}")
            return output_path
        except Exception as e:
            raise RuntimeError(f"音频拼接失败: {str(e)}")

    def create_training_audio(self,
                            command_audios: List[Path],
                            output_path: Path,
                            include_silence: bool = True) -> Path:
        """
        创建训练音频，在命令之间插入静音

        Args:
            command_audios: 命令音频文件列表
            output_path: 输出文件路径
            include_silence: 是否在命令间插入静音

        Returns:
            训练音频文件路径
        """
        if not command_audios:
            raise ValueError("没有命令音频文件")

        try:
            audio_segments = []
            temp_silence_files = []

            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)

                # 在命令间插入静音
                for i, audio_file in enumerate(command_audios):
                    audio_segments.append(audio_file)

                    # 如果不是最后一个命令且需要静音，则插入静音
                    if i < len(command_audios) - 1 and include_silence:
                        silence_file = temp_path / f"silence_{i}.mp3"
                        self.generate_silence(self.silence_duration, silence_file)
                        audio_segments.append(silence_file)

                # 拼接所有音频段
                self.concatenate_audio_files(audio_segments, output_path)

            return output_path
        except Exception as e:
            raise RuntimeError(f"训练音频创建失败: {str(e)}")

    def get_audio_duration(self, audio_path: Path) -> float:
        """
        获取音频文件时长

        Args:
            audio_path: 音频文件路径

        Returns:
            音频时长(秒)
        """
        try:
            probe = ffmpeg.probe(str(audio_path))
            duration = float(probe['streams'][0]['duration'])
            return duration
        except Exception as e:
            raise RuntimeError(f"获取音频时长失败: {str(e)}")

    def validate_audio_file(self, audio_path: Path) -> bool:
        """
        验证音频文件是否有效

        Args:
            audio_path: 音频文件路径

        Returns:
            是否为有效音频文件
        """
        try:
            if not audio_path.exists():
                return False

            probe = ffmpeg.probe(str(audio_path))
            return 'streams' in probe and len(probe['streams']) > 0
        except Exception:
            return False

def test_audio_processor():
    """测试音频处理器"""
    processor = AudioProcessor()

    try:
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # 生成静音文件测试
            silence_file = temp_path / "test_silence.mp3"
            processor.generate_silence(2.0, silence_file)

            if processor.validate_audio_file(silence_file):
                duration = processor.get_audio_duration(silence_file)
                print(f"静音文件生成成功，时长: {duration:.2f}秒")
            else:
                print("静音文件验证失败")

    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_audio_processor()