import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import os

import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi,NoTranscriptFound, TranscriptsDisabled


from fpdf import FPDF
import tempfile


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = '''
        You are a highly accurate and efficient YouTube transcript summarizer.

Given a YouTube transcript as input (in plain text), your task is to:
1. Understand the context and key topics.
2. Generate a concise, accurate summary in simple, easy-to-understand language.
3. Include key highlights, bullet points (if needed), and structure it into meaningful sections (e.g., Introduction, Main Points, Conclusion).
4. Maintain the tone of the speaker (formal, casual, educational, etc.) when summarizing.
5. Avoid redundancy, filler words, and irrelevant data.

--- Example Input Format ---
Transcript: 
"[Start of transcript text here...]"

--- Example Output Format ---
**Title:** [Optional -in largest heading with bold characters, also Generate a suitable title if not given]

**Summary:**
- [Concise overview paragraph in 350 words]

**Key Highlights:**
- Point 1
- Point 2
- Point 3
...

**Conclusion (if applicable):**
[Wrap-up of main takeaway or final thoughts]

Now summarize the following transcript_text:



'''





# def extract_transcript_details(youtube_video_url):
#     try:
#         video_id =  youtube_video_url.split("=")[1]
#         # print(video_id)
#         try:
#             transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
#         except NoTranscriptFound:
#             # Fallback to Hindi (or any available language)
#             transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])

#         transcript = ""
#         for i in transcript_text:
#             transcript += " "+i["text"]
        
#         return transcript

#     except Exception as e:
#         raise e

st.set_page_config(
    page_title="YouTube Transcript Summarizer",  
    page_icon="🎥",                             
    layout="centered",                            
    initial_sidebar_state="auto"                
)

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[-1].split("&")[0]

        try:
            # Try to get English transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except NoTranscriptFound:
            # Fallback to Hindi if English is not available
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])

        # Combine transcript text into a single string
        transcript = " ".join([item["text"] for item in transcript_list])
        return transcript

    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        raise Exception("Transcript not available in supported languages (en, hi).")
    except Exception as e:
        raise e

def generate_gemini_content(transcript_text,prompt):

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt + transcript_text)
    return response.text


st.title("Youtube Transcript to Detailed Notes Converter")

youtube_link = st.text_input("Enter Youtube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    # print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get Detailed Notes"):
    with st.spinner("Fetching transcript and generating summary..."):
         transcript_text = extract_transcript_details(youtube_link)

         if transcript_text:
            summary =  generate_gemini_content(transcript_text,prompt)

            st.markdown('## Summary Notes :');
            st.write(summary)

           
           