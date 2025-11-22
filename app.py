import streamlit as st
import pandas as pd
import re
from datetime import datetime
from collections import Counter
import plotly.express as px

# Page config
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide"
)

# Title
st.markdown('<h1 style="text-align: center; color: #25D366;">💬 WhatsApp Chat Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center;">Upload your WhatsApp chat export and discover insights!</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">Created by: Shashwat Pathak</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📤 Upload Chat File")
    uploaded_file = st.file_uploader(
        "Choose your WhatsApp chat (.txt)",
        type=['txt'],
        help="Export chat from WhatsApp: More > Export Chat > Without Media"
    )
    st.markdown("---")
    st.info("""
    **Features:**
    - Member activity stats
    - Peak chat times
    - Emoji usage
    - Word frequency
    - Interactive visualizations
    """)

if uploaded_file:
    content = uploaded_file.read().decode('utf-8')
    lines = content.split('\n')
    
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M)\s-\s([^:]+):\s(.+)'
    
    messages = []
    for line in lines:
        match = re.match(pattern, line)
        if match:
            date_time, author, message = match.groups()
            messages.append({'date': date_time, 'author': author.strip(), 'message': message.strip()})
    
    if messages:
        df = pd.DataFrame(messages)
        
        st.success(f"✅ Loaded {len(df)} messages!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Messages", len(df))
        with col2:
            st.metric("Total Members", df['author'].nunique())
        with col3:
            emoji_count = sum(df['message'].str.count(r'[😀-🙏🌀-🗿🚀-🛿]'))
            st.metric("Emojis Used", emoji_count)
        
        tab1, tab2 = st.tabs(["👥 Member Activity", "📊 Statistics"])
        
        with tab1:
            member_counts = df['author'].value_counts()
            fig = px.bar(x=member_counts.values, y=member_counts.index, 
                        orientation='h',
                        title="Most Active Members")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.dataframe(df.head(50), use_container_width=True)
    else:
        st.error("Could not parse messages. Please check the file format.")
else:
    st.info("👆 Please upload a WhatsApp chat file to begin analysis")
    st.markdown("""
    ### How to export your WhatsApp chat:
    1. Open WhatsApp
    2. Go to the chat you want to analyze
    3. Tap on ⋮ (three dots)
    4. Select **More** → **Export chat**
    5. Choose **Without Media**
    6. Save the .txt file
    7. Upload it here!
    """)
