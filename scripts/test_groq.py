import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')
if api_key and api_key != 'your_groq_api_key_here':
    print(f"✅ Groq API key found: {api_key[:5]}...{api_key[-5:]}")
    
    # Test a simple API call
    try:
        client = Groq(api_key=api_key)
        print("✅ Groq client initialized")
        
        # Optional: Test with a simple completion
        # completion = client.chat.completions.create(
        #     model="mixtral-8x7b-32768",
        #     messages=[{"role": "user", "content": "Say hello"}],
        #     max_tokens=10
        # )
        # print("✅ API call successful")
        
    except Exception as e:
        print(f"❌ Groq client error: {e}")
else:
    print("❌ API key not set or still using placeholder")