import streamlit as st
import pymorphy2
from datetime import datetime

morph = pymorphy2.MorphAnalyzer()

# ==== ДАННЫЕ ====

# План адаптации
adaptation_plan = {
    1: "Знакомство с банком и командой",
    2: "Обзор внутренних сервисов и регламентов",
    3: "Оформление доступов и вход в системы",
    4: "Обзор корпоративной культуры ПСБ",
    5: "Знакомство с продуктами ПСБ",
    6: "Первая обратная связь с наставником",
    7: "Обед с командой. В 13:00 в кафе на 1 этаже."
}

# Частые вопросы
faq = {
    "доступ": "Чтобы оформить доступы, обратись в HelpDesk через портал сотрудников.",
    "продукт": "Информацию о продуктах ПСБ можно найти в разделе «База знаний» на интранете.",
    "обед": "Обед с командой запланирован на 13:00. Место: кафе на 1 этаже.",
    "обратная связь": "Обратную связь можно оставить прямо здесь, через анкету ниже.",
}

# Напоминания
reminders = {
    5: "Завтра тренинг «Технология эффективных продаж» в 10:00",
    6: "Не забудь пройти короткий опрос о самочувствии!",
}

# Мини-квиз
quiz_question = "Какой документ нужно оформить при приёме на работу?"
quiz_answer = "трудовой договор"

# Статус
employee_progress = {
    "Анна": 0.7,
    "Виктор": 0.4,
}

# ==== ФУНКЦИИ ====

def lemmatize(text):
    return [morph.parse(word)[0].normal_form for word in text.lower().split()]

def match_faq(lemmas):
    for lemma in lemmas:
        for key in faq:
            if key in lemma:
                return faq[key]
    return "Не удалось найти ответ. Обратитесь к наставнику."

def check_reminder(day):
    return reminders.get(day, "На сегодня нет напоминаний.")

def get_today_plan(day):
    return adaptation_plan.get(day, "План на сегодня не найден.")

def quiz_check(answer):
    return answer.lower().strip() == quiz_answer.lower()

# ==== ИНТЕРФЕЙС ====

st.set_page_config(page_title="PSB Start | Ева", page_icon="🤖")
st.title("🤖 Ева — Ваш помощник в адаптации в ПСБ")

# Ввод текущего дня
st.sidebar.header("📆 Текущий день адаптации")
day = st.sidebar.number_input("Введите день адаптации (от 1 до 7):", min_value=1, max_value=7, value=1)

# План на день
st.subheader("📋 План на сегодня")
st.info(get_today_plan(day))

# Напоминание
st.subheader("🔔 Напоминание")
st.warning(check_reminder(day))

# Ввод вопроса
st.subheader("❓ Быстрые ответы")
user_question = st.text_input("Введите вопрос:")

if user_question:
    lemmas = lemmatize(user_question)
    answer = match_faq(lemmas)
    st.success(answer)

# Эмоциональное состояние
st.subheader("📈 Как вы себя чувствуете?")
feeling = st.slider("Оцените ваше состояние от 1 (плохо) до 5 (отлично)", 1, 5)
if feeling <= 2:
    st.error("❗️ Вы отметили низкий уровень комфорта. Рекомендуем сообщить об этом менеджеру.")
elif feeling <= 3:
    st.warning("👀 Мы видим, что адаптация идёт не просто. Если что — Ева рядом.")
else:
    st.success("✅ Отлично! Так держать!")

# Мини-квиз
st.subheader("🎓 Мини-обучение")
user_quiz = st.text_input(quiz_question)
if user_quiz:
    if quiz_check(user_quiz):
        st.success("Правильно!")
    else:
        st.error("Неправильно. Попробуй ещё раз.")

# Прогресс для менеджера
st.sidebar.header("👨‍💼 Панель менеджера")
selected_emp = st.sidebar.selectbox("Выберите сотрудника:", list(employee_progress.keys()))
progress = employee_progress[selected_emp]
st.sidebar.metric("Прогресс сотрудника", f"{int(progress * 100)}%")

if selected_emp == "Виктор" and feeling <= 3:
    st.sidebar.error("⚠️ Сигнал риска: Виктор оценил адаптацию ниже 3 дважды")
