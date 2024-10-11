import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = "3d36ad419a384d8183297cc7fd9cb84d"
client_secret = "8f03472b9d424a4a8194f53740137fde"
date = input("Enter the date you want to get the top songs from (YYYY-MM-DD format):-")
URL = f"https://www.billboard.com/charts/india-songs-hotw/{date}/"

response = requests.get(URL)
contents = response.text
soup = BeautifulSoup(contents, features="html.parser")
final_list =[]
list = soup.find_all(id="title-of-a-story")
list2 = [item.getText().replace("\n", "") for item in list]
list3 = [item.replace("\t", "") for item in list2]
for item in list3[2:27]:
    final_list.append(item)



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
))
uri_list = []
for i in range(25):

    user = sp.search(q=final_list[i], type="track")
    track_uri = user["tracks"]["items"][0]["uri"]
    uri_list.append(track_uri)

playlist = sp.user_playlist_create(user="murad.adnan", name=f"{date} billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=uri_list)
