"""
AI Agent for Voice to Image conversion.
Converts transcripts to image descriptions and generates images using DALL-E.
"""
import os
import logging
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VoiceToImageAgent:
    """AI Agent for converting voice transcripts to images."""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.text_model = "gpt-4"
        self.image_model = "dall-e-3"
        self.image_size = "1024x1024"
        self.image_quality = "standard"
        
    def transcript_to_image_description(self, transcript: str) -> str:
        """Convert transcript to detailed image description."""
        prompt = f"""Convert the following voice transcript into a detailed, professional image description suitable for AI image generation.

Transcript: {transcript}

Requirements:
- Create a vivid, detailed description
- Include visual elements: colors, composition, mood, style
- Be specific about the scene, objects, and atmosphere
- Keep it concise but descriptive (2-3 sentences)
- Focus on visual details that will help generate a beautiful image

Image Description:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating detailed image descriptions for AI image generation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            description = response.choices[0].message.content.strip()
            logger.info(f"Generated image description from transcript")
            return description
            
        except Exception as e:
            logger.error(f"Error generating image description: {e}", exc_info=True)
            raise
    
    def generate_image(self, description: str) -> Optional[str]:
        """Generate image using DALL-E."""
        try:
            response = self.client.images.generate(
                model=self.image_model,
                prompt=description,
                size=self.image_size,
                quality=self.image_quality,
                n=1
            )
            
            image_url = response.data[0].url
            logger.info(f"Image generated successfully")
            return image_url
            
        except Exception as e:
            logger.error(f"Error generating image: {e}", exc_info=True)
            raise
    
    def process_voice_to_image(self, transcript: str) -> Dict[str, Any]:
        """Complete pipeline: transcript -> description -> image."""
        result = {
            "transcript": transcript,
            "text_model": self.text_model,
            "image_model": self.image_model,
            "image_size": self.image_size,
            "image_quality": self.image_quality
        }
        
        try:
            # Step 1: Convert transcript to image description
            image_description = self.transcript_to_image_description(transcript)
            result["image_description"] = image_description
            
            # Step 2: Generate image
            image_url = self.generate_image(image_description)
            result["image_url"] = image_url
            
            logger.info("Pipeline completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Pipeline error: {e}", exc_info=True)
            result["error"] = str(e)
            return result
