# "Import Flask to create the web app,
# render_template to load HTML pages,
# and request so Python can read information sent by the browser."
from flask import  Flask, render_template
from service_request import service_request_bp


# Create the Flask web app.
app = Flask(__name__)


# Register the Service Request routes from service_request.py.
app.register_blueprint(service_request_bp)


# Different temporary routes to test the web app. These will be replaced with the final routes later.
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/incidents")
def incidents():
    return render_template("incidents.html")


@app.route("/health")
def health():
    return render_template("health.html")



# "If this file is being run directly, start the Flask web server."
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
