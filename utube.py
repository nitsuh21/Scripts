from googleapiclient.discovery import build

API_KEY = "YOUR_API_KEY"

def get_channels_with_1m_subscribers(api_key):
    youtube = build("youtube", "v3", developerKey=api_key)

    # Set parameters for the search
    search_response = youtube.search().list(
        part="snippet",
        type="channel",
        order="viewCount",  # You can change this to sort by different criteria
        maxResults=50,  # Adjust the number of results as needed
        q="",  # An empty search string returns all channels
    ).execute()

    channels = []

    # Iterate through the search results
    for search_result in search_response.get("items", []):
        channel_id = search_result["id"]["channelId"]
        channel_response = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id,
        ).execute()

        # Check if the channel has over 1 million subscribers
        if int(channel_response["items"][0]["statistics"]["subscriberCount"]) > 1000000:
            channels.append(channel_response["items"][0])

    return channels

if __name__ == "__main__":
    channels = get_channels_with_1m_subscribers(API_KEY)

    for channel in channels:
        print(f"Channel: {channel['snippet']['title']}")
        print(f"Subscribers: {channel['statistics']['subscriberCount']}")
        print("=" * 30)
