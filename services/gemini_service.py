import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

# Configure the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def analyze_category_of_query(topic):
    
    query = """ Is the following query  something that could be recommended like the following categories: movie, book, game, music, anime, manga, tv show,tv series,or anything other?
    Only respond with the category (e.g., 'movie') if it belongs to one of these, or respond with 'not recommendable' if it does not
    Query :  """ + topic

    model = genai.GenerativeModel("gemini-1.5-flash-8b")  # Use the appropriate model
    # Generate the analysis result from Gemini
    response = model.generate_content(query)

    if response.text == 'not recommendable':
        print('not recommendable')
    else:
        return response.text


def analyze_comments_with_gemini(post_data):
    """Analyzes comments with the Gemini API to generate a tier list."""

    # Combine the comments into a single string (or modify as needed)
    comments_text = "\n".join(
        [
            f"Title: {post['title']}\nComments:\n" + "\n".join(post["comments"])
            for post in post_data
        ]
    )

    # Create a prompt for the Gemini model
    prompt = """
        Generate a tier list for recommendations. The goal is to categorize relevant items into the following tiers:
        - S Tier: Most Recommended
        - A Tier: Highly Recommended
        - B Tier: Recommended
        - C Tier: Niche or Specialized Audience
        - Unranked: Items mentioned but lacking relevance or context.

        Strict requirements:
        1. Only include specific items directly relevant to the query topic (e.g., specific movies for 'Top Movies of All Time').
        2. Exclude any general lists, unrelated advice, or discussions that do not refer to specific items within the topic.
        3. Each item's title must clearly represent an individual work (e.g., a movie, book, or song). Exclude vague or aggregated titles (e.g., "Top 1000 Movies List").
        4. Provide a concise, context-specific reason for why each item fits its tier.

        Output structure:
        {
            "S Tier": [
                {"title": "Item 1", "reason": "Reason for recommendation."},
                {"title": "Item 2", "reason": "Reason for recommendation."}
            ],
            "A Tier": [
                {"title": "Item 3", "reason": "Reason for recommendation."}
            ],
            "B Tier": [
                {"title": "Item 4", "reason": "Reason for recommendation."}
            ],
            "C Tier": [
                {"title": "Item 5", "reason": "Reason for recommendation."}
            ],
            "Unranked": [
                {"title": "Excluded Item", "reason": "Explanation of irrelevance."}
            ]
        }

        Remember:
        - Do not include aggregated lists as titles (e.g., "Top 1000 Movies List").
        - Exclude items that lack a clear relationship to the topic (e.g., advice, comparisons, societal issues).
        - Filter out any entries without a specific recommendation or context.

        Here's the reference data for analysis:
""" + comments_text


    # try:
    model = genai.GenerativeModel("gemini-1.5-flash")  # Use the appropriate model
    # Generate the analysis result from Gemini
    response = model.generate_content(prompt)
    # print(response)
    
    return parse_tier_list(response.text)

    # except Exception as e:
    #     print(f"Error during Gemini API call: {e}")
    #     return None


import json

def parse_tier_list(raw_response):
    # Step 1: Trim any unwanted content before the first '{' and after the last '}'
    start_index = raw_response.find('{')
    end_index = raw_response.rfind('}') + 1

    # cleaned_response = raw_response[start_index:end_index]
    cleaned_response = raw_response

    # Step 2: Remove any unwanted escape sequences like \n, \t, etc.
    cleaned_response = cleaned_response.replace("\n", "").replace("\t", "")

    # Step 3: Remove the Markdown wrapping (````json\n` and `\n```), if present
    cleaned_response = cleaned_response.replace("```json", "").replace("```", "")

    # Step 4: Remove trailing commas if they exist
    # Remove trailing commas from the list/array before the closing bracket
    cleaned_response = cleaned_response.rstrip(',')  # Remove trailing comma

    # Step 5: Try to parse the cleaned string into JSON
    # try:
    parsed_data = json.loads(cleaned_response)

    return parsed_data
    # except json.JSONDecodeError as e:
        # print(f"Error parsing JSON: {e}")
        # return None
