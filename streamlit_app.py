import html
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Day 2 Geostatistics Quiz",
    page_icon="📝",
    layout="centered",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 900px; padding-top: 2rem; padding-bottom: 3rem;}
    .subject-title {text-align:center; color:#123B66; font-size:34px; font-weight:700; margin-bottom:4px;}
    .subtitle {text-align:center; color:#5A6B7B; margin-bottom:20px;}
    .question-number {color:#555; font-size:17px; font-weight:600; margin-top:18px;}
    .correct-box {background:#E8F5E9; border-left:6px solid #2E7D32; color:#1B5E20; padding:15px; border-radius:6px; margin-top:15px;}
    .incorrect-box {background:#FFEBEE; border-left:6px solid #C62828; color:#B71C1C; padding:15px; border-radius:6px; margin-top:15px;}
    .explanation-box {background:#F4F7FA; border-left:6px solid #1565C0; color:#1F2937; padding:15px; border-radius:6px; margin-top:10px;}
    .score-box {text-align:center; background:#EEF4FB; border:1px solid #B7CCE3; padding:12px; border-radius:8px; font-size:19px; font-weight:700; color:#123B66;}
    </style>
    """,
    unsafe_allow_html=True,
)

QUESTION_FILE = Path(__file__).with_name("questions_file.csv")
REQUIRED_COLUMNS = [
    "subject", "question", "option_a", "option_b", "option_c", "option_d",
    "correct_answer", "explanation",
]


@st.cache_data
def load_questions(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path, encoding="utf-8")
    df.columns = df.columns.str.strip()

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))
    if df.empty:
        raise ValueError("The question file contains no questions.")

    for column in REQUIRED_COLUMNS:
        df[column] = df[column].fillna("").astype(str).str.strip()

    blank_rows = df[(df[REQUIRED_COLUMNS] == "").any(axis=1)]
    if not blank_rows.empty:
        rows = ", ".join(str(index + 2) for index in blank_rows.index)
        raise ValueError(f"Blank required value in CSV row(s): {rows}")

    df["correct_answer"] = df["correct_answer"].str.upper()
    invalid = df[~df["correct_answer"].isin({"A", "B", "C", "D"})]
    if not invalid.empty:
        rows = ", ".join(str(index + 2) for index in invalid.index)
        raise ValueError(f"Invalid correct_answer in CSV row(s): {rows}")

    if df["subject"].nunique() != 1:
        raise ValueError("All rows must use the same subject title.")

    return df


def initialise_quiz() -> None:
    defaults = {
        "question_index": 0,
        "score": 0,
        "submitted": False,
        "selected_answer": None,
        "answers": {},
        "quiz_completed": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_quiz() -> None:
    for key in [
        "question_index", "score", "submitted", "selected_answer",
        "answers", "quiz_completed",
    ]:
        st.session_state.pop(key, None)
    st.rerun()


try:
    if not QUESTION_FILE.exists():
        raise FileNotFoundError(f"{QUESTION_FILE.name} was not found.")
    questions = load_questions(QUESTION_FILE)
except Exception as error:
    st.error(f"Unable to load the quiz: {error}")
    st.stop()

initialise_quiz()
total_questions = len(questions)
subject_title = html.escape(questions.iloc[0]["subject"])
attempted = len(st.session_state.answers)

st.markdown(f'<div class="subject-title">{subject_title}</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Day 2 • Medium-Level Objective Assessment</div>', unsafe_allow_html=True)

score_col, attempted_col = st.columns(2)
with score_col:
    st.markdown(
        f'<div class="score-box">Score: {st.session_state.score}/{total_questions}</div>',
        unsafe_allow_html=True,
    )
with attempted_col:
    st.markdown(
        f'<div class="score-box">Answered: {attempted}/{total_questions}</div>',
        unsafe_allow_html=True,
    )

st.progress(attempted / total_questions, text=f"Quiz progress: {attempted} of {total_questions}")

if st.session_state.quiz_completed:
    percentage = 100 * st.session_state.score / total_questions
    st.success("Quiz completed successfully.")
    st.metric("Final score", f"{st.session_state.score}/{total_questions}", f"{percentage:.1f}%")

    if percentage >= 80:
        st.success("Excellent performance!")
    elif percentage >= 60:
        st.info("Good performance. Review the explanations to strengthen weaker areas.")
    else:
        st.warning("Review the explanations and attempt the quiz again.")

    with st.expander("Review all answers"):
        for index, row in questions.iterrows():
            mapping = {
                "A": row["option_a"], "B": row["option_b"],
                "C": row["option_c"], "D": row["option_d"],
            }
            student_answer = st.session_state.answers.get(index)
            correct = row["correct_answer"]
            st.markdown(f"### Question {index + 1}: {row['question']}")
            if student_answer == correct:
                st.success(f"Your answer: {student_answer}. {mapping[student_answer]}")
            else:
                st.error(f"Your answer: {student_answer}. {mapping.get(student_answer, 'No answer')}")
                st.success(f"Correct answer: {correct}. {mapping[correct]}")
            st.info(f"Explanation: {row['explanation']}")
            st.divider()

    if st.button("Restart quiz", type="primary", use_container_width=True):
        reset_quiz()
    st.stop()

question_index = st.session_state.question_index
row = questions.iloc[question_index]
option_mapping = {
    "A": row["option_a"], "B": row["option_b"],
    "C": row["option_c"], "D": row["option_d"],
}

st.markdown(
    f'<div class="question-number">Question {question_index + 1} of {total_questions}</div>',
    unsafe_allow_html=True,
)
st.subheader(row["question"])
radio_options = [f"{letter}. {text}" for letter, text in option_mapping.items()]

if not st.session_state.submitted:
    with st.form(key=f"question_form_{question_index}", clear_on_submit=False):
        selected_option = st.radio("Select one answer:", radio_options, index=None)
        submit_answer = st.form_submit_button(
            "Submit answer", type="primary", use_container_width=True
        )

    if submit_answer:
        if selected_option is None:
            st.warning("Please select an option before submitting.")
        else:
            selected_letter = selected_option[0]
            st.session_state.selected_answer = selected_letter
            st.session_state.answers[question_index] = selected_letter
            st.session_state.submitted = True
            if selected_letter == row["correct_answer"]:
                st.session_state.score += 1
            st.rerun()

if st.session_state.submitted:
    selected = st.session_state.selected_answer
    correct = row["correct_answer"]

    if selected == correct:
        st.markdown(
            f'<div class="correct-box"><strong>Correct!</strong><br>'
            f'Correct answer: {correct}. {html.escape(option_mapping[correct])}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="incorrect-box"><strong>Your answer is incorrect.</strong><br>'
            f'You selected: {selected}. {html.escape(option_mapping[selected])}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="correct-box"><strong>Correct answer:</strong><br>'
            f'{correct}. {html.escape(option_mapping[correct])}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="explanation-box"><strong>Explanation:</strong><br>'
        f'{html.escape(row["explanation"])}</div>',
        unsafe_allow_html=True,
    )

    if question_index < total_questions - 1:
        if st.button("Next question", type="primary", use_container_width=True):
            st.session_state.question_index += 1
            st.session_state.submitted = False
            st.session_state.selected_answer = None
            st.rerun()
    elif st.button("Finish quiz", type="primary", use_container_width=True):
        st.session_state.quiz_completed = True
        st.rerun()

st.sidebar.header("Quiz information")
st.sidebar.write(f"**Subject:** {questions.iloc[0]['subject']}")
st.sidebar.write(f"**Questions:** {total_questions}")
st.sidebar.write(f"**Current score:** {st.session_state.score}/{total_questions}")
st.sidebar.caption("The question file is loaded internally. No upload or question-bank controls are exposed to students.")
if st.sidebar.button("Reset quiz"):
    reset_quiz()
