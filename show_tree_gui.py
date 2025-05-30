import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage
from pypinyin import pinyin, Style

# ======================== 多语言支持 ========================
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
    }
}

# 语言选项排序配置
LANGUAGE_OPTIONS = [
    ('en', 'English'),
    ('ja', '日本語'),
    ('ko', '한국어'),
    ('zh-CN', '简体中文'),
    ('zh-TW', '繁體中文')
]


# 按第一个字/字母的罗马音排序
def get_sort_key(item):
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


LANGUAGE_OPTIONS.sort(key=get_sort_key)

current_lang = 'en'


def tr(key):
    return LANG[current_lang].get(key, key)


# ======================== 主应用类 ========================
class DirectoryTreeApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        self.root.title(tr('title'))

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._configure_styles()

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self._setup_header()
        self._setup_tree_display()
        self._setup_statusbar()
        self._setup_menus()

    def _configure_styles(self):
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TButton', padding=6, font=('Segoe UI', 10))
        self.style.configure('TEntry', padding=5, font=('Segoe UI', 10))
        self.style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 10))
        self.style.configure('Status.TLabel', background='#e0e0e0', relief=tk.SUNKEN, padding=5)

        self.style.configure('Primary.TButton', foreground='white', background='#2c7be5',
                             font=('Segoe UI', 10, 'bold'))
        self.style.configure('Warning.TButton', foreground='white', background='#dc3545',
                             font=('Segoe UI', 10))

    def _setup_header(self):
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # 路径输入部分
        path_frame = ttk.Frame(header_frame)
        path_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)

        ttk.Label(path_frame, text=tr('label')).pack(side=tk.LEFT)
        self.entry_path = ttk.Entry(path_frame)
        self.entry_path.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.entry_path.bind('<Return>', lambda e: self.display_tree())

        ttk.Button(path_frame, text=tr('choose_dir'), command=self.browse_directory).pack(side=tk.LEFT)

        # 生成按钮
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text=tr('generate'), style='Primary.TButton',
                   command=self.display_tree).pack(side=tk.LEFT, padx=2)

    def _setup_tree_display(self):
        display_frame = ttk.Frame(self.main_frame)
        display_frame.pack(expand=True, fill=tk.BOTH)

        # 文本显示区域
        text_frame = ttk.Frame(display_frame)
        text_frame.pack(expand=True, fill=tk.BOTH)

        self.text_output = tk.Text(text_frame, wrap=tk.WORD, font=('Consolas', 10), padx=10, pady=10)
        scrollbar = ttk.Scrollbar(text_frame, command=self.text_output.yview)
        self.text_output.config(yscrollcommand=scrollbar.set)

        self.text_output.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 操作按钮
        btn_frame = ttk.Frame(display_frame)
        btn_frame.pack(fill=tk.X, pady=(5, 0))

        self.btn_copy = ttk.Button(btn_frame, text=tr('copy'), command=self.copy_to_clipboard)
        self.btn_copy.pack(side=tk.LEFT, padx=5)

        self.btn_clear = ttk.Button(btn_frame, text=tr('clear'), style='Warning.TButton',
                                    command=self.clear_output)
        self.btn_clear.pack(side=tk.LEFT, padx=5)

        ttk.Button(btn_frame, text=tr('save_txt'), command=lambda: self.save_output(False)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=tr('save_md'), command=lambda: self.save_output(True)).pack(side=tk.LEFT, padx=5)

    def _setup_statusbar(self):
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        ttk.Label(status_frame, text="Copyright © 2025 Ryan Joo", style='Status.TLabel').pack(side=tk.RIGHT, padx=5)

    def _setup_menus(self):
        menubar = tk.Menu(self.root)

        # 选项菜单
        options_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=tr('options_menu'), menu=options_menu)

        # 语言子菜单
        lang_menu = tk.Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label=tr('language_menu'), menu=lang_menu)

        # 添加排序后的语言选项
        for lang_code, lang_name in LANGUAGE_OPTIONS:
            checked = '✓ ' if current_lang == lang_code else ''
            lang_menu.add_command(
                label=f"{checked}{lang_name}",
                command=lambda lc=lang_code: self.switch_language(lc)
            )

        options_menu.add_command(label=tr('about'), command=self.show_about)
        self.root.config(menu=menubar)

    def switch_language(self, lang):
        global current_lang
        if current_lang != lang:
            current_lang = lang
            self.root.title(tr('title'))
            self._update_widget_texts()
            self._setup_menus()  # 重建菜单以更新语言选项

    def _update_widget_texts(self):
        widgets = [
            (self.entry_path.master.winfo_children()[0], 'label'),
            (self.entry_path.master.winfo_children()[2], 'choose_dir'),
            (self.main_frame.winfo_children()[0].winfo_children()[1].winfo_children()[0], 'generate'),
            (self.btn_copy, 'copy'),
            (self.btn_clear, 'clear'),
            *[(btn, text) for btn, text in zip(
                self.main_frame.winfo_children()[1].winfo_children()[1].winfo_children()[2:4],
                ['save_txt', 'save_md'])]
        ]

        for widget, key in widgets:
            widget.config(text=tr(key))

    def show_about(self):
        messagebox.showinfo(tr('about_title'), tr('about_content'))

    def browse_directory(self):
        if path := filedialog.askdirectory():
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, path)

    def generate_tree(self, dir_path, prefix=''):
        tree_str = f"{prefix}{os.path.basename(dir_path)}/\n"
        prefix += '....'
        try:
            for item in sorted(os.listdir(dir_path)):
                path = os.path.join(dir_path, item)
                tree_str += self.generate_tree(path, prefix) if os.path.isdir(path) else f"{prefix}{item}\n"
        except PermissionError:
            tree_str += f"{prefix}[Permission Denied]\n"
        return tree_str

    def display_tree(self):
        dir_path = self.entry_path.get().strip()
        if not os.path.isdir(dir_path):
            messagebox.showerror(tr('error'), tr('invalid_path'))
            return

        try:
            self.text_output.delete(1.0, tk.END)
            self.text_output.insert(tk.END, self.generate_tree(dir_path))
        except Exception as e:
            messagebox.showerror(tr('error'), str(e))

    def save_output(self, as_md=False):
        if not (content := self.text_output.get(1.0, tk.END).strip()):
            messagebox.showwarning(tr('error'), tr('empty'))
            return

        # 设置默认文件名（基于当前目录名）
        default_dir = os.path.basename(self.entry_path.get().strip())
        default_name = f"{default_dir}_tree.{'md' if as_md else 'txt'}" if default_dir else "directory_tree"

        filetypes = [("Markdown Files", "*.md")] if as_md else [("Text Files", "*.txt")]

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

        # 保存文件
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("OK", tr('save_success').format(file_path))
        except Exception as e:
            messagebox.showerror(tr('save_fail'), str(e))

    def copy_to_clipboard(self):
        if content := self.text_output.get(1.0, tk.END).strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.btn_copy.config(text=tr('copy_success'))
            self.root.after(2000, lambda: self.btn_copy.config(text=tr('copy')))
        else:
            messagebox.showinfo(tr('error'), tr('copy_empty'))

    def clear_output(self):
        self.text_output.delete(1.0, tk.END)
        self.btn_clear.config(text=tr('clear_success'))
        self.root.after(2000, lambda: self.btn_clear.config(text=tr('clear')))


if __name__ == "__main__":
    root = tk.Tk()


    # 获取图标路径（兼容打包和直接运行）
    def get_resource_path(relative_path):
        try:
            base_path = sys._MEIPASS  # PyInstaller 临时目录
        except AttributeError:
            base_path = os.path.dirname(os.path.abspath(__file__))  # 直接运行时的目录
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
            print(f"图标加载失败: {e}")  # 调试信息（可选）

    app = DirectoryTreeApp(root)
    root.mainloop()