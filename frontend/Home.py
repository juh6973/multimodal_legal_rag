import streamlit as st
from src.utils import send_request, convert_image


def chat_history():
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


def format_input() -> dict:
    return {
        "messages": st.session_state.messages,
        }


def input_image() -> str:
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            st.session_state["image"] = convert_image(uploaded_file)
            st.session_state["vision"] = True
        except Exception as e:
            st.error(f"An error occurred: {e}")


def generate_message():
    """Send query to backend and display response."""

    st.write("## Chat")
    # Show chat history
    chat_history()

    st.chat_input("Enter your message here...", key="prompt")

    # Send message to backend
    if st.session_state["prompt"]:

        try:
            # Display user message
            st.chat_message("user").write(st.session_state["prompt"])

            # Send request to backend
            with st.spinner("Generating response..."):

                # Add user message to chat history and format input
                st.session_state["messages"].append({"role": "user", "content": st.session_state["prompt"]})
                body = format_input()

                # Send request to backend
                endpoint = "api/test"
                response = send_request(endpoint, data={"message": st.session_state["prompt"]})

            # Display response
            if response["status_code"] == 200:
                st.chat_message("assistant").write(response["content"])
                st.session_state["messages"].append({"role": "assistant", "content": response["content"]})

            # Display error message
            else:
                st.error(f"Failed to generate response: Status Code: {response['status_code']} {response['content']}")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")
        

def main():
    st.set_page_config(
        page_title="Legal Assistant",
        page_icon=":balance_scale:",
        layout="wide",
    )
    st.title("Multimodal Legal Assistant")

    st.write("This is a multimodal legal assistant that can help you with your legal queries. You can ask questions, upload images, and get responses in text format.")
    st.write("System uses RAG to find the most relevant historical legal cases and help with legal arguments to your current case.")

    st.write("You also can chat with the assistant to get more information about the legal cases.")
    st.divider()

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]


    #input_image()
    generate_message()


if __name__ == "__main__":
    main()