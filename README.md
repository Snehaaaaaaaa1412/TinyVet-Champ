# 🐾 TinyVet: Multimodal AI Pet Assistant for Champ

**TinyVet** is a localized, privacy-first AI health assistant designed to provide instant care guidance for pets. By combining **Computer Vision** and **Retrieval-Augmented Generation (RAG)**, TinyVet can "see" symptoms in photos and "read" professional veterinary documents to provide expert-level advice.

---

## 📖 The Story (How it Works)
TinyVet operates on a dual-intelligence system:

1.  **The Eyes (Vision):** When you upload a photo of Champ, the **Moondream (1.8b)** vision model analyzes pixels to identify visible issues like skin redness, eye cloudiness, or ear infections.
2.  **The Brain (RAG):** When you ask a question, the system doesn't just "guess." It searches through a curated library of **Veterinary PDF manuals**. It finds the most relevant paragraphs using **FAISS (Vector Database)** and feeds that context to **Llama3**.
3.  **The Output:** Llama3 combines the visual analysis and the medical text to give a precise, safe, and context-aware answer.




---

## 🛠️ Installation & Setup (Full Guide)

Follow these steps to set up TinyVet on your local machine:

### 1. Prerequisites
- **Python 3.10+** installed.
- **Ollama** installed (Download from [ollama.com](https://ollama.com)).
- **Models:** Open your terminal and pull the required models:
  ```bash
  ollama pull llama3
  ollama pull moondream:1.8b
2. Environment Setup
Clone this repository and navigate to the project folder:

Bash

# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
3. Install Dependencies
Install all required Python libraries:

Bash

pip install flask ollama langchain langchain-community faiss-cpu sentence-transformers pypdf
4. Knowledge Base Setup
Create a folder named data/ in the root directory.

Drop your pet care PDFs (medical manuals, breed guides) into this folder.

TinyVet will automatically index these files when the RAG script runs.

🚀 Running the Application
Every time you want to use TinyVet:

Ensure Ollama is running in the background.

Activate your virtual environment: venv\Scripts\activate

Run the Flask server:

Bash

python app.py
Open your browser and go to: http://localhost:5000

✨ Features Highlight
Privacy-First: All processing happens on your CPU/GPU. Champ's data never leaves your room.

Dog-Friendly UI: High-contrast Yellow/Blue theme designed for the canine vision spectrum.

Puffy Click: A custom-built, playful dark mode toggle for night-time checks.

Personalized: Specifically tuned to recognize and care for Champ.

⚖️ Disclaimer
TinyVet is an educational AI tool. It provides suggestions based on medical documents but is not a replacement for a professional licensed veterinarian.

Built with ❤️ for Champ.
