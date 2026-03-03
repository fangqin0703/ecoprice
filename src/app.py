from flask import Flask, request, render_template_string
from prometheus_flask_exporter import PrometheusMetrics
import requests
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>EcoPrice Pulse MVP</title></head>
<body>
    <h1>EcoPrice: Sustainability Tracker</h1>
    <p>Search for a refurbished device to see its impact score.</p>
    <form action="/echo_user_input" method="POST">
        <input name="user_input" placeholder="e.g. iPhone">
        <input type="submit" value="Check Sustainability">
    </form>
    {% if output %}
        <hr>
        <h3>Search Result:</h3>
        <p>You searched for: <strong>{{ output }}</strong></p>
        {% if devices %}
            <ul>
            {% for device in devices %}
                <li>{{ device.title }} - ${{ device.price }} (Eco Score: {{ device.eco_score }})</li>
            {% endfor %}
            </ul>
        {% else %}
            <p>No matching devices found.</p>
        {% endif %}
    {% endif %}
</body>
</html>
'''

@app.route("/")
def main():
    return render_template_string(HTML_TEMPLATE)

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    user_text = request.form.get("user_input", "")
    
    devices = []
    if user_text:
        try:
            # Query the REST API
            api_url = os.environ.get('INTERNAL_API_URL', 'http://localhost:5001/api/devices')
            response = requests.get(api_url)
            if response.status_code == 200:
                all_devices = response.json()
                # Filter based on user input
                devices = [d for d in all_devices if user_text.lower() in d['title'].lower()]
        except requests.exceptions.RequestException as e:
            print(f"Error querying API: {e}")
            
    return render_template_string(HTML_TEMPLATE, output=user_text, devices=devices)

if __name__ == "__main__":
    app.run(port=5000, debug=True)