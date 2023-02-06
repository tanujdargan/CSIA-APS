import os
import threading

import av
import pyrebase
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer

from audio_handling import AudioFrameHandler
from drowsy_detection import VideoFrameHandler

# Define the audio file to use.
alarm_file_path = os.path.join("audio", "wake_up.wav")
logged_in = False

# Streamlit Components
st.set_page_config(
    page_title="Drowsiness Detection | APS",
    page_icon="https://framerusercontent.com/modules/466qV2P53XLpEfUjjmZC/FNnZTYISEsUGPpjII54W/assets/VebAVoINVBFxBTpsrQVLHznVo.png",
    initial_sidebar_state="expanded",
)

menu_choice = option_menu(
            menu_title=None,  
            options=["Home", "Login", "Signup", "About"],  
            icons=["house", "box-arrow-in-right", "images", "question-circle", "envelope"],  
            menu_icon="cast",  
            default_index=0,  
            orientation="horizontal",
        )

config = {"apiKey": "AIzaSyBzAOFDCn0D4CJCMqfwwQrnuTltMKZowDw",
  "authDomain": "csia-5825d.firebaseapp.com",
  "databaseURL": "https://csia-5825d-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "projectId": "csia-5825d",
  "storageBucket": "csia-5825d.appspot.com",
  "messagingSenderId": "144604127326",
  "appId": "1:144604127326:web:d63d822a8327f708e154cf",
  "measurementId": "G-ENG9V1LE8C"}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

if menu_choice == "Home":
    st.title("Drowsiness Detection")
    with st.container():
        c1, c2 = st.columns(spec=[1, 1])
        with c1:
            # The amount of time (in seconds) to wait before sounding the alarm.
            WAIT_TIME = st.slider("Seconds to wait before sounding alarm:", 0.0, 5.0, 1.0, 0.25)

        with c2:
            # Lowest valid value of Eye Aspect Ratio. Ideal values [0.15, 0.2].
            EAR_THRESH = st.slider("Eye Aspect Ratio threshold:", 0.0, 0.4, 0.18, 0.01)

    thresholds = {
        "EAR_THRESH": EAR_THRESH,
        "WAIT_TIME": WAIT_TIME
    }

    # For streamlit-webrtc
    video_handler = VideoFrameHandler()
    audio_handler = AudioFrameHandler(sound_file_path=alarm_file_path)

    lock = threading.Lock()  # For thread-safe access & to prevent race-condition.
    shared_state = {"play_alarm": False}  # Shared state between callbacks.

    def video_frame_callback(frame: av.VideoFrame):
        frame = frame.to_ndarray(format="bgr24")  # Decode and convert frame to RGB

        frame, play_alarm = video_handler.process(frame, thresholds)  # Process frame
        with lock:
            shared_state["play_alarm"] = play_alarm  # Update shared state

        return av.VideoFrame.from_ndarray(frame, format="bgr24")  # Encode and return BGR frame

    def audio_frame_callback(frame: av.AudioFrame):
        with lock:  # access the current “play_alarm” state
            play_alarm = shared_state["play_alarm"]

        new_frame: av.AudioFrame = audio_handler.process(frame, play_sound=play_alarm)
        return new_frame

    ctx = webrtc_streamer(
        key="drowsiness-detection",
        video_frame_callback=video_frame_callback,
        audio_frame_callback=audio_frame_callback,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},  # Add this to config for cloud deployment.
        media_stream_constraints={"video": {"height": {"ideal": 480}}, "audio": False},
        video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False),
    )

#handling login

if menu_choice == "Login":
    st.text('Login')
    email = st.text_input('Enter email')
    password = st.text_input('Enter password',type="password")
    if st.button('Login'):
        try:
            global login
            login = auth.sign_in_with_email_and_password(email, password)
            st.success("Successfully logged in!")
            menu_choice = "Home"
            user_id = auth.get_account_info(login["idToken"])["users"][0]["localId"]
            email = auth.get_account_info(login["idToken"])["users"][0]["email"]
            os.environ["email"] = email
            os.environ["user_id"] = user_id
            os.environ["logged_in"] = "True"
        except:
            st.error("Invalid email or password")
    

#Signup Function
if menu_choice == "Signup":
    st.text('Signup')
    email = st.text_input('Enter email')
    password = st.text_input('Enter password',type="password")
    if st.button('Signup'):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            st.success("Successfully signed up!")
        except:
            st.error("Email already exists")
    
    
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)