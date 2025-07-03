import redis
from pymongo import MongoClient
import praw
from prawcore.exceptions import PrawcoreException
from config import (
    REDIS_HOST,
    REDIS_PORT,
    MONGO_URI,
    MONGO_DB_NAME,
    MONGO_COLLECTION_NAME,
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
)

# Initialize Redis client (for background tasks only)
redis_client = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True
)

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

# Initialize PRAW Reddit instance
try:
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )
    reddit.read_only = True  # We are only reading data
except PrawcoreException as e:
    print(f"Error initializing PRAW: {e}")
    reddit = None


def get_last_post_id():
    """Get the last processed post ID from MongoDB."""
    # Find the most recent post by created_utc timestamp
    last_post = collection.find_one(
        sort=[("created_utc", -1)]
    )
    return last_post["id"] if last_post else None


def set_last_post_id(post_id):
    """Store the last processed post ID in MongoDB for tracking."""
    # Update or insert the last post ID in a separate collection
    db.crawler_state.update_one(
        {"key": "last_post_id"},
        {"$set": {"value": post_id}},
        upsert=True
    )


def fetch_comments_for_submission(submission):
    """Fetch comments for a Reddit submission."""
    comments_data = []
    try:
        submission.comments.replace_more(limit=0)  # Flatten comment tree
        for comment in submission.comments.list():
            if hasattr(comment, "body"):
                comments_data.append(
                    {
                        "id": comment.id,
                        "author": (
                            comment.author.name if comment.author else "[deleted]"
                        ),
                        "body": comment.body,
                        "created_utc": comment.created_utc,
                    }
                )
    except PrawcoreException as e:
        print(f"Error fetching comments for submission {submission.id}: {e}")
    return comments_data


def fetch_new_reddit_posts():
    """Fetch and save new Reddit posts using MongoDB for state tracking."""
    if not reddit:
        print("PRAW not initialized. Skipping Reddit crawl.")
        return

    last_post_id = get_last_post_id()
    new_posts = []

    try:
        # Fetch new posts from r/all
        for submission in reddit.subreddit("all").new(limit=10):
            if submission.id == last_post_id:
                break

            comments = fetch_comments_for_submission(submission)

            new_posts.append(
                {
                    "id": submission.id,
                    "title": submission.title,
                    "url": submission.url,
                    "description": submission.selftext,
                    "created_utc": submission.created_utc,
                    "comments": comments,
                }
            )

        if new_posts:
            # Insert new posts (in reverse order to maintain chronological order in DB)
            collection.insert_many(list(reversed(new_posts)))
            set_last_post_id(new_posts[0]["id"])

        print(f"Fetched {len(new_posts)} new posts from Reddit")

    except PrawcoreException as e:
        print(f"Error fetching posts from Reddit: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during Reddit crawl: {e}")
