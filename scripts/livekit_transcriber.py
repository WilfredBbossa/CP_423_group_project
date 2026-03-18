"""
LiveKit Real-time Transcriber with Groq Whisper
For Person A - Audio Processing Lead
"""

import os
import asyncio
import logging
from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    AgentSession,
    Agent
)
from livekit.plugins import groq
from livekit.plugins.silero import VAD  # Correct import for Silero VAD
import time

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("transcriber")


class TranscriptionAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a real-time transcriber. Just transcribe what you hear.",
            stt=groq.STT(),  # Uses Groq Whisper
        )

    async def on_user_turn_completed(self, chat_ctx, new_message):
        """Called when user speech is transcribed"""
        if new_message and hasattr(new_message, 'text_content') and new_message.text_content:
            # Get timestamp
            timestamp = time.strftime("%H:%M:%S")

            # Print the transcription with speaker info
            print(f"[{timestamp}] {new_message.text_content}")

            # Also save to a file
            with open("transcript_log.txt", "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {new_message.text_content}\n")


async def entrypoint(ctx: JobContext):
    """Main entry point for the agent"""
    print("\n" + "=" * 60)
    print("LIVEKIT REAL-TIME TRANSCRIBER")
    print("=" * 60)

    # Verify credentials
    required_vars = ["LIVEKIT_URL", "LIVEKIT_API_KEY",
                     "LIVEKIT_API_SECRET", "GROQ_API_KEY"]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        print(f"❌ Missing env vars: {', '.join(missing)}")
        return

    print(f"✅ Connecting to room: {ctx.room.name}")

    try:
        # Connect to the room (audio only)
        await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
        print("✅ Connected to LiveKit room")

        # Initialize VAD (Voice Activity Detection)
        vad = VAD.load()  # <-- This is the correct way to use Silero VAD

        # Create the agent session with Groq STT
        session = AgentSession(
            stt=groq.STT(),
            vad=vad,  # Pass the loaded VAD instance
        )

        # Create the transcriber agent
        agent = TranscriptionAgent()

        # Start the session
        await session.start(
            agent=agent,
            room=ctx.room,
        )

        print("\n🎤 Transcriber ready! Waiting for participants...")
        print("   Speaker labels will appear automatically")
        print("   Press Ctrl+C to stop\n")

        # Keep running
        while True:
            await asyncio.sleep(1)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n👋 Transcriber stopped")

if __name__ == "__main__":
    # Run the worker
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )
