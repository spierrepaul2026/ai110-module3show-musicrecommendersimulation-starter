# 🎧 Model Card: Music Recommender Simulation

## Model Name

**VibeMatch 1.0** — a simple music recommender that matches songs to a listener's vibe based on genre, mood, and energy level.

---

## Goal / Task

VibeMatch tries to suggest the songs a listener will most enjoy given their stated taste. You tell it your favorite genre, your favorite mood, and the energy level you're in the mood for, and it predicts which songs from the catalog best fit that vibe. It then ranks every song and hands back the top five, along with a short reason for each pick. It isn't predicting a numeric rating or the "next song played" — it's ranking the whole catalog by how well each song matches your profile.

---

## Data Used

The catalog is a small hand-made set of **20 songs**, stored in `data/songs.csv`. Each song has a title, artist, genre, mood, and five numeric features: energy, tempo (BPM), valence, danceability, and acousticness.

For such a small set it covers a wide spread of genres — pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop, classical, electronic, folk, metal, r&b, reggae, country, blues, and funk (lofi is the only genre with more than one song). Moods are varied too: happy, chill, intense, relaxed, moody, focused, energetic, melancholic, and more.

**Limits:** the dataset is tiny, and most genres have only one song, so a listener quickly runs out of same-genre options. There's no world/non-Western music, no release year or era, no lyrics or language, and no popularity signal — so whole dimensions of musical taste are simply missing.

---

## Algorithm Summary

Think of it like a points contest. Every song earns points based on how well it matches what you said you like, and the highest-scoring songs rise to the top.

- If a song is in your **favorite genre**, it earns some points.
- If its **mood** matches yours, it earns a few more.
- The closer a song's **energy** is to the energy you asked for, the more points it earns — a perfect energy match earns a lot, while one that's far off earns almost nothing.

Add up the points, sort every song from most to fewest, and return the top five. I also tuned the weights so **energy counts twice as much** as the starter version and **genre counts half as much**, which makes the overall "feel" matter more than the exact genre label.

---

## Observed Behavior / Biases

The recommender's scoring function optimizes entirely for similarity to the user's existing profile — every term rewards matching their stated genre, mood, or target energy (score_song), with no term anywhere for novelty, diversity, or exploration. Because recommend is a purely deterministic sort with no randomization, the same profile returns the identical list every single session, so nothing outside the top-k can ever surface. This is a textbook filter bubble: the system only ever exploits known preferences and never explores. Over repeated use it keeps narrowing the user to the slice of the catalog closest to where they started, and it compounds because the exact-string genre check even walls them off from adjacent tastes (a pop user gets zero genre credit for indie pop). The fix is to add an exploration or diversity signal that intentionally surfaces off-profile picks.

---

## Evaluation Process

Yes i tested very vasty different profiles and it seems the recmmender ended exactly it is suppose. Fortunatly it seems to catch smaller issues i didn't think of, like deterministic ranking, same input, same output, forever

For the profiles
profiles = [
        {"genre": "lofi", "mood": "chill", "energy": 0.3},
        {"genre": "pop", "mood": "happy", "energy": 0.8},
        {"genre": "rock", "mood": "energetic", "energy": 0.9},
    ]
As we can see the first profile goes with more softer slower songs being laid back shifting to low BPM msuic

The second profile wants more happy upbeat music, not too much since it seems a happy good pace music wanted

The third profile wants more fast pace heart bumping music.

No numeric metrics were used; evaluation was based on whether the results matched intuition.

---

## Intended Use and Non-Intended Use

**Intended use:** classroom exploration. VibeMatch is a teaching tool for showing how a scoring-based recommender works, how changing feature weights changes results, and where recommenders develop biases like filter bubbles. It assumes the user can describe their taste up front and that those preferences stay fixed for a session.

**Non-intended use:** it should **not** be used as a real music service or for any real decision-making. With only 20 songs, no learning from listening history, and known diversity bias, it isn't suitable for real users, for comparing artists, or for any setting where fair or comprehensive recommendations matter.

---

## Ideas for Improvement

1. **Add an exploration / diversity signal.** Reserve a slot (or add a small off-profile boost) so the top results aren't always the closest match to existing taste — this directly attacks the filter-bubble problem.
2. **Use the features that are currently ignored.** The data already has valence, tempo, danceability, and acousticness, and the user profile has a `likes_acoustic` flag that's never used. Scoring on more of these would give richer, more personalized matches.
3. **Make genre matching smarter.** Replace the exact-string genre check with a genre-similarity map (so `pop` gets partial credit for `indie pop`), and add an artist-diversity cap so one artist can't fill multiple top slots.

---

## Personal Reflection

Building this was a process that kidna surpised me with how much AI could help with but needs to be gudided with out logic to help develop the systems and truly build up the code over time.
