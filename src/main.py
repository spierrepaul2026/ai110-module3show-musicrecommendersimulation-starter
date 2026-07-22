"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Three distinct example profiles
    profiles = [
        {"genre": "lofi", "mood": "chill", "energy": 0.3},
        {"genre": "pop", "mood": "happy", "energy": 0.8},
        {"genre": "rock", "mood": "energetic", "energy": 0.9},
    ]

    for user_prefs in profiles:
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print()
        print("=" * 48)
        print(f"  TOP RECOMMENDATIONS — {user_prefs['genre']} / "
              f"{user_prefs['mood']} / energy {user_prefs['energy']}")
        print("=" * 48)

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n{rank}. {song['title']} — {song['artist']}")
            print(f"   Score: {score:.2f}")
            print("   Reasons:")
            for reason in explanation.split("; "):
                print(f"     • {reason}")

        print()
        print("=" * 48)


if __name__ == "__main__":
    main()
