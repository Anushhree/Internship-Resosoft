import os
from typing import Optional
import threading
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Hugging Face token (optional here; model load will raise if missing)
HF_TOKEN: Optional[str] = os.getenv("HF_TOKEN")

# Model id
MODEL_ID = "runwayml/stable-diffusion-v1-5"

# Internal pipeline and lock for lazy initialization
_pipe = None
_pipe_lock = threading.Lock()


def _get_pipe():
    global _pipe
    if _pipe is None:
        with _pipe_lock:
            if _pipe is None:
                try:
                    from diffusers import StableDiffusionPipeline
                    import torch
                except Exception as e:
                    raise RuntimeError(f"Failed to import model libraries: {e}")

                if not HF_TOKEN:
                    raise RuntimeError(
                        "HF_TOKEN is not set. Create a Hugging Face access token and set HF_TOKEN in your environment or .env file."
                    )

                device = "cuda" if torch.cuda.is_available() else "cpu"
                dtype = torch.float16 if torch.cuda.is_available() else torch.float32

                _pipe = StableDiffusionPipeline.from_pretrained(
                    MODEL_ID,
                    use_auth_token=HF_TOKEN,
                    torch_dtype=dtype,
                )
                _pipe = _pipe.to(device)
    return _pipe


def generate_image(prompt: str):
    pipe = _get_pipe()
    image = pipe(prompt, num_inference_steps=25, guidance_scale=7.5).images[0]
    return image