"""
Streamlit UI for Voice to Image App - Capstone Project 2
"""
import streamlit as st
import logging
import hashlib
from agent import VoiceToImageAgent
from audio_processor import transcribe_audio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Voice to Image",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "history" not in st.session_state:
    st.session_state.history = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "processed_audio_hash" not in st.session_state:
    st.session_state.processed_audio_hash = None
if "current_result" not in st.session_state:
    st.session_state.current_result = None


def initialize_agent():
    """Initialize the AI agent."""
    try:
        if st.session_state.agent is None:
            st.session_state.agent = VoiceToImageAgent()
            logger.info("Agent initialized successfully")
        return True
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        logger.error(f"Agent initialization error: {e}")
        return False


def get_audio_hash(audio_bytes):
    """Generate a hash for audio data to detect if it's new."""
    return hashlib.md5(audio_bytes).hexdigest()


def process_audio(audio_bytes):
    """Process audio input and generate image."""
    if st.session_state.processing:
        return
    
    audio_hash = get_audio_hash(audio_bytes)
    
    if audio_hash == st.session_state.processed_audio_hash:
        return
    
    st.session_state.processing = True
    st.session_state.processed_audio_hash = audio_hash
    
    try:
        transcript = transcribe_audio(audio_bytes)
        
        if not transcript:
            st.error("❌ Failed to transcribe audio. Please try again.")
            st.info("💡 Tips: Speak clearly, reduce background noise, and ensure your microphone is working.")
            st.session_state.processing = False
            st.session_state.processed_audio_hash = None
            return
        
        result = st.session_state.agent.process_voice_to_image(transcript)
        
        if result.get("error"):
            st.error(f"❌ Error during processing: {result.get('error')}")
            st.session_state.processing = False
            st.session_state.processed_audio_hash = None
            return
        
        st.session_state.current_result = result
        st.session_state.history.insert(0, result)
        
        st.success("✅ Image generated successfully!")
        st.rerun()
        
    except Exception as e:
        logger.error(f"Error processing audio: {e}", exc_info=True)
        st.error(f"❌ An error occurred: {str(e)}")
        st.session_state.processed_audio_hash = None
    finally:
        st.session_state.processing = False


def display_result(result):
    """Display processing result."""
    if not result:
        return
    
    st.subheader("📝 Transcription")
    transcript = result.get("transcript", "N/A")
    st.write(transcript if transcript else "N/A")
    
    st.subheader("✨ Enhanced Description")
    description = result.get("image_description", "N/A")
    st.write(description if description else "N/A")
    
    st.subheader("🎨 Generated Image")
    image_url = result.get("image_url")
    
    if image_url:
        try:
            st.image(image_url, use_container_width=True)
        except Exception as e:
            logger.error(f"Error displaying image: {e}", exc_info=True)
            st.error(f"❌ Error displaying image: {str(e)}")
            st.info(f"Image URL: {image_url}")
    else:
        if result.get("error"):
            st.error(f"❌ Image generation failed: {result.get('error')}")
        else:
            st.error("❌ Image generation failed - no image URL returned")
    
    st.subheader("🔧 Processing Details")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Text Model", result.get("text_model", "N/A"))
    with col2:
        st.metric("Image Model", result.get("image_model", "N/A"))


