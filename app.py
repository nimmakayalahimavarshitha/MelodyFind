"""Melody search UI. Run with ``streamlit run app.py``."""

import json
from pathlib import Path

import streamlit as st

from src.engine import MelodySearchEngine


ROOT = Path(__file__).resolve().parent
SONGS_FILE = ROOT / "data" / "songs.json"
NOTE_NAMES = ("C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B")


def note_name(midi: int) -> str:
    return f"{NOTE_NAMES[midi % 12]}{midi // 12 - 1}"


def clear_melody() -> None:
    st.session_state.melody_notes = []
    st.session_state.search_results = None
    st.session_state.typed_notes = ""


@st.cache_resource
def get_engine(path: str, modified: float) -> MelodySearchEngine:
    del modified  # part of the cache key so rebuilding the JSON refreshes the index
    songs = json.loads(Path(path).read_text(encoding="utf-8"))
    return MelodySearchEngine(songs)


st.set_page_config(page_title="MelodyFind", page_icon="🎵", layout="wide")
st.markdown(
    """
    <style>
    :root { color-scheme: light; }
    .stApp {
        background:
            radial-gradient(ellipse at 10% 0%, rgba(199, 151, 99, .15), transparent 33rem),
            radial-gradient(ellipse at 92% 16%, rgba(125, 132, 99, .10), transparent 28rem),
            #f3efe7;
        color: #302a25;
    }
    [data-testid="stAppViewContainer"] { background: transparent; }
    [data-testid="stHeader"] { background: rgba(243, 239, 231, .84); }
    [data-testid="stAppDeployButton"], button[data-testid="stAppDeployButton"] { display: none !important; }
    .block-container { max-width: 1120px; padding-top: 2.1rem; }
    h1 { color: #302a25; letter-spacing: -.035em; }
    h2, h3, h4 { color: #40372f; }
    p, label, [data-testid="stCaptionContainer"] { color: #74685c; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 253, 249, .88);
        border: 1px solid #e4dbce;
        border-radius: 18px;
        box-shadow: 0 16px 36px rgba(70, 51, 34, .06);
    }
    .st-key-piano_keyboard { position: relative !important; overflow: visible !important; }
    .st-key-piano_whites [data-testid="stHorizontalBlock"] { gap: 0 !important; }
    .st-key-piano_whites [data-testid="column"] { padding: 0 !important; min-width: 0; }
    .st-key-piano_whites .stButton > button {
        position: relative;
        height: 174px;
        border: 1px solid #cfc5b8;
        border-radius: 0 0 10px 10px;
        background: linear-gradient(180deg, #fffefa 0%, #eee8dd 100%);
        color: #40362d;
        font-weight: 700;
        align-items: flex-end;
        padding: 0 0 13px;
        box-shadow: 0 5px 0 #d2c8ba, 0 10px 18px rgba(64, 47, 31, .13);
        transition: filter .12s ease, transform .12s ease, box-shadow .12s ease;
    }
    .st-key-piano_whites .stButton > button:hover {
        border-color: #a76a48;
        color: #6e3d2c;
        filter: brightness(1.04);
        transform: translateY(2px);
        box-shadow: 0 3px 0 #c5b29e, 0 8px 16px rgba(64, 47, 31, .14);
    }
    .st-key-piano_whites .stButton > button:active {
        transform: translateY(5px);
        box-shadow: 0 0 0 #c5b29e;
    }
    .st-key-piano_blacks {
        position: absolute !important;
        inset: 0 0 auto 0 !important;
        z-index: 5;
        height: 0 !important;
        overflow: visible !important;
        pointer-events: none;
    }
    .st-key-piano_blacks [data-testid="stHorizontalBlock"] { gap: 0 !important; height: 112px; }
    .st-key-piano_blacks [data-testid="column"] { padding: 0 !important; min-width: 0; }
    .st-key-piano_blacks .stButton { pointer-events: auto; }
    .st-key-piano_blacks .stButton > button {
        z-index: 2;
        width: 4rem;
        height: 112px;
        margin-left: -2rem;
        border: 1px solid #1f1b18;
        border-radius: 0 0 8px 8px;
        background: linear-gradient(180deg, #51463d 0%, #29231f 88%);
        color: #fffaf2;
        font-size: .78rem;
        box-shadow: 0 5px 0 #171310, 0 10px 14px rgba(44, 33, 25, .25);
    }
    .st-key-piano_blacks .stButton > button:hover {
        border-color: #cb8a63;
        color: #ffe0c8;
        background: linear-gradient(180deg, #685044 0%, #332821 88%);
    }
    .melody-readout {
        display: flex;
        flex-direction: column;
        gap: .35rem;
        min-height: 3.2rem;
        margin: 1.1rem 0 .9rem;
        padding: .75rem 1rem;
        border: 1px solid #e3d8c9;
        border-radius: 12px;
        background: #f6f1e9;
    }
    .melody-readout span { color: #8a573c; font-size: .64rem; font-weight: 800; letter-spacing: .16em; }
    .melody-readout strong { color: #332c26; font-size: 1.05rem; font-weight: 650; }
    [data-testid="stAppDeployButton"] { display: none !important; }
    .st-key-search_button button {
        background: #793b28 !important;
        border: 1px solid #693321 !important;
        color: #fffaf4 !important;
        font-weight: 750;
        box-shadow: 0 6px 15px rgba(121, 59, 40, .2);
    }
    .st-key-search_button button:hover { background: #63301f !important; border-color: #542619 !important; color: #fffaf4 !important; }
    .st-key-clear_button button {
        background: #eee7dc !important;
        border: 1px solid #d7c9b8 !important;
        color: #4d4034 !important;
        font-weight: 650;
    }
    .st-key-clear_button button:hover { background: #e5dacb !important; border-color: #c8b39d !important; color: #352c24 !important; }
    button[kind="primary"] {
        background: #793b28 !important;
        border-color: #693321 !important;
        color: #fffaf4 !important;
    }
    button[kind="primary"] *, button[kind="primary"] p {
        color: #fffaf4 !important;
        fill: #fffaf4 !important;
        opacity: 1 !important;
    }
    [data-testid="stButton"] button:not([kind="primary"]) { color: #40362d !important; }
    [data-testid="stButton"] button:not([kind="primary"]) p { color: inherit !important; opacity: 1 !important; }
    .st-key-piano_blacks .stButton > button,
    .st-key-piano_blacks .stButton > button p { color: #fffaf2 !important; }
    .st-key-piano_blacks .stButton > button:hover,
    .st-key-piano_blacks .stButton > button:hover p { color: #ffe0c8 !important; }
    input, textarea, [data-baseweb="select"] > div {
        background-color: #fffefa !important;
        color: #302a25 !important;
        border-color: #d9cdbd !important;
    }
    input:focus, textarea:focus { border-color: #996246 !important; box-shadow: 0 0 0 1px #996246 !important; }
    [data-testid="stTable"] { border: 1px solid #ded3c5; border-radius: 12px; overflow: hidden; }
    [data-testid="stTable"] table { background: #fffdf9 !important; color: #302a25 !important; border-collapse: collapse !important; }
    [data-testid="stTable"] thead th {
        background: #e9e0d4 !important;
        color: #46392f !important;
        border-bottom: 1px solid #d8cbbc !important;
        font-weight: 700 !important;
    }
    [data-testid="stTable"] tbody td {
        background: #fffdf9 !important;
        color: #342d27 !important;
        border-bottom: 1px solid #ece4da !important;
    }
    [data-testid="stTable"] tbody tr:nth-child(even) td { background: #f6f1e9 !important; }
    [data-testid="stStatusWidget"] button {
        background: #eee7dc !important;
        color: #453a31 !important;
        border: 1px solid #d7c9b8 !important;
    }
    [data-testid="stStatusWidget"] button * { color: #453a31 !important; fill: #453a31 !important; opacity: 1 !important; }
    [data-testid="stAlert"] { background: #f6efe5; color: #4a3d31; border-color: #e4d1bd; }
    @media (max-width: 650px) {
        .st-key-piano_whites .stButton > button { height: 148px; font-size: .75rem; padding-bottom: 10px; }
        .st-key-piano_blacks .stButton > button { width: 2.8rem; height: 96px; margin-left: -1.4rem; font-size: .65rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎵 MelodyFind")
st.caption("Play a short melody and find matching tunes in the Nottingham collection.")

if not SONGS_FILE.exists():
    st.error("Song data is missing. Run `python prepare_data.py` after adding cleaned ABC files to `data/nottingham/`.")
    st.stop()

engine = get_engine(str(SONGS_FILE), SONGS_FILE.stat().st_mtime)
st.caption(f"{len(engine.songs):,} songs in the collection")

if "melody_notes" not in st.session_state:
    st.session_state.melody_notes = []
if "search_results" not in st.session_state:
    st.session_state.search_results = None

with st.container(border=True):
    st.subheader("Play a melody")
    octave = st.radio("Octave", (3, 4, 5), index=1, horizontal=True)
    st.caption("Choose an octave, then play the keys in sequence.")
    with st.container(key="piano_keyboard"):
        with st.container(key="piano_whites"):
            white_columns = st.columns(7, gap="small")
            white_notes = (0, 2, 4, 5, 7, 9, 11)
            for column, pitch_class in zip(white_columns, white_notes):
                if column.button(NOTE_NAMES[pitch_class], key=f"note_{pitch_class}", width="stretch"):
                    st.session_state.melody_notes.append(12 * (octave + 1) + pitch_class)
                    st.session_state.search_results = None
                    st.session_state.typed_notes = ""
        with st.container(key="piano_blacks"):
            black_columns = st.columns([1, .12, 1, .12, 1, 1, .12, 1, .12, 1, .12, 1], gap="small")
            for column, pitch_class in zip((black_columns[i] for i in (1, 3, 6, 8, 10)), (1, 3, 6, 8, 10)):
                if column.button(NOTE_NAMES[pitch_class], key=f"note_{pitch_class}", width="stretch"):
                    st.session_state.melody_notes.append(12 * (octave + 1) + pitch_class)
                    st.session_state.search_results = None
                    st.session_state.typed_notes = ""

    typed_notes = st.text_input("Or type MIDI pitches", placeholder="60 62 64 67", key="typed_notes")
    if typed_notes.strip():
        try:
            query = [int(value) for value in typed_notes.split()]
            if any(pitch < 0 or pitch > 127 for pitch in query):
                raise ValueError
            st.session_state.melody_notes = query
        except ValueError:
            st.warning("Enter MIDI pitch numbers from 0 to 127, separated by spaces.")

    notes = st.session_state.melody_notes
    melody_label = "  ·  ".join(note_name(n) for n in notes) or "Your melody will appear here"
    st.markdown(f"<div class='melody-readout'><span>MELODY</span><strong>{melody_label}</strong></div>", unsafe_allow_html=True)
    search_col, clear_col, _ = st.columns([1, 1, 5])
    if search_col.button("Search", type="primary", width="stretch", key="search_button"):
        if len(notes) < 2:
            st.warning("Add at least two notes to search for a melody pattern.")
        else:
            st.session_state.search_results = engine.search(notes)
    clear_col.button("Clear", on_click=clear_melody, width="stretch", key="clear_button")

if st.session_state.search_results is not None:
    results = st.session_state.search_results
    st.subheader(f"Matching tunes · {len(results)}")
    if results:
        st.table(
            [
                {
                    "Title": song["title"],
                    "Source": song.get("source", ""),
                    "Key": song.get("key") or "",
                    "Meter": song.get("meter") or "",
                    "Notes": len(song["pitches"]),
                }
                for song in results
            ],
            hide_index=True,
            width="stretch",
        )
    else:
        st.info("No matching melody found.")
