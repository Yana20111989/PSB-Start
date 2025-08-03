import streamlit as st
from pymorphy2 import MorphAnalyzer

# Инициализация морфологического анализатора
morph = MorphAnalyzer(lang='ru')

# Функция лемматизации
def lemmatize(text):
    return [morph.parse(word)[0].normal_form for word in text.lower().split()]

# Данные
adaptation_plan = {
    1: "День 1: Знакомство с банком и командой",
    2: "День 2: Оформление доступов",
    3: "День 3: Знакомство с продуктами ПСБ"
}

faq = {
    "доступ": "Оформление доступов происходит через HelpDesk.",
    "продукт": "Информацию о продуктах можно найти в базе знаний.",
    "обратная связь": "Обратную связь можно оставить через корпоративный портал."
}

reminders = {
    2: "Завтра в 10:00 тренинг по продуктам ПСБ",
    3: "Сегодня обед с командой в 13:00"
}

# Интерфейс
st.set_page_config(page_title="Ева — ассистент ПСБ", page_icon="🤖")
st.title("🤖 Ева — Ваш ассистент адаптации")

day = st.sidebar.number_input("Введите день адаптации (1-3):", min_value=1, max_value=3, value=1)
st.sidebar.markdown("📅 Сегодня: " + adaptation_plan.get(day, "Нет данных"))
st.sidebar.markdown("🔔 Напоминание: " + reminders.get(day, "Нет напоминаний"))

# Ввод вопроса
st.subheader("❓ Задай вопрос")
user_input = st.text_input("Например: как оформить доступы?")
if user_input:
    lemmas = lemmatize(user_input)
    response = "Пока не знаю ответа. Обратись к наставнику."
    for lemma in lemmas:
        for keyword in faq:
            if keyword in lemma:
                response = faq[keyword]
                break
    st.info("Ответ: " + response)

# Эмоциональное состояние
st.subheader("🧠 Как настроение?")
mood = st.slider("Оцени своё состояние от 1 (плохо) до 5 (отлично)", 1, 5)
if mood <= 2:
    st.error("Вы отметили низкое самочувствие. Сообщи об этом менеджеру.")
elif mood <= 3:
    st.warning("Если адаптация даётся трудно — обсуди это с наставником.")
else:
    st.success("Отлично, продолжай в том же духе!")
