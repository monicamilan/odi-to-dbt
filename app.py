import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from graph import Graph


def main():
    if "messages" not in st.session_state:
        # default initial message to render in message state
        st.session_state["messages"] = [AIMessage(
            content="""Hi! I'm your ODI to dbt assistant.
            You can directly share your XML code with me for conversion, 
            or you can ask me questions about it  :)""")]

    # Loop through all messages in the session state and render them as a chat on every st.refresh mech
    for msg in st.session_state.messages:
        # we store them as AIMessage and HumanMessage as its easier to send to LangGraph
        if isinstance(msg, AIMessage):
            st.chat_message("assistant").write(msg.content)
        if isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)

    graph = Graph()

    with st.sidebar:
        st.image("google_cloud_logo.png", caption="ODI to dbt assistant")

    # takes new input in chat box from user and invokes the graph
    if prompt := st.chat_input("Please write your query here"):
        st.session_state.messages.append(HumanMessage(content=prompt))
        st.chat_message("user").write(prompt)

        # Process the AI's response and handles graph events using the callback mechanism
        with st.spinner("Wait a moment.."):
            response = graph.invoke(st.session_state.messages)
            last_msg = response["messages"][-1].content
            # Add that last message to the st_message_state
            st.session_state.messages.append(AIMessage(content=last_msg))
            # visually refresh the complete response after the callback container
            st.chat_message("assistant").write(last_msg)


if __name__ == '__main__':
    main()
