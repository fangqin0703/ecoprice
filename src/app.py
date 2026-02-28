from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>EcoPrice Pulse MVP</title></head>
<body>
    <h1>EcoPrice: Sustainability Tracker</h1>
    <p>Search for a refurbished device to see its impact score.</p>
    <form action="/echo_user_input" method="POST">
        <input name="user_input" placeholder="e.g. iPhone 17">
        <input type="submit" value="Check Sustainability">
    </form>
    {% if output %}
        <hr>
        <h3>Search Result:</h3>
        <p>You searched for: <strong>{{ output }}</strong></p>
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
    return render_template_string(HTML_TEMPLATE, output=user_text)

if __name__ == "__main__":
    app.run(debug=True)