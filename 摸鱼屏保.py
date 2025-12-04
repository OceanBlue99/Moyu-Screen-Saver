import sys
import random
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QComboBox, QCheckBox, QLabel, QMenu, QHBoxLayout)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QAction, QPixmap

class LoafingScreen(QWidget):
    def __init__(self, mode, allow_top, allow_menu):
        super().__init__()
        self.mode = mode
        self.allow_menu = allow_menu
        self.click_counter = 0
        self.spinner_index = 0
        
        # 基础窗口设置
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        if allow_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            
        self.showFullScreen()
        
        # 布局容器
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 初始化内容
        self.init_ui()

    def init_ui(self):
        """根据选择的模式绘制界面"""
        
        # 字体设置：为了逼真，必须用微软雅黑 (Microsoft YaHei)
        font_main = QFont("Microsoft YaHei", 25)
        font_bsod = QFont("Microsoft YaHei", 20)
        
        # --- 1. 蓝屏模式 (BSOD - 中文) ---
        if self.mode == "蓝屏 (BSOD)":
            self.setStyleSheet("background-color: #0078D7; color: white;")
            
            face_label = QLabel(":(")
            face_label.setFont(QFont("Microsoft YaHei", 100)) # 表情不需要改
            face_label.setContentsMargins(100, 100, 0, 0)
            
            # 标准中文文案
            text_label = QLabel("你的电脑遇到问题，需要重新启动。\n我们只收集某些错误信息，然后为你重新启动。")
            text_label.setFont(font_bsod)
            text_label.setContentsMargins(100, 20, 100, 50)
            
            self.progress_label = QLabel("完成 20%")
            self.progress_label.setFont(font_bsod)
            self.progress_label.setContentsMargins(100, 0, 0, 100)
            
            self.layout.addStretch(1)
            self.layout.addWidget(face_label)
            self.layout.addWidget(text_label)
            self.layout.addWidget(self.progress_label)
            self.layout.addStretch(1)
            
            self.percent = 20
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_bsod_progress)
            self.timer.start(2000)

        # --- 2. 系统更新模式 (中文) ---
        elif self.mode == "系统更新":
            self.setStyleSheet("background-color: #000000; color: white;")
            center_widget = QWidget()
            v_layout = QVBoxLayout(center_widget)
            
            # 字符动画加载圈
            self.spinner_label = QLabel("⣾") 
            self.spinner_label.setFont(QFont("Segoe UI Symbol", 50)) # 符号字体
            self.spinner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.update_text = QLabel("正在进行更新  已完成 1%\n请勿关闭计算机")
            self.update_text.setFont(QFont("Microsoft YaHei", 18))
            self.update_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            v_layout.addWidget(self.spinner_label)
            v_layout.addWidget(self.update_text)
            
            self.layout.addStretch(1)
            self.layout.addWidget(center_widget)
            self.layout.addStretch(1)
            
            self.percent = 1
            self.anim_timer = QTimer(self)
            self.anim_timer.timeout.connect(self.animate_spinner)
            self.anim_timer.start(100) # 动画速度
            
            self.prog_timer = QTimer(self)
            self.prog_timer.timeout.connect(self.update_windows_progress)
            self.prog_timer.start(1500)

        # --- 3. 系统重启 (中文) ---
        elif self.mode == "系统重启 (Restarting)":
            self.setStyleSheet("background-color: #0078D7; color: white;")
            center_widget = QWidget()
            v_layout = QVBoxLayout(center_widget)
            
            self.spinner_label = QLabel("⣾")
            self.spinner_label.setFont(QFont("Segoe UI Symbol", 60))
            self.spinner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            restart_text = QLabel("正在重启")
            restart_text.setFont(QFont("Microsoft YaHei", 24))
            restart_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            v_layout.addWidget(self.spinner_label)
            v_layout.addWidget(restart_text)
            
            self.layout.addStretch(1)
            self.layout.addWidget(center_widget)
            self.layout.addStretch(1)
            
            self.anim_timer = QTimer(self)
            self.anim_timer.timeout.connect(self.animate_spinner)
            self.anim_timer.start(80)

        # --- 4. 系统恢复 (中文) ---
        elif self.mode == "系统恢复 (Recovery)":
            self.setStyleSheet("background-color: black; color: white;")
            center_widget = QWidget()
            v_layout = QVBoxLayout(center_widget)
            v_layout.setSpacing(25)
            
            # Windows 蓝色 Logo (用田字模拟，或者留空)
            logo_label = QLabel("田") 
            logo_label.setFont(QFont("Microsoft YaHei", 45))
            logo_label.setStyleSheet("color: #00A4EF;") 
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.spinner_label = QLabel("⣾")
            self.spinner_label.setFont(QFont("Segoe UI Symbol", 35))
            self.spinner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.restore_text = QLabel("正在准备自动修复")
            self.restore_text.setFont(QFont("Microsoft YaHei", 16))
            self.restore_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            v_layout.addWidget(logo_label)
            v_layout.addSpacing(30)
            v_layout.addWidget(self.spinner_label)
            v_layout.addWidget(self.restore_text)
            
            self.layout.addStretch(1)
            self.layout.addWidget(center_widget)
            self.layout.addStretch(1)
            
            self.anim_timer = QTimer(self)
            self.anim_timer.timeout.connect(self.animate_spinner)
            self.anim_timer.start(100)
            
            self.percent = 0
            self.prog_timer = QTimer(self)
            self.prog_timer.timeout.connect(self.update_restore_text)
            self.prog_timer.start(4000)

        # --- 5. FBI Warning (保持英文原味，或者你想改成中文也可以) ---
        elif self.mode == "FBI Warning":
            self.setStyleSheet("background-color: black; color: white;")
            red_box = QLabel()
            red_box.setStyleSheet("background-color: #BE0000;")
            red_box.setFixedSize(600, 400)
            red_layout = QVBoxLayout(red_box)
            
            title = QLabel("FBI WARNING")
            title.setFont(QFont("Impact", 40, QFont.Weight.Bold))
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setStyleSheet("color: white; letter-spacing: 5px;")
            
            content = QLabel("Federal Law provides severe civil and criminal penalties for\nthe unauthorized reproduction, distribution\nor exhibition of copyrighted motion pictures,\nvideo tapes or video discs.")
            content.setFont(QFont("Helvetica", 14, QFont.Weight.Bold))
            content.setAlignment(Qt.AlignmentFlag.AlignCenter)
            content.setStyleSheet("color: white;")
            
            red_layout.addWidget(title)
            red_layout.addWidget(content)
            
            h_layout = QHBoxLayout()
            h_layout.addStretch(1)
            h_layout.addWidget(red_box)
            h_layout.addStretch(1)
            
            self.layout.addStretch(1)
            self.layout.addLayout(h_layout)
            self.layout.addStretch(1)

        # --- 6. 卡崩 (截图伪装) ---
        elif self.mode == "卡崩 (截图伪装)":
            screen = QApplication.primaryScreen()
            if screen:
                screenshot = screen.grabWindow(0)
                bg_label = QLabel(self)
                bg_label.setPixmap(screenshot)
                bg_label.setScaledContents(True)
                self.layout.addWidget(bg_label)
            self.setCursor(Qt.CursorShape.WaitCursor)

        # --- 7. Matrix ---
        elif self.mode == "黑客 (Matrix)":
            self.setStyleSheet("background-color: black; color: #00FF00;")
            self.console_label = QLabel()
            self.console_label.setFont(QFont("Consolas", 12))
            self.console_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            self.console_label.setContentsMargins(10,10,10,10)
            self.console_label.setWordWrap(True)
            self.layout.addWidget(self.console_label)
            
            self.matrix_lines = []
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_matrix)
            self.timer.start(80)

    # --- 逻辑更新函数 ---
    
    def animate_spinner(self):
        """核心：字符动画 (Braille Patterns)"""
        # 这组字符完美模拟圆圈旋转，且因为是字体渲染，无锯齿，很清晰
        chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        self.spinner_index = (self.spinner_index + 1) % len(chars)
        self.spinner_label.setText(chars[self.spinner_index])

    def update_bsod_progress(self):
        if self.percent < 100:
            self.percent += random.randint(0, 10)
            if self.percent > 100: self.percent = 100
            self.progress_label.setText(f"完成 {self.percent}%")
    
    def update_windows_progress(self):
        if self.percent < 99:
            if random.random() > 0.6: 
                self.percent += 1
            self.update_text.setText(f"正在进行更新  已完成 {self.percent}%\n请勿关闭计算机")

    def update_restore_text(self):
        texts = [
            "正在准备自动修复",
            "正在诊断你的电脑",
            "正在检查磁盘错误...",
            "正在尝试修复..."
        ]
        idx = (self.percent) % len(texts)
        self.restore_text.setText(texts[idx])
        self.percent += 1

    def update_matrix(self):
        chars = "ABCDEF0123456789"
        line = "".join([random.choice(chars) + " " for _ in range(12)])
        self.matrix_lines.append(f"Sys_Root_Trace: {line} ... [OK]")
        if len(self.matrix_lines) > 40:
            self.matrix_lines.pop(0)
        self.console_label.setText("\n".join(self.matrix_lines))

    # --- 事件处理 (Esc无效化) ---

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            return # 按 Esc 没反应，增加真实度

        # 组合键退出: Ctrl + Alt + Q
        modifiers = event.modifiers()
        if (modifiers & Qt.KeyboardModifier.ControlModifier) and \
           (modifiers & Qt.KeyboardModifier.AltModifier) and \
           event.key() == Qt.Key.Key_Q:
            self.close()

    def mousePressEvent(self, event):
        # 左上角连点3次退出
        if event.button() == Qt.MouseButton.LeftButton:
            if event.pos().x() < 50 and event.pos().y() < 50:
                self.click_counter += 1
                if self.click_counter >= 3:
                    self.close()
            else:
                self.click_counter = 0
        super().mousePressEvent(event)

    def contextMenuEvent(self, event):
        if self.allow_menu:
            context_menu = QMenu(self)
            context_menu.setStyleSheet("""
                QMenu { background-color: #f0f0f0; border: 1px solid #ccc; }
                QMenu::item { padding: 5px 20px; color: black; font-family: 'Microsoft YaHei'; }
                QMenu::item:selected { background-color: #0078d7; color: white; }
            """)
            action_exit = QAction("恢复桌面 (Exit)", self)
            action_exit.triggered.connect(self.close)
            
            context_menu.addAction(QAction("刷新", self))
            context_menu.addAction(QAction("显示设置", self))
            context_menu.addSeparator()
            context_menu.addAction(action_exit)
            context_menu.exec(event.globalPos())

