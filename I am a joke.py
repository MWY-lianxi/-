import streamlit as st
from pathlib import Path
import pandas as pd
import random
from fastai.vision.all import *
import pickle

# 设置工作目录
project_path = Path(__file__).parent
model_path = project_path / "export_windows.pkl"  # 使用Path对象来构建路径

# 加载模型
learn_inf = load_learner(str(model_path))

# 定义函数以从Excel文件加载笑话
def load_jokes_from_excel(filename):
    df = pd.read_excel(filename)
    jokes = df['joke'].tolist()
    return jokes

# 调用函数并传入文件名
jokes = load_jokes_from_excel(project_path / 'jokes.xlsx')  # 使用Path对象

# Streamlit应用界面
st.title("笑话推荐")

# 随机显示3个笑话并获取评分
initial_jokes = random.sample(jokes, 3)
ratings = {joke: 0 for joke in initial_jokes}  # 初始化评分字典

# 遍历笑话并显示评分组件
for joke in initial_jokes:
    st.write(joke)
    ratings[joke] = st.slider("Rate this joke", 0, 5, 3)  # 直接在循环中获取评分

# 创建一个提交评分的按钮
if st.button("Submit Ratings"):
    # 显示推荐的笑话并获取评分
    recommended_jokes = random.sample(jokes, 5)
    recommended_ratings = {joke: st.slider("Rate this joke", 0, 5, 3) for joke in recommended_jokes}

    # 计算并显示用户满意度
    satisfaction = sum(recommended_ratings.values()) / len(recommended_ratings)
    st.write(f"本次推荐的满意度为: {satisfaction:.2f}/5")

# 创建一个提交推荐的评分的按钮
if st.button("Submit Recommended Ratings"):
    # 计算用户对所有笑话的平均评分
    avg_score = sum(ratings.values()) / len(ratings)

    # 计算百分比
    percentage_score = (avg_score / 5) * 100

    # 显示结果
    st.write(f"You rated the jokes {percentage_score:.2f}% of the total possible score.")