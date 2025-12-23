import streamlit as st
from history_manager import load_history, save_history, new_chat, delete_chat
from backend_interface import run_research
from summarizers.pdf_summarizer import run_pdf_summary
from summarizers.url_summarizer import run_url_summary
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile

st.set_page_config(page_title="Open Deep Researcher", layout="wide")


def export_chat_to_pdf(chat):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_file.name, pagesize=A4)
    width, height = A4

    y = height - 40
    c.setFont("Helvetica", 10)

    c.drawString(40, y, f"Chat Title: {chat['title']}")
    y -= 30

    for msg in chat["messages"]:
        text = f"{msg['role'].upper()}: {msg['content']}"
        for line in text.split("\n"):
            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - 40
            c.drawString(40, y, line)
            y -= 14
        y -= 10

    c.save()

    with open(temp_file.name, "rb") as f:
        st.download_button(
            label="⬇ Download Chat PDF",
            data=f,
            file_name=f"{chat['title']}.pdf",
            mime="application/pdf"
        )


def main():
    if "chat_id" not in st.session_state:
        history = load_history()
        st.session_state.chat_id = history[0]["id"] if history else new_chat()

    history = load_history()
    chat = next(c for c in history if c["id"] == st.session_state.chat_id)

    # ---------------- SIDEBAR ----------------
    with st.sidebar:
        st.title("🧠 Open Deep Researcher")

        if st.button("➕ New Chat"):
            st.session_state.chat_id = new_chat()
            st.rerun()

        if st.button("📄 Export Chat as PDF"):
            export_chat_to_pdf(chat)

        st.divider()

        with st.expander("🕒 Chat History", expanded=False):
            for c in history:
                col1, col2 = st.columns([8, 1])

                label = f"{c.get('timestamp','')} — {c.get('title','Untitled')}"

                if col1.button(label, key=f"open_{c['id']}"):
                    st.session_state.chat_id = c["id"]
                    st.rerun()

                if col2.button("🗑", key=f"del_{c['id']}"):
                    delete_chat(c["id"])
                    if st.session_state.chat_id == c["id"]:
                        st.session_state.chat_id = new_chat()
                    st.rerun()

        st.divider()

        tool = st.radio(
            "Choose Tool",
            ["Research Assistant", "PDF Summarizer", "URL Summarizer"]
        )

        if tool == "Research Assistant":
            mode = st.radio(
                "Search Focus",
                ["General Web", "Academic Papers"]
            )
        else:
            mode = None

    # ---------------- MAIN ----------------
    st.title(tool)

    # -------- Research Assistant --------
    if tool == "Research Assistant":
        for m in chat["messages"]:
            st.chat_message(m["role"]).markdown(m["content"])

        query = st.chat_input("Ask your question")
        if query:
            chat["messages"].append({"role": "user", "content": query})

            answer, refs = run_research(
                query=query,
                messages=chat["messages"],
                mode=mode
            )

            response = answer
            if refs:
                response += "\n\n### References\n"
                for r in refs:
                    response += f"- {r}\n"

            chat["messages"].append({
                "role": "assistant",
                "content": response,
                "references": refs
            })

            if chat["title"] == "New Chat":
                chat["title"] = query[:50]

            save_history(history)
            st.rerun()

    # -------- PDF Summarizer --------
    elif tool == "PDF Summarizer":
        length = st.radio("Summary Length", ["Short", "Medium", "Long"])
        pdf = st.file_uploader("Upload PDF", type=["pdf"])

        if pdf:
            st.write(run_pdf_summary(pdf, length))

    # -------- URL Summarizer --------
    elif tool == "URL Summarizer":
        length = st.radio("Summary Length", ["Short", "Medium", "Long"])
        url = st.text_input("Enter URL")

        if url:
            st.write(run_url_summary(url, length))


if __name__ == "__main__":
    main()
