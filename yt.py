import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    VideoUnavailable,
    NoTranscriptFound,
    TooManyRequests,
)

st.set_page_config(
    page_title="YouTube Transcriptor",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 YouTube Transcripxtractor")
st.markdown("Paste a YouTube link to extract and download its transcript.")

# Extract video ID
def extract_video_id(url):
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Get transcript using preferred method
def fetch_transcript(video_id):
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcripts.find_transcript(['en'])
        full_text = " ".join([entry['text'] for entry in transcript.fetch()])
        return full_text, None
    except TranscriptsDisabled:
        return None, "🚫 Transcripts are disabled for this video."
    except VideoUnavailable:
        return None, "🚫 This video is unavailable."
    except NoTranscriptFound:
        return None, "⚠️ No transcript found for this video in English."
    except TooManyRequests:
        return None, "🚫 Rate limit exceeded. Try again later."
    except Exception as e:
        return None, f"❌ Unexpected error: {str(e)}"

# Input
youtube_url = st.text_input("📎 Paste YouTube video URL", placeholder="https://www.youtube.com/watch?v=...")

if youtube_url:
    video_id = extract_video_id(youtube_url)

    if video_id:
        st.video(f"https://www.youtube.com/watch?v={video_id}")

        if st.button("📄 Get Transcript"):
            with st.spinner("Fetching transcript..."):
                transcript, error = fetch_transcript(video_id)

                if transcript:
                    st.success("✅ Transcript fetched successfully!")

                    st.text_area("Transcript:", transcript, height=300)

                    st.download_button(
                        label="⬇️ Download Transcript",
                        data=transcript,
                        file_name=f"{video_id}_transcript.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(error)
    else:
        st.error("❌ Invalid YouTube link. Please check and try again.")
