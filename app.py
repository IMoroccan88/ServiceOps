from flask import Flask, render_template

app = Flask(__name__)

# "When somebody requests /, execute home(),
# and send whatever home() returns back to them."
@app.route("/")
def home():
    return render_template("index.html")


# "When somebody requests /service-request, execute service_request(),
# and send whatever service_request() returns back to them."
@app.route("/service-request")
def service_request():
    return render_template("service_request.html")


# "When somebody requests /incidents, execute incidents(),
# load incidents.html, and send that webpage back to them."
@app.route("/incidents")
def incidents():
    return render_template("incidents.html")


# "When somebody requests /health, execute health(),
# load health.html, and send that webpage back to them."
@app.route("/health")
def health():
    return render_template("health.html")

# "If this file is being run directly, start the Flask web server."
if __name__ == "__main__":
    app.run(debug=True)