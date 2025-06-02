"""
目录结构查看器 - show_tree_gui.py
功能：生成可视化的目录结构树，支持多语言、保存文件、复制内容等功能
新增：支持拖放文件夹到输入框自动识别路径
作者：Ryan Joo
版本：v1.1
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage
from pypinyin import pinyin, Style
from tkinterdnd2 import DND_FILES, TkinterDnD

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
        'drop_placeholder': '拖放文件夹到此处...',
    },
    'zh-TW': {
        'title': '目錄結構查看器',
        'label': '目錄路徑：',
        'generate': '生成',
        'save_txt': '保存為文本',
        'save_md': '保存為Markdown',
        'choose_dir': '瀏覽...',
        'error': '錯誤',
        'invalid_path': '目錄路徑無效或不存在',
        'empty': '沒有可保存的目錄結構',
        'save_success': '目錄結構已保存到：\n{}',
        'save_fail': '保存失敗',
        'copy': '複製內容',
        'copy_success': '內容已複製！',
        'copy_empty': '沒有內容可複製',
        'clear': '清空內容',
        'clear_success': '內容已清空',
        'options_menu': '選項',
        'language_menu': '語言',
        'about': '關於',
        'about_title': '關於目錄結構查看器',
        'about_content': '目錄結構查看器 v1.0\n\nCopyright © 2025 Ryan Joo\n\n一款簡單易用的目錄結構生成工具',
        'empty_filename': '請輸入檔案名稱',
        'drop_placeholder': '拖放文件夾到此處...',
    },
    'ja': {
        'title': 'ディレクトリツリービューアー',
        'label': 'ディレクトリパス：',
        'generate': '生成',
        'save_txt': 'テキストで保存',
        'save_md': 'Markdownで保存',
        'choose_dir': '参照...',
        'error': 'エラー',
        'invalid_path': '無効なディレクトリパスまたは存在しません',
        'empty': '保存可能なディレクトリ構造がありません',
        'save_success': 'ディレクトリ構造を保存しました：\n{}',
        'save_fail': '保存に失敗しました',
        'copy': '内容をコピー',
        'copy_success': '内容をコピーしました！',
        'copy_empty': 'コピーする内容がありません',
        'clear': '内容をクリア',
        'clear_success': '内容をクリアしました',
        'options_menu': 'オプション',
        'language_menu': '言語',
        'about': 'について',
        'about_title': 'ディレクトリツリービューアーについて',
        'about_content': 'ディレクトリツリービューアー v1.0\n\nCopyright © 2025 Ryan Joo\n\nディレクトリ構造を生成するシンプルなツール',
        'empty_filename': 'ファイル名を入力してください',
        'drop_placeholder': 'フォルダをここにドラッグ...',
    },
    'ko': {
        'title': '디렉토리 트리 뷰어',
        'label': '디렉토리 경로：',
        'generate': '생성',
        'save_txt': '텍스트로 저장',
        'save_md': 'Markdown으로 저장',
        'choose_dir': '찾아보기...',
        'error': '오류',
        'invalid_path': '유효하지 않은 디렉토리 경로 또는 존재하지 않음',
        'empty': '저장할 디렉토리 구조가 없습니다',
        'save_success': '디렉토리 구조가 저장되었습니다：\n{}',
        'save_fail': '저장 실패',
        'copy': '내용 복사',
        'copy_success': '내용이 복사되었습니다！',
        'copy_empty': '복사할 내용이 없습니다',
        'clear': '내용 지우기',
        'clear_success': '내용이 지워졌습니다',
        'options_menu': '옵션',
        'language_menu': '언어',
        'about': '정보',
        'about_title': '디렉토리 트리 뷰어 정보',
        'about_content': '디렉토리 트리 뷰어 v1.0\n\nCopyright © 2025 Ryan Joo\n\n디렉토리 구조를 생성하는 간단한 도구',
        'empty_filename': '파일 이름을 입력하세요',
        'drop_placeholder': '폴더를 여기에 드래그...',
    },
    'en': {
        'title': 'Directory Tree Viewer',
        'label': 'Path:',
        'generate': 'Generate',
        'save_txt': 'Save as .txt',
        'save_md': 'Save as .md',
        'choose_dir': 'Browse...',
        'error': 'Error',
        'invalid_path': 'Invalid directory path',
        'empty': 'No content to save',
        'save_success': 'Saved to:\n{}',
        'save_fail': 'Save failed',
        'copy': 'Copy',
        'copy_success': 'Copied!',
        'copy_empty': 'No content',
        'clear': 'Clear',
        'clear_success': 'Content cleared',
        'options_menu': 'Options',
        'language_menu': 'Language',
        'about': 'About',
        'about_title': 'About Directory Tree Viewer',
        'about_content': 'Directory Tree Viewer v1.0\n\nCopyright © 2025 Ryan Joo\n\nA simple tool for generating directory structures',
        'empty_filename': 'Please enter a file name',
        'drop_placeholder': 'Drag folder here...',
    }
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
            # 中文、日文、韩文字符处理
            if '\u4e00' <= first_char <= '\u9fff':  # 中文
                return pinyin(first_char, style=Style.NORMAL)[0][0]
            elif '\u3040' <= first_char <= '\u309f':  # 日文平假名
                return first_char
            elif '\u30a0' <= first_char <= '\u30ff':  # 日文片假名
                return first_char
            elif '\uac00' <= first_char <= '\ud7a3':  # 韩文
                return first_char
            else:
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
        self._setup_header()
        self._setup_tree_display()
        self._setup_statusbar()
        self._setup_menus()
        self.setup_drag_drop()

    def _configure_styles(self):
        """配置GUI样式"""
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TButton', padding=6, font=('Segoe UI', 10))
        self.style.configure('TEntry', padding=5, font=('Segoe UI', 10))
        self.style.configure(
            'TLabel', background='#f5f5f5', font=('Segoe UI', 10))
        self.style.configure(
            'Status.TLabel', background='#e0e0e0', relief=tk.SUNKEN, padding=5)

        self.style.configure('Primary.TButton', foreground='white', background='#2c7be5',
                             font=('Segoe UI', 10, 'bold'))
        self.style.configure('Warning.TButton', foreground='white', background='#dc3545',
                             font=('Segoe UI', 10))

        self.style.configure('Drop.TEntry', foreground='#888', font=('Segoe UI', 10))

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
        ttk.Button(path_frame, text=tr('choose_dir'),
                   command=self.browse_directory).pack(side=tk.LEFT)

        # 生成按钮
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text=tr('generate'), style='Primary.TButton',
                   command=self.display_tree).pack(side=tk.LEFT, padx=2)

        # 初始设置拖放占位符
        self.set_drop_placeholder()

        # 设置拖放功能
        self.setup_drag_drop()

    def setup_drag_drop(self):
        """使用 tkinterdnd2 设置跨平台拖放功能"""
        # 焦点事件处理
        self.entry_path.bind('<FocusIn>', self.on_focus_in)
        self.entry_path.bind('<FocusOut>', self.on_focus_out)

        # 使用 tkinterdnd2 的拖放事件
        self.entry_path.drop_target_register(DND_FILES)
        self.entry_path.dnd_bind('<<DropEnter>>', self.on_dnd_drag_enter)
        self.entry_path.dnd_bind('<<DropLeave>>', self.on_dnd_drag_leave)
        self.entry_path.dnd_bind('<<Drop>>', self.on_dnd_drop)

    def setup_windows_drag_drop(self):
        """Windows 特定的拖放实现 - 无需额外依赖"""
        # 注册拖放事件（Windows原生方式）
        self.entry_path.bind('<Enter>', self.on_drag_enter)  # 在Windows上使用Enter事件
        self.entry_path.bind('<Leave>', self.on_drag_leave)  # 使用Leave事件
        self.entry_path.bind('<ButtonRelease-1>', self.on_windows_drop)  # 使用鼠标释放事件

    def on_windows_drop(self, event):
        """Windows 上的拖放模拟处理"""
        try:
            # 检查剪贴板中是否有文件/路径
            import win32clipboard
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):
                # 获取拖放的文件列表
                hdrop = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
                if hdrop and len(hdrop) > 0:
                    path = hdrop[0]
                    if os.path.isdir(path):
                        self.clear_drop_placeholder()
                        self.entry_path.delete(0, tk.END)
                        self.entry_path.insert(0, path)
                        self.entry_path.configure(background='white')  # 恢复背景色
                        self.display_tree()
            win32clipboard.CloseClipboard()
        except ImportError:
            # 如果无法导入 win32clipboard，则显示提示
            messagebox.showinfo("提示", "在Windows上使用拖放功能需要pywin32模块")
        except Exception as e:
            self.entry_path.configure(background='white')  # 确保背景恢复
            messagebox.showwarning(tr('error'), f"拖放处理错误: {str(e)}")

    def set_drop_placeholder(self):
        """设置拖放占位文本"""
        if not self.entry_path.get():
            self.entry_path.configure(style='Drop.TEntry')
            self.entry_path.insert(0, tr('drop_placeholder'))

    def clear_drop_placeholder(self):
        """清除拖放占位文本"""
        current_text = self.entry_path.get()
        if current_text == tr('drop_placeholder'):
            self.entry_path.delete(0, tk.END)
            self.entry_path.configure(style='TEntry')

    def on_focus_in(self, event):
        """输入框获得焦点时的处理"""
        self.clear_drop_placeholder()

    def on_focus_out(self, event):
        """输入框失去焦点时的处理"""
        if not self.entry_path.get():
            self.set_drop_placeholder()

    def on_dnd_drag_enter(self, event):
        """拖放进入时的处理"""
        if event.data:
            self.entry_path.configure(background='#e3f2fd')  # 高亮背景
        return event.action  # 允许拖放

    def on_dnd_drag_leave(self, event):
        """拖放离开时的处理"""
        self.entry_path.configure(background='white')  # 恢复背景色
        return event.action

    def on_dnd_drop(self, event):
        """处理拖放文件事件"""
        self.entry_path.configure(background='white')  # 恢复背景色

        # 获取拖放的数据
        data = event.data.strip()

        # 处理特殊格式（Windows路径带有{}）
        if data.startswith('{') and data.endswith('}'):
            data = data[1:-1]

        # 分割多个文件路径（拖放可能包含多个文件）
        paths = data.split()
        if not paths:
            return

        # 只取第一个有效文件夹
        for path in paths:
            if os.path.isdir(path):
                self.clear_drop_placeholder()
                self.entry_path.delete(0, tk.END)
                self.entry_path.insert(0, path)
                self.display_tree()  # 自动生成目录结构
                break
            elif os.path.isfile(path):
                # 如果是文件，使用其所在目录
                self.clear_drop_placeholder()
                self.entry_path.delete(0, tk.END)
                self.entry_path.insert(0, os.path.dirname(path))
                self.display_tree()  # 自动生成目录结构
                break
        else:
            # 没有找到有效文件夹或文件
            messagebox.showwarning(tr('error'), tr('invalid_path'))

    def _setup_tree_display(self):
        """创建目录树显示区域"""
        display_frame = ttk.Frame(self.main_frame)
        display_frame.pack(expand=True, fill=tk.BOTH)

        # 文本显示区（带滚动条）
        text_frame = ttk.Frame(display_frame)
        text_frame.pack(expand=True, fill=tk.BOTH)

        self.text_output = tk.Text(text_frame, wrap=tk.WORD, font=(
            'Consolas', 10), padx=10, pady=10)
        scrollbar = ttk.Scrollbar(text_frame, command=self.text_output.yview)
        self.text_output.config(yscrollcommand=scrollbar.set)

        self.text_output.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 功能按钮区
        btn_frame = ttk.Frame(display_frame)
        btn_frame.pack(fill=tk.X, pady=(5, 0))

        self.btn_copy = ttk.Button(btn_frame, text=tr(
            'copy'), command=self.copy_to_clipboard)
        self.btn_copy.pack(side=tk.LEFT, padx=5)

        self.btn_clear = ttk.Button(btn_frame, text=tr('clear'), style='Warning.TButton',
                                    command=self.clear_output)
        self.btn_clear.pack(side=tk.LEFT, padx=5)

        # 保存按钮
        ttk.Button(btn_frame, text=tr('save_txt'), command=lambda: self.save_output(
            False)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=tr('save_md'), command=lambda: self.save_output(
            True)).pack(side=tk.LEFT, padx=5)

    def _setup_statusbar(self):
        """创建底部状态栏"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        ttk.Label(status_frame, text="Copyright © 2025 Ryan Joo",
                  style='Status.TLabel').pack(side=tk.RIGHT, padx=5)

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
            current_text = self.entry_path.get()
            old_placeholder = tr('drop_placeholder')  # 切换前的旧占位符
            current_lang = lang  # 切换语言
            new_placeholder = tr('drop_placeholder')  # 切换后的新占位符

            self.root.title(tr('title'))  # 更新窗口标题
            self._update_widget_texts()  # 更新控件文本
            self._setup_menus()  # 重新创建菜单更新语言标记

            # ✅ 更新占位符（如果当前是旧的占位符）
            if current_text == old_placeholder:
                self.entry_path.delete(0, tk.END)
                self.entry_path.insert(0, new_placeholder)

    def _update_widget_texts(self):
        """更新界面控件上的文本（多语言支持）"""
        widgets = [
            (self.entry_path.master.winfo_children()[0], 'label'),
            (self.entry_path.master.winfo_children()[2], 'choose_dir'),
            (self.main_frame.winfo_children()[0].winfo_children()[
                 1].winfo_children()[0], 'generate'),
            (self.btn_copy, 'copy'),
            (self.btn_clear, 'clear'),
            *[(btn, text) for btn, text in zip(
                self.main_frame.winfo_children()[1].winfo_children()[
                    1].winfo_children()[2:4],
                ['save_txt', 'save_md'])]
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
        prefix += '....'
        try:
            for item in sorted(os.listdir(dir_path)):
                path = os.path.join(dir_path, item)
                tree_str += self.generate_tree(path, prefix) if os.path.isdir(
                    path) else f"{prefix}{item}\n"
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
        if not (content := self.text_output.get(1.0, tk.END).strip()):
            messagebox.showwarning(tr('error'), tr('empty'))
            return

        # 生成默认文件名（当前目录名+格式后缀）
        default_dir = os.path.basename(self.entry_path.get().strip())
        default_name = f"{default_dir}_tree.{'md' if as_md else 'txt'}" if default_dir else "directory_tree"

        # 设置文件类型过滤器
        filetypes = [("Markdown Files", "*.md")
                     ] if as_md else [("Text Files", "*.txt")]

        # 弹出保存对话框
        file_path = filedialog.asksaveasfilename(
            defaultextension=".md" if as_md else ".txt",
            filetypes=filetypes,
            initialfile=default_name,
            title=tr('save_md') if as_md else tr('save_txt')
        )

        # 如果用户取消或未选择文件，直接返回
        if not file_path:
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
        if content := self.text_output.get(1.0, tk.END).strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            # 显示成功提示（2秒后恢复）
            self.btn_copy.config(text=tr('copy_success'))
            self.root.after(
                2000, lambda: self.btn_copy.config(text=tr('copy')))
        else:
            messagebox.showinfo(tr('error'), tr('copy_empty'))

    def clear_output(self):
        """清空文本框内容"""
        self.text_output.delete(1.0, tk.END)
        # 显示清除成功提示（2秒后恢复）
        self.btn_clear.config(text=tr('clear_success'))
        self.root.after(2000, lambda: self.btn_clear.config(text=tr('clear')))


if __name__ == "__main__":
    root = TkinterDnD.Tk()  # 使用 TkinterDnD 的窗口


    def get_resource_path(relative_path):
        """获取资源路径（兼容打包环境和源码执行）

        参数：
            relative_path: 资源相对路径

        返回：
            资源的绝对路径
        """
        try:
            base_path = sys._MEIPASS  # PyInstaller 临时目录
        except AttributeError:
            base_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件目录
        return os.path.join(base_path, relative_path)


    # 尝试加载图标
    try:
        ico_path = get_resource_path('iconmonstr-folder-30.ico')
        root.iconbitmap(ico_path)  # Windows 优先使用 .ico
    except Exception as e:
        try:
            png_path = get_resource_path('iconmonstr-folder-30.png')
            img = PhotoImage(file=png_path)  # 备用方案（macOS/Linux）
            root.iconphoto(True, img)
        except Exception as e:
            print(f"图标加载失败: {e}")  # 失败提示（不影响运行）

    # 启动主应用
    app = DirectoryTreeApp(root)
    root.mainloop()
