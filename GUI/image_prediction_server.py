from flask import Flask, request, jsonify
from img import custom_image
import os

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    if not image:
        return jsonify({"error": "Invalid image"}), 400

    try:
        # Save the uploaded image temporarily
        temp_image_path = "temp_image.jpg"
        image.save(temp_image_path)
        
        # Call your image prediction function with the image path
        predicted_name = custom_image(temp_image_path)

        # Remove the temporary image file
        os.remove(temp_image_path)

        return jsonify({"predicted_name": predicted_name})
    except Exception as e:
        # Print the exception to identify the issue
        print(f"Image prediction error: {str(e)}")
        return jsonify({"error": "Error predicting the image. Please try again."}), 500
    
if __name__ == "__main__":
    app.run(host="localhost", port=5001)
