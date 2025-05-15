from flask import Flask, request, render_template_string

app = Flask(__name__)

html_form = """
<!DOCTYPE html>
<html>
<head><title>Booking Form</title></head>
<body>
    <h2>Medical Booking Form</h2>
    <form action="/submit" method="post">
        Name: <input type="text" name="name"><br><br>
        Location: <input type="text" name="location"><br><br>
        Symptoms: <input type="text" name="symptoms"><br><br>
        SSN: <input type="text" name="ssn"><br><br>
        <input type="submit" value="Submit" id="submit_button">
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(html_form)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form.to_dict()
    print("[SERVER] Received form data:", data)
    return f"<h3>Data submitted successfully!</h3><pre>{data}</pre>"

if __name__ == "__main__":
    app.run(port=8005, debug=True)
