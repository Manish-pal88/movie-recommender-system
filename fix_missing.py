import requests
import pickle
import pandas as pd
import time

API_KEY = "3bf17b085b1956b082db3c53432344e1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

# Load existing poster_map
poster_map = pickle.load(open('poster_map.pkl', 'rb'))

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movies['movie_id'] = movies['movie_id'].astype(int)

# ✅ Only fix the ones that failed or have placeholder
missing = {k: v for k, v in poster_map.items()
           if "placehold" in str(v) or "No+Poster" in str(v)}

print(f"Found {len(missing)} missing posters — fixing now...\n")

fixed = 0
for movie_id, _ in missing.items():
    # Get movie title for display
    title_row = movies[movies['movie_id'] == movie_id]
    title = title_row['title'].values[0] if len(title_row) > 0 else "Unknown"

    for attempt in range(3):  # Try 3 times each
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
            r = requests.get(url, headers=headers, timeout=20)  # longer timeout
            data = r.json()
            poster_path = data.get('poster_path')

            if poster_path:
                poster_map[movie_id] = f"https://image.tmdb.org/t/p/w500{poster_path}"
                print(f"✅ Fixed: {title} (ID: {movie_id})")
                fixed += 1
            else:
                print(f"⚠️ No poster exists on TMDB for: {title} (ID: {movie_id})")
            break  # success or no poster, stop retrying

        except Exception as e:
            print(f"❌ Attempt {attempt + 1}/3 failed for {title}: {type(e).__name__}")
            time.sleep(2)  # wait longer before retry
            continue

    time.sleep(1)  # gap between movies

# Save updated poster_map
pickle.dump(poster_map, open('poster_map.pkl', 'wb'))
print(f"\n✅ Done! Fixed {fixed} posters — poster_map.pkl updated!")