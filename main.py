import re

def replace_math_symbols(text):
    # �滻 \( �� \) Ϊ $
    text = re.sub(r'\\\(', r'$', text)
    text = re.sub(r'\\\)', r'$', text)
    
    # �滻 \[ �� \] Ϊ $$
    text = re.sub(r'\\\[\s*', r'$$', text)
    text = re.sub(r'\s*\\\]', r'$$', text)
    
    return text

# ʾ���ı�
input_text = r"""
�ڱ�׼״̬�£�����������Ϊ����˫ԭ�ӷ��ӣ��͵�������������������Ϊ \( V_1 / V_2 = 1 / 2 \)��
��������֮�� \[ E_1 / E_2 \] Ϊ��
"""

# ִ���滻
output_text = replace_math_symbols(input_text)

# ������
print(output_text)
