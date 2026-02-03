# 🖼️ Image Generation FastAPI Project

This project provides a FastAPI service to generate images from text prompts using Stable Diffusion.  
Generated images are saved into a `generated_images/` folder, and their file paths are stored in a SQLite database.

---

## 📂 Project Structure
project-root/ │
 ├── app/ │  
  ├── init.py │ 
  ├── main.py              # FastAPI entry point │  
  ├── database.py          # SQLite connection + table creation │ 
  ├── models.py            # Pydantic schemas │ 
  ├── image_generator.py   # Stable Diffusion pipeline │  
  └── routers/ │     
    ├── init.py │     
    ├── generate.py      # Image generation endpoint │      
    └── images.py        # Image retrieval endpoint │ 
├── generated_images/        # Folder for saved images
├── images.db                # SQLite database file
├── requirements.txt         # Dependencies
└── .env                     # Hugging Face token


---

## ⚙️ Setup Instructions

### 1. Clone and enter project
```bash
git clone <your-repo-url>
cd project-root

2. 2. Create virtual environment

python -m venv venv
# Activate
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Add Hugging Face token
Create a .env file in project root:
HF_TOKEN=hf_your_actual_token_here


Make sure you’ve accepted the license for runwayml/stable-diffusion-v1-5.
5. Initialize database
Tables (images) are auto‑created on server startup.

6. Run server
uvicorn app.main:app --reload

-------------------------

🚀 API Endpoints
Image Generator
- POST /generate/
- Request:
{ "prompt": "sunset over mountains" }
- Response:
{
  "message": "Image generated and stored successfully",
  "filepath": "generated_images/20260203_095300.png"
}


---------------------------------

mage Retrieval
- GET /images/{id}
- Response:
{
  "prompt": "sunset over mountains",
  "filepath": "generated_images/20260203_095300.png"
}




✅ Notes
- Images are saved in generated_images/ as .png files.
- SQLite (images.db) stores the prompt and file path.
- Swagger UI available at: http://127.0.0.1:8000/docs (127.0.0.1 in Bing)

📌 Requirements
- Python 3.9+
- Hugging Face account + access token
- Dependencies: fastapi, uvicorn, pydantic, torch, transformers, diffusers, python-dotenv

---

This README is **ready to paste** into your project root.  
Do you want me to also add a **section with troubleshooting tips** (like handling `MemoryError` or CUDA issues) so your teammates don’t run into the same problems you did?


---

This README is **ready to paste** into your project root.  
Do you want me to also add a **section with troubleshooting tips** (like handling `MemoryError` or CUDA issues) so your teammates don’t run into the same problems you did?

