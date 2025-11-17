# Quick Start Guide - Voice to Image App

## Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd voice_to_image
pip install -r requirements.txt
```

**Note**: If you encounter issues with audio libraries:
- The app uses Google Speech Recognition which works via API (no local installation needed)
- For local microphone access, you may need system audio libraries, but Streamlit's audio input should work in most browsers

### Step 2: Configure Environment
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## First Use

1. **Record Your Voice**: Click the microphone button and describe your image
   - Example: "A beautiful sunset over the ocean with pink and orange clouds"
   
2. **Wait for Processing**: The app will:
   - Transcribe your voice
   - Enhance the description
   - Generate the image

3. **View Results**: See your image and all intermediate steps

## Tips

- **Speak clearly** for better transcription
- **Be descriptive** - the more details, the better the image
- **Check the enhanced description** - see how AI improved your prompt
- **View history** - scroll down to see previous generations

## Troubleshooting

**Audio not recording?**
- Check browser microphone permissions
- Try a different browser (Chrome/Firefox recommended)
- Ensure microphone is connected

**Transcription fails?**
- Speak more clearly
- Reduce background noise
- Check internet connection

**Image generation fails?**
- Verify OPENAI_API_KEY is set correctly
- Check you have API credits
- Ensure your key has DALL-E 3 access

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions
- Experiment with different image sizes and qualities in the sidebar


