"""
目录结构查看器 - show_tree_gui.py
功能：生成可视化的目录结构树，支持多语言、保存文件、复制内容等功能
作者：Ryan Joo
版本：v1.0
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage
from pypinyin import pinyin, Style  # 用于中文拼音处理

# ======================== 多语言支持 ========================
# 支持的语言: 简体中文/繁体中文/英文/日文/韩文
LANG = {
    'zh-CN': {
        'title': '目录结构查看器',
        'label': '目录路径：',
        'generate': '生成',
        'save_txt': '保存为文本',
        'save_md': '保存为Markdown',
        'choose_dir': '浏览...',
        'error': '错误',
        'invalid_path': '目录路径无效或不存在',
        'empty': '没有可保存的目录结构',
        'save_success': '目录结构已保存到：\n{}',
        'save_fail': '保存失败',
        'copy': '复制内容',
        'copy_success': '内容已复制！',
        'copy_empty': '没有内容可复制',
        'clear': '清空内容',
        'clear_success': '内容已清空',
        'options_menu': '选项',
        'language_menu': '语言',
        'about': '关于',
        'about_title': '关于目录结构查看器',
        'about_content': '目录结构查看器 v1.0\n\nCopyright © 2025 Ryan Joo\n\n一款简单易用的目录结构生成工具',
        'empty_filename': '请输入文件名',
    },
    # ... 其他语言翻译（此处省略保持简洁）
}

# 语言选项配置（语言代码，显示名称）
LANGUAGE_OPTIONS = [
    ('en', 'English'),
    ('ja', '日本語'),
    ('ko', '한국어'),
    ('zh-CN', '简体中文'),
    ('zh-TW', '繁體中文')
]


# 按首字母拼音/字母排序语言选项
def get_sort_key(item):
    """获取排序依据：非ASCII字符按拼音/原字符，ASCII字符转小写"""
    first_char = item[1][0]
    if ord(first_char) > 255:  # 非ASCII字符
        try:
            if '\u4e00' <= first_char <= '\u9fff':  # 中文
                return pinyin(first_char, style=Style.NORMAL)[0][0]
            else:  # 日文/韩文
                return first_char
        except:
            return first_char
    else:  # ASCII字符
        return first_char.lower()


# 对语言选项进行排序
LANGUAGE_OPTIONS.sort(key=get_sort_key)

# 当前语言（默认为英文）
current_lang = 'en'


def tr(key):
    """翻译函数：根据当前语言返回对应文本"""
    return LANG[current_lang].get(key, key)


# ======================== 主应用类 ========================
class DirectoryTreeApp:
    """目录树生成器主应用类"""

    def __init__(self, root):
        """初始化应用窗口"""
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        """设置主界面布局"""
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        self.root.title(tr('title'))  # 多语言标题

        # 样式配置
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._configure_styles()

        # 主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # 构建界面组件
        self._setup_header()  # 顶部区域
        self._setup_tree_display()  # 主显示区域
        self._setup_statusbar()  # 状态栏
        self._setup_menus()  # 菜单栏

    def _configure_styles(self):
        """配置GUI样式"""
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TButton', padding=6, font=('Segoe UI', 10))
        # ...（其他样式配置略）...

    def _setup_header(self):
        """创建顶部路径选择区域"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # 路径输入框和浏览按钮
        path_frame = ttk.Frame(header_frame)
        path_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)

        ttk.Label(path_frame, text=tr('label')).pack(side=tk.LEFT)
        self.entry_path = ttk.Entry(path_frame)
        self.entry_path.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        # 回车键绑定生成功能
        self.entry_path.bind('<Return>', lambda e: self.display_tree())

        # 目录浏览按钮
        ttk.Button(path_frame, text=tr('choose_dir'), command=self.browse_directory).pack(side=tk.LEFT)

        # 生成按钮
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text=tr('generate'), style='Primary.TButton',
                   command=self.display_tree).pack(side=tk.LEFT, padx=2)

    def _setup_tree_display(self):
        """创建目录树显示区域"""
        display_frame = ttk.Frame(self.main_frame)
        display_frame.pack(expand=True, fill=tk.BOTH)

        # 文本显示区（带滚动条）
        text_frame = ttk.Frame(display_frame)
        text_frame.pack(expand=True, fill=tk.BOTH)

        self.text_output = tk.Text(text_frame, wrap=tk.WORD, font=('Consolas', 10), padx=10, pady=10)
        scrollbar = ttk.Scrollbar(text_frame, command=self.text_output.yview)
        self.text_output.config(yscrollcommand=scrollbar.set)

        self.text_output.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 功能按钮区
        btn_frame = ttk.Frame(display_frame)
        btn_frame.pack(fill=tk.X, pady=(5, 0))

        self.btn_copy = ttk.Button(btn_frame, text=tr('copy'), command=self.copy_to_clipboard)
        self.btn_copy.pack(side=tk.LEFT, padx=5)

        self.btn_clear = ttk.Button(btn_frame, text=tr('clear'), style='Warning.TButton',
                                    command=self.clear_output)
        self.btn_clear.pack(side=tk.LEFT, padx=5)

        # 保存按钮
        ttk.Button(btn_frame, text=tr('save_txt'), command=lambda: self.save_output(False)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=tr('save_md'), command=lambda: self.save_output(True)).pack(side=tk.LEFT, padx=5)

    def _setup_statusbar(self):
        """创建底部状态栏"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        ttk.Label(status_frame, text="Copyright © 2025 Ryan Joo", style='Status.TLabel').pack(side=tk.RIGHT, padx=5)

    def _setup_menus(self):
        """创建菜单系统"""
        menubar = tk.Menu(self.root)

        # 选项菜单
        options_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=tr('options_menu'), menu=options_menu)

        # 语言子菜单
        lang_menu = tk.Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label=tr('language_menu'), menu=lang_menu)

        # 动态生成排序后的语言选项
        for lang_code, lang_name in LANGUAGE_OPTIONS:
            # 添加选中的标记
            checked = '✓ ' if current_lang == lang_code else ''
            lang_menu.add_command(
                label=f"{checked}{lang_name}",
                command=lambda lc=lang_code: self.switch_language(lc)
            )

        # 关于菜单项
        options_menu.add_command(label=tr('about'), command=self.show_about)
        self.root.config(menu=menubar)

    def switch_language(self, lang):
        """切换应用程序语言"""
        global current_lang
        if current_lang != lang:
            current_lang = lang
            self.root.title(tr('title'))  # 更新窗口标题
            self._update_widget_texts()  # 更新控件文本
            self._setup_menus()  # 重新创建菜单更新语言标记

    def _update_widget_texts(self):
        """更新界面控件上的文本（多语言支持）"""
        # 获取需要更新的控件列表及对应的翻译键
        widgets = [
            (self.entry_path.master.winfo_children()[0], 'label'),
            (self.entry_path.master.winfo_children()[2], 'choose_dir'),
            # ...（其他控件绑定略）...
        ]

        # 遍历更新所有控件文本
        for widget, key in widgets:
            widget.config(text=tr(key))

    def show_about(self):
        """显示关于对话框"""
        messagebox.showinfo(tr('about_title'), tr('about_content'))

    def browse_directory(self):
        """打开目录选择对话框"""
        if path := filedialog.askdirectory():
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, path)

    def generate_tree(self, dir_path, prefix=''):
        """递归生成目录树结构文本

        参数：
            dir_path: 当前目录路径
            prefix: 缩进前缀（用于递归）

        返回：
            格式化的目录树字符串
        """
        tree_str = f"{prefix}{os.path.basename(dir_path)}/\n"
        prefix += '....'  # 每层增加4个空格缩进

        try:
            # 遍历目录并排序展示
            for item in sorted(os.listdir(dir_path)):
                path = os.path.join(dir_path, item)
                if os.path.isdir(path):
                    # 递归处理子目录
                    tree_str += self.generate_tree(path, prefix)
                else:
                    # 文件项
                    tree_str += f"{prefix}{item}\n"
        except PermissionError:
            tree_str += f"{prefix}[Permission Denied]\n"
        return tree_str

    def display_tree(self):
        """在文本框中显示目录树"""
        dir_path = self.entry_path.get().strip()

        # 路径验证
        if not os.path.isdir(dir_path):
            messagebox.showerror(tr('error'), tr('invalid_path'))
            return

        try:
            # 清空文本框并插入新内容
            self.text_output.delete(1.0, tk.END)
            self.text_output.insert(tk.END, self.generate_tree(dir_path))
        except Exception as e:
            messagebox.showerror(tr('error'), str(e))

    def save_output(self, as_md=False):
        """保存目录树到文件（文本或Markdown格式）

        参数：
            as_md: 是否为Markdown格式（默认False为纯文本）
        """
        # 获取文本框内容
        content = self.text_output.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning(tr('error'), tr('empty'))
            return

        # 生成默认文件名（当前目录名+格式后缀）
        default_dir = os.path.basename(self.entry_path.get().strip())
        default_name = f"{default_dir}_tree.{'md' if as_md else 'txt'}" if default_dir else "directory_tree"

        # 设置文件类型过滤器
        filetypes = [("Markdown Files", "*.md")] if as_md else [("Text Files", "*.txt")]

        # 弹出保存对话框
        file_path = filedialog.asksaveasfilename(
            defaultextension=".md" if as_md else ".txt",
            filetypes=filetypes,
            initialfile=default_name,
            title=tr('save_md') if as_md else tr('save_txt')
        )

        if not file_path:  # 用户取消
            return

        # 写入文件
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("OK", tr('save_success').format(file_path))
        except Exception as e:
            messagebox.showerror(tr('save_fail'), str(e))

    def copy_to_clipboard(self):
        """复制文本框内容到剪贴板"""
        content = self.text_output.get(1.0, tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            # 显示成功提示（2秒后恢复）
            self.btn_copy.config(text=tr('copy_success'))
            self.root.after(2000, lambda: self.btn_copy.config(text=tr('copy')))
        else:
            messagebox.showinfo(tr('error'), tr('copy_empty'))

    def clear_output(self):
        """清空文本框内容"""
        self.text_output.delete(1.0, tk.END)
        # 显示清除成功提示（2秒后恢复）
        self.btn_clear.config(text=tr('clear_success'))
        self.root.after(2000, lambda: self.btn_clear.config(text=tr('clear')))


# ======================== 程序入口 ========================
if __name__ == "__main__":
    root = tk.Tk()  # 创建主窗口


    def get_resource_path(relative_path):
        """获取资源路径（兼容打包环境和源码执行）

        参数：
            relative_path: 资源相对路径

        返回：
            资源的绝对路径
        """
        try:
            base_path = sys._MEIPASS  # PyInstaller临时目录
        except AttributeError:
            base_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件目录
        return os.path.join(base_path, relative_path)


    # 尝试加载程序图标
    try:
        ico_path = get_resource_path('iconmonstr-folder-30.ico')
        root.iconbitmap(ico_path)  # Windows .ico
    except Exception:
        try:
            png_path = get_resource_path('iconmonstr-folder-30.png')
            img = PhotoImage(file=png_path)  # macOS/Linux
            root.iconphoto(True, img)
        except Exception as e:
            print(f"图标加载失败: {e}")  # 失败提示（不影响运行）

    # 启动主应用
    app = DirectoryTreeApp(root)
    root.mainloop()
