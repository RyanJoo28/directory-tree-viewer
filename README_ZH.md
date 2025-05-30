# 📂 目录树查看器

![Python版本](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![GUI支持](https://img.shields.io/badge/GUI-Tkinter-orange)

**多语言目录结构可视化工具** | [English](#-features) | [中文](#-功能特性)

---

## ✨ 功能特性
- 支持中文/英文/日文/韩文/繁体中文
- 图形化界面(Tkinter)
- 导出目录树为文本/Markdown格式
- 自动识别系统语言并适配排序规则

![](./docs/SCREENSHOTS/preview1.png)

![](./docs/SCREENSHOTS/preview2.png)

![](./docs/SCREENSHOTS/preview3.png)

---

## 🚀 快速开始
### 基础安装
```bash
# 克隆项目
git clone https://github.com/yourname/dir-tree-viewer.git

# 安装依赖
pip install -r requirements.txt

# 启动GUI
python show_tree_gui.py
```

### 可执行文件

Windows用户可直接下载 [Releases页面](https://github.com/yourname/dir-tree-viewer/releases) 的 `.exe` 文件

## 🛠️ 开发构建

### 依赖管理

```bash
# 生成新requirements.txt
pip freeze > requirements.txt

# 构建可执行文件
pyinstaller --onefile --icon=assets/icon.ico show_tree_gui.py
```

## 📜 许可证

本项目采用 [MIT License](LICENSE)

