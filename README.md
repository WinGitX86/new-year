# 2026 马年拜年动画

作者：WinGitX86  
许可证：GNU General Public License v3.0

## 简介

一款运行于终端的拜年动画，采用 Python 标准库 `curses` 编写，无任何外部依赖。  
动画包含红色主题边框、手绘灯笼、鞭炮、小马简笔画、随机飘落的祝福字（福禄寿喜财马吉祥等）及横向滚动祝福语。  
播放时长为 **30 秒**，结束后**自动删除自身脚本文件**，以释放存储空间。

## ⚠️ 重要警告

- **程序会在运行结束后删除自身**（`new_year_animation.py` 文件将被永久删除）。  
- **如果您希望多次使用本动画，请务必在运行前备份一份副本。**  
- 备份命令示例：`cp new_year_animation.py new_year_animation_backup.py`

## 运行环境

- **操作系统**：Linux / macOS / Termux (Android) 等支持 `curses` 的系统  
- **Python 版本**：3.6 或更高（需包含 `curses` 模块，Termux 默认自带）  
- **终端尺寸**：建议至少 80 列 × 24 行，否则会提示放大终端

## 使用方法

1. 将本脚本保存为 `new_year_animation.py`  
2. 打开终端，执行：  
   ```bash
   python new_year_animation.py