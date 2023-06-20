#!/usr/bin/env python3.9.6

import time
import praw
import sqlite3
import concurrent.futures
from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Database connection
DB_NAME = 'reddit_posts.db'


def create_reddit_instance(client_id, client_secret, user_agent):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )
    return reddit


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create table for storing posts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            title TEXT,
            author TEXT,
            timestamp INTEGER,
            content TEXT,
            subreddit TEXT
        )
    ''')
    conn.commit()
    conn.close()


def store_post_in_database(post):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if post already exists in the database
    cursor.execute('SELECT * FROM posts WHERE id=?', (post.id,))
    existing_post = cursor.fetchone()

    if existing_post is None:
        # Insert new post into the database
        cursor.execute('''
            INSERT INTO posts (id, title, author, timestamp, content, subreddit)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (post.id, post.title, post.author.name, post.created_utc, post.selftext, post.subreddit.display_name))
        conn.commit()

    conn.close()


def get_posts_from_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if the 'posts' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts'")
    table_exists = cursor.fetchone()

    if table_exists:
        # Retrieve all posts from the database
        cursor.execute('SELECT * FROM posts')
        posts = cursor.fetchall()
    else:
        posts = []

    conn.close()

    return posts


@app.route('/posts')
def get_all_posts():
    # Fetch posts from the database
    posts = get_posts_from_database()

    # Convert posts to a list of dictionaries
    post_dicts = [
        {
            'id': post[0],
            'title': post[1],
            'author': post[2],
            'timestamp': post[3],
            'content': post[4],
            'subreddit': post[5]
        }
        for post in posts
    ]

    return jsonify(post_dicts)


def crawl_and_store_posts(reddit, subreddits):
    while True:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Create a list to store the futures
            futures = []

            for subreddit_name in subreddits:
                print(f"Crawling posts from subreddit: {subreddit_name}")
                subreddit = reddit.subreddit(subreddit_name)

                # Get the latest stored post timestamp for the subreddit
                latest_timestamp = get_latest_timestamp(subreddit_name)

                # Submit the crawling task to the executor
                future = executor.submit(crawl_posts_from_subreddit, subreddit, latest_timestamp)
                futures.append(future)

            # Wait for all futures to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    # Retrieve the result of the completed future (if any)
                    result = future.result()
                    if result is not None:
                        subreddit_name, new_posts_count = result
                        print(f"Crawling finished for subreddit: {subreddit_name}, New posts stored: {new_posts_count}")
                except Exception as e:
                    print(f"Exception occurred: {str(e)}")

        time.sleep(60)  # Wait for 60 seconds before checking for new posts again


def crawl_posts_from_subreddit(subreddit, latest_timestamp):
    # Fetch a larger number of posts from the subreddit
    posts = subreddit.new(limit=10)  # Fetch 10 posts

    # Counter for the number of new posts stored
    new_posts_count = 0

    # Iterate over the fetched posts in reverse order (latest first)
    for post in reversed(list(posts)):
        if post.created_utc > latest_timestamp:
            # Store the new post in the database
            store_post_in_database(post)
            new_posts_count += 1

            if new_posts_count > 5:
                # Stop storing additional posts after storing the last 5 new posts
                break

    return subreddit.display_name, new_posts_count


def get_latest_timestamp(subreddit_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Retrieve the latest stored post timestamp for the subreddit
    cursor.execute('SELECT MAX(timestamp) FROM posts WHERE subreddit=?', (subreddit_name,))
    result = cursor.fetchone()
    latest_timestamp = result[0] if result[0] else 0

    conn.close()

    return latest_timestamp


if __name__ == '__main__':
    # Create the database if it doesn't exist
    create_database()

    # User input for Reddit API credentials
    client_id = input("Enter your Reddit client ID: ")
    client_secret = input("Enter your Reddit client secret: ")
    user_agent = input("Enter your Reddit user agent: ")

    # Create the Reddit instance
    reddit = create_reddit_instance(client_id, client_secret, user_agent)

    # User input for subreddits to track
    subreddits_to_track = []
    while True:
        subreddit = input("Enter a subreddit to track (or enter 'done' to finish): ")
        if subreddit == 'done':
            break
        subreddits_to_track.append(subreddit)

    # Start crawling and storing posts in the background
    crawler_thread = concurrent.futures.ThreadPoolExecutor().submit(crawl_and_store_posts, reddit, subreddits_to_track)

    # Run the Flask app
    app.run(debug=True)
