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
支持直劈训练：
- 原地直劈 (Stationary)：无步法，专注手臂动作
- 弓步直劈 (Lunge)：结合步法的直劈攻击

### 目标部位
训练聚焦于三个手腕位置：
- 三部位：内侧手腕区域
- 四部位：中心手腕区域
- 五部位：外侧手腕区域

### 自定义参数
- **攻击类型**：选择原地或弓步攻击
- **目标部位**：选择训练的手腕位置
- **攻击次数**：设置每个组合的攻击次数
- **间隔频率**：控制攻击之间的时间间隔

### 标准训练流程
每个攻击组合的训练遵循固定结构：
1. **训练开始** - 说明目标和攻击方式
2. **动作指导** - 提供技术要点
3. **计数训练** - 重复攻击练习
4. **组合完成** - 本组合训练结束

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
python fencing_trainer.py --mode stationary,lunge --position 3,4,5 --count 10 --output training.mp3
```

## 输出格式
- 生成MP3格式的训练音频文件
- 包含完整的训练流程语音指导
- 支持自定义文件名和保存位置

## 基本用法

### 基础直劈训练（推荐初学者）
```bash
python fencing_trainer.py --mode stationary --position 3 --count 5 --output basic_training.mp3
```

### 组合训练（原地+弓步）
```bash
python fencing_trainer.py --mode stationary,lunge --position 3,4,5 --count 10 --output combo_training.mp3
```

### 弓步专项训练
```bash
python fencing_trainer.py --mode lunge --position 3,4 --count 8 --interval 2.5 --output lunge_training.mp3
```

## 参数说明

| 参数 | 说明 | 默认值 | 选项 |
|------|------|--------|------|
| `--mode` | 攻击类型，逗号分隔 | 必需 | stationary（原地）、lunge（弓步） |
| `--position` | 目标部位，逗号分隔 | 必需 | 3、4、5 |
| `--count` | 每个组合的攻击次数 | 5 | 1-50 |
| `--interval` | 攻击间隔时间(秒) | 2.0 | 2.0-10.0 |
| `--output` | 输出音频文件名 | fencing_training.mp3 | - |
| `--voice` | 语音类型 | chinese_male | chinese、chinese_male |
| `--no-silence` | 不在命令间插入静音 | False | - |
| `--verbose` | 显示详细输出 | False | - |

## 训练流程详解

每个攻击组合的训练遵循标准流程：
1. **训练开始** - 说明目标和攻击方式
2. **动作指导** - 提供技术要点
3. **计数训练** - 重复攻击练习（保持-还原循环）
4. **组合完成** - 本组合训练结束

### 攻击类型详解
- **原地直劈 (Stationary)**：无步法移动，专注手臂伸展和手腕动作
- **弓步直劈 (Lunge)**：结合弓步步法的完整攻击动作

### 目标部位详解
- **三部位**：内侧手腕区域，适合近身距离
- **四部位**：中心手腕区域，标准攻击距离
- **五部位**：外侧手腕区域，远距离攻击

## 使用建议

### 初学者建议
- 从原地直劈开始，三部位基础训练
- 每个组合5-10次攻击
- 间隔时间3-4秒
- 重点关注动作准确性和手腕控制

### 进阶者建议
- 尝试弓步直劈和组合训练
- 每个组合10-20次攻击
- 间隔时间2-3秒
- 注重速度、节奏和步法配合

### 训练频率建议
- 初学者：每周2-3次，每次15-20分钟
- 进阶者：每周3-4次，每次20-30分钟

## 项目结构
```
fencing_coach/
├── README.md                # 项目说明
├── requirements.txt         # Python依赖
├── fencing_trainer.py      # 主程序入口
├── config/                 # 配置文件
│   ├── wrist_positions.py  # 手腕位置配置
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

## 安装步骤

### 1. 安装Python依赖
```bash
pip install -r requirements.txt
```

### 2. 确保系统已安装FFmpeg
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# 从 https://ffmpeg.org/download.html 下载安装
```

### 3. 运行测试
```bash
python test_setup.py      # 测试项目设置
python test_modules.py    # 测试模块功能
```

## 故障排除

### 常见问题

**1. TTS生成失败 - Connection timeout**
- 原因：网络连接问题或EdgeTTS服务不稳定
- 解决：检查网络连接，稍后重试

**2. FFmpeg错误**
- 原因：FFmpeg未安装或不在PATH中
- 解决：安装FFmpeg并确保可访问

**3. 权限错误**
- 原因：输出目录无写入权限
- 解决：更改输出路径或修改目录权限

**4. 内存不足**
- 原因：生成大量音频文件占用内存
- 解决：减少攻击次数或分批生成

### 验证安装
```bash
# 测试项目设置
python test_setup.py

# 测试模块功能
python test_modules.py

# 查看帮助信息
python fencing_trainer.py --help
```

## 技术特性

- **纯本地生成**: 音频文件在本地生成，无需上传数据
- **高质量语音**: 使用EdgeTTS提供自然中文语音
- **灵活配置**: 支持多种训练模式和参数自定义
- **隐私保护**: 所有处理都在本地完成，保护用户隐私

## 更新日志

### v2.0.0
- 重构为直劈训练系统
- 添加手腕位置配置 (3,4,5部位)
- 支持原地和弓步攻击类型
- 改进训练流程和技术指导

### v1.0.0
- 初始版本发布
- 支持传统部位训练模式
- 集成EdgeTTS语音合成

## 许可证

本项目仅供学习和个人使用。
