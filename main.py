# -*- coding: GBK -*-
import sys
import re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton

def replace_math_symbols(text):
    ### Notice： 下面两组不能倒过来，否则会替换不完全，按照由严格到宽松的替换原则
    # 替换\( 和 \)为 $
    text = re.sub(r'\\\( ', r'$', text)
    text = re.sub(r' \\\)', r'$', text)
    # 替换\(和\)为 $
    text = re.sub(r'\\\(', r'$', text)
    text = re.sub(r'\\\)', r'$', text)

    # 替换\[和\]为 $$
    text = re.sub(r'\\\[\s*', r'$$', text)
    text = re.sub(r'\s*\\\]', r'$$', text)
    
    return text

class MathSymbolReplacerApp(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("数学符号替换工具")
        self.setGeometry(200, 200, 600, 400)

        # 创建布局
        self.layout = QVBoxLayout()

        # 输入框
        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText("在这里输入包含数学符号的文本...")
        self.layout.addWidget(self.input_text)

        # 按钮
        self.replace_button = QPushButton("替换符号", self)
        self.replace_button.clicked.connect(self.on_replace_clicked)
        self.layout.addWidget(self.replace_button)

        # 输出框
        self.output_text = QTextEdit(self)
        self.output_text.setPlaceholderText("替换后的文本将显示在这里...")
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        # 设置布局
        self.setLayout(self.layout)

    def on_replace_clicked(self):
        # 获取输入文本
        input_text = self.input_text.toPlainText()
        
        # 替换数学符号
        output_text = replace_math_symbols(input_text)

        # 设置输出框的文本
        self.output_text.setPlainText(output_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MathSymbolReplacerApp()
    window.show()

    sys.exit(app.exec())
