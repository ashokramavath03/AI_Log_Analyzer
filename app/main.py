# === app/main.py ===
import streamlit as st
from utils import split_logs_by_lines, extract_timestamped_chunks
from query_engine import QueryEngine
from concurrent.futures import ThreadPoolExecutor

st.set_page_config(page_title="AI Log Analyzer", layout="wide")
st.title("🤖 AI Log Analyzer (Keyword Search)")

uploaded_file = st.file_uploader("📄 Upload your log file", type=["txt", "log"])

if uploaded_file:
    try:
        raw_logs = uploaded_file.read().decode("utf-8")
        lines = split_logs_by_lines(raw_logs)
        chunks = list(extract_timestamped_chunks(lines, window_size=5))

        st.success(f"Indexing {len(chunks)} log chunks for analysis.")
        qe = QueryEngine()
        qe.index_logs(chunks, lines)  # pass raw lines too

        st.subheader("💬 Ask your questions (multi-line supported)")
        user_input = st.text_area("Questions", placeholder="What are the error messages?\nSummarize failed login attempts...")

        if st.button("🔍 Analyze"):
            questions = [q.strip() for q in user_input.strip().splitlines() if q.strip()]

            with st.spinner("Processing your queries..."):
                with ThreadPoolExecutor() as executor:
                    answers = list(executor.map(qe.answer_queries, [[q] for q in questions]))

            for result_list in answers:
                for result in result_list:
                    st.markdown(f"**💬 Question:** {result['question']}")
                    if result['matched_logs']:
                        st.markdown("**🧾 Matched Log Lines:**")
                        for log in result['matched_logs'][:5]:
                            st.code(log, language="text")
                    else:
                        st.markdown("_No log lines matched the query._")
                    
                    st.markdown(f"**🤖 AI Explanation:** {result['answer']}")
                    st.markdown("---")

    except Exception as e:
        st.error(f"⚠️ An error occurred while processing the file: {e}")
