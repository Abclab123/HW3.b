import streamlit as st
from PIL import Image
import openai
import requests
from io import BytesIO

test_image_url = "https://via.placeholder.com/300.png"  # 一个占位符图像链接

# 假设我们的OpenAIGenerator类如下所定义
class OpenAIGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate(self, user_input: str, history: list = []) -> str:
        # 这里应该是调用OpenAI API生成故事的逻辑
        # 因为我们暂时不使用真实的API，我们将返回一个固定的故事片段
        return "After a long journey, the hero finally arrived at the village."

# 假设我们的ImageGenerator类如下所定义
class ImageGenerator:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate_image(self, prompt: str) -> str:
        # 这里应该是调用图像生成API的逻辑
        # 因为我们暂时不使用真实的API，我们将返回一个示例图像的URL
        return test_image_url

# 实例化这些类
story_generator = OpenAIGenerator(api_key='your-openai-api-key')
image_generator = ImageGenerator(model_name='stable-diffusion-model-name')

# 定义generate_story函数，它调用OpenAIGenerator的generate方法
def generate_story(prompt, session_history):
    return story_generator.generate(prompt, session_history)

# 定义generate_image函数，它调用ImageGenerator的generate_image方法
def generate_image(prompt):
    return image_generator.generate_image(prompt)

# Streamlit session state to keep track of the story
if 'session_history' not in st.session_state:
    st.session_state['session_history'] = []

st.title('Interactive Storytelling')




# 在底部放置一個輸入框供用戶輸入
user_input = st.text_input("Continue your story here:", key="user_input")

# 布局按鈕
col1, col2 = st.columns(2)
with col1:
    if st.button('Continue', key="continue"):
        # 處理用戶輸入，並調用相關函數來生成故事和圖像
        # ...
        # 這裡假設generate_story和generate_image是已經定義好的函數
        # 如果session_history为空或者用户输入不等于最后一个元素，则添加用户输入
        if not st.session_state['session_history'] or user_input != st.session_state['session_history'][-1]:
            image_url1 = generate_image(user_input)

            story_piece = generate_story(user_input, st.session_state['session_history'])
            image_url = generate_image(story_piece)

            st.session_state['session_history'].append((user_input, image_url1))
            st.session_state['session_history'].append((story_piece, image_url))
            

with col2:
    if st.button('End', key="end"):
        story_piece = "The End"
        img_url = generate_image(story_piece)
        st.session_state['session_history'].append((story_piece, img_url))
        # 這裡可以添加額外的結束故事的邏輯

# 显示故事和图像的UI逻辑
for i, item in enumerate(reversed(st.session_state['session_history'])):
    # 根据元素类型创建对应的列
    if isinstance(item, tuple) and len(item) == 2:
        text, img_url = item
        if i % 2 == 0:  # 假设AI的输出在左边
            col1, col2 = st.columns([7, 3])
            with col1:
                st.write(text)
            with col2:
                st.image(img_url, use_column_width=True)
        else:  # 假设用户的输入在右边
            col1, col2 = st.columns([3, 7])
            with col1:
                st.image(img_url, use_column_width=True)
            with col2:
                st.write(text)
