# 击剑居家训练语音口令生成器

一个为击剑初学者设计的CLI工具，生成个性化的训练语音口令，帮助用户进行居家训练。

![项目状态](https://img.shields.io/badge/状态-已完成-green.svg)
![版本](https://img.shields.io/badge/版本-v1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)

## 项目特点

- **目标用户**：击剑初学者
- **简洁实用**：专注于佩剑直刺训练
- **CLI工具**：命令行界面，简单易用
- **本地生成**：输出MP3音频文件，无需网络连接训练

## 功能特性

### 训练模式
支持佩剑直刺训练：
- 三部位攻击
- 四部位攻击
- 五部位攻击

### 自定义参数
- **训练部位**：选择攻击的具体部位
- **攻击次数**：设置每个部位的攻击次数
- **间隔频率**：控制攻击口令之间的时间间隔

### 标准训练流程
每个部位的训练遵循固定结构：
1. **训练要求** - 说明攻击部位和要求
2. **准备开始** - 提示准备状态
3. **训练口令** - 连续的攻击口令
4. **结束提示** - 完成本部位训练

## 技术实现

- **Python 3.12**：主要开发语言
- **EdgeTTS**：高质量中文语音合成
- **FFmpeg**：音频处理和MP3输出
- **纯本地生成**：无需数据上传，保护隐私

## 安装使用

```bash
# 安装依赖
pip install -r requirements.txt

# 生成训练音频文件
python fencing_trainer.py --parts 四部位 --count 5 --interval 2 --output training.mp3
```

## 输出格式
- 生成MP3格式的训练音频文件
- 包含完整的训练流程语音指导
- 支持自定义文件名和保存位置

## 项目结构
```
fencing_coach/
├── README.md                # 项目说明
├── USAGE.md                 # 详细使用说明
├── requirements.txt         # Python依赖
├── fencing_trainer.py      # 主程序入口
├── config/                 # 配置文件
│   ├── training_areas.py   # 训练部位配置
│   └── voices.py           # 语音配置
├── src/                    # 源代码
│   ├── __init__.py
│   ├── tts_generator.py    # TTS语音生成
│   ├── audio_processor.py  # 音频处理
│   ├── training_commands.py # 训练命令生成
│   └── cli_handler.py      # CLI处理
├── tests/                  # 测试文件
└── output/                 # 输出目录
```

## 快速开始

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **运行测试**
   ```bash
   python test_setup.py      # 测试项目设置
   python test_modules.py    # 测试模块功能
   ```

3. **生成训练内容**
   ```bash
   # 离线版本（推荐，无需网络）
   python fencing_trainer_offline.py --parts 四部位 --count 3 --output training.mp3

   # 在线版本（需要网络连接）
   python fencing_trainer.py --parts 四部位 --count 3 --output training.mp3
   ```

## 离线版本特性
- ✅ **完全离线**：无需网络连接即可使用
- ✅ **命令文本**：生成完整的训练命令文本文件
- ✅ **训练脚本**：生成模拟实际训练节奏的Python脚本
- ✅ **实用工具**：可直接进行模拟训练练习

## 详细文档
查看 [USAGE.md](./USAGE.md) 获取完整的使用说明。
