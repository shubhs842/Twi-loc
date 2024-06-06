import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, make_response
import random
import time

# Dictionary to store email-password pairs
users = {
    "vedant191202@gmail.com": "Pass@123",
    "another_user@example.com": "AnotherPass123",
    "twiloc2024@gmail.com": "twiloc@2024"
}

app = Flask(__name__)

app.secret_key = 'your_really_secret_key_here'

# Function to create database and load CSV data into it
def create_database_and_load_data():
    csv_file_path = 'file:///C:/Users/HP/OneDrive/Desktop/Project/final_processed_dataset.csv'
    db_url = 'sqlite:///tweets.db'
    data = pd.read_csv(csv_file_path)
    data.reset_index(drop=True, inplace=True)
    data['Serial No.'] = data.index + 1
    data.to_sql('tweets', db_url, index=False, if_exists='replace')

def filter_tweets_by_hashtag(data, hashtag):
    return data[data['hashtags_extracted'].str.lower().str.contains(hashtag.lower())]

def get_filtered_tweets(user_hashtag):
    db_url = 'sqlite:///tweets.db'
    query = "SELECT * FROM tweets"
    data = pd.read_sql_query(query, db_url)
    return filter_tweets_by_hashtag(data, user_hashtag)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']
        if user_email in users and users[user_email] == user_password:
            session['user_email'] = user_email
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Incorrect email or password. Please try again.")
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/input')
def get_tweets():
    # return render_template('input.html')
    if 'user_email' not in session:  # Check if user_email is in session
        return redirect(url_for('login'))
    return render_template('input.html')

@app.route('/results', methods=['POST'])
def results():
    user_hashtag = request.form['hashtag']
    filtered_data = get_filtered_tweets(user_hashtag)
    if not filtered_data.empty:
        time.sleep(5)
        filtered_data = filtered_data.sample(frac=1).reset_index(drop=True)
        return render_template('results.html', hashtag=user_hashtag, data=filtered_data.head(15))
    else:
        time.sleep(5)
        return render_template('no_results.html', hashtag=user_hashtag)
    
@app.route('/logout')
def logout():
    # Clear the session if you're using session management
    session.clear()
    # Redirect to the welcome page
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    create_database_and_load_data()
    app.run(debug=True)
