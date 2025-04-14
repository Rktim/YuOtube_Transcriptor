import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import os

# Set page configuration
st.set_page_config(
    page_title="YouTube Transcript Extractor",
    page_icon="🎬",
    layout="wide"
)

# App title and description
st.title("YouTube Transcriptor📽️")
st.markdown("Extract and save transcripts from YouTube videos")

def extract_video_id(youtube_link):
    """Extract the YouTube video ID from a URL."""
    video_id_pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(video_id_pattern, youtube_link)
    if match:
        return match.group(1)
    return None

def get_transcript(video_id):
    """Get the transcript for a YouTube video."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry['text'] for entry in transcript])
        return text, None
    except Exception as e:
        return None, str(e)

def save_transcript_to_file(transcript, filename):
    """Save the transcript to a text file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(transcript)
        return True, None
    except Exception as e:
        return False, str(e)

# Input for YouTube URL
youtube_link = st.text_input("Enter a YouTube link:", placeholder="https://www.youtube.com/watch?v=...")

# Process when a link is provided
if youtube_link:
    video_id = extract_video_id(youtube_link)
    
    if video_id:
        st.success(f"Successfully extracted video ")
        
        # Display the embedded YouTube video
        st.video(f"https://www.youtube.com/watch?v={video_id}")
        
        # Get transcript button
        if st.button("Get Transcript"):
            with st.spinner("Fetching transcript..."):
                transcript, error = get_transcript(video_id)
                
                if transcript:
                    st.subheader("Transcript")
                    
                    # Display transcript in a scrollable text area
                    st.text_area("", transcript, height=300)
                    
                    # Save transcript section
                    st.subheader("Save Transcript")
                    filename = st.text_input("Filename:", value=f"{video_id}_transcript.txt")
                    
                    if st.button("Save to File"):
                        success, error = save_transcript_to_file(transcript, filename)
                        if success:
                            st.success(f"Transcript saved to {filename}")
                            
                            # Provide download button for the saved file
                            with open(filename, "rb") as file:
                                st.download_button(
                                    label="Download Transcript",
                                    data=file,
                                    file_name=filename,
                                    mime="text/plain"
                                )
                        else:
                            st.error(f"Error saving transcript: {error}")
                else:
                    st.error(f"Error fetching transcript: {error}")
    else:
        st.error("Invalid YouTube link. Please enter a valid YouTube URL.")

# Footer
st.markdown("---")
st.markdown("Hope you find this tool useful! 🚀 If you like it, consider sharing it with your friends. \n\n💡 Created with ❤️ by [Raktim](https://github.com/Rktim)")