import os
import streamlit as st
import pandas as pd

# The path to the CSV file used in the background
CSV_FILE_PATH = "C:\Users\gbsan\Downloads\MEDICAL-CHATBOT\data\MedQUAD\medquad.csv"

# Check for required libraries and imports
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
    from langchain_core.messages import HumanMessage, AIMessage
except ImportError as e:
    st.error(f"Required libraries are missing. Please run `pip install -r requirements.txt`. Error: {e}")
    st.stop()


# --- Configuration and Initialization Checks ---

MODEL_NAME = "gemini-2.5-flash"

# !!! TEMPORARY HARDCODING FOR TROUBLESHOOTING !!!
# REPLACE THIS WITH YOUR ACTUAL GEMINI API KEY
API_KEY = "AIzaSyD9Xs5HQ029KTVJjlWisu1bjPYFSJwHBtY" 

# NOTE: The conditional check for the environment variable is commented out
# because the key is now hardcoded above.
# if not API_KEY:
#     st.error("The GEMINI_API_KEY environment variable is not set. Please set it in your terminal before running the app.")
#     st.stop()

if not os.path.exists(CSV_FILE_PATH):
    st.error(f"Error: Required data file not found at path: {CSV_FILE_PATH}. Please ensure the file is created.")
    st.stop()

# --- Data Loading and Caching ---

@st.cache_resource
def load_data(file_path):
    """Loads the static CSV file into a Pandas DataFrame."""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Failed to load data from {file_path}. Error: {e}")
        return None

@st.cache_resource
def get_pandas_agent(df):
    """
    Initializes and caches the Pandas DataFrame Agent with the Gemini model.
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME, 
            google_api_key=API_KEY, 
            temperature=0.0
        )
        
        agent = create_pandas_dataframe_agent(
            llm=llm,
            df=df,
            verbose=True, 
            allow_dangerous_code=True,
            agent_type="openai-tools"
        )
        return agent
    except Exception as e:
        st.error(f"Error initializing LLM/Agent. Check your API Key or network. Details: {e}")
        return None

def clear_session_state():
    """Resets the chat."""
    st.session_state.messages = []

# --- Main Streamlit App ---

def main():
    st.set_page_config(page_title="Medibot", layout="wide")
    st.title("🤖 Medibot")
    st.markdown("This application loads a fixed CSV file and uses the Gemini model to analyze it.")
    
    # 1. Load Data
    df = load_data(CSV_FILE_PATH)
    if df is None:
        return # Stop execution if data loading failed

    # Store DataFrame and file info in session state for consistency
    st.session_state.df = df
    st.session_state.file_name = CSV_FILE_PATH

    # Initialize Agent
    if 'agent' not in st.session_state or st.session_state.agent is None:
        st.session_state.agent = get_pandas_agent(st.session_state.df)

    # Display status and data preview in sidebar
    st.sidebar.success(f"Loaded Data Source: **{st.session_state.file_name}**")
    st.sidebar.dataframe(st.session_state.df.head(), use_container_width=True)


    # 2. Chat Interface and Agent Interaction
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    agent_is_ready = 'agent' in st.session_state and st.session_state.agent is not None
    
    if agent_is_ready:
        
        # Initial greeting
        if len(st.session_state.messages) == 0:
            initial_message = (
                f"Hello! I am connected to the **Employee Data** set. "
                f"It has {len(st.session_state.df)} rows and {len(st.session_state.df.columns)} columns. "
                "Ask me a question, such as 'What is the average salary by department?'"
            )
            st.chat_message("assistant").markdown(initial_message)
            st.session_state.messages.append({"role": "assistant", "content": initial_message})


        # Handle user input
        if prompt := st.chat_input("Ask a question about the employee data..."):
            
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                with st.spinner("Analyzing data..."):
                    try:
                        response = st.session_state.agent.invoke({"input": prompt})
                        result = response["output"]

                        st.markdown(result)
                        st.session_state.messages.append({"role": "assistant", "content": result})
                        
                    except Exception as e:
                        print(f"Agent execution error: {e}")
                        error_message = f"I apologize, I encountered an error while processing that request. Please try rephrasing your question. Error Details: {e}"
                        st.error(error_message)
                        st.session_state.messages.append({"role": "assistant", "content": error_message})
            
    else:
        st.info("The chat interface is waiting for the LLM agent to initialize. Please check the Streamlit console for initialization errors.")


if __name__ == "__main__":
    main()