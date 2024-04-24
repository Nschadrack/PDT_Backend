import sqlite3
from models import User


def create_user(user):
    result = get_user_by_email(user.get_email())
    conn = None
    if not result[1]:
        try:
            conn = sqlite3.connect("pdt.db")

            query = """INSERT INTO users(name, email, password) 
                                    VALUES(?, ?, ?)"""

            cursor = conn.cursor()
            cursor.execute(query, (user.get_name(),
                                   user.get_email(),
                                   user.get_password()))
            conn.commit()
            return "Account  created successfully!", True
        except Exception as e:
            return f"Error: {str(e)}", False
        finally:
            if conn:
                conn.close()
    else:
        return f"User with email: {user.get_email()} already exists.", False


def get_user_by_email(email):
    conn = None
    try:
        conn = sqlite3.connect("pdt.db")
        query = "SELECT * FROM users WHERE email=?"
        cursor = conn.cursor()
        cursor.execute(query, (email,))
        row = cursor.fetchone()

        if row is not None:
            return User(name=row[1],
                        email=row[2], password=row[3]), True
        else:
            return None, False
    except Exception as e:
        return f"Error: {str(e)}", False
    finally:
        if conn:
            conn.close()


def delete_user(email):
    conn = None
    try:
        conn = sqlite3.connect("pdt.db")
        query = "DELETE FROM users WHERE email=?"
        cursor = conn.cursor()
        cursor.execute(query, (email,))
        conn.commit()
        return "deleted successfully", True
    except Exception as e:
        return f"Error: {str(e)}", False
    finally:
        if conn:
            conn.close()


def get_users():
    conn = None
    try:
        conn = sqlite3.connect("pdt.db")
        query = "SELECT * FROM users"
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        users = []
        for row in rows:
            users.append(User(name=row[1],
                              email=row[2], password=row[3]))
        return users, True
    except Exception as e:
        return f"Error: {str(e)}", False
    finally:
        if conn:
            conn.close()


def get_user_session_by_email(email):
    conn = None
    try:
        conn = sqlite3.connect("pdt.db")
        query = "SELECT * FROM sessions WHERE email=?"
        cursor = conn.cursor()
        cursor.execute(query, (email,))
        row = cursor.fetchone()

        if row is not None:
            return row, True
        else:
            return None, False
    except Exception as e:
        return f"Error: {str(e)}", False
    finally:
        if conn:
            conn.close()


def create_or_update_user_session(email, login_logout):
    result = get_user_session_by_email(email)
    conn = None
    try:
        conn = sqlite3.connect("pdt.db")
        values = (login_logout, email)
        if result[1]:
            query = "UPDATE sessions SET logged_in=? WHERE email=?"
        elif result[0] is None:
            query = "INSERT INTO sessions(logged_in, email) VALUES(?, ?)"
        else:
            return result

        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return "Success", True
    except Exception as e:
        return f"Error: {str(e)}", False
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    result = get_users()
    for user in result[0]:
        print("name: ", user.get_name())
        print("email: ", user.get_email())
        print("Password: ", user.get_password())
