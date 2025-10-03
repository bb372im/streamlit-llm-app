from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
#from langchain.llms import OpenAI 
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

def generate_llm_response(input_text: str, expert_type: str) -> str:
    if expert_type == "キャリアアドバイザー":
        system_message_content = "あなたはIT業界に特化したキャリアアドバイザーです。ユーザーのキャリアに関する質問に、具体的で前向きなアドバイスを提供してください。"
    elif expert_type == "料理の専門家":
        system_message_content = "あなたは栄養と手軽さを重視した料理の専門家です。ユーザーの食材や調理に関する質問に、簡単なレシピやヒントを提供してください。"
    else:
        # 基本となるアシスタントの役割
        system_message_content = "あなたは親切で役立つAIアシスタントです。質問に丁寧に答えてください。"

    try:
        # Lesson 8を参考にLangChainのChatOpenAIを利用してLLMとやり取り
        # ChatOpenAIは内部で環境変数 OPENAI_API_KEY を参照します
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

        messages = [
            SystemMessage(content=system_message_content),
            HumanMessage(content=input_text),
        ]

        # LLMを実行
        result = llm(messages)
        return result.content
        
    except Exception as e:
        # APIキーの設定ミスなど、エラーが発生した場合の処理
        return f"エラーが発生しました: {e}"


# --- 2. Webアプリの概要と操作方法を表示 ---
# Webアプリの概要や操作方法をユーザーに明示するためのテキストを表示（条件に合致）
st.set_page_config(page_title="専門家AIチャットアプリ", layout="centered")
st.title("👨‍💼 専門家AIチャットアプリ")

st.markdown("""
    このアプリでは、選択した**専門家（LLM）**に質問できます。
    
    1. **動作モード**：下のラジオボタンから相談したい専門家を選んでください。（条件に合致）
    2. **質問入力**：質問を入力フォームに記入し、「回答を生成」ボタンを押してください。
    
    選択された専門家が、その役割に特化した回答を生成します。
    ---
""")


# --- 3. ラジオボタンで専門家の種類を選択 ---
# ラジオボタンでLLMに振る舞わせる専門家の種類を選択（条件に合致）
expert_options = ["キャリアアドバイザー", "料理の専門家", "一般的な質問"]
selected_expert = st.radio(
    "相談したい専門家を選んでください:",
    options=expert_options,
    index=0 # デフォルトで「キャリアアドバイザー」を選択
)
st.info(f"現在の専門家: **{selected_expert}**")

# --- 4. 入力フォームと回答表示 ---
# 画面に入力フォームを1つ用意（条件に合致）
query = st.text_area("ここに質問を入力してください：", height=100)

# 入力フォームから送信したテキストをLangChainを使ってLLMにプロンプトとして渡し、回答結果が画面上に表示（条件に合致）
if st.button("回答を生成", type="primary"):
    if query:
        # スピナーを表示し、処理中であることを示す
        with st.spinner("AIが回答を考え中です..."):
            # 定義した関数を利用
            response = generate_llm_response(query, selected_expert)
            
            # 回答結果を表示（条件に合致）
            st.markdown("---")
            st.subheader(f"🤖 {selected_expert}からの回答")
            st.write(response)
    else:
        st.error("質問内容を入力してください。")
    