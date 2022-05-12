import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth


CLIENT_ID="7ea53380dceb4651920aa0d91d296ea4"
CLIENT_SECRET="8d369c0d06cb4d43b52c9a99e00a4e7f"
REDIRECT_URI = "https://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)


date = input("Which year do you want to travel to? Type date in this format YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/"+date)
website_html = response.text

#Creating the soup
soup = BeautifulSoup(website_html,"html.parser")
song_titles = soup.select(selector="div li ul li h3")

user_id = sp.current_user()["id"]
top_100_songs_list = [song.getText().strip() for song in song_titles]

song_uris =[]
year = date.split("-")[0]
for song in top_100_songs_list:
    result = sp.search(q=f"track:{song} year:{year}",type="track")
    #print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} does not exist in Spotify.Skipped.")
#print(song_list)

playlist = sp.user_playlist_create(user=user_id,name=f"{date} Billboard 100",public=False)
#print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"],items=song_uris)