import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Initialize ChatGroq with the API key and model
llm = ChatGroq(
    temperature=0, 
    groq_api_key=os.getenv("GROQ_API_KEY"), 
    model_name="llama-3.1-70b-versatile"
)

# Initialize the prompt template
prompt_teacher = PromptTemplate.from_template(
    """
    ### STUDENT QUERY:
    {student_query}
    
    ### INSTRUCTION:
    You are an IT Helpdesk Virtual Assistant designed to assist users with troubleshooting and resolving IT-related issues efficiently. Your goal is to provide clear, step-by-step guidance tailored to the user’s specific needs while maintaining a friendly, professional tone throughout the interaction.

    When users approach you with a problem, first determine the category of their issue. Classify it into one of the following areas:

    User Account Management (e.g., password resets, account permissions, MFA setup).
    Hardware Support (e.g., troubleshooting devices, installation, and repairs).
    Software Support (e.g., application installation, updates, and error resolution).
    Network Support (e.g., Wi-Fi issues, VPN setup, or network outages).
    IT Security (e.g., antivirus, phishing incidents, and data protection).
    also all the other category. Once the category is identified, provide relevant sub-options and guide the user through troubleshooting steps. Ensure instructions are concise and actionable, using simple language that even non-technical users can understand. Present steps in a logical sequence and confirm if the issue is resolved before proceeding.

    For example, if the user selects "User Account Management," ask clarifying questions like, “Are you looking to reset a password or manage permissions?” Based on their response, outline the specific steps required to address the issue. Always encourage users to provide feedback or ask further questions if they need more assistance.

    If the issue is resolved, acknowledge their success with a positive response like, "That’s great to hear! If you have more questions, feel free to ask." If the problem persists or needs escalation, guide the user on how to contact the IT team or submit a support ticket.

    By following this approach, you will ensure users receive precise, effective, and satisfactory support for their IT concerns.
    
    ### RESPONSE:
    """
)

st.set_page_config(layout="wide")

# Streamlit App Title
st.title("WatsonX IT Support : Your AI-Powered IT Support Partner")
st.caption("Powered by IBM watsonX")


# Initialize session state to store past interactions
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

# Function to get response from LLM using the PromptTemplate
def get_response(user_query):
    # Prepare the input for the prompt template
    formatted_prompt = prompt_teacher.format(student_query=user_query)
    response = llm.invoke(formatted_prompt)
    return response.content  # Access the content attribute

# User input field
user_input = st.text_input("Ask a question about your subject:")

# If there is user input, call the LLM and store the interaction
if user_input:
    with st.spinner("Generating response..."):
        # Append user message to the conversation
        st.session_state['conversation'].append({"role": "user", "content": user_input})
        
        # Get AI response using the prompt template
        response = get_response(user_input)

        # Append AI response to the conversation
        st.session_state['conversation'].append({"role": "ai", "content": response})

# Display chat history with formatted chat bubbles
for message in st.session_state['conversation']:
    if message["role"] == "user":
        st.markdown(
            f"""
            <div style='background-color: #DCF8C6; color: black; padding: 10px; border-radius: 15px; margin-left: 80px; max-width: 100%;'>
            <strong>You:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
    elif message["role"] == "ai":
        st.markdown(
            f"""
            <div style='background-color: #E3F2FD; color: black; padding: 10px; border-radius: 15px; margin: 10px; max-width: 100%; margin-left: auto;'>
            <strong>AI:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)

# Add JavaScript for auto-scrolling
st.markdown(
    """
    <script>
    const chatContainer = document.querySelector('div[data-baseweb="container"]');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    </script>
    """,
    unsafe_allow_html=True
)
