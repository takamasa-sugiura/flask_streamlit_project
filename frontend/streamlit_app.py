import streamlit as st

# Streamlit アプリのタイトル
st.title('My Streamlit App')

# ユーザーによる入力を受け取る
user_input = st.text_input("ユーザー名を入力してください", '')

# ボタンが押されたときの動作
if st.button('挨拶'):
    st.write(f'こんにちは、{user_input}さん！')

# スプレッドシートのデータを表示するためのプレースホルダー
data_placeholder = st.empty()

# スプレッドシートからデータをロードして表示
def load_data():
    # ここにデータをロードするコードを書く
    data = {"example": "データ"}
    data_placeholder.table(data)

if st.button('データをロード'):
    load_data()
