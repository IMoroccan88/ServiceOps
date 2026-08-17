# "Import Flask to create the web app,
# render_template to load HTML pages,
# and request so Python can read information sent by the browser."
from flask import  (Flask, 
render_template, 
request,
)
import psycopg

app = Flask(__name__)

# Create and return a connection to the ServiceOps database.
def get_db_connection():
    connection = psycopg.connect(
        host="localhost",
        dbname="serviceops",
        user="postgres",
        password="1A2l3a4e$",
        port=5433
    )

    # Give the database connection back to whatever route called this function.
    return connection


# "When somebody requests /, execute home(),
# and send whatever home() returns back to them."
@app.route("/")
def home():
    return render_template("index.html")


# Allow this route to receive both GET and POST requests.
@app.route("/service-request", methods=["GET", "POST"])
def service_request():

    # Check if the browser sent a GET request.
    if request.method == "GET":

        # Get the value of "sr_number" from the URL.
        # If no SR number was provided, this will return None.
        sr_number = request.args.get("sr_number")

        # If an SR number was entered, show what the customer searched for.
        if sr_number:
            # Open a connection to the ServiceOps database.
            connection = get_db_connection()

            # Use the connection to create a cursor for running SQL.
            cursor = connection.cursor()

            # After Cursor calls the DB, enter the syntax that should take place.
            cursor.execute(
                """
                SELECT service_requests.sr_number,
                service_requests.issue,
                customers.name,
                companies.company_name
                FROM service_requests

                JOIN customers
                ON service_requests.customer_id = customers.customer_id

                JOIN companies
                ON customers.company_id = companies.company_id

                WHERE service_requests.sr_number = %s
                """
            ,
            (sr_number,)
            )

            # and store it in the Python variable service_request.
            service_request = cursor.fetchone()

            # Close the cursor when we're finished using it.
            cursor.close()

            # Close the database connection when we're finished.
            connection.close()


            # "If PostgreSQL returned a Service Request
            if service_request:

                    return f"""
                        SR Number: {service_request[0]}<br>
                        Issue: {service_request[1]}<br>
                        Customer: {service_request[2]}<br>
                        Company: {service_request[3]}
                        """

            else:

                    return "Requested Service Request does not exist."
            
            # Send a response back to the browser.
            #return f"You searched for Service Request: {sr_number}" 

        # If no SR number was entered, simply display the Service Request page.
        else:
            return render_template("service_request.html")
    
    # If it wasn't GET, it must be POST.
    # POST will eventually create a new Service Request.
    else:
    # Get the customer's name from the submitted form.
        customer_name = request.form.get("customer_name")

    # Get the customer's email from the submitted form.
        email = request.form.get("email")

    # Get the selected priority from the submitted form.
        priority = request.form.get("priority")

    # Get the issue description from the submitted form.
        issue = request.form.get("issue")

    # Temporarily display the submitted information
    # so we can prove Flask received everything correctly.
        return f"""
        Customer: {customer_name}<br>
        Email: {email}<br>
        Priority: {priority}<br>
        Issue: {issue}
        """

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