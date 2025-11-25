"""
语音合成配置

定义EdgeTTS语音参数和音频设置。
"""

# 语音配置
VOICE_CONFIG = {
    "chinese": {
        "voice": "zh-CN-XiaoxiaoNeural",  # 中文女声
        "rate": "+0%",  # 语速
        "volume": "+0%",  # 音量
        "pitch": "+0Hz"  # 音调
    },
    "chinese_male": {
        "voice": "zh-CN-YunyangNeural",  # 中文男声
        "rate": "+0%",
        "volume": "+0%",
        "pitch": "+0Hz"
    }
}

# 音频设置
AUDIO_CONFIG = {
    "sample_rate": 44100,  # 采样率
    "bitrate": "192k",  # 比特率
    "silence_duration": 2.0,  # 命令间静音时长(秒)
    "area_break_duration": 3.0,  # 部位间休息时长(秒)
    "format": "mp3"  # 输出格式
}

# 默认使用的语音
DEFAULT_VOICE = "chinese"