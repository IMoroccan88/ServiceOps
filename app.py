from flask import Flask

app = Flask(__name__)

# "When somebody requests /, execute home(),
# and send whatever home() returns back to them."
@app.route("/")
def home():
    return "ServiceOps is running"


# "When somebody requests /service-request, execute service_request(),
# and send whatever service_request() returns back to them."
@app.route("/service-request")
def service_request():
    return "Service request page is working!"


# "If this file is being run directly, start the Flask web server."
if __name__ == "__main__":
    app.run(debug=True)