import requests
import streamlit as st
import json
from bs4 import BeautifulSoup

#set page title
st.title('Stackoverflow Profile Summary')

#load local css file for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")


# Code for the sidebar text input
with st.sidebar:
    st.subheader('Enter Stackoverflow User ID:')
    userId = st.text_input('')
    
# Code for the profile info display page
if userId:
    BASEURL = "https://api.stackexchange.com/2.2/users/"+userId
    params = {
    "site" : "stackoverflow"
    }

    #send request and save response in JSON
    resp = requests.get(BASEURL, params=params)
    user_details = resp.json()

    #Scrape user's rating directly
    rank_link = 'https://stackoverflow.com/users/rank?userId='+userId
    profile_page = requests.get(rank_link)
    soup = BeautifulSoup(profile_page.content, 'html.parser')
    
    #assign user details to variables
    display_name = user_details['items'][0]['display_name']
    reputation = user_details['items'][0]['reputation']
    image_url = user_details['items'][0]['profile_image']
    badges = user_details['items'][0]['badge_counts']
    gold = badges['gold']
    silver = badges['silver']
    bronze = badges['bronze']
    percentile = soup.find('b').get_text()

    #Display user details in main page
    st.image(image_url)
    st.markdown(f'<p class="big-font"> Name: {display_name}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="big-font"> Reputation: {reputation}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="big-font"> Badges: </p>', unsafe_allow_html=True)
    st.markdown(f'''
                * <b id="gold">Gold: {gold}</b>
                * <b id="silver">Silver: {silver}</b>
                * <b id="bronze">Bronze: {bronze}</b>
                ''', unsafe_allow_html=True)
    st.markdown(f'<p class="big-font" id="top"> Top: {percentile} Overall</p>', unsafe_allow_html=True)
    
else :
    st.info("Please enter Stackoverflow UserId in the left input box")


