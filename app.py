from flask import Flask, render_template, send_file, request
import base64
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    resultDescription = None
    image_base64 = None

    if request.method == "POST":
        prompt = request.form["prompt"]

        try:
            # Generate tombstone label
            response = openai.responses.create(
                model="gpt-5.6-luna",
                input=[
                    {
                        "role": "developer",
                        "content": (
                            "You are an AI that manages a museum. "
                            "Use sophisticated language and artistic terms to create "
                            "an exhibition tombstone label that only states the artist's name, "
                            "the title and year of the piece, the medium, dimensions, "
                            "provenance, and credits. "
                            "If information is missing, invent it."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                max_output_tokens=200,
            )

            # Generate description
            responseDescription = openai.responses.create(
                model="gpt-5.6-luna",
                input=[
                    {
                        "role": "developer",
                        "content": (
                            "You are an AI that manages a museum. "
                            "Describe the object as if it were displayed in a contemporary museum."
                            "No need to include the object's name, date or maker."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                max_output_tokens=500,
            )

            # Generate image
            imageResponse = openai.responses.create(
                model="gpt-5.6-luna",
                input=[
                    {
                        "role": "developer",
                        "content": (
                            "You are an AI that manages a museum. "
                            "Create an image that displays the object the prompt describes "
                            "in a museum exhibit space."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                tools=[
                    {
                        "type": "image_generation",
                        "model": "gpt-image-2.5-sunburst",
                        "size": "1024x1024",
                        "quality": "high",
                    }
                ],
            )

            result = response.output_text
            resultDescription = responseDescription.output_text

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

    return render_template(
        "index.html",
        result=result,
        resultDescription=resultDescription,
    )

@app.route("/image")
def image():
    return send_file("output.png", mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)