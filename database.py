# Make necessary imports for database manipulation
import sqlite3
from cryptography.fernet import Fernet
from datetime import datetime, timedelta


class Database:
    # Connect to the database
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()

    # Add the "users", "user_topics", "topics" table to the database
    c.execute("CREATE TABLE IF NOT EXISTS users(user_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
              "username TEXT,"
              "password TEXT,"
              "company_ID INTEGER,"
              "FOREIGN KEY(company_ID) REFERENCES companies(company_ID))")

    c.execute("CREATE TABLE IF NOT EXISTS companies(company_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
              "name TEXT)")

    c.execute("CREATE TABLE IF NOT EXISTS user_topics(user_ID INTEGER,"
              "topic_ID INTEGER,"
              "FOREIGN KEY(user_ID) REFERENCES users(user_ID)"
              "FOREIGN KEY(topic_ID) REFERENCES topics(topic_ID))")
    c.execute("CREATE TABLE IF NOT EXISTS topics(topic_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
              "name TEXT,"
              "sentiment FLOAT)")

    c.execute("CREATE TABLE IF NOT EXISTS logs(topic_ID INTEGER,"
              "company_ID INTEGER,"
              "sentiment FLOAT,"
              "date DATE,"
              "pos_tweets INT,"
              "neg_tweets INT,"
              "FOREIGN KEY(topic_ID) REFERENCES topics(topic_ID),"
              "FOREIGN KEY(company_ID) REFERENCES companies(company_ID))")

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

        # Decrypt the stored password
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

        # If the username exists, don't add the new user details
        if username_exists:
            c.close()
            return "Username already exists"

        # Encrypt the password
        encrypted_password = cls.encrypt(password)

        # Check if the company already exists in the companies table
        c.execute("SELECT company_ID FROM companies WHERE name = ?", (company,))
        company_exists = c.fetchone()

        if company_exists:
            # Get the ID of the company the user has entered
            companyID = company_exists[0]

            # Add the new user record
            c.execute("INSERT INTO users (user_ID, username, password, company_ID) VALUES (NULL, ?, ?, ?)",
                      (username, encrypted_password, companyID))
        else:
            # Add the new company record
            c.execute("INSERT INTO companies (company_ID, name) VALUES (NULL, ?)", (company,))

            # Get the ID of this new company
            c.execute("SELECT company_ID FROM companies WHERE name = ?", (company,))
            companyID = c.fetchone()[0]

            # Add the new user record
            c.execute("INSERT INTO users (user_ID, username, password, company_ID) VALUES (NULL, ?, ?, ?)",
                      (username, encrypted_password, companyID))

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

        # Check if the company already exists in the companies table
        c.execute("SELECT company_ID FROM companies WHERE name = ?", (new_company,))
        new_company_exists = c.fetchone()

        if new_company_exists:
            # Get the ID of the company the user has entered
            newCompanyID = new_company_exists[0]

            # Update the record with the new company
            c.execute("UPDATE users SET company_id = ? WHERE username = ?", (newCompanyID, username))

        else:
            # Add the new company record
            c.execute("INSERT INTO companies (company_ID, name) VALUES (NULL, ?)", (new_company,))

            # Get the ID of this new company
            c.execute("SELECT company_ID FROM companies WHERE name = ?", (new_company,))
            newCompanyID = c.fetchone()[0]

            # Update the record with the new company
            c.execute("UPDATE users SET company_id = ? WHERE username = ?", (newCompanyID, username))

        conn.commit()
        c.close()

    @staticmethod
    def new_topic(userID, topicName, topicSentiment=None):

        # Connect to the database
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()

        # Check if the topic already exists in the topics table
        c.execute("SELECT topic_ID FROM topics WHERE name = ?", (topicName,))
        topic_exists = c.fetchone()

        if topic_exists:
            # Get the ID of the existing topic the user has entered
            topicID = topic_exists[0]

            # Link this topic with the user's record
            c.execute("INSERT INTO user_topics (user_ID, topic_ID) VALUES (?, ?)", (userID, topicID))

        else:
            # Add the topic to the topic table
            c.execute("INSERT INTO topics (topic_ID, name, sentiment) VALUES (NULL, ?, NULL)", (topicName,))

            # Get the ID of this new topic
            c.execute("SELECT topic_ID FROM topics WHERE name = ?", (topicName,))
            topicID = c.fetchone()[0]

            # Link this topic with the user's record
            c.execute("INSERT INTO user_topics (user_ID, topic_ID) VALUES (?, ?)", (userID, topicID))

        conn.commit()
        c.close()

        return topicID

    @staticmethod
    def remove_topic(userID, topicID):
        # Connect to database
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()

        # Remove the record linking the user account to the topic and save changes
        c.execute("DELETE FROM user_topics WHERE user_ID = ? AND topic_ID = ?", (userID, topicID))
        conn.commit()
        c.close()

    @staticmethod
    def make_log(topic):
        # Connect to the database
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()

        # Get the current date
        date = datetime.now()
        date = date.strftime("%d/%m/%Y")

        # Check whether it is a company or topic log being made
        if topic.type == "topic":
            # Insert topic log data
            c.execute(
                "INSERT INTO logs (topic_ID, company_ID, sentiment, date, pos_tweets, neg_tweets) VALUES (?, NULL, ?, "
                "?, ?, ?)", (topic.id, topic.currentSentiment, date, topic.posTweets, topic.negTweets))

        elif topic.type == "company":
            # Insert company log data
            c.execute(
                "INSERT INTO logs (topic_ID, company_ID, sentiment, date, pos_tweets, neg_tweets) VALUES (NULL, ?, ?, "
                "?, ?, ?)", (topic.id, topic.currentSentiment, date, topic.posTweets, topic.negTweets))

        conn.commit()
        c.close()

    @staticmethod
    def get_logs(topic):
        # Connect to the database
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()

        # Check whether it is a company or topic log being retrieved
        if topic.type == "topic":
            # Get the logs of the topic with the provided id
            c.execute("SELECT * FROM logs WHERE topic_ID = ?", (topic.id,))

        elif topic.type == "company":
            # Get the logs of the company with the provided id
            c.execute("SELECT * FROM logs WHERE company_ID = ?", (topic.id,))

        # Get the results of the query
        logs = c.fetchall()

        # Remove company/topic id
        logs = [log[2:] for log in logs]

        c.close()

        return logs

    @staticmethod
    def get_user_info(username):
        # Connect to the database
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()

        # Get the user's record
        c.execute("SELECT user_ID, company_ID FROM users WHERE username = ?", (username,))
        data = c.fetchone()
        userID = data[0]
        companyID = data[1]

        # Get the user's company name based on their associated company ID
        c.execute("SELECT name FROM companies WHERE company_ID = ?", (companyID,))
        company = c.fetchone()[0]

        c.close()

        # Return the user id and user company
        return userID, company, companyID

    @staticmethod
    def get_user_topics(user_id):
        # Connect to the database
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()

        # Get all of the user's associated topics
        c.execute("SELECT topic_ID FROM user_topics WHERE user_ID = ?", (user_id,))
        topic_ids = [i[0] for i in c.fetchall()]

        # Get all of the topics using the retrieved IDs
        topics = []
        for index in topic_ids:
            c.execute("SELECT topic_ID,name FROM topics WHERE topic_ID = ?", (index,))
            current_topic = [topic for topic in c.fetchone()]
            topics.append(current_topic)

        c.close()

        return topics


# This can be added as a method to the Database class and when run will reset the contents of the db tables
    # @staticmethod
    # def delete():
    #
    #     # Connect to the database
    #     conn = sqlite3.connect('sentiment.db')
    #     c = conn.cursor()
    #
    #     # Remove each table
    #     c.execute("DROP TABLE users")
    #     c.execute("DROP TABLE user_topics")
    #     c.execute("DROP TABLE topics")
    #     c.execute("DROP TABLE companies")
    #     c.execute("DROP TABLE logs")
    #
    #     conn.commit()
    #     c.close()
