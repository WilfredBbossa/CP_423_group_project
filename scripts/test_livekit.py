import os
import asyncio
from dotenv import load_dotenv
from livekit import api

load_dotenv()

async def test_livekit():
    print("=" * 50)
    print("TESTING LIVEKIT CONNECTION")
    print("=" * 50)
    
    # Get credentials from .env
    url = os.getenv('LIVEKIT_URL')
    api_key = os.getenv('LIVEKIT_API_KEY')
    api_secret = os.getenv('LIVEKIT_API_SECRET')
    
    # Check if they exist
    if not url or url == 'wss://your-project.livekit.cloud':
        print("❌ LIVEKIT_URL not set or still using placeholder")
        return
    
    if not api_key or api_key == 'your_livekit_api_key_here':
        print("❌ LIVEKIT_API_KEY not set or still using placeholder")
        return
    
    if not api_secret or api_key == 'your_livekit_api_secret_here':
        print("❌ LIVEKIT_API_SECRET not set or still using placeholder")
        return
    
    print(f"✅ LiveKit URL: {url}")
    print(f"✅ API Key: {api_key[:5]}...{api_key[-5:]}")
    print(f"✅ API Secret: {api_secret[:5]}...{api_secret[-5:]}")
    
    try:
        # Try to create a LiveKit API client
        livekit_api = api.LiveKitAPI(
            url=url,
            api_key=api_key,
            api_secret=api_secret
        )
        
        # List rooms (basic connectivity test)
        rooms = await livekit_api.room.list_rooms(api.ListRoomsRequest())
        print(f"\n✅ Successfully connected to LiveKit!")
        print(f"   Found {len(rooms.rooms)} existing rooms")
        
        await livekit_api.aclose()
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_livekit())