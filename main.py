from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.reddit_service import get_top_posts_and_comments
from services.gemini_service import analyze_comments_with_gemini, analyze_category_of_query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Allowing requests from your frontend (localhost:3000)
origins = [
    "http://localhost:3000",  # Your frontend URL
    "http://127.0.0.1:8000",  # If you want to allow backend-to-backend requests
    "https://curio-frontend-azure.vercel.app"
]

# Adding CORSMiddleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins in the list
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define a request model for input validation
class TopicRequest(BaseModel):
    topic: str


@app.post("/recommend")
async def recommend(topic_request: TopicRequest):
    topic = topic_request.topic

    # Analyze the category of the topic using Gemini
    category = analyze_category_of_query(topic)
    if category == "not recommendable":
        raise HTTPException(status_code=400, detail="The provided topic is not recommendable.")

    # Fetch posts and comments from Reddit
    try:
        post_data = get_top_posts_and_comments(topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from Reddit: {str(e)}")

    # Analyze comments with Gemini to generate a tier list
    try:
        tier_list = analyze_comments_with_gemini(post_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing data with Gemini: {str(e)}")

    # Return the tier list
    return {
        "topic": topic,
        "category": category,
        "tier_list": tier_list,
    }
