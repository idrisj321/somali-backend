from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase_client import supabase  # Ensure this file exists and is configured correctly

app = FastAPI()

# Enable CORS (important for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Test route ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Somali Pronunciation App"}

# --- Fetch audio for a specific word ---
@app.get("/get_audio/{word}")
def get_audio(word: str):
    try:
        print(f"🔍 Searching for audio of word: '{word}'")
        response = supabase.table("audio_files").select("audio_url").eq("word", word).execute()
        print("🧾 Supabase audio response:", response.data)

        if response.data:
            audio_url = response.data[0]["audio_url"]
            return {"word": word, "audio_url": audio_url}
        else:
            return {"error": "Audio not found for this word."}

    except Exception as e:
        return {"error": str(e)}

# --- Fetch word + audio + mnemonic + picture ---
@app.get("/get_word_data/{word}")
def get_word_data(word: str):
    try:
        print(f"🔍 Searching for word: '{word}'")

        # Fetch ALL rows for debugging
        all_data = supabase.table("word_data").select("word").execute()
        print("📋 All words in Supabase:", all_data.data)

        # Case-insensitive search
        response = supabase.table("word_data").select("word", "audio_url", "mnemonic", "image_url").ilike("word", word).execute()

        print("🧾 Supabase filtered response:", response.data)

        if response.data:
            word_info = response.data[0]
            return {
                "word": word_info["word"],
                "audio_url": word_info["audio_url"],
                "mnemonic": word_info["mnemonic"],
                "image_url": word_info["image_url"]
            }
        else:
            return {"error": "Word data not found."}

    except Exception as e:
        return {"error": str(e)}

# --- Test Supabase connection ---
@app.get("/test_supabase")
def test_supabase():
    try:
        data = supabase.table("word_data").select("word").limit(1).execute()
        print("✅ Test Supabase connection successful.")
        return {"status": "connected", "data": data.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}