import os
from dotenv import load_dotenv
from pyannote.audio import Pipeline
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

# Get Hugging Face token
hf_token = os.getenv('HF_TOKEN')

if hf_token and hf_token != 'your_huggingface_token_here':
    print(f"✅ Hugging Face token found: {hf_token[:5]}...{hf_token[-5:]}")

    try:
        # Use the correct parameter: 'token' instead of 'use_auth_token'
        pipeline = Pipeline.from_pretrained(
            'pyannote/speaker-diarization-3.1',
            token=hf_token  # <-- THIS IS THE FIX
        )
        print("✅ Pyannote pipeline loaded successfully!")
        print("\nYour environment is fully ready for the project!")
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("❌ Please add your Hugging Face token to .env")
    print("Get one at: https://huggingface.co/settings/tokens")
