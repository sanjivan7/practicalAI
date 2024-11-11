from flask import Flask, request, jsonify, render_template
from analyze import read_image
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, template_folder='templates')


@app.route("/")
def home():
    return render_template('index.html')


# API at /api/v1/analysis/
@app.route("/api/v1/analysis/", methods=['GET'])
def analysis():
    # Attempt to retrieve the URI from the JSON request
    try:
        get_json = request.get_json()
        image_uri = get_json.get('uri', None)

        if not image_uri:
            logging.error("URI not provided in JSON request")
            return jsonify({'error': 'Missing URI in JSON'}), 400

    except Exception as e:
        logging.error(f"Error parsing JSON request: {e}")
        return jsonify({'error': 'Invalid JSON format'}), 400

    # Attempt to analyze the image
    try:
        res = read_image(image_uri)

        if res == "error" or res == "max retries reached":
            logging.error("Error in image processing or max retries reached")
            return jsonify({'error': 'Error in processing'}), 500

        response_data = {
            "text": res
        }

        return jsonify(response_data), 200

    except Exception as e:
        logging.error(f"Error during image analysis: {e}")
        return jsonify({'error': 'Error in processing'}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)