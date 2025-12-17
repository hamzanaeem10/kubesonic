import os
import time
import redis
import shutil
from fastapi import FastAPI, UploadFile, File
import threading
import sys

# --- CONFIGURATION ---
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
QUEUE_NAME = "audio_jobs"
SHARED_FOLDER = "/data"  # Where files are stored

# Connect to Redis
r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
app = FastAPI()

# --- PART A: THE API (Frontend) ---
@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    # 1. Save the file to shared storage
    file_location = f"{SHARED_FOLDER}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    # 2. Push job to Redis Queue
    r.lpush(QUEUE_NAME, file.filename)
    
    return {"info": f"File '{file.filename}' queued for processing", "queue_length": r.llen(QUEUE_NAME)}

@app.get("/health")
def health():
    return {"status": "ok"}

# --- PART B: THE WORKER (Backend Processor) ---
def process_audio(filename):
    print(f"🎵 Starting AI processing on: {filename}")
    
    # --- SIMULATION MODE (Use this to test KEDA scaling first) ---
    time.sleep(5) # Simulate 5 seconds of heavy GPU work
    
    # --- REAL AI MODE (Uncomment when ready) ---
    # from sam_audio import SAMAudio
    # model = SAMAudio.from_pretrained("facebook/sam-audio-base")
    # ... run inference ...
    
    print(f"✅ Finished processing: {filename}")

def start_worker():
    print("🚀 Worker started. Waiting for jobs...")
    while True:
        # Blocking pop: waits until item appears in queue
        # msg is a tuple: (queue_name, data)
        msg = r.brpop(QUEUE_NAME)
        filename = msg[1].decode("utf-8")
        
        try:
            process_audio(filename)
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

if __name__ == "__main__":
    # If run with argument "worker", start the worker loop
    if len(sys.argv) > 1 and sys.argv[1] == "worker":
        start_worker()
    else:
        # Otherwise run the API server
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
