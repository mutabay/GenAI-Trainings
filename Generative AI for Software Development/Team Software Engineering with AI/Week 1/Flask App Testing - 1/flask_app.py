from flask import Flask, jsonify, abort, request
import re

app = Flask(__name__)

# 1st version
# @app.route('/api/greet/<name>', methods=['GET'])
# def greet(name):
#     return jsonify(message=f"Hello, {name}!")

# 2d version
# Function to check for HTML tags
def contains_html_tags(text):
    html_tag_pattern = re.compile(r'<[^>]+>')
    return bool(html_tag_pattern.search(text))

@app.route('/api/greet', methods=['GET'])
def greet():
    name = request.args.get('name')
    if not name:
        abort(400, description="Name parameter is required.")
    if contains_html_tags(name):
        abort(400, description="HTML content is not allowed in the name parameter.")
    return jsonify(message=f"Hello, {name}!")

@app.errorhandler(400)
def handle_bad_request(e):
    response = jsonify(error=str(e))
    response.status_code = 400
    return response

@app.errorhandler(404)
def handle_not_found(e):
    response = jsonify(error="Not Found")
    response.status_code = 404
    return response


if __name__ == '__main__':
    app.run(debug=True)