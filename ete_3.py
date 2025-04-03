import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from wordcloud import WordCloud
from PIL import Image
import os

# Load dataset
file_path = "chrispo_2025_dataset.csv"
df = pd.read_csv(file_path)

# Streamlit App
st.set_page_config(page_title="CHRISPO '25 Dashboard", layout="wide")
st.title("🏆 CHRISPO '25 Inter-College Tournament Analysis")
st.markdown("An interactive dashboard to analyze participation trends and feedback.")

# Sidebar Filters (Dropdowns with Selected Fields Displayed in Button Section)
st.sidebar.header("🔍 Filters")
selected_sport = st.sidebar.selectbox("Select Sport", ["All"] + list(df['Sport'].unique()))
selected_college = st.sidebar.selectbox("Select College", ["All"] + list(df['College'].unique()))
selected_state = st.sidebar.selectbox("Select State", ["All"] + list(df['State'].unique()))

# Display selected fields below the dropdowns
if selected_sport != "All":
    st.sidebar.button(f"Selected Sport: {selected_sport}")
if selected_college != "All":
    st.sidebar.button(f"Selected College: {selected_college}")
if selected_state != "All":
    st.sidebar.button(f"Selected State: {selected_state}")

# Filter data
if selected_sport != "All":
    df = df[df['Sport'] == selected_sport]
if selected_college != "All":
    df = df[df['College'] == selected_college]
if selected_state != "All":
    df = df[df['State'] == selected_state]

df_filtered = df

# Display Data
if st.sidebar.checkbox("Show Raw Data", False):
    st.subheader("Raw Data Preview")
    st.write(df_filtered.head(10))

# Participation Trends
st.subheader("📊 Participation Trends")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Participants per Sport")
    fig, ax = plt.subplots()
    sns.countplot(x='Sport', data=df_filtered, order=df_filtered['Sport'].value_counts().index, palette='coolwarm', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.markdown("### Participants per College")
    fig, ax = plt.subplots()
    sns.countplot(x='College', data=df_filtered, order=df_filtered['College'].value_counts().index, palette='viridis', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

col3, col4 = st.columns(2)

with col3:
    st.markdown("### Participants by State")
    fig, ax = plt.subplots()
    sns.countplot(x='State', data=df_filtered, order=df_filtered['State'].value_counts().index, palette='magma', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col4:
    st.markdown("### Participation Over Days")
    fig, ax = plt.subplots()
    sns.countplot(x='Day of Participation', data=df_filtered, palette='plasma', ax=ax)
    st.pyplot(fig)

# Feedback Analysis
st.subheader("💬 Feedback Analysis")

def get_sentiment(text):
    return "Positive" if TextBlob(text).sentiment.polarity > 0 else "Negative"
df_filtered['Sentiment'] = df_filtered['Feedback'].apply(get_sentiment)

col5, col6 = st.columns(2)

with col5:
    st.markdown("### Sentiment Distribution")
    fig, ax = plt.subplots()
    sns.countplot(x='Sentiment', data=df_filtered, palette='coolwarm', ax=ax)
    st.pyplot(fig)

with col6:
    st.markdown("### Word Cloud of Feedback")
    txt = " ".join(df_filtered['Feedback'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(txt)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

# Image Processing Module
st.subheader("📸 Sports Image Processing")

# Day-wise Image Gallery
st.markdown("### 📅 Day-wise Image Gallery")
days = df['Day of Participation'].unique()
selected_day = st.selectbox("Select a Day", sorted(days))

# Directory to store images
day_image_folder = f"images/day_{selected_day}"  # Each day gets its own folder
os.makedirs(day_image_folder, exist_ok=True)

# Upload images per day
uploaded_image = st.file_uploader("Upload an Image for Selected Day", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    image = image.resize((300, 200))  # Resize image to smaller dimensions
    image_path = os.path.join(day_image_folder, uploaded_image.name)
    image.save(image_path)
    st.success("Image uploaded successfully!")

# Display images for the selected day in a 3-column layout
image_files = os.listdir(day_image_folder)
if image_files:
    st.markdown(f"### Uploaded Images for Day {selected_day}")
    cols = st.columns(3)  # Create 3 columns
    for index, img_file in enumerate(image_files):
        img_path = os.path.join(day_image_folder, img_file)
        with cols[index % 3]:  # Arrange images in 3 columns
            st.image(img_path, caption=img_file, width=200)
else:
    st.warning(f"No images available for Day {selected_day}.")

st.markdown("### 📌 Summary")
st.write("✅ This dashboard provides insights into participation trends and feedback for CHRISPO '25.")
st.write("✅ Use the filters to customize your analysis.")
st.write("✅ Check the raw data for a detailed look at participant details.")
st.write("✅ Upload images for each day and view them.")
st.write("✅ Browse day-wise sports images.")

st.write("🔹 Developed for CHRISPO '25 Inter-College Tournament Analysis")