class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("摸鱼伪装器 v4.0 (中文增强版)")
        self.setFixedSize(450, 380)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("摸鱼伪装系统")
        title.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.combo_mode = QComboBox()
        self.combo_mode.setFont(QFont("Microsoft YaHei", 10))
        modes = [
            "系统重启 (Restarting)", 
            "系统恢复 (Recovery)",   
            "系统更新",
            "蓝屏 (BSOD)",
            "卡崩 (截图伪装)", 
            "FBI Warning", 
            "黑客 (Matrix)"
        ]
        self.combo_mode.addItems(modes)
        layout.addWidget(self.combo_mode)

        self.check_top = QCheckBox("窗口置顶 (覆盖任务栏)")
        self.check_top.setFont(QFont("Microsoft YaHei", 9))
        self.check_top.setChecked(True)
        layout.addWidget(self.check_top)

        self.check_menu = QCheckBox("启用右键菜单 (推荐)")
        self.check_menu.setFont(QFont("Microsoft YaHei", 9))
        self.check_menu.setChecked(True)
        layout.addWidget(self.check_menu)
        
        # 安全提示
        tips_frame = QWidget()
        tips_frame.setStyleSheet("background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 5px;")
        tips_layout = QVBoxLayout(tips_frame)
        
        warn_content = QLabel(
            "⚠️ 紧急退出方式:\n"
            "1. 右键菜单 -> '恢复桌面'\n"
            "2. 键盘按: [Ctrl] + [Alt] + [Q]\n"
            "3. 鼠标在【左上角】连续点 3 次"
        )
        warn_content.setFont(QFont("Microsoft YaHei", 9))
        warn_content.setStyleSheet("color: #d9534f; font-weight: bold;")
        
        tips_layout.addWidget(warn_content)
        layout.addWidget(tips_frame)

        btn_start = QPushButton("开始伪装")
        btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_start.setMinimumHeight(45)
        btn_start.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        btn_start.setStyleSheet("""
            QPushButton {
                background-color: #0078d7; color: white; border-radius: 5px;
            }
            QPushButton:hover { background-color: #0063b1; }
        """)
        btn_start.clicked.connect(self.start_loafing)
        layout.addWidget(btn_start)
        
        self.setLayout(layout)

    def start_loafing(self):
        mode = self.combo_mode.currentText()
        top = self.check_top.isChecked()
        menu = self.check_menu.isChecked()
        self.loaf_screen = LoafingScreen(mode, top, menu)
        self.loaf_screen.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    window = ConfigWindow()
    window.show()
    sys.exit(app.exec())