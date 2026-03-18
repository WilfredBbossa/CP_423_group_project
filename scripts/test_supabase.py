import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

if not url or url == 'https://your-project.supabase.co':
    print("❌ Please update SUPABASE_URL in your .env file")
elif not key or key == 'your_supabase_key_here':
    print("❌ Please update SUPABASE_KEY in your .env file")
else:
    print(f"✅ Supabase URL: {url}")
    print(f"✅ Supabase Key: {key[:10]}...{key[-5:]}")
    
    try:
        # Initialize Supabase client
        supabase: Client = create_client(url, key)
        print("✅ Supabase client initialized successfully!")
        
        # Try a simple query (this will work even if no tables exist yet)
        result = supabase.table('_dummy').select('*').execute()
        print("✅ Connection test passed!")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")