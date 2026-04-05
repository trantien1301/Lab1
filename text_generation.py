#  # text_generation.py
 
# from transformers import pipeline
# import logging

# class TextGenerationService:
#     """
#     Service sinh câu trả lời bằng mô hình text-generation.
#     """
#     def __init__(self):
#         self.pipeline = None
#         self.model_id = "LiquidAI/LFM2.5-350M-Base"

#         logging.info(f"Loading model: {self.model_id} ...")
#         try:
#             self.pipeline = pipeline(
#                 "text-generation",
#                 model=self.model_id,
#                 tokenizer=self.model_id,
#                 trust_remote_code=True
#             )
#             logging.info("Model loaded successfully.")
#         except Exception as e:
#             logging.error(f"Could not load model: {e}")

#     def health_check(self) -> bool:
#         return self.pipeline is not None

#     def get_answer(self, question: str, context: str) -> dict:
#         if not self.health_check():
#             return {"error": "AI service is not available."}

#         prompt = f"""Bạn là trợ lý AI. Hãy trả lời CỰC NGẮN GỌN bằng tiếng Việt.
# Chỉ dựa vào ngữ cảnh được cung cấp.
# Nếu không có thông tin, trả lời: "Không tìm thấy trong ngữ cảnh."

# Ngữ cảnh:
# {context}

# Câu hỏi:
# {question}

# Trả lời:"""

#         try:
#             outputs = self.pipeline(
#                 prompt,
#                 max_new_tokens=80,
#                 do_sample=True,
#                 temperature=0.7,
#                 top_p=0.9,
#                 return_full_text=False
#             )

#             # Với return_full_text=False, thường lấy trực tiếp phần mới sinh
#             answer = outputs[0].get("generated_text", "").strip()

#             return {
#                 "answer": answer,
#                 "model": self.model_id
#             }
#         except Exception as e:
#             logging.error(f"Inference error: {e}")
#             return {"error": str(e)}

# text_generation.py
import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class TextGenerationService:
    """
    Service sinh văn bản bằng model Qwen/Qwen3-0.6B.
    """
    def __init__(self):
        self.pipe = None
        self.model_id = "Qwen/Qwen3-0.6B"

        logging.info(f"Loading model: {self.model_id} ...")
        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.float16 if self.device == "cuda" else torch.float32

            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_id,
                trust_remote_code=True
            )

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                torch_dtype=dtype,
                trust_remote_code=True
            )

            if self.device == "cuda":
                self.model = self.model.to("cuda")

            self.pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer
            )

            logging.info(f"Model loaded successfully on {self.device}.")
        except Exception as e:
            logging.exception(f"Could not load model: {e}")
            self.pipe = None

    def health_check(self) -> bool:
        return self.pipe is not None

    def generate(self, prompt: str, max_new_tokens: int, temperature: float, top_p: float) -> dict:
        if not self.health_check():
            return {"error": "AI service is not available."}

        final_prompt = f"Bạn là trợ lý AI, trả lời ngắn gọn bằng tiếng Việt.\nUser: {prompt}\nAssistant:"

        try:
            outputs = self.pipe(
                final_prompt,
                max_new_tokens=max_new_tokens,
                do_sample=(temperature > 0),
                temperature=temperature,
                top_p=top_p,
                return_full_text=False
            )

            generated_text = outputs[0].get("generated_text", "").strip()

            return {
                "model": self.model_id,
                "device": self.device,
                "prompt": prompt,
                "generated_text": generated_text
            }
        except Exception as e:
            logging.exception(f"Inference error: {e}")
            return {"error": str(e)}