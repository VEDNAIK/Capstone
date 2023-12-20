import json
from flask import Flask, request, jsonify
from Model import custom  # Import your backend code

app = Flask(__name__)

@app.route("/recommend", methods=["POST"])
def recommend():
    user_input = request.json.get("user_input")
    if not user_input:
        return jsonify({"error": "Invalid input"}), 400

    # Call your existing recommendation function with user input
    recommendations = custom(user_input)

    # Convert the DataFrame to a list of dictionaries
    recommendation_list = recommendations.to_dict(orient="records")

    return jsonify({"recommendations": recommendation_list})

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
