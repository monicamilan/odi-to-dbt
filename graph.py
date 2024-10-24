from typing import Annotated, TypedDict

from langgraph.graph import START, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from langchain_google_vertexai import ChatVertexAI

from system_prompt import system_prompt


class State(TypedDict):
    """
    Class intended to create a conversation history.

    Messages have the type "list". The `add_messages` function
    in the annotation defines how this state key should be updated
    (in this case, it appends messages to the list, rather than overwriting them)
    """
    messages: Annotated[list[AnyMessage], add_messages]


class Graph:
    def __init__(self) -> None:
        """
        Class containing the necessary tools to build the graph.
        """
        self.llm: ChatVertexAI = ChatVertexAI(model_name="gemini-1.5-pro", temperature=0.0, top_k=1)

        graph: StateGraph = StateGraph(State)
        graph.add_edge(START, "model_node")
        graph.add_node("model_node", self._call_model)

        self.graph_runnable = graph.compile()

    def _call_model(self, state: State) -> dict:
        """ Private method that performs the core invocation of the model.

            args:
                state (State): Conversation status
        """
        messages = state["messages"]
        response = self.llm.invoke([system_prompt] + messages)
        return {"messages": [response]}  # add the response to the messages using LangGraph reducer paradigm

    # Function to invoke the compiled graph externally
    def invoke(self, messages) -> dict:
        """ Private method that invokes the graph with the current messages.

            args:
                messages (State): Conversation history
        """
        return self.graph_runnable.invoke({"messages": messages})
