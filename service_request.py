from flask import Blueprint, request, render_template
from db import get_db_connection

service_request_bp = Blueprint("service_request", __name__)

# Allow this route to receive both GET and POST requests.
@service_request_bp.route("/service-request", methods=["GET", "POST"])
def service_request():

    # Check if the browser sent a GET request.
    if request.method == "GET":

        # Get the value of "sr_number" from the URL.
        # If no SR number was provided, this will return None.
        sr_number = request.args.get("sr_number")

        # If no SR number was entered, display the Service Request page.
        if not sr_number:
            return render_template("service_request.html")

    # Open one database connection for this request.
        connection = get_db_connection()
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
            
            
    # If it wasn't GET, it must be POST.
    # POST will eventually create a new Service Request.
    else:
    # Get the customer's name from the submitted form.
        customer_name = request.form.get("customer_name")

    # Get the company name from the submitted form.
        company_name = request.form.get("company_name")

    # Get the customer's email from the submitted form.
        email = request.form.get("email")

    # Get the selected priority from the submitted form.
        priority = request.form.get("priority")

    # Get the issue description from the submitted form.
        issue = request.form.get("issue")

    # "Open one connection to PostgreSQL and create a cursor
    # we can use for the entire Service Request creation process."
        connection = get_db_connection()
        cursor = connection.cursor()

    # "Search for the company the user entered."
        cursor.execute(
        """
        SELECT *
        FROM companies
        WHERE company_name = %s
        """,
        (company_name,)
        )

        # "Store the matching company row, if PostgreSQL found one."
        company = cursor.fetchone()

    # "If the company exists, get its company_id."
    if company:
        company_id = company[0]

        # "Now look for this customer's email under this specific company."
        cursor.execute(
        """
        SELECT *
        FROM customers
        WHERE email = %s
        AND company_id = %s
        """,
        (email, company_id)
        )
        # Store the customer returned by PostgreSQL.
        customer = cursor.fetchone()

    # If the customer exists, get their customer ID.
        if customer:
            customer_id = customer[0]


        else: 
            #create a new customer, associate them with the existing company, and create a new Service Request for them.
            cursor.execute(
            """
            INSERT INTO customers (name, email, company_id)
            VALUES (%s, %s, %s)
            RETURNING customer_id
            """,
            (customer_name, email, company_id)
            )
            customer_id = cursor.fetchone()[0]


    else:
        # If the company doesn't exist, create a new company, then create a new customer and Service Request associated with that company.
        cursor.execute(
        """
        INSERT INTO companies (company_name)
        VALUES (%s)
        RETURNING company_id
        """,
        (company_name,)
        )   
        company_id = cursor.fetchone()[0]

        # Create a new customer associated with the newly created company.
        cursor.execute(
        """
        INSERT INTO customers (name, email, company_id)
        VALUES (%s, %s, %s)
        RETURNING customer_id
        """,
        (customer_name, email, company_id)
        )   
        customer_id = cursor.fetchone()[0]

        # These still need to exist before the INSERT.
        status = "Open"

            # Generate the next SR number.
        cursor.execute(
            """
            SELECT sr_number
            FROM service_requests
            ORDER BY sr_number DESC
            LIMIT 1
            """
            )

        last_sr = cursor.fetchone()

        if last_sr:
                last_number = int(last_sr[0].replace("SR-", ""))
                next_number = last_number + 1
                sr_number = f"SR-{next_number:04d}"
        else:
            sr_number = "SR-0001"


            # Create a new Service Request associated with the customer.
            cursor.execute(
            """
            INSERT INTO service_requests
            (sr_number, customer_id, issue, priority, status)
            VALUES(%s, %s, %s, %s, %s)
            """,
            (sr_number, customer_id, issue, priority, status)
            )

            # Save the new Service Request to the database.
            connection.commit()

            # Close the database resources after the transaction is complete.
            cursor.close()
            connection.close()

            # Display confirmation and the newly created Service Request details.
            return f"""
                Service Request Created Successfully<br><br>
                SR Number: {sr_number}<br>
                Customer: {customer_name}<br>
                Company: {company_name}<br>
                Priority: {priority}<br>
                Status: {status}<br>
                Issue: {issue}
                """
