import random
import streamlit as st
st.set_page_config(page_title="Мій Streamlit Веб-додаток", page_icon="🚀", layout="wide")

st.title("🌟 Мій многофункціональный веб-сайт")


tab1, tab2, tab3 = st.tabs(
    ["📌 Головна", "🎮 Гра 'Вгадай число'", "🔗 Корисні посилання"]
)

with tab1:
    st.header("Ласкаво просимо!")
    st.write("Це головна сторінка вашого Streamlit-додатка.")

with tab2:
    st.subheader("🎲 Гра: Вгадай число від 1 до 100")

    if "secret_number" not in st.session_state:
        st.session_state.secret_number = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False

    user_guess = st.number_input(
        "Твій варіант:", min_value=1, max_value=100, step=1
    )

    col1, col2 = st.columns(2)

    with col1:
    
        if st.button("Перевірити"):
            st.session_state.attempts += 1

            if user_guess < st.session_state.secret_number:
                st.info("📉 Загадане число БІЛЬШЕ!")
            elif user_guess > st.session_state.secret_number:
                st.info("📈 Загадане число МЕНШЕ!")
            else:
                st.success(
                    f"🎉 Перемога! Ти вгадав число {st.session_state.secret_number} за {st.session_state.attempts} спроб!"
                )
                st.session_state.game_over = True

    with col2:

        if st.button("Зіграти знову"):
            st.session_state.secret_number = random.randint(1, 100)
            st.session_state.attempts = 0
            st.session_state.game_over = False
            st.rerun()

with tab3:
    st.header("🔗 Корисні посилання")
    st.write("Нижче наведено список цікавих та корисних ресурсів:")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📚 Навчання та IT")
        st.markdown("[🌐 W3Schools](https://www.w3schools.com) — Туторіали з веб-розробки")
        st.markdown("[🐍 Python.org](https://www.python.org) — Офіційний сайт Python")

    with col_right:
        st.subheader("🎮 Ігри та Розваги")
        st.markdown("[🎮 Steam](https://store.steampowered.com) — Магазин ігор")
        st.markdown("[📺 YouTube](https://www.youtube.com) — Відео та стріми")