from flask_app.config.mysqlconnection import connectToMySQL

class Skeptic:
    db_name = 'flaskappdatabase'

    @classmethod
    def check_skeptic(cls, data):
        query = """
        SELECT * FROM skeptics 
        WHERE users_id = %(user_id)s AND sightings_id = %(sighting_id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print("Check Skeptic Query Results:", results)  # Debugging: Log the results
        return bool(results)  # Return True if results exist, otherwise False

    @classmethod
    def add_skeptic(cls, data):
        query = """
        INSERT INTO skeptics (users_id, sightings_id, sightings_users_id, created_at) 
        VALUES (%(users_id)s, %(sightings_id)s, %(sightings_users_id)s, NOW());
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def remove_skeptic(cls, data):
        query = """
        DELETE FROM skeptics 
        WHERE users_id = %(users_id)s AND sightings_id = %(sightings_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)


