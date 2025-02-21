import pandas as pd

# 读取Excel文件（支持xlsm/xlsx格式）
df = pd.read_excel(
    "C:\\Users\\13300\Desktop\\test.xlsx",          # 文件名
    sheet_name="Sheet1",  # 指定工作表
    engine="openpyxl"     # 使用openpyxl引擎
)

# 查找最高分
max_score = df["成绩"].max()

# 获取所有最高分学生（处理并列情况）
top_students = df[df["成绩"] == max_score]["学生姓名"].tolist()

# 输出结果
if len(top_students) == 1:
    print(f"成绩最高的学生是：{top_students[0]}（分数：{max_score}）")
else:
    print(f"并列最高分的学生有：{', '.join(top_students)}（分数：{max_score}）")