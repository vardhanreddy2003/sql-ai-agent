import streamlit as st
import requests

st.set_page_config(
    page_title="SQL AI Agent",
    page_icon="🤖",
    layout="wide"
)

API_URL = "http://127.0.0.1:5000/getAnswer"

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 SQL AI Agent")
st.caption("Ask questions about your database in natural language.")

# ---------------- Sidebar ---------------- #

with st.sidebar:

    st.header("Example Questions")

    examples = [
        "Show all customers",
        "List all active customers",
        "Show each customer's orders",
        "Top 5 expensive products"
    ]

    for example in examples:
        st.write(f"• {example}")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------- Chat History ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            # Workflow Error
            if message.get("error"):

                with st.expander("Workflow Error", expanded=True):
                    st.error(message["error"])

            # Database Error
            elif message.get("database_error"):

                if message.get("query"):
                    with st.expander("Generated SQL", expanded=True):
                        st.code(message["query"], language="sql")

                with st.expander("Database Error", expanded=True):
                    st.error(message["database_error"])

            # SQL Success
            elif message.get("query"):

                with st.expander("Generated SQL", expanded=True):
                    st.code(message["query"], language="sql")

                with st.expander("Database Result", expanded=True):
                    st.dataframe(
                        message.get("query_result", []),
                        use_container_width=True
                    )

            # Normal Response
            elif message.get("result"):

                with st.expander("Result", expanded=True):
                    st.write(message["result"])

# ---------------- User Input ---------------- #

prompt = st.chat_input("Ask a SQL question...")

if prompt:

    # Display User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    # Assistant Response
    with st.chat_message("assistant"):

        with st.spinner("Generating response..."):

            try:

                response = requests.post(
                    API_URL,
                    json={"question": prompt},
                    timeout=120
                )

                response.raise_for_status()

                response_data = response.json()

                data = response_data.get("result", {})

                query = data.get("query", "")
                query_result = data.get("query_result", [])
                answer = data.get("result", "No result")
                workflow_error = data.get("Error", "")
                database_error = data.get("database_error", "")

                # ---------------- Workflow Error ---------------- #

                # if workflow_error:

                #     st.error("⚠️ Workflow Error")

                #     with st.expander("Workflow Error Details", expanded=True):
                #         st.write(workflow_error)

                #     st.session_state.messages.append(
                #         {
                #             "role": "assistant",
                #             "content": "⚠️ Workflow Error",
                #             "error": workflow_error
                #         }
                #     )

                # ---------------- Database Error ---------------- #

                if database_error:

                    st.error("❌ Database Execution Failed")

                    if query:
                        with st.expander("Generated SQL", expanded=True):
                            st.code(query, language="sql")

                    with st.expander("Error", expanded=True):
                        st.write(workflow_error)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": "❌ Database Execution Failed",
                            "query": query,
                            "database_error": workflow_error
                        }
                    )

                # ---------------- SQL Success ---------------- #

                elif query.strip():

                    st.success("✅ Query generated successfully.")

                    with st.expander("Generated SQL", expanded=True):
                        st.code(query, language="sql")

                    with st.expander("Database Result", expanded=True):
                        st.dataframe(
                            query_result,
                            use_container_width=True
                        )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": "✅ Query generated successfully.",
                            "query": query,
                            "query_result": query_result
                        }
                    )

                # ---------------- Normal Response ---------------- #

                else:

                    st.markdown("🤖😊 I can generate SQL queries for you. Wanna give it a try? 🚀")

                    with st.expander("Result", expanded=True):
                        st.write(answer)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": "🤖😊 I can generate SQL queries for you. Wanna give it a try? 🚀",
                            "result": answer
                        }
                    )

            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: {e}")

            except Exception as e:
                st.error(f"Unexpected Error: {e}")