"""
Generate LiveKit tokens for testing
"""

import os
import time
from dotenv import load_dotenv
from livekit import api

load_dotenv()


def generate_tokens(room_name=f"test-room-{int(time.time())}"):
    """Generate patient and clinician tokens"""

    url = os.getenv('LIVEKIT_URL')
    api_key = os.getenv('LIVEKIT_API_KEY')
    api_secret = os.getenv('LIVEKIT_API_SECRET')

    if not all([url, api_key, api_secret]):
        print("❌ Missing LiveKit credentials in .env")
        return

    # Patient token
    patient_token = api.AccessToken(api_key, api_secret) \
        .with_identity("patient") \
        .with_name("Patient") \
        .with_grants(api.VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=True,
            can_subscribe=True
        )).to_jwt()

    # Clinician token
    clinician_token = api.AccessToken(api_key, api_secret) \
        .with_identity("clinician") \
        .with_name("Clinician") \
        .with_grants(api.VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=True,
            can_subscribe=True
        )).to_jwt()

    print("\n" + "=" * 60)
    print(f"ROOM: {room_name}")
    print("=" * 60)
    print("\n🔑 PATIENT TOKEN:")
    print(patient_token)
    print("\n🔑 CLINICIAN TOKEN:")
    print(clinician_token)
    print("\n" + "=" * 60)
    print("Go to: https://meet.livekit.io/")
    print("=" * 60)


if __name__ == "__main__":
    generate_tokens()
