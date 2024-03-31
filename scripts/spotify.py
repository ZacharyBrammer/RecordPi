import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Connect to Spotify API
scope = "user-read-playback-state,user-modify-playback-state"

sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

# Get list of available devices
devices = sp.devices()
print(devices)

# Find active device, if none are active use first
device_id = devices['devices'][0]['id']
for device in devices['devices']:
  if device['is_active'] == True:
    device_id = device['id']
    break

print(device_id)

uri = input("URI for playback: ")

# Start playback of URI
results = sp.start_playback(context_uri=f'{uri}')
print(results)