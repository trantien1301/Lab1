
# # --- Hướng dẫn chạy ---
# # 1. Lưu file này với tên là main.py.
# # 2. Mở terminal trong cùng thư mục.
# # 3. Chạy lệnh: uvicorn main:app --reload

# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from text_generation import TextGenerationService
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Text Generation API",
    description="API sử dụng model Qwen/Qwen3-0.6B để sinh văn bản."
)

tg_service = TextGenerationService()


class GenerationInput(BaseModel):
    prompt: str = Field(..., description="Nội dung yêu cầu sinh văn bản.")
    max_new_tokens: int = Field(default=128, ge=1, le=512)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "prompt": "Giải thích AI là gì trong 2 câu ngắn.",
                "max_new_tokens": 100,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
    }


@app.get("/", tags=["General"])
def read_root():
    return {"message": "Chào mừng đến Text Generation API. Dùng POST /generate."}


@app.get("/health", tags=["General"])
def health_check():
    if tg_service.health_check():
        return {"status": "ok", "message": "Model is ready."}
    raise HTTPException(status_code=503, detail="Model is not available.")


@app.post("/generate", tags=["Text Generation"])
def generate_text(data: GenerationInput):
    if not data.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    result = tg_service.generate(
        prompt=data.prompt,
        max_new_tokens=data.max_new_tokens,
        temperature=data.temperature,
        top_p=data.top_p
    )

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result