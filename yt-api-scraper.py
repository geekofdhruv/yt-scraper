import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('YOUTUBE_API_KEY')

def channel_details(forHandle):
    
    base_url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "snippet,statistics",  
        "forHandle": forHandle,       
        "key": api_key                
    }
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()
        
        # Extract relevant details
        if "items" in data and len(data["items"]) > 0:
            channel = data["items"][0]
            snippet = channel.get("snippet", {})
            statistics = channel.get("statistics", {})
            
            # Return extracted details
            return {
                "title": snippet.get("title", "N/A"),
                "description": snippet.get("description", "N/A"),
                "customUrl": snippet.get("customUrl", "N/A"),
                "country": snippet.get("country", "N/A"),
                "publishedAt": snippet.get("publishedAt", "N/A"),
                "viewCount": statistics.get("viewCount", "N/A"),
                "subscriberCount": statistics.get("subscriberCount", "N/A"),
                "videoCount": statistics.get("videoCount", "N/A")
            }
        else:
            return {"error": "No channel found with the provided handle."}
    else:
        # Handle API errors
        return {"error": f"API request failed with status code {response.status_code}: {response.text}"}
    

def video_info(id):
    base_url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "statistics,snippet",
        "id": id,       
        "key": api_key                
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        
        # Extract relevant details
        if "items" in data and len(data["items"]) > 0:
            channel = data["items"][0]
            snippet = channel.get("snippet",{})
            statistics = channel.get("statistics", {})
            
            # Return extracted details
            return { 
               "publishedAt": snippet.get('publishedAt', 'N/A'),
               "title": snippet.get('title','N/A'),
               "viewCount": statistics.get('viewCount','N/A'),
                "likeCount": statistics.get('likeCount','N/A'),
                "favoriteCount": statistics.get('favoriteCount','N/A'),
                "commentCount": statistics.get('commentCount','N/A')
            }
        else:
            return {"error": "No video found"}
    else:
        # Handle API errors
        return {"error": f"API request failed with status code {response.status_code}: {response.text}"}


# Test the function
urlInput = input("URL link : ")
def info(urlInput) : 
    if 'watch?v=' in urlInput:
        id = urlInput.split('=')[-1]
        print(video_info(id))
    elif '@' in urlInput:
        channel_handle = urlInput.split('/')[-1]
        print(channel_details(channel_handle))
    else:
        print ("error: Invalid URL. Please provide a valid YouTube channel or video URL.")

info(urlInput)
