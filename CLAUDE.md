# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Chinese fencing trainer application that generates audio training commands for foil fencing practice. It's a Python CLI tool that creates personalized MP3 training sessions with voice commands for different training modes.

## Common Development Commands

### Installation and Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Ensure FFmpeg is installed (required for audio processing)
brew install ffmpeg  # macOS
sudo apt-get install ffmpeg  # Ubuntu/Debian
```

### Running the Application
```bash
# Basic usage - generate 4-area training audio
python fencing_trainer.py --parts 四部位 --count 5 --interval 2 --output training.mp3

# Using short flags
python fencing_trainer.py -p 三部位 -c 3 -i 1.5 -o basic_training.mp3

# Advanced 5-area training
python fencing_trainer.py -p 五部位 -c 5 -i 2.5 -o advanced_training.mp3

# Show help
python fencing_trainer.py --help
```

### Testing Individual Modules
```bash
# Test CLI handler
python src/cli_handler.py

# Test training command generator
python src/training_commands.py

# Test TTS generator
python src/tts_generator.py

# Test audio processor
python src/audio_processor.py
```

## Architecture Overview

### Core Components
- **fencing_trainer.py**: Main entry point that orchestrates the entire workflow
- **src/cli_handler.py**: Command-line argument parsing and validation
- **src/training_commands.py**: Generates training command sequences based on training areas
- **src/tts_generator.py**: Text-to-speech synthesis using EdgeTTS
- **src/audio_processor.py**: Audio processing, concatenation, and MP3 generation using FFmpeg

### Configuration System
- **config/training_areas.py**: Defines training modes (3/4/5 areas) with Chinese names and descriptions
- **config/voices.py**: Voice synthesis configurations for different TTS settings

### Training Modes
The application supports three training modes with Chinese terminology:
- **三部位 (3 areas)**: 头部 (Head), 躯干 (Torso), 手臂 (Arm)
- **四部位 (4 areas)**: 头部 (Head), 胸前 (Chest), 腰侧 (Waist), 手臂 (Arm)
- **五部位 (5 areas)**: 头部 (Head), 胸前 (Chest), 腰侧 (Waist), 后背 (Back), 手臂 (Arm)

### Workflow
1. Parse CLI arguments and validate parameters
2. Generate training command sequences for each area
3. Convert text commands to audio using EdgeTTS
4. Process and concatenate audio files with silence intervals
5. Output final MP3 training file

## Key Dependencies
- **edge-tts>=6.1.0**: Microsoft Edge Text-to-Speech for Chinese voice synthesis
- **ffmpeg-python>=0.2.0**: Audio processing and MP3 encoding
- **asyncio-throttle>=1.0.2**: Rate limiting for TTS requests
- **numpy>=1.24.0**: Audio data processing

## File Structure Conventions
- All source code is in the `src/` directory
- Configuration files are in the `config/` directory
- Chinese text is used throughout for training commands and UI
- Temporary audio files are managed automatically and cleaned up after processing
- Each module includes a self-test function that can be run directly

## Important Notes
- The application requires internet connection for EdgeTTS service
- FFmpeg must be installed and available in PATH for audio processing
- All text content is in Chinese, specifically for fencing training terminology
- The tool generates MP3 files locally - no data is uploaded to external servers
- Training commands follow a specific structure: area description → ready → attacks → recovery → complete