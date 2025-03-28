from fastapi import FastAPI, Request
from pydantic import BaseModel
from model import TranslationModel
import uvicorn
import webbrowser
import threading
import time
import psutil  # For memory usage
import time as t

# Global metrics
request_count = 0

# Initialize model
model = TranslationModel()

# Initialize FastAPI   
app = FastAPI(
    title="Real-Time Translation API",
    description="An API that translates English text to Spanish and computes BLEU & Perplexity scores, with live performance monitoring.",
    version="1.2",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware to monitor performance
@app.middleware("http")
async def add_metrics(request: Request, call_next):
    global request_count
    request_count += 1 

    # Start time & memory
    process = psutil.Process()
    start_mem = process.memory_info().rss / (1024 ** 2)  # In MB
    start_time = t.time()

    # Process request
    response = await call_next(request)

    # End time & memory
    end_time = t.time()
    end_mem = process.memory_info().rss / (1024 ** 2)

    # Attach timing/memory to headers
    response.headers["X-Response-Time-ms"] = str(round((end_time - start_time) * 1000, 2))
    response.headers["X-Memory-Used-MB"] = str(round(end_mem - start_mem, 4))
    response.headers["X-Total-Requests"] = str(request_count)

    return response

# Request model
class TranslationRequest(BaseModel):
    text: str

# Main translation endpoint
@app.post("/translate", summary="Translate and evaluate", tags=["Translation"])
def translate(request: TranslationRequest):
    english_text = request.text
    translated = model.translate(english_text)

    # Get Hugging Face reference
    model.tokenizer.src_lang = "en"
    encoded = model.tokenizer(english_text, return_tensors="pt")
    generated = model.model.generate(**encoded, forced_bos_token_id=model.tokenizer.get_lang_id("es"))
    hf_reference = model.tokenizer.decode(generated[0], skip_special_tokens=True)

    # Compute scores
    bleu = model.compute_bleu(hf_reference, translated)
    perplexity = model.compute_perplexity(translated)

    return {
        "original_text": english_text,
        "translated_text": translated,
        "reference_translation": hf_reference,
        "bleu_score": round(bleu, 4),
        "perplexity": round(perplexity, 4)
    }

# Metrics endpoint
@app.get("/metrics", tags=["Monitoring"])
def get_metrics():
    process = psutil.Process()
    mem_usage = process.memory_info().rss / (1024 ** 2)
    return {
        "total_requests": request_count,
        "current_memory_usage_mb": round(mem_usage, 2)
    }

# Auto-open browser on startup
def start_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    threading.Thread(target=start_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
