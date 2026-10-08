from flask import Flask, render_template, request
import openai
import base64
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key
client = OpenAI()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            response = client.responses.create(
                model="gpt-5.6-luna",  
                input=[{"role": "developer", "content": "You are an AI that manages a museum. Use sophisticated language and artistic terms to describe the item the user presents to you as a piece that is exposed in a contemporary museum."}, 
                          {"role": "user", "content": prompt}],
                          max_output_tokens=100
                tools=[{"type": "image_generation", "model": "gpt-image-2.5-sunburst"}],
            )

    # Save the image to a file
    image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
    ]
    if image_data:
    image_base64 = image_data[0]
    with open("otter.png", "wb") as f:
        f.write(base64.b64decode(image_base64))

            result = response.output_text
            imageResult = image_data

        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing