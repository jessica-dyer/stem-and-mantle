# Stem and Mantle

A Climbing Tracker App: Keep a record of your completed climbs at the gym.

## Local development

Prerequisites
Make sure you have the following installed on your machine:

Python 3.11.1
Poetry
PostgreSQL
Setup Steps

### Clone the Repository:

Open a terminal and navigate to the directory where you want to set up your project. Then, clone the repository:

`git clone https://github.com/jessica-dyer/stem-and-mantle.git`
cd your-app

### Install Dependencies:

Use Poetry to install the project dependencies:

poetry install

### Create a PostgreSQL Database:

Create a local PostgreSQL database for your app. You can use a tool like psql or a graphical interface like pgAdmin.

bash
Copy code
createdb yourappdb
Configure Environment Variables:

Create a .env file in the project root to store your environment variables:

plaintext
Copy code
DATABASE_URL=postgresql://yourusername:yourpassword@localhost:5432/yourappdb
Replace yourusername, yourpassword, and yourappdb with your PostgreSQL username, password, and the database name you created.