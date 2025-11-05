from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the SUPABASE_URL and SUPABASE_KEY from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize the Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

