# Curio: Ride the Trend, Get the Best Recommendations

Curio is an idea and content discovery app that taps into trending topics and recommendations. Whether you're looking for the best movies, trending manga, or creative inspiration, this app serves as your personal guide to the best recommendations out there. With real-time data, you can uncover popular opinions, lists, and ideas curated by real people across various topics. 

**This is the process of production. There is no UI or anything, but there will be. So stay tuned for more 😊**

## Installation Guide

### Clone the Repository

```bash
git clone https://github.com/mrinshad/Curio.git
cd Curio
```
### Install Dependencies

Make sure to install the necessary packages by running:
```bash
pip install -r requirements.txt
```

### Configure the API Credentials

- Create a .env file in the project root directory.
- Add your API credentials to the .env file:

```bash
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
USER_AGENT=your_user_agent
GEMINI_API_KEY=your_gemini_api_key
```
### Run the App

Now you’re all set! Run the app with:
```bash
python -m uvicorn main:app --reload
```
Start exploring the best recommendations and ride the trend with Curio!