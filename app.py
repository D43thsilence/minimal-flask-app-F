from flask import Flask, send_file, render_template, request
import openai
import base64
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

# Always use an absolute path for the generated image
IMAGE_PATH = Path(__file__).resolve().parent / "output.png"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    resultDescription = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            # Creates the information for the tombstone label
            response = openai.responses.create(
                model="gpt-5.6-luna",  
                input=[{"role": "developer", "content": "You are an AI that manages a museum. Use sophisticated language and artistic terms to create an exhibition tombstone label with appropriate formatting that only states the artist's name, the title and year of the piece, the medium it was created in, its dimensions, the provenance and the credits for the item the user presents to you. "
                "If the artist's name, the title and year of the piece, the medium it was created in, object dimensions, the provenance and the credits are not specified by the user, you can make them up."}, 
                          {"role": "user", "content": prompt}],
                          max_output_tokens=200,
            )

            # Creates the object description
            responseDescription = openai.responses.create(
                            model="gpt-5.6-luna",  
                            input=[{"role": "developer", "content": "You are an AI that manages a museum. Use sophisticated language and artistic terms to describe the item the user presents to you as a piece that is exposed in a contemporary museum."}, 
                                      {"role": "user", "content": prompt}],
                                      max_output_tokens=500,
                        )

            # Generates the image
            imageResponse = openai.responses.create(
            model="gpt-5.6-luna",
            input=[{"role": "developer", "content": "You are an AI that manages a museum. Create an image that displays the object the prompt describes in a museum exhibit space."}, 
                                      {"role": "user", "content": prompt}],
            tools=[{"type": "image_generation", "model": "gpt-image-2.5-sunburst"}],
            )

            # Assigns the text responses to variable that will be sent to the webpage
            result = response.output_text
            resultDescription = responseDescription.output_text

            # Save the image to a file
            image_data = [
                output.result
                for output in imageResponse.output
                if output.type == "image_generation_call"
            ]
            
            if image_data:
                image_base64 = image_data[0]
                with open("output.png", "wb") as f:
                    f.write(base64.b64decode(image_base64))

        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("index.html", result=result, resultDescription=resultDescription)

@app.route("/image")
def get_image():
    # Prevent browser caching of the image
    response = send_file(
        IMAGE_PATH,
        mimetype="image/png",
        max_age=0
    )
    response.headers["Cache-Control"] = "no-store"
    return response

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing