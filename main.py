import re

def replace_math_symbols(text):
    # 替换 \( 和 \) 为 $
    text = re.sub(r'\\\(', r'$', text)
    text = re.sub(r'\\\)', r'$', text)
    
    # 替换 \[ 和 \] 为 $$
    text = re.sub(r'\\\[\s*', r'$$', text)
    text = re.sub(r'\s*\\\]', r'$$', text)
    
    return text

# 示例文本
input_text = r"""
在标准状态下，若氧气（视为刚性双原子分子）和氮气的理想气体的体积比为 \( V_1 / V_2 = 1 / 2 \)，
则其内能之比 \[ E_1 / E_2 \] 为：
"""

# 执行替换
output_text = replace_math_symbols(input_text)

# 输出结果
print(output_text)
