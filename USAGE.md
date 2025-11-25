# 使用说明

## 击剑居家训练语音口令生成器

这是一个专为击剑初学者设计的CLI工具，生成个性化的训练语音口令，帮助用户进行居家训练。

## 安装

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

## 基本用法

### 生成四部位训练音频（推荐初学者）
```bash
python fencing_trainer.py --parts 四部位 --count 5 --interval 2 --output basic_training.mp3
```

### 生成三部位训练音频
```bash
python fencing_trainer.py -p 三部位 -c 3 -i 1.5 -o three_parts.mp3
```

### 生成五部位训练音频（进阶）
```bash
python fencing_trainer.py -p 五部位 -c 5 -i 2.5 -o advanced_training.mp3
```

## 参数说明

| 参数 | 简写 | 说明 | 默认值 | 选项 |
|------|------|------|--------|------|
| `--parts` | `-p` | 训练部位模式 | 必需 | 三部位、四部位、五部位 |
| `--count` | `-c` | 每个部位的攻击次数 | 5 | 1-20 |
| `--interval` | `-i` | 攻击口令间隔时间(秒) | 2.0 | 0.5-10.0 |
| `--output` | `-o` | 输出音频文件名 | fencing_training.mp3 | - |
| `--voice` | - | 语音类型 | chinese | chinese、chinese_male |
| `--no-silence` | - | 不在命令间插入静音 | False | - |
| `--verbose` | - | 显示详细输出 | False | - |

## 训练模式详解

### 三部位训练
- **头部**: 头顶部位攻击
- **躯干**: 胸部和腹部攻击
- **手臂**: 前臂或手部攻击

适合：完全初学者，基础动作练习

### 四部位训练
- **头部**: 头顶部位攻击
- **胸前**: 胸前区域攻击
- **腰侧**: 腰部侧面攻击
- **手臂**: 前臂或手部攻击

适合：有一定基础的练习者

### 五部位训练
- **头部**: 头顶部位攻击
- **胸前**: 胸前区域攻击
- **腰侧**: 腰部侧面攻击
- **后背**: 后背区域攻击
- **手臂**: 前臂或手部攻击

适合：进阶练习者，全面训练

## 训练流程

每个部位的训练遵循标准流程：
1. **训练要求** - 说明攻击部位和技术要求
2. **准备开始** - 提示进入准备状态
3. **训练口令** - 连续的攻击命令和还原指令
4. **结束提示** - 完成本部位训练

## 使用建议

### 初学者建议
- 从三部位训练开始
- 每个部位3-5次攻击
- 间隔时间2-3秒
- 重点关注动作准确性

### 进阶者建议
- 尝试四部位或五部位训练
- 每个部位5-10次攻击
- 间隔时间1.5-2秒
- 注重速度和节奏控制

### 训练频率建议
- 初学者：每周2-3次，每次15-20分钟
- 进阶者：每周3-4次，每次20-30分钟

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

## 文件说明

- `fencing_trainer.py`: 主程序入口
- `config/`: 配置文件目录
  - `training_areas.py`: 训练部位配置
  - `voices.py`: 语音合成配置
- `src/`: 源代码目录
  - `tts_generator.py`: TTS语音生成
  - `audio_processor.py`: 音频处理
  - `training_commands.py`: 训练命令生成
  - `cli_handler.py`: CLI参数处理
- `requirements.txt`: Python依赖列表
- `test_*.py`: 测试文件

## 技术特性

- **纯本地生成**: 音频文件在本地生成，无需上传数据
- **高质量语音**: 使用EdgeTTS提供自然中文语音
- **灵活配置**: 支持多种训练模式和参数自定义
- **隐私保护**: 所有处理都在本地完成，保护用户隐私

## 更新日志

### v1.0.0
- 初始版本发布
- 支持三/四/五部位训练模式
- 集成EdgeTTS语音合成
- 支持音频拼接和静音插入
- 完整的CLI界面

## 许可证

本项目仅供学习和个人使用。