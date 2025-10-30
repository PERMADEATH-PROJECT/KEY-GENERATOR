# S30 Launcher - Invite Key Generator

This is a simple yet effective Python script designed to generate unique invitation keys and insert them into a MariaDB/MySQL database for the 's30\_launcher' application. It's built to be run from the command line, prompting the user for the number of keys to generate and the necessary database credentials.

-----

## Features

  * **Key Generation**: Creates a user-defined number of keys in the `PDSMP-XXXX-XXXX` format.
  * **Secure Characters**: Uses Python's `secrets` module for cryptographically strong random character generation (`A-Z`, `0-9`).
  * **Database Integration**: Seamlessly connects to a MariaDB/MySQL database to store the keys.
  * **Bulk Insertion**: Efficiently inserts all generated keys into the `invites` table in a single database transaction.
  * **Error Handling**: Gracefully handles potential database connection errors and rolls back changes if an insertion fails.
  * **User-Friendly CLI**: Interactive command-line interface for ease of use.

-----

## Prerequisites

Before you begin, ensure you have the following installed:

  * Python 3.6+
  * Access to a running MariaDB or MySQL database server.
  * The `mysql-connector-python` library.

-----

## Installation & Setup

1.  **Download the files**
    Clone this repository or download the source files (`main.py`, `logic.py`, `sql_handler.py`) into a single directory.

2.  **Install the required library**
    Open your terminal or command prompt and install the necessary Python package:

    ```sh
    pip install mysql-connector-python
    ```

3.  **Set up the Database**
    You need to create the database and tables before running the script. Execute the following SQL script in your MariaDB/MySQL server. This will create the `s30_launcher` database (if it doesn't exist) and the required tables (`users`, `invites`, etc.).

    ```sql
    -- Create the database if it doesn't exist
    CREATE DATABASE IF NOT EXISTS s30_launcher;
    USE s30_launcher;

    -- Create the users table
    CREATE TABLE IF NOT EXISTS users (
       id INT PRIMARY KEY AUTO_INCREMENT,
       minecraft_username VARCHAR(16) NOT NULL,
       password_hash VARCHAR(255) NOT NULL
    );

    -- Create the invites table
    CREATE TABLE IF NOT EXISTS invites (
       id INT PRIMARY KEY AUTO_INCREMENT,
       code VARCHAR(64) NOT NULL,
       user_id INT,
       claimed BOOLEAN DEFAULT FALSE,
       FOREIGN KEY (user_id) REFERENCES users(id)
    );

    -- Ensure all invite codes are unique
    ALTER TABLE invites ADD UNIQUE (code);

    -- Create the sessions table
    CREATE TABLE IF NOT EXISTS sessions (
       id INT PRIMARY KEY AUTO_INCREMENT,
       user_id INT NOT NULL,
       session_token VARCHAR(255) NOT NULL,
       expires_at DATETIME NOT NULL,
       FOREIGN KEY (user_id) REFERENCES users(id)
    );

    -- Create the account_status table
    CREATE TABLE IF NOT EXISTS account_status (
       id INT PRIMARY KEY AUTO_INCREMENT,
       user_id INT NOT NULL,
       player_status BOOLEAN DEFAULT TRUE,
       days_survived INT DEFAULT 0,
       last_connection DATETIME,
       FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ```

-----

## How to Use

1.  Navigate to the directory where you saved the Python files.
2.  Run the `main.py` script from your terminal:
    ```sh
    python main.py
    ```
3.  The script will prompt you for the following information:
      * **How many keys you want to generate**: Enter a positive integer.
      * **Database Host**: The IP address or hostname of your database server (e.g., `localhost` or `192.168.1.100`).
      * **Database User**: The username for your database.
      * **Database Password**: The password for the user (input will be hidden for security).
      * **Database Name**: The name of the database where the tables were created (e.g., `s30_launcher`).

The script will then generate the keys and attempt to insert them into the `invites` table, printing status messages along the way.

-----

## File Structure

The project is organized into three distinct files for clarity and separation of concerns:

  * `main.py`: The main entry point of the application. It handles user input and orchestrates the key generation and database insertion process.
  * `logic.py`: Contains the `generate_keys` function. This module is solely responsible for the business logic of creating the formatted, random keys.
  * `sql_handler.py`: A class-based module (`SQLHandler`) for managing all database interactions. It handles connecting, inserting data, and disconnecting from the database.