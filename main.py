import praw
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

def search_reddit():
    try:
        query = input("Enter a search term (e.g., 'top 10 Hollywood movies'): ")
        limit = int(input("Enter the number of posts you'd like to see (e.g., 10): "))

        search_results = reddit.subreddit('all').search(query, limit=limit, sort='relevance')

        print(f"\nTop {limit} posts for '{query}':\n")
        for index, post in enumerate(search_results, start=1):
            print(f"{index}. {post.title} (Subreddit: r/{post.subreddit})")
    except ValueError:
        print("Please enter a valid number.")
    except Exception as e:
        print("An error occurred:", e)

search_reddit()
