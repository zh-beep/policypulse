import streamlit as st
import requests
import time
import requests
import twilio

from twilio.rest import Client

# Set the main page configuration
st.set_page_config(page_title="Policy Pulse", layout="wide", initial_sidebar_state="expanded")

# Define custom CSS for styling, including a visible gradient background
st.markdown(
    """
    <style>
        /* Set the body background gradient */
        
        /* Title styling */
        .title {
            text-align: center;
            color: #2b4b7c; /* Dark blue */
            font-size: 70px;
            margin-bottom: 10px;
            font-weight: bold;
        }

        /* Subtitle styling */
        .subtitle {
            text-align: center;
            color: #555;
            font-size: 30px;
            font-weight: 300;
            margin-top: -10px;
        }

        /* Sidebar tweaks */
        .css-1lcbmhc { 
            background-color: #2b4b7c !important; /* Dark blue sidebar */
            color: white !important; /* White text */
        }
        .css-1lcbmhc a {
            color: #f8f9fa !important;
            font-weight: bold;
        }
        .css-1lcbmhc a:hover {
            color: #dfe6e9 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display the title and subtitle with custom styling
st.markdown('<div class="title">Policy Pulse</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Austin</div>', unsafe_allow_html=True)

# Sidebar for always-visible tabs
st.sidebar.title("Navigation")
tab = st.sidebar.radio("Select a Tab", ["Engage", "Connect"], index=0)


# Monitoring function
def monitor_website(url, interval=60):
    global previous_content
    while True:
        try:
            # Fetch the webpage
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the main content (adjust based on the HTML structure of the website)
            new_content = soup.find('div', class_='muni_section').text.strip()

            # Compare with the previous content
            if previous_content != new_content:
                #st.success("Change detected in the Austin Code of Ordinances!")
                #send_alert("Change detected in the Austin Code of Ordinances!")
                previous_content = new_content

            # Wait for the next interval
            time.sleep(interval)
        except Exception as e:
            st.error(f"Error monitoring website: {e}")
            time.sleep(interval)

# Function to send an alert via Twilio
def send_alert(message):
    try:
        phone_number = st.sidebar.text_input("Enter your phone number:", key="phone_number")
        if phone_number:
            twilio_message = client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            st.sidebar.success(f"Alert sent! Message SID: {twilio_message.sid}")
        else:
            st.sidebar.warning("Please enter a valid phone number to receive alerts.")
    except Exception as e:
        st.sidebar.error(f"Failed to send alert: {e}")





if tab == "Engage":
    # Engage Tab - Chatbot
    st.subheader("Engage")
    st.write("Learn more about the laws that affect us")
    
    # Text input for chatbot interaction
    user_input = st.text_input("Type your message here:")
    
    LANGFLOW_API_URL = LANGFLOW_1
    APPLICATION_TOKEN = "APPLICATION_TOKEN_1"  # Replace with your actual token
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {APPLICATION_TOKEN}',
    }
    params = {
    'stream': 'false',
    }

    tweaks = {
    'ChatInput-pkVq3': {},
    'ChatOutput-YHE4F': {},
    'GroqModel-X5O7K': {},
    'SearchAPI-yoQRO': {},
    'AstraDB-lo0ro': {},
    'ParseData-Y0Cmf': {},
    'ParseData-RQfxH': {},
    'CombineText-Rcs8x': {},
   'Prompt-o6x0d': {},
    }
    
    if user_input:
        # Make an API request to LangFlow with the user's input
        # Assume you have an API endpoint (replace with your actual LangFlow API URL)
        url = LANGFLOW_API_URL # Replace with actual LangFlow API URL
        #headers = {"Authorization": "Bearer <TOKEN>"}  # Replace with your API key if necessary
        payload = {'input_value': user_input,
                'output_type': 'chat',
                 'tweaks': {
          'ChatInput-pkVq3': {},
         'ChatOutput-YHE4F': {},
            'GroqModel-X5O7K': {},
        'SearchAPI-yoQRO': {},
        'AstraDB-lo0ro': {},
        'ParseData-Y0Cmf': {},
        'ParseData-RQfxH': {},
        'CombineText-Rcs8x': {},
        'Prompt-o6x0d': {},
    },
}
        
        # Send POST request to LangFlow API
        try:
            response = requests.post(url, params=params,json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for bad responses
            
            # Extract the bot response from the API response
            if response.status_code == 200:
                text_response = response.json()
                bot_reply = text_response['outputs'][0]['outputs'][0]['results']['message']['text']
            else:
                bot_reply = "Error" #bot_reply = response.json().get('reply', 'Sorry, there was an error in processing your request.')
            
            # Show bot response in the UI
            st.write(f"**Bot Response:** {bot_reply}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with LangFlow: {e}")



elif tab == "Connect":
    # Connect Tab - Topics & Contact
    st.subheader("Connect")
    st.write("Select topics you'd like to stay informed on")
    
    # Define the topics list
    topics = [
        {'id': 'housing', 'label': 'Affordable Housing'},
        {'id': 'traffic', 'label': 'Traffic Management'},
        {'id': 'safety', 'label': 'Public Safety'},
        {'id': 'environment', 'label': 'Environmental Protection'},
        {'id': 'education', 'label': 'Education Reform'},
        {'id': 'infrastructure', 'label': 'Infrastructure Development'},
        {'id': 'other', 'label': 'Other'}
    ]
    
    # Extract only the labels for the multiselect
    topic_labels = [topic['label'] for topic in topics]
    
    # Multi-select widget for topics
    selected_topics = st.multiselect("Select Topics", options=topic_labels)
    
    # Input for phone number
    phone_number = st.text_input("Enter your phone number:")
    
    # Button to submit
    if st.button("Subscribe"):
        if selected_topics and phone_number:
            # Add delay of 5 seconds
            st.success(f"Thank you for connecting! You have selected the following topics: {', '.join(selected_topics)}")
            st.success(f"We will reach out to you at: {phone_number}")

            
            # Extract the first selected topic
            first_topic = selected_topics[0]
            
            # LangFlow API request
            LANGFLOW_API_URL = LANGFLOW_2_URL 
            APPLICATION_TOKEN = APPLICATION_TOKEN_2
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {APPLICATION_TOKEN}',
            }
            params = {'stream': 'false'}
            payload = {
                'input_value': first_topic,
                'output_type': 'chat',
                'tweaks': {
                    'ChatInput-pkVq3': {},
                    'ChatOutput-YHE4F': {},
                    'GroqModel-X5O7K': {},
                    'SearchAPI-yoQRO': {},
                    'AstraDB-lo0ro': {},
                    'ParseData-Y0Cmf': {},
                    'ParseData-RQfxH': {},
                    'CombineText-Rcs8x': {},
                    'Prompt-o6x0d': {},
                },
            }
            
            try:
                # Make the LangFlow API request
                response = requests.post(LANGFLOW_API_URL, params=params, json=payload, headers=headers)
                response.raise_for_status()
                
                # Extract the LangFlow response
                if response.status_code == 200:
                    langflow_response = response.json()
                    bot_reply = langflow_response['outputs'][0]['outputs'][0]['results']['message']['text']
                    #bot_reply = langflow_response.get('outputs', [{}])[0].get('outputs', [{}])[0].get('results', {}).get('message', {}).get('text', 'No response received.')
                else:
                    bot_reply = "Error communicating with LangFlow."
                
                # Display LangFlow response
                #st.success(f"LangFlow Response for '{first_topic}': {bot_reply}")
                
                # Twilio API to send SMS
                account_sid = 'AC68684ade52ccd42202590dcf0bebef7e'
                auth_token = TWILIO_AUTH_TOKEN # Replace with your Twilio Auth Token
                client = Client(account_sid, auth_token)
                
                try:
                    # Send the LangFlow response as an SMS
                    message = client.messages.create(
                        from_='+18773605348',  # Replace with your Twilio number
                        body=f"New Law Alert for '{first_topic}': {bot_reply}",
                        to='+18777804236'  # The phone number entered by the user
                    )
                    #st.success(f"SMS sent successfully to {phone_number}. Message SID: {message.sid}")
                except Exception as e:
                    st.error(f"Error sending SMS: {e}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error communicating with LangFlow: {e}")
            
            # Success message
            
        else:
            st.warning("Please select at least one topic and provide your phone number.")

