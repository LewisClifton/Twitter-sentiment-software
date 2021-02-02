import sqlite3
from cryptography.fernet import Fernet


class Database:
    # Connect to the database
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()

    # Check if the tables in the database have been created yet
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ")
    # If not, create the tables in the database
    if c.fetchone()[0] == 0:

        # Add the "users", "user_topics", "topics" table to the database
        c.execute("CREATE TABLE users(user_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                  "username TEXT,"
                  "password TEXT,"
                  "company TEXT,"
                  "FOREIGN KEY(user_ID) REFERENCES user_topics(user_ID))")
        # c.execute("CREATE TABLE companies(company_id INTEGER,"
        #           "topic_ID INTEGER,"
        #           "FOREIGN KEY(user_ID) REFERENCES user_topics(user_ID)"
        #           "FOREIGN KEY(topic_ID) REFERENCES topics(topic_ID))")
        c.execute("CREATE TABLE user_topics(user_ID INTEGER,"
                  "topic_ID INTEGER,"
                  "FOREIGN KEY(user_ID) REFERENCES user_topics(user_ID)"
                  "FOREIGN KEY(topic_ID) REFERENCES topics(topic_ID))")
        c.execute("CREATE TABLE topics(topic_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                  "topic_name TEXT,"
                  "topic_sentiment FLOAT, "
                  "topic_date DATE,"
                  "FOREIGN KEY(topic_ID) REFERENCES user_topics(topic_ID))")

        # Commit changes to the database
        conn.commit()

    # Disconnect from the database
    c.close()

    @staticmethod
    def encrypt(password):

        # Import the externally saved encryption key
        from keys import encryption_key

        # Return the encrypted password
        f = Fernet(encryption_key)
        password_in_bytes = password.encode()
        encrypted_password = f.encrypt(password_in_bytes)
        return encrypted_password

    @staticmethod
    def decrypt(encrypted_password):

        # Import the externally saved encryption key
        from keys import encryption_key
        f = Fernet(encryption_key)

        # Return the decrypted password
        decrypted_password = f.decrypt(encrypted_password).decode()
        return decrypted_password

    @classmethod
    def authenticate(cls, username, entered_password):

        # Connect to database
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()

        # Check if record with this username exists
        c.execute("SELECT count(username) FROM users WHERE username=?", (username,))
        if c.fetchone()[0] == 0:
            c.close()
            return False

        # Get the stored password
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        stored_password = c.fetchone()[0]

        c.close()

        # Decrpyt the stored password
        decrypted_password = cls.decrypt(stored_password)

        # Check if the entered and stored passwords match
        if decrypted_password == entered_password:
            return True
        else:
            return False

    @classmethod
    def new_user(cls, username, password, company):

        # Check if they have entered a valid username
        if len(username) < 2 or len(username) > 30:
            return "Please enter a valid username"

        # Check if they have entered a valid company name
        if len(company) < 2 or len(company) > 30:
            return "Please enter a valid company name"

        # Check if the password is long enough
        valid_length = True
        if len(password) < 4:
            valid_length = False

        # Check if there is at least one special character in the password
        special_chars = "!\"£$%^&*(){}[];\':@<>,./?\|"
        contains_special = False
        for char in special_chars:
            if char in password:
                contains_special = True
                break

        # Check if there is at least one uppercase character
        contains_upper = False
        for char in password:
            if char.isupper():
                contains_upper = True
                break

        # Don't add the new details if the password isn't strong enough
        if not (valid_length and contains_special and contains_upper):
            return "Password not strong enough"

        # Query user table to see if the username exists
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        username_exists = c.fetchone()

        if username_exists:
            # Don't add the new user details
            c.close()
            return "Username already exists"
        else:
            # Encrypt the password and add the new user details
            encrypted_password = cls.encrypt(password)
            c.execute("INSERT INTO users (user_ID, username, password,company) VALUES (NULL, ?, ?, ?)",
                      (username, encrypted_password, company))
            conn.commit()
            c.close()

            return

    @classmethod
    def change_password(cls, username, new_password):

        # Connect to the database
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()

        # Encrypt the new password
        encrypted_password = cls.encrypt(new_password)

        # Update the record with the new password
        c.execute("UPDATE users SET password = ? WHERE username = ?", (encrypted_password, username))
        conn.commit()
        c.close()

    @classmethod
    def change_company(cls, username, new_company):
        # Connect to the database
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()

        # Update the record with the new company
        c.execute("UPDATE users SET company = ? WHERE username = ?", (new_company, username))
        conn.commit()
        c.close()

    @staticmethod
    def delete():
        # Connect to the database
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()

        # Remove each table
        c.execute("DROP TABLE users")
        c.execute("DROP TABLE user_topics")
        c.execute("DROP TABLE topics")

        conn.commit()
        c.close()

    @staticmethod
    def new_topic(user_id, topic_name, topic_sentiment=None):

        # Get the current date
        from datetime import datetime
        date = datetime.today().strftime('%d/%m/%Y')

        # Connect to the database
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()

        # Add the topic to the topic table
        c.execute("INSERT INTO topics (topic_ID, topic_name, topic_sentiment, topic_date) VALUES (NULL, ?, NULL, ?)",
                  (topic_name, date))

        # Update the user topics table
        c.execute("SELECT topic_ID FROM topics WHERE topic_name = ?", (topic_name,))
        topic_id = c.fetchone()[0]

        c.execute("INSERT INTO user_topics (user_ID, topic_ID) VALUES (?, ?)",
                  (user_id, topic_id))
        conn.commit()

        c.close()

    @staticmethod
    def get_user_info(username):

        # Connect to the database
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()

        # Get the user record
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        arr = c.fetchone()
        c.close()

        # Return the user id and user company
        return arr[0], arr[3]

    @staticmethod
    def get_user_topics(user_id):
        # Connect to the database
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()

        # Get the user record
        c.execute("SELECT topic_ID FROM user_topics WHERE user_ID = ?", (user_id,))
        topic_ids = [i[0] for i in c.fetchall()]

        topics = []
        for index in topic_ids:
            c.execute("SELECT topic_name,topic_sentiment,topic_date FROM topics WHERE topic_ID = ?", (index,))
            current_topic = [topic for topic in c.fetchone()]
            topics.append(current_topic)
        c.close()

        return topics



    # def update_topic(self, topic_sentiment):
    #     pass

# import model
import scraper