def main():
    """Main application."""
    st.title("🎨 Voice to Image")
    st.markdown("**Transform your voice into stunning AI-generated images**")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        image_size = st.selectbox(
            "Image Size",
            ["1024x1024", "1792x1024", "1024x1792"],
            index=0
        )
        
        image_quality = st.selectbox(
            "Image Quality",
            ["standard", "hd"],
            index=0
        )
        
        if st.button("🔄 Clear History", use_container_width=True):
            st.session_state.history = []
            st.session_state.current_result = None
            st.session_state.processed_audio_hash = None
            st.rerun()
        
        st.divider()
        st.header("📖 How It Works")
        st.markdown("""
        1. **Record** your voice describing an image
        2. **Transcribe** to text automatically
        3. **Enhance** description with AI
        4. **Generate** stunning image with DALL-E
        """)
    
    # Initialize agent
    if not initialize_agent():
        st.stop()
    
    # Update agent settings
    st.session_state.agent.image_size = image_size
    st.session_state.agent.image_quality = image_quality
    
    # Main content area
    st.header("🎤 Record Your Voice")
    st.markdown("Click the microphone button below and describe the image you want to create.")
    
    # Show helpful info about recording
    with st.expander("ℹ️ How to record"):
        st.markdown("""
        **Option 1: Record directly (recommended)**
        1. Click the microphone button below
        2. Allow microphone access if prompted by your browser
        3. Speak clearly into your microphone
        4. Click the stop button when finished
        5. The app will automatically process your recording
        
        **Option 2: Upload audio file (if recording fails)**
        - Use the file uploader below to upload a WAV or WebM audio file
        - Record audio using your phone or another app, then upload it here
        
        **Troubleshooting:**
        - Make sure microphone permissions are granted
        - Try using Chrome or Firefox browser
        - Check that your microphone is working in other applications
        - If recording doesn't work, use the file upload or text input option
        """)
    
    # Audio input
    try:
        audio_bytes = st.audio_input("Record your voice", key="voice_recorder")
        
        if audio_bytes is not None:
            # Handle UploadedFile object
            if hasattr(audio_bytes, 'read'):
                try:
                    audio_bytes = audio_bytes.read()
                except Exception as e:
                    logger.error(f"Error reading audio file: {e}", exc_info=True)
                    st.error(f"❌ Error reading audio file: {str(e)}")
                    audio_bytes = None
            
            if audio_bytes is not None and isinstance(audio_bytes, bytes):
                if not st.session_state.processing:
                    audio_hash = get_audio_hash(audio_bytes)
                    
                    if audio_hash != st.session_state.processed_audio_hash:
                        with st.spinner("Processing your voice recording..."):
                            process_audio(audio_bytes)
    except Exception as e:
        logger.error(f"Error with audio input: {e}", exc_info=True)
        st.error(f"❌ Error with audio input: {str(e)}")
        st.info("💡 Make sure your browser has microphone permissions enabled.")
    
    # File upload option
    st.divider()
    st.subheader("📁 Alternative: Upload Audio File")
    st.markdown("If the microphone recording doesn't work, you can upload an audio file instead.")
    st.info("💡 **Note:** Keep audio files under 10MB for best results.")
    
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    uploaded_file = st.file_uploader(
        "Choose an audio file (WAV, WebM, MP3, etc.)",
        type=['wav', 'webm', 'mp3', 'ogg', 'm4a'],
        key="audio_file_uploader"
    )
    
    if uploaded_file is not None:
        try:
            file_size = uploaded_file.size
            
            if file_size > MAX_FILE_SIZE:
                st.error(f"❌ File too large! Maximum size is {MAX_FILE_SIZE / (1024*1024):.1f}MB. Your file is {file_size / (1024*1024):.1f}MB.")
                st.info("💡 Please compress your audio file or record a shorter clip.")
            elif file_size == 0:
                st.error("❌ File is empty. Please upload a valid audio file.")
            elif not st.session_state.processing:
                try:
                    file_bytes = uploaded_file.read()
                    
                    if len(file_bytes) == 0:
                        st.error("❌ Failed to read file. The file might be corrupted or empty.")
                    else:
                        file_hash = get_audio_hash(file_bytes)
                        
                        if file_hash != st.session_state.processed_audio_hash:
                            with st.spinner("Processing uploaded audio file..."):
                                process_audio(file_bytes)
                        else:
                            st.info("ℹ️ This file has already been processed. Upload a different file or record new audio.")
                except Exception as e:
                    logger.error(f"Error reading file: {e}", exc_info=True)
                    st.error(f"❌ Error reading file: {str(e)}")
            else:
                st.warning("⏳ Processing in progress. Please wait for the current task to complete.")
        except Exception as e:
            logger.error(f"Error handling uploaded file: {e}", exc_info=True)
            st.error(f"❌ Error with uploaded file: {str(e)}")
    
    # Text input option
    st.divider()
    st.subheader("✍️ Alternative: Text Input")
    st.markdown("If audio recording and file upload don't work, you can type your image description directly.")
    
    text_input = st.text_area(
        "Describe the image you want to generate:",
        placeholder="e.g., A beautiful sunset over the ocean with pink and orange clouds, serene and peaceful atmosphere",
        key="text_description_input",
        height=100
    )
    
    if st.button("🎨 Generate Image from Text", key="generate_from_text", use_container_width=True):
        if text_input and text_input.strip():
            if not st.session_state.processing:
                with st.spinner("Processing your description and generating image..."):
                    try:
                        result = st.session_state.agent.process_voice_to_image(text_input.strip())
                        
                        if result.get("error"):
                            st.error(f"❌ Error during processing: {result.get('error')}")
                        else:
                            st.session_state.current_result = result
                            st.session_state.history.insert(0, result)
                            st.success("✅ Image generated successfully!")
                            st.rerun()
                    except Exception as e:
                        logger.error(f"Error processing text input: {e}", exc_info=True)
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⏳ Processing in progress. Please wait.")
        else:
            st.warning("⚠️ Please enter a description first.")
    
    # Show status
    if not st.session_state.processing:
        if audio_bytes is None and uploaded_file is None:
            st.info("🎤 Ready to record. Click the microphone button above to start recording, upload an audio file, or type your description below.")
    
    # Show processing status
    if st.session_state.processing:
        st.info("🔄 Processing your audio... Please wait.")
        st.progress(0.5)
    
    # Display current result
    if st.session_state.current_result:
        st.divider()
        display_result(st.session_state.current_result)
    
    # Display history
    if st.session_state.history:
        st.divider()
        st.header("📚 History")
        for idx, result in enumerate(st.session_state.history[1:], 1):
            with st.expander(f"Result #{idx} - {result.get('transcript', 'N/A')[:50]}..."):
                display_result(result)


if __name__ == "__main__":
    main()
