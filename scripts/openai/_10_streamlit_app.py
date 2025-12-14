"""
A Streamlit application for interacting with the agent.

Got a bit more complex than expected, but it works.
"""

import asyncio
import atexit
from queue import Queue
from threading import Thread

import streamlit as st
from agents import Agent, Runner, SQLiteSession
from agents.mcp.server import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(page_title="Elsa - Agent Chat", page_icon="🤖")
st.title("Elsa - Agent Chat")


class AsyncRunner:
    """Persistent event loop in a background thread for async operations."""

    def __init__(self):
        self.loop = None
        self.thread = None
        self.queue = Queue()
        self._start()

    def _start(self):
        """Start the background thread with event loop."""

        def run_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()

        self.thread = Thread(target=run_loop, daemon=True)
        self.thread.start()

        # Wait for loop to be ready
        while self.loop is None:
            pass

    def run(self, coro):
        """Run a coroutine in the background event loop."""
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        return future.result()

    def cleanup(self):
        """Cleanup the event loop."""
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.thread.join(timeout=5)


# Initialize persistent async runner
@st.cache_resource
def get_async_runner():
    runner = AsyncRunner()
    atexit.register(runner.cleanup)
    return runner


async_runner = get_async_runner()


# Initialize MCP server and agent
@st.cache_resource
def init_agent_and_connect(_async_runner):
    """Initialize agent and connect to MCP server."""
    titanic_mcp_server = MCPServerStreamableHttp(
        params=MCPServerStreamableHttpParams(
            url="http://localhost:8000/mcp",
        )
    )

    agent = Agent(
        name="Elsa",
        instructions="You are a helpful agent.",
        mcp_servers=[titanic_mcp_server],
    )

    # Connect to the MCP server
    _async_runner.run(titanic_mcp_server.connect())

    return agent


agent = init_agent_and_connect(async_runner)

# Initialize chat history and session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm Elsa, your helpful agent. How can I assist you today?"}
    ]

if "session" not in st.session_state:
    st.session_state.session = SQLiteSession("streamlit_chat")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            try:
                # Run the agent with the session to maintain conversation history
                result = async_runner.run(Runner.run(agent, prompt, session=st.session_state.session))
                full_response = result.final_output
            except Exception as e:
                full_response = f"❌ An error occurred: {str(e)}"
                st.error(full_response)

        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
