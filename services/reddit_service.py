import praw
import os
from dotenv import load_dotenv

load_dotenv()
# Initialize the Reddit API instance
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent=os.getenv('USER_AGENT')
)

def get_top_posts_and_comments(query, post_limit=3, comment_limit=3, top_communities=3):
    """Fetches top posts from the top communities based on the query and retrieves comments."""
    post_data = []
    
    # Step 1: Search for the query across all Reddit communities to find the top subreddits
    search_results = reddit.subreddit('all').search(query, limit=post_limit, sort='relevance')

    # Step 2: Collect top subreddits from the search results
    top_subreddits = set()  # Using a set to avoid duplicate subreddit names
    for post in search_results:
        top_subreddits.add(post.subreddit.display_name)

    # Limit the number of top subreddits to top_communities
    top_subreddits = list(top_subreddits)[:top_communities]

    # Step 3: For each of the top subreddits, fetch top posts and comments
    for subreddit_name in top_subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        
        # Search for the query within the current subreddit
        subreddit_posts = subreddit.search(query, limit=post_limit, sort='relevance')
        
        for post in subreddit_posts:
            comments = []
            post.comments.replace_more(limit=0)  # Get only top-level comments
            
            # Step 4: Fetch the top comments (limit to 'comment_limit')
            for comment in post.comments[:comment_limit]:
                comments.append(comment.body)
            
            post_data.append({
                'title': post.title,
                'url': post.url,
                'subreddit': subreddit_name,
                'comments': comments
            })
    
    return post_data
