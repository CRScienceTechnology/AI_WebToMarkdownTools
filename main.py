# -*- coding: GBK -*-
import sys
import re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton

def replace_math_symbols(text):
    ### Notice�� �������鲻�ܵ�������������滻����ȫ���������ϸ񵽿��ɵ��滻ԭ��
    # �滻\( �� \)Ϊ $
    text = re.sub(r'\\\( ', r'$', text)
    text = re.sub(r' \\\)', r'$', text)
    # �滻\(��\)Ϊ $
    text = re.sub(r'\\\(', r'$', text)
    text = re.sub(r'\\\)', r'$', text)

    # �滻\[��\]Ϊ $$
    text = re.sub(r'\\\[\s*', r'$$', text)
    text = re.sub(r'\s*\\\]', r'$$', text)
    
    return text

class MathSymbolReplacerApp(QWidget):
    def __init__(self):
        super().__init__()

        # ���ô��ڱ���ʹ�С
        self.setWindowTitle("��ѧ�����滻����")
        self.setGeometry(200, 200, 600, 400)

        # ��������
        self.layout = QVBoxLayout()

        # �����
        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText("���������������ѧ���ŵ��ı�...")
        self.layout.addWidget(self.input_text)

        # ��ť
        self.replace_button = QPushButton("�滻����", self)
        self.replace_button.clicked.connect(self.on_replace_clicked)
        self.layout.addWidget(self.replace_button)

        # �����
        self.output_text = QTextEdit(self)
        self.output_text.setPlaceholderText("�滻����ı�����ʾ������...")
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        # ���ò���
        self.setLayout(self.layout)

    def on_replace_clicked(self):
        # ��ȡ�����ı�
        input_text = self.input_text.toPlainText()
        
        # �滻��ѧ����
        output_text = replace_math_symbols(input_text)

        # �����������ı�
        self.output_text.setPlainText(output_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MathSymbolReplacerApp()
    window.show()

    sys.exit(app.exec())
