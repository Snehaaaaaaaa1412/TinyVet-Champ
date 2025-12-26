from flask import Flask, render_template, request, jsonify
from rag import build_rag_chain, analyze_image
import os
import time

app = Flask(__name__)

# --- INITIALIZATION ---
print("--- [DEBUG] STEP 1: Script started ---")

# Database aur chain ko load hone dein
try:
    print("--- [DEBUG] STEP 2: Building RAG Chain (Loading PDFs)... ---")
    rag_chain = build_rag_chain()
    print("--- [DEBUG] STEP 3: RAG Chain is ready! ---")
except Exception as e:
    print(f"--- [DEBUG] CRITICAL ERROR: {e} ---")
    rag_chain = None 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Frontend se data lena
    user_input = request.form.get("message", "")
    image_file = request.files.get("image")
    
    if not rag_chain:
        return jsonify({"answer": "Error: AI Models are still booting up. Please wait."}), 503

    final_query = user_input

    # --- IMAGE HANDLING LOGIC ---
    if image_file and image_file.filename != '':
        try:
            print(f"[DEBUG] Image detected: {image_file.filename}")
            
            # Temporary file path setup
            temp_path = os.path.join(os.getcwd(), "temp_upload.jpg")
            image_file.save(temp_path)
            
            # Analysis start (Isme time lag sakta hai)
            print("[DEBUG] Analysis started by Moondream. Terminal par nazar rakhein...")
            img_description = analyze_image(temp_path, user_input)
            print(f"[DEBUG] Analysis Complete: {img_description}")
            
            # Constructing final query for Llama3
            final_query = f"User has provided an image. Analysis: {img_description}. Question: {user_input}"
            
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
        except Exception as img_err:
            print(f"[DEBUG] Vision Model Timeout/Error: {img_err}")
            final_query = user_input 

    # --- RAG INVOCATION WITH ERROR CATCHING ---
    try:
        print(f"[DEBUG] Sending to Llama3: {final_query}")
        result = rag_chain.invoke({"question": final_query})
        
        if result and "answer" in result:
            return jsonify({"answer": result["answer"]})
        else:
            return jsonify({"answer": "I understood the image but couldn't find relevant info in documents."})

    except Exception as e:
        print(f"--- [DEBUG] BACKEND TIMEOUT/ERROR: {e} ---")
        return jsonify({"answer": "The model is taking too long to respond. Please try a simpler question or check your GPU/RAM."}), 500

if __name__ == "__main__":
    print("--- [DEBUG] STEP 4: Starting Flask Server ---")
    # threaded=True allow karta hai backend ko heavy tasks handle karne ke liye bina block huye
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False, threaded=True)