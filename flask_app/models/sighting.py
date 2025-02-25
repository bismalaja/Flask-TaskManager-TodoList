from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Sighting:
    db_name = 'flaskappdatabase'

    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.date_of_sighting = data['date_of_sighting']
        self.what_happened = data['what_happened']
        self.num_sasquatches = data['num_sasquatches']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_sighting(data):
        is_valid = True
        if len(data['location']) < 2:
            flash("Location must be at least 2 characters.", "sighting_error")
            is_valid = False
        if int(data['num_sasquatches']) < 1:
            flash("Number of Sasquatches must be greater than 0.", "sighting_error")
            is_valid = False
        return is_valid

    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO sightings (location, date_of_sighting, num_sasquatches, what_happened, users_id)
        VALUES (%(location)s, %(date_of_sighting)s, %(num_sasquatches)s, %(what_happened)s, %(users_id)s);
        """
        # Debugging: Check if data is passed correctly
        print("Inserting data into the database:", data)  # Debugging line
        connection = connectToMySQL(cls.db_name)
        return connection.query_db(query, data)


    @classmethod
    def update(cls, data):
        query = """
        UPDATE sightings
        SET location = %(location)s, date_of_sighting = %(date_of_sighting)s, 
            num_sasquatches = %(num_sasquatches)s, what_happened = %(what_happened)s, 
            updated_at = NOW()
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, sighting_id):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, {'id': sighting_id})

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings ORDER BY date_of_sighting DESC;"  # Orders by the most recent sighting
        results = connectToMySQL(cls.db_name).query_db(query)

        # Loop through the results and fetch user data for each sighting
        for sighting in results:
            query_user = "SELECT first_name, last_name FROM users WHERE id = %(users_id)s;"
            user_data = connectToMySQL(cls.db_name).query_db(query_user, {"users_id": sighting['users_id']})
            print(f"User Data for users_id {sighting['users_id']}:", user_data)  # Debugging: Log user data
            
            if user_data:
                sighting['first_name'] = user_data[0]['first_name']
                sighting['last_name'] = user_data[0]['last_name']
            else:
                sighting['first_name'] = "Unknown"
                sighting['last_name'] = "User"

        print("Final Combined Data:", results)  # Debugging: Log combined data
        return results

    @classmethod
    def get_sighting_by_user_id(cls, data):
        query_sightings = """
        SELECT id, location, date_of_sighting, num_sasquatches, what_happened
        FROM sightings
        WHERE users_id = %(users_id)s;
        """
        sightings = connectToMySQL(cls.db_name).query_db(query_sightings, data)

        if not sightings:
            return []

        for sighting in sightings:
            query_user = """
            SELECT first_name, last_name 
            FROM users 
            WHERE id = %(users_id)s;
            """
            user_data = connectToMySQL(cls.db_name).query_db(query_user, {"users_id": data['users_id']})
            if user_data:
                sighting['first_name'] = user_data[0]['first_name']
                sighting['last_name'] = user_data[0]['last_name']
            else:
                sighting['first_name'] = "Unknown"
                sighting['last_name'] = "User"

            query_skeptics = """
            SELECT COUNT(*) AS num_skeptics
            FROM skeptics
            WHERE sightings_id = %(sighting_id)s;
            """
            skeptics_data = connectToMySQL(cls.db_name).query_db(query_skeptics, {"sighting_id": sighting['id']})
            sighting['num_skeptics'] = skeptics_data[0]['num_skeptics'] if skeptics_data else 0

        return sightings

    @classmethod
    def get_skeptics_for_sighting(cls, sighting_id):
        # Fetch user details for skeptics of the given sighting in a single query
        query = """
        SELECT users.first_name, users.last_name
        FROM skeptics
        JOIN users ON skeptics.users_id = users.id
        WHERE skeptics.sightings_id = %(sighting_id)s;
        """
        data = {"sighting_id": sighting_id}
        results = connectToMySQL(cls.db_name).query_db(query, data)
        
        # Debugging: Log fetched skeptics
        print("Skeptics for Sighting ID", sighting_id, ":", results)
        
        return results if results else []  # Return the list of skeptics or an empty list if none found


    @classmethod
    def get_sighting_by_id(cls, sighting_id):
        query_sighting = "SELECT * FROM sightings WHERE id = %(sighting_id)s;"
        data = {"sighting_id": sighting_id}
        sighting = connectToMySQL(cls.db_name).query_db(query_sighting, data)

        if not sighting:
            return None

        query_user = "SELECT first_name, last_name FROM users WHERE id = %(users_id)s;"
        user_data = connectToMySQL(cls.db_name).query_db(query_user, {"users_id": sighting[0]['users_id']})

        if user_data:
            sighting[0]['first_name'] = user_data[0]['first_name']
            sighting[0]['last_name'] = user_data[0]['last_name']
        else:
            sighting[0]['first_name'] = "Unknown"
            sighting[0]['last_name'] = "User"

        return sighting[0]