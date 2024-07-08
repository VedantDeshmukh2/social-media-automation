import streamlit as st
import requests
import json
from utils import calculate_api_price
import os

# Set your API key as an environment variable
os.environ['OPENROUTER_API_KEY'] = YOUR_KEY_HERE"

# Load samples from the 'twitter_posts.txt' file
with open('twitter_posts.txt', 'r') as file:
    samples = file.read()

# Streamlit app for generating Twitter posts
def main():
    st.set_page_config(page_title='Twitter Post Generator', page_icon=':bird:', layout='wide')
    
    st.markdown("<h1 style='text-align: center;'>Twitter Post Generator</h1>", unsafe_allow_html=True)

    # Get the API key from environment variables
    api_key = os.getenv('OPENROUTER_API_KEY')

    # Initialize session state variable for content
    if 'content' not in st.session_state:
        st.session_state.content = ''

    # Get the content input from the user
    st.session_state.content = st.text_area('Enter the content to convert into a Twitter post:', value=st.session_state.content, height=200)

    if st.button('Generate Twitter Post'):
        if api_key and st.session_state.content:
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            data = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    { "role": "user", "content": f"Convert the below content into a Twitter post in my writing style.\n\n{st.session_state.content}\n\n\nHere are some of my previous Twitter posts:\n\n{samples}\n\n\n\n\n" }
                ]
            }
            
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(data)
            )
            response_data = response.json()
            
            if 'choices' in response_data and len(response_data['choices']) > 0 and 'message' in response_data['choices'][0] and 'content' in response_data['choices'][0]['message']:
                post_text = response_data['choices'][0]['message']['content']
                st.success('Twitter Post Generated!')
                
                # Extract plain text from the API response and display it in a scrollable text area
                st.text_area('Generated Twitter Post:', value=post_text, height=400)
                
                # Add a button to copy the generated post to clipboard
                if st.button('Copy to Clipboard'):
                    st.code(post_text)
                    st.success('Twitter post copied to clipboard!')
                
                # Calculate and display the API cost
                total_price, input_tokens, input_price, output_tokens, output_price, total_tokens = calculate_api_price(response_data)
                
                st.markdown(f"<h3>API Cost Breakdown:</h3>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                col1.metric("Input Tokens", input_tokens)
                col2.metric("Output Tokens", output_tokens)
                col3.metric("Total Tokens", total_tokens)
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Input Cost", f"${input_price:.2f}")
                col2.metric("Output Cost", f"${output_price:.2f}")
                col3.metric("Total Cost", f"${total_price:.2f}")
            else:
                st.error('Failed to generate post. Check API response structure.')
        else:
            st.warning('Please enter both the API key and content.')

if __name__ == '__main__':
    main()
