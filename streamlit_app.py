import requests
import uuid
import streamlit as st
st.set_page_config(
    page_title="SQL AI Agent",
    page_icon="🤖",
    layout="wide"
)


API_URL = "http://127.0.0.1:5000/getAnswer"


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())


# ============================================================
# PAGE
# ============================================================

st.title("🤖 SQL AI Agent")
st.caption("Ask questions about your database in natural language.")


# ============================================================
# SIDEBAR
# ============================================================

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

    st.write("Conversation ID:")
    st.code(st.session_state.thread_id)

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())

        st.rerun()


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        # ----------------------------------------------------
        # Workflow Error
        # ----------------------------------------------------

        if message.get("error"):

            with st.expander("Workflow Error", expanded=True):
                st.error(message["error"])


        # ----------------------------------------------------
        # Database Error
        # ----------------------------------------------------

        elif message.get("database_error"):

            if message.get("query"):

                with st.expander("Generated SQL", expanded=True):
                    st.code(
                        message["query"],
                        language="sql"
                    )

            with st.expander("Database Error", expanded=True):
                st.error(message["database_error"])


        # ----------------------------------------------------
        # SQL Success
        # ----------------------------------------------------

        elif message.get("query"):

            with st.expander("Generated SQL", expanded=True):
                st.code(
                    message["query"],
                    language="sql"
                )

            with st.expander("Database Result", expanded=True):
                st.dataframe(
                    message.get("query_result", []),
                    use_container_width=True
                )

            # Show generated answer
            if message.get("result"):

                with st.expander("Answer", expanded=True):
                    st.write(message["result"])


        # ----------------------------------------------------
        # Normal Response
        # ----------------------------------------------------

        elif message.get("result"):

            with st.expander("Result", expanded=True):
                st.write(message["result"])


# ============================================================
# USER INPUT
# ============================================================

prompt = st.chat_input("Ask a SQL question...")


if prompt:

    # ========================================================
    # DISPLAY USER MESSAGE
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)


    # ========================================================
    # ASSISTANT RESPONSE
    # ========================================================

    with st.chat_message("assistant"):

        with st.spinner("Generating response..."):

            try:

                # ------------------------------------------------
                # Send question + thread_id to Flask
                # ------------------------------------------------

                response = requests.post(
                    API_URL,
                    json={
                        "question": prompt,
                        "thread_id": st.session_state.thread_id
                    },
                    timeout=120
                )

                response.raise_for_status()

                response_data = response.json()

                print("Response:", response_data)


                # ------------------------------------------------
                # Extract response
                # ------------------------------------------------

                query = response_data.get(
                    "query",
                    ""
                )

                query_result = response_data.get(
                    "query_result",
                    None
                )

                answer = response_data.get(
                    "result",
                    None
                )

                workflow_error = response_data.get(
                    "workflow_error",
                    None
                )

                database_error = response_data.get(
                    "database_error",
                    None
                )


                # =================================================
                # DATABASE ERROR
                # =================================================

                if database_error:

                    st.error(
                        "❌ Database Execution Failed"
                    )

                    if query:

                        with st.expander(
                            "Generated SQL",
                            expanded=True
                        ):

                            st.code(
                                query,
                                language="sql"
                            )

                    with st.expander(
                        "Database Error",
                        expanded=True
                    ):

                        st.error(database_error)


                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": "❌ Database Execution Failed",
                            "query": query,
                            "database_error": database_error
                        }
                    )


                # =================================================
                # WORKFLOW ERROR
                # =================================================

                elif workflow_error:

                    st.error(
                        "⚠️ Workflow Error"
                    )

                    with st.expander(
                        "Workflow Error Details",
                        expanded=True
                    ):

                        st.write(workflow_error)


                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": "⚠️ Workflow Error",
                            "error": workflow_error
                        }
                    )


                # =================================================
                # SQL SUCCESS
                # =================================================

                elif query.strip():

                    st.success(
                        "✅ Query generated successfully."
                    )


                    # ------------------------------------------------
                    # Generated SQL
                    # ------------------------------------------------

                    with st.expander(
                        "Generated SQL",
                        expanded=True
                    ):

                        st.code(
                            query,
                            language="sql"
                        )


                    # ------------------------------------------------
                    # Database Result
                    # ------------------------------------------------

                    with st.expander(
                        "Database Result",
                        expanded=True
                    ):

                        st.dataframe(
                            query_result,
                            use_container_width=True
                        )


                    # ------------------------------------------------
                    # Answer
                    # ------------------------------------------------

                    if answer:

                        with st.expander(
                            "Answer",
                            expanded=True
                        ):

                            st.write(answer)


                    # ------------------------------------------------
                    # Save to chat history
                    # ------------------------------------------------

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": "✅ Query generated successfully.",
                            "query": query,
                            "query_result": query_result,
                            "result": answer
                        }
                    )


                # =================================================
                # NORMAL RESPONSE
                # =================================================

                else:

                    st.markdown(
                        "🤖😊 I can generate SQL queries for you. "
                        "Wanna give it a try? 🚀"
                    )


                    if answer:

                        with st.expander(
                            "Result",
                            expanded=True
                        ):

                            st.write(answer)


                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": (
                                "🤖😊 I can generate SQL queries for you. "
                                "Wanna give it a try? 🚀"
                            ),
                            "result": answer
                        }
                    )


            # ====================================================
            # REQUEST ERROR
            # ====================================================

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Connection Error: {e}"
                )


            # ====================================================
            # OTHER ERROR
            # ====================================================

            except Exception as e:

                st.error(
                    f"Unexpected Error: {e}"
                )
