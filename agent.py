import ollama
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play  # This is the correct import in recent versions

# ───────────────────────────────────────────────
#              ElevenLabs Configuration
# ───────────────────────────────────────────────
# !!! IMPORTANT !!!
# Never hardcode API keys in production code!
# Use environment variables instead:
# import os
# client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

client = ElevenLabs(api_key="")  # ← replace or use env var!

# Very natural sounding voice (Adam - very popular choice)
# You can also use: "21m00Tcm4TlvDq8ikWAM", "pNInz6obpg8ndclKuztD", etc.
VOICE_ID = "8WIK7Rlcat5dhMqR5A8i"           # Your current choice
MODEL_ID = "eleven_flash_v2_5"              # fast & good quality in 2025


def speak_human(text: str) -> None:
    """Convert text to speech and play it immediately"""
    try:
        audio_stream = client.text_to_speech.convert(
            text=text,
            voice_id=VOICE_ID,
            model_id=MODEL_ID,
            output_format="mp3_44100_128",      # you can also use pcm_44100 or pcm_22050
        )

        # play() can accept generator/iterator of bytes
        play(audio_stream)

    except Exception as e:
        print(f"TTS Error: {e}")


# ───────────────────────────────────────────────
#                   Main Chat Loop
# ───────────────────────────────────────────────

messages = [
    {"role": "system", "content": "You are a helpful, clever and slightly sarcastic assistant."}
]

print("═══ Professional AI Chat with Voice (Llama 3.2 + ElevenLabs) ═══")
print("   Type 'quit' or 'exit' to finish\n")

while True:
    try:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye! 👋")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        # Get response from local model
        print("Thinking...", end="\r")
        response = ollama.chat(
            model="llama3.2:latest",
            messages=messages,
            options={"temperature": 0.75}
        )

        answer = response["message"]["content"].strip()

        print(f"\rAgent: {answer}\n")
        messages.append({"role": "assistant", "content": answer})

        # Speak the answer
        speak_human(answer)

    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye! 👋")
        break

    except Exception as e:
        print(f"\nError: {e}\n")