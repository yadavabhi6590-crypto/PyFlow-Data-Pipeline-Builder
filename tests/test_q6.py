from pyflow.utils import db_connection

if __name__=="__main__":
    print("--Question 6 database manager context manager test---")
    db_file = "test_database.db"

    try:
        # Context Manager (with) user the with to open the connection 
        with db_connection(db_file) as conn:
            cursor = conn.cursor()

            cursor.execute("""Create table if not exists sample_table(
                            id integer primary key autoincrement,
                            name text,
                            role text)""")

            # usme data insert karte hain

            cursor.execute("Insert into sample_table( name, role)Values ('Anshu','Data Engineer')")
            print("[Success] table ic create and data is inserted")

        print("[Success] Context manager can close the connection automatic")
    except Exception as e:
        print(f"[Error] Test fail ho g")