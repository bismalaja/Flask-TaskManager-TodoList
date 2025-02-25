import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        # Default connection to None
        self.connection = None
        
        try:
            self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='root',  # replace with your password
                db=db,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            print(f"Connected to {db} database successfully.")
        except Exception as e:
            print(f"Error connecting to {db} database: {e}")
            # Raise the exception to prevent silent failures
            raise

    def query_db(self, query, data=None):
        # Check if connection exists before proceeding
        if self.connection is None:
            raise RuntimeError("Database connection has not been established.")

        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data) if data else query
                cursor.execute(query)
                if query.lower().startswith("insert"):
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().startswith("select"):
                    results = cursor.fetchall()
                    return results
                else:
                    self.connection.commit()
            except Exception as e:
                print("Query Execution Failed:", e)
                return False

def connectToMySQL(db):
    return MySQLConnection(db)