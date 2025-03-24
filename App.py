import streamlit as st # type: ignore
import spotipy # type: ignore
from spotipy.oauth2 import SpotifyClientCredentials # type: ignore
from dotenv import load_dotenv # type: ignore
import os
import matplotlib.pyplot as plt # type: ignore

# Set page config as the first command
st.set_page_config(page_title="Bollywood Playlist", page_icon="🎵", layout="centered", initial_sidebar_state="collapsed")

# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# Spotify API authentication
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

# Initialize session state for mood and pagination
if "offset" not in st.session_state:
    st.session_state.offset = 0
if "mood" not in st.session_state:
    st.session_state.mood = None
if "liked_songs" not in st.session_state:
    st.session_state.liked_songs = []
if "playlist_generated" not in st.session_state:
    st.session_state.playlist_generated = False
if "feedback_data" not in st.session_state:
    st.session_state.feedback_data = {"Loved it!": 0, "It was good": 0, "Not my style": 0}

# Mood to query mapping
mood_to_query = {
    "Happy": "Bollywood upbeat party",
    "Sad": "Bollywood emotional sad songs",
    "Romantic": "Bollywood romantic love songs",
    "Party": "Bollywood dance party",
    "Relaxed": "Bollywood acoustic chill",
    "Devotional": "Bollywood devotional bhajan"
}

# Define background colors for mood
mood_colors = {
    "Happy": "#FFEB3B",  # Yellow
    "Sad": "#3F51B5",    # Blue
    "Romantic": "#F44336", # Red
    "Party": "#FF5722",   # Orange
    "Relaxed": "#9C27B0",  # Purple
    "Devotional": "#8BC34A" # Green
}

# Define light/dark theme based on mood
mood_themes = {
    "Happy": "light",
    "Sad": "dark",
    "Romantic": "dark",
    "Party": "light",
    "Relaxed": "light",
    "Devotional": "dark"
}

# Streamlit app
st.title("🎵 Bollywood Mood-Based Playlist Generator With Abhi")
st.write("Select your mood and discover a Bollywood playlist tailored to you!")


# Add beat png to sidebar
beat_png_path = "beat.png"  # Ensure this file is in the same directory as your script

try:
    # Remove use_container_width if it's causing an error
    st.sidebar.image(beat_png_path)
except FileNotFoundError:
    st.sidebar.warning("beat.png not found. Please check the file path.")
    

# Add dj png to sidebar
dj_png_path = "dj.png"  # Ensure this file is in the same directory as your script

try:
    # Remove use_container_width if it's causing an error
    st.sidebar.image(dj_png_path)
except FileNotFoundError:
    st.sidebar.warning("dj.png not found. Please check the file path.")
    
    
# Add music png to sidebar
music_png_path = "music.png"  # Ensure this file is in the same directory as your script

try:
    # Remove use_container_width if it's causing an error
    st.sidebar.image(music_png_path)
except FileNotFoundError:
    st.sidebar.warning("music.png not found. Please check the file path.")
    


st.sidebar.title("Developer: Abhishek Kumar")

# Add my jpg to sidebar
my_jpg_path = "pic.jpg"  # Ensure this file is in the same directory as your script

try:
    # Remove use_container_width if it's causing an error
    st.sidebar.image(my_jpg_path)
except FileNotFoundError:
    st.sidebar.warning("pic.jpg not found. Please check the file path.")
    
    
    

# Mood selection dropdown (no default selection)
selected_mood = st.selectbox(
    "What's your current mood?",
    ["", "Happy", "Sad", "Romantic", "Party", "Relaxed", "Devotional"]
)

# Display motivational quote based on mood
mood_quotes = {
    "Happy": "Happiness is not something ready-made. It comes from your own actions.",
    "Sad": "Sometimes, we need a little rain to appreciate the sun.",
    "Romantic": "Love is composed of a single soul inhabiting two bodies.",
    "Party": "Life is a party, dress like it!",
    "Relaxed": "Take a deep breath and relax, everything is going to be okay.",
    "Devotional": "Faith is the bird that feels the light when the dawn is still dark."
}

if selected_mood:
    st.markdown(f"### {mood_quotes[selected_mood]}")

    # Change background color based on selected mood
    st.markdown(f"<style>body{{background-color: {mood_colors[selected_mood]};}}</style>", unsafe_allow_html=True)

    # Apply theme mode based on user mood
    if mood_themes[selected_mood] == "light":
        st.markdown("""
        <style>
            .css-1d391kg {background-color: #ffffff; color: #000000;}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .css-1d391kg {background-color: #121212; color: #ffffff;}
        </style>
        """, unsafe_allow_html=True)

    # Generate playlist on button click
    if st.button("Generate Playlist"):
        # Reset offset and mood in session state
        st.session_state.offset = 0
        st.session_state.mood = selected_mood
        st.session_state.playlist_generated = True

    # Only fetch songs if a mood is selected
    if st.session_state.mood:
        # Get the query for the selected mood
        query = mood_to_query[st.session_state.mood]

        try:
            # Fetch tracks from Spotify
            results = sp.search(q=query, type='track', limit=10, offset=st.session_state.offset)

            # Display playlist
            st.write(f"### Here’s your {st.session_state.mood.lower()} Bollywood playlist:")

            # Display each song with play and rating options
            for track in results['tracks']['items']:
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                spotify_url = track['external_urls']['spotify']  # Spotify URL for full song
                preview_url = track['preview_url']  # Preview URL for short song preview
                track_id = track['id']  # Unique track ID for the song

                # Song information display
                st.markdown(f"{track_name} by {artist_name}")

                # Song preview (if available)
                if preview_url:
                    st.audio(preview_url, format="audio/mp3")

                # Thumbs up/down for rating with unique keys
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍", key=f"{track_id}_like"):  # Use track_id to ensure unique key
                        st.session_state.liked_songs.append(track_name)
                        st.success(f"You liked {track_name}!")
                with col2:
                    if st.button("👎", key=f"{track_id}_dislike"):  # Use track_id to ensure unique key
                        st.session_state.liked_songs.append(track_name)
                        st.error(f"You disliked {track_name}.")

                # Link to open song on Spotify
                st.markdown(f"[Open on Spotify]({spotify_url})")

            # Create navigation buttons for Previous and Next
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.offset > 0:  # Prevent negative offset
                    if st.button("Previous Songs"):
                        st.session_state.offset -= 10
            with col2:
                if st.button("Next Songs"):
                    st.session_state.offset += 10

            # Social sharing options
            st.write("\n")
            st.markdown("#### Share your playlist with your friends!")

            # Replace 'YOUR_APP_URL' with your actual Streamlit app URL
            app_url = "https://your-app-url.streamlit.app"  # Replace with your actual app URL

           

            # Feedback poll after generating playlist
            if st.session_state.playlist_generated:
                st.write("\n")
                feedback = st.radio("How do you feel about this playlist?", ("Loved it!", "It was good", "Not my style"))
                if feedback:
                    st.write(f"Thank you for your feedback! You selected: {feedback}")
                    st.session_state.feedback_data[feedback] += 1
                    st.write("You are truly amazing! Keep enjoying the music and always stay positive. 🎶")
                    st.write("Let the rhythm of the beats inspire you.")
                    st.write("You're the star of your own playlist, and this is just the beginning.")
                    st.write("Feel the music, feel the joy, and dance through life!")
                    st.write("Wishing you many more fantastic playlists and happy vibes ahead!")

                # Feedback analytics
                st.write("\n")
                st.write("### Feedback Analytics:")
                fig, ax = plt.subplots()
                ax.bar(st.session_state.feedback_data.keys(), st.session_state.feedback_data.values(), color=['green', 'blue', 'red'])
                st.pyplot(fig)
                
                
                # Display trending songs or artists
                st.markdown("### Trending Songs or Artists Right Now!")
                try:
                    trending_results = sp.search(q="Bollywood", type='track', limit=5)
                    for track in trending_results['tracks']['items']:
                        st.write(f"🎵 {track['name']} by {track['artists'][0]['name']}")
                        st.markdown(f"[Open on Spotify]({track['external_urls']['spotify']})")
                except Exception as e:
                    st.error(f"Unable to fetch trending songs: {e}")


            
            # Search functionality
            st.write("\n")
            st.markdown("### Search for Songs or Artists")
            search_query = st.text_input("Search for a song or artist:")
            if search_query:
                try:
                    search_results = sp.search(q=search_query, type='track', limit=10)
                    for track in search_results['tracks']['items']:
                        track_name = track['name']
                        artist_name = track['artists'][0]['name']
                        spotify_url = track['external_urls']['spotify']  # Direct Spotify link

                        # Display search result with Spotify link
                        st.write(f"{track_name} by {artist_name}")
                        st.markdown(f"[Open on Spotify]({spotify_url})")

                except Exception as e:
                    st.error(f"Error: {e}")

            # Timer-based playlists
            st.write("\n")
            st.markdown("### Generate a Playlist for a Specific Duration")
            duration = st.slider("How many minutes do you want your playlist for?", 10, 120, 30)
            if st.button("Generate Duration-Based Playlist"):
                total_duration_ms = duration * 60 * 1000  # Convert minutes to milliseconds
                results = sp.search(q=query, type='track', limit=50)
                current_duration = 0
                st.write(f"### Your {duration}-minute playlist:")
                for track in results['tracks']['items']:
                    if current_duration + track['duration_ms'] > total_duration_ms:
                        break
                    current_duration += track['duration_ms']
                    st.write(f"{track['name']} by {track['artists'][0]['name']}")
                    st.audio(track['preview_url'], format="audio/mp3")
                    
            # Poll for User Preferences
            st.markdown("### What’s Your Bollywood Favorite?")

            # Initialize poll_option in session state
            if "poll_option" not in st.session_state:
                st.session_state.poll_option = None

            # Display radio buttons
            poll_option = st.radio("Pick one:", ["Romantic Songs", "Party Hits", "Classics", "Devotional"])

            # Button logic to update the session state
            if st.button("Submit Poll"):
                st.session_state.poll_option = poll_option
                st.success(f"Great choice! We love {st.session_state.poll_option} too!")
            
            
            
            # Additional feedback box for user suggestions
            st.write("\n")
            st.markdown("### Help Us Improve")
            user_feedback = st.text_area("Do you have any suggestions or feedback for us?", "")
            if st.button("Submit Feedback"):
                if user_feedback.strip():
                    st.success("Thank you for your feedback! We appreciate your input and will use it to improve the app.")
                else:
                    st.error("Please enter some feedback before submitting.")
                    
                    
             # Share links for WhatsApp, LinkedIn, Facebook, and Twitter
            st.write("\n")
            st.markdown("### Share My App with Your Friends")
            st.markdown(f"[Share on WhatsApp](https://api.whatsapp.com/send?text=Check%20out%20this%20Bollywood%20Playlist%20I%20generated!%20{app_url})")
            st.markdown(f"[Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url={app_url})")
            st.markdown(f"[Share on Facebook](https://www.facebook.com/sharer/sharer.php?u={app_url})")
            st.markdown(f"[Share on Twitter](https://twitter.com/intent/tweet?url={app_url})")


            # # Rating system at the end
            st.write("\n")
            st.markdown("### Rate Our App")
            rating = st.radio("How would you rate your experience?", [1, 2, 3, 4, 5], index=4)
            if st.button("Submit Rating"):
                st.success(f"Thank you for rating us {rating} stars! We value your feedback.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
