import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    VideoUnavailable,
    NoTranscriptFound,
    TooManyRequests,
)

# Streamlit page config
st.set_page_config(
    page_title="YouTube Transcript Extractor",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 YouTube Transcriptor")
st.markdown("Extract and download transcripts from YouTube videos. Paste your link and get started!")

# Extract YouTube Video ID
def extract_video_id(link: str) -> str | None:
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|v\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, link)
    return match.group(1) if match else None

# Get transcript
def get_transcript(video_id: str) -> tuple[str | None, str | None]:
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcripts.find_transcript(["en"])
        text = " ".join([entry["text"] for entry in transcript.fetch()])
        return text, None
    except TranscriptsDisabled:
        return None, "❌ Transcripts are disabled for this video."
    except VideoUnavailable:
        return None, "❌ Video is unavailable."
    except NoTranscriptFound:
        return None, "❌ No transcript found in available languages."
    except TooManyRequests:
        return None, "🚫 Rate limited by YouTube. Try again later."
    except Exception as e:
        return None, f"⚠️ Unexpected error: {str(e)}"

# YouTube Link Input
youtube_link = st.text_input("Enter a YouTube link:", placeholder="https://www.youtube.com/watch?v=...")

if youtube_link:
    video_id = extract_video_id(youtube_link)

    if video_id:
        st.video(f"https://www.youtube.com/watch?v={video_id}")
        st.success(f"✅ Video ID extracted: `{video_id}`")

        if st.button("📄 Get Transcript"):
            with st.spinner("Fetching transcript..."):
                transcript, error = get_transcript(video_id)

                if transcript:
                    st.subheader("📝 Transcript")
                    st.text_area("", transcript, height=300)

                    file_name = f"{video_id}_transcript.txt"
                    st.download_button(
                        label="⬇️ Download Transcript",
                        data=transcript,
                        file_name=file_name,
                        mime="text/plain"
                    )
                else:
                    st.error(error)
    else:
        st.error("❌ Invalid YouTube URL. Please enter a correct link.")

st.markdown("---")
st.markdown("Built with ❤️ by [Raktim](https://github.com/Rktim)")
