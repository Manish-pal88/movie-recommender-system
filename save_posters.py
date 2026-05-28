import requests
import pickle
import pandas as pd
import time

API_KEY = "3bf17b085b1956b082db3c53432344e1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movies['movie_id'] = movies['movie_id'].astype(int)

print(f"Total movies: {len(movies)}")
poster_map = {}

for idx, row in movies.iterrows():
    try:
        url = f"https://api.themoviedb.org/3/movie/{row['movie_id']}?api_key={API_KEY}"
        r = requests.get(url, headers=headers, timeout=15)
        data = r.json()
        poster_path = data.get('poster_path')

        if poster_path:
            poster_map[row['movie_id']] = f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            poster_map[row['movie_id']] = "https://placehold.co/500x750?text=No+Poster"

        print(f"✅ {idx+1}/{len(movies)} - {row['title']}")
        time.sleep(0.5)

    except Exception as e:
        poster_map[row['movie_id']] = "https://placehold.co/500x750?text=No+Poster"
        print(f"❌ {idx+1}/{len(movies)} - {row['title']} - {type(e).__name__}: {e}")
        time.sleep(1)

pickle.dump(poster_map, open('poster_map.pkl', 'wb'))
print(f"\n✅ Done! Saved {len(poster_map)} posters to poster_map.pkl")