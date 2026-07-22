import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Scores a Song against a UserProfile, returning (score, reasons)."""
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        return score_song(prefs, {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
        })

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs for the given user profile."""
        # Edge cases: non-positive k and empty catalog both yield no picks.
        if k <= 0 or not self.songs:
            return []

        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable reason the song was recommended."""
        _, reasons = self._score(user, song)
        # Edge case: nothing matched — still return a non-empty explanation.
        return "; ".join(reasons) if reasons else "no strong matches, but a reasonable pick"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    numeric_fields = {
        "id": int,
        "energy": float,
        "tempo_bpm": float,
        "valence": float,
        "danceability": float,
        "acousticness": float,
    }

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Edge case: empty file or missing header row.
        if reader.fieldnames is None:
            return songs

        for line_no, row in enumerate(reader, start=2):  # header is line 1
            song = dict(row)
            for field, cast in numeric_fields.items():
                raw = song.get(field)
                # Edge case: missing column or blank/whitespace-only value.
                if raw is None or str(raw).strip() == "":
                    raise ValueError(
                        f"Missing value for '{field}' on line {line_no} of {csv_path}"
                    )
                try:
                    song[field] = cast(raw)
                except ValueError:
                    # Edge case: non-numeric text where a number is expected.
                    raise ValueError(
                        f"Invalid {field} value {raw!r} on line {line_no} of {csv_path}"
                    )
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    # Categorical match: genre (strongest taste signal)
    # Edge case: song may be missing a genre/mood field — use .get, not [].
    song_genre = song.get("genre")
    if song_genre is not None and song_genre == user_prefs.get("genre"):
        score += 1.0  # halved from 2.0
        reasons.append(f"matches your favorite genre ({song_genre})")

    # Categorical match: mood (secondary signal)
    song_mood = song.get("mood")
    if song_mood is not None and song_mood == user_prefs.get("mood"):
        score += 1.5
        reasons.append(f"matches your mood ({song_mood})")

    # Numerical feature: energy closeness (partial credit for being close)
    if "energy" in user_prefs and "energy" in song:
        energy_diff = abs(user_prefs["energy"] - song["energy"])
        # Edge case: out-of-range values could push this negative; floor at 0.
        energy_score = max(0.0, (1 - energy_diff) * 3.0)  # doubled from 1.5
        score += energy_score
        if energy_diff <= 0.1:
            reasons.append(f"energy ({song['energy']:.2f}) closely matches yours")

    return score, reasons

def _score_with_explanation(user_prefs: Dict, song: Dict) -> Tuple[Dict, float, str]:
    """Scores a song and packages it with a human-readable explanation."""
    score, reasons = score_song(user_prefs, song)
    explanation = "; ".join(reasons) if reasons else "no strong matches, but a reasonable pick"
    return (song, score, explanation)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Edge case: non-positive k and empty catalog both yield no picks.
    if k <= 0 or not songs:
        return []

    scored = [_score_with_explanation(user_prefs, song) for song in songs]
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
