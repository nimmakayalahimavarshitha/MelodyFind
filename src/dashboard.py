
import streamlit as st
from src.evaluation import evaluate_results

st.set_page_config(
    page_title="MelodyFind Evaluation",
    page_icon="🎵",
    layout="centered",
)

st.title("🎵 MelodyFind")
st.subheader("Song Recognition Evaluation Dashboard")

st.write(
    "Evaluate how accurately the system identifies songs "
    "from melody queries."
)

st.info(
    "Enter the expected song and the song predicted by the system "
    "for each query."
)

number_of_queries = st.number_input(
    "Number of song queries",
    min_value=1,
    max_value=100,
    value=3,
    step=1,
)

with st.form("evaluation_form"):
    expected_songs = []
    predicted_songs = []

    for i in range(int(number_of_queries)):
        st.markdown(f"### Query {i + 1}")

        expected = st.text_input(
            "Expected song",
            key=f"expected_{i}",
            placeholder="Example: Song A",
        )

        predicted = st.text_input(
            "Predicted song",
            key=f"predicted_{i}",
            placeholder="Example: Song A",
        )

        expected_songs.append(expected.strip())
        predicted_songs.append(predicted.strip())

    submitted = st.form_submit_button("Evaluate Results")

if submitted:
    if any(not song for song in expected_songs + predicted_songs):
        st.error("Please fill in every song field.")
    else:
        results = evaluate_results(expected_songs, predicted_songs)

        st.divider()
        st.header("Evaluation Results")

        col1, col2, col3 = st.columns(3)

        col1.metric("Accuracy", f"{results['accuracy_percent']}%")
        col2.metric("Correct Matches", results["correct_matches"])
        col3.metric("Incorrect Matches", results["incorrect_matches"])

        st.subheader("Query-by-Query Results")

        for i, (expected, predicted) in enumerate(
            zip(expected_songs, predicted_songs), start=1
        ):
            if expected == predicted:
                st.success(
                    f"Query {i}: Correct — identified {predicted}"
                )
            else:
                st.error(
                    f"Query {i}: Incorrect — expected {expected}, "
                    f"predicted {predicted}"
                )
