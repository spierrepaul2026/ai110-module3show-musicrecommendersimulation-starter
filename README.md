# 🎵 VibeMatch: Music Recommender

VibeMatch recommends songs that fit a listener's vibe. You give it a favorite genre, a mood, and the energy level you want, and it scores all 20 songs in the catalog, ranks them, and returns the top 5 with a plain-English reason for each pick.

**Built by Stephen Pierre-Paul** for CodePath AI110: Foundations of AI Engineering. See the [model card](model_card.md) for how it behaves, what data it uses, and where it falls short.

---

## How it works

1. `load_songs()` reads `data/songs.csv` and converts each numeric column to the right type, with errors for bad values.
2. `score_song()` gives every song points against the listener's profile:

| Signal | Points |
| --- | --- |
| Genre matches | +1.0 |
| Mood matches | +1.5 |
| Energy closeness | up to +3.0, scaled by how close the song's energy is to the target |

3. `recommend_songs()` sorts every song by score and keeps the top 5.
4. Each pick comes with the reasons it scored well, such as "matches your mood (chill)."

There is also an object-oriented version in `src/recommender.py` built on `Song`, `UserProfile`, and `Recommender` classes.

---

## Run it

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python src/main.py   # run the recommender for three sample listeners
pytest               # run the tests
```

---

## Sample output

```
================================================
  TOP RECOMMENDATIONS — lofi / chill / energy 0.3
================================================

1. Library Rain — Paper Lanterns
   Score: 5.35
   Reasons:
     • matches your favorite genre (lofi)
     • matches your mood (chill)
     • energy (0.35) closely matches yours

2. Midnight Coding — LoRoom
   Score: 5.14
   Reasons:
     • matches your favorite genre (lofi)
     • matches your mood (chill)

3. Spacewalk Thoughts — Orbit Bloom
   Score: 4.44
   Reasons:
     • matches your mood (chill)
     • energy (0.28) closely matches yours
```

---

## Experiments You Tried

**Reweighting energy and genre.** I doubled the weight on energy (from 1.5 to 3.0) and halved the weight on genre (from 2.0 to 1.0), so the overall "feel" of a song matters more than its genre label. This visibly changed the rankings. For the `rock / energetic / 0.9` profile, the one actual rock song (*Storm Runner*) dropped to #3, and two non-rock but high-energy tracks (*Neon Overdrive*, *Groove Machine*) rose above it. For `pop / happy / 0.8`, *Rooftop Lights* (an `indie pop` song) climbed to #2, beating pop songs that only matched on genre. So genre became a weak tiebreaker and energy closeness became the strongest signal.

**Testing different user types.** I ran three very different profiles — `lofi/chill/0.3`, `pop/happy/0.8`, and `rock/energetic/0.9`. Each one returned sensible picks: the low-energy profile got calm, slow songs; the pop profile got upbeat happy songs; the rock profile got fast, high-energy tracks. Running the same profile more than once always returned the exact same list, which is how I noticed the deterministic-ranking limitation (same input, same output, every time).

**What I did not change.** I kept the scoring on just genre, mood, and energy — I did not add tempo or valence to the score. Adding those is listed as future work in the model card.

---

## Limitations and Risks

- **Tiny catalog.** It only ranks 20 songs, and most genres have just one song, so a listener runs out of same-genre options almost immediately.
- **Filter bubble / no exploration.** The score only rewards similarity to what the user already likes — there's no term for novelty or diversity. It never surfaces anything outside the user's stated taste.
- **Deterministic ranking.** The same profile returns the identical list every session, so the user is shown the same narrow slice over and over with no discovery.
- **Exact-string genre matching.** A `pop` user gets zero genre credit for `indie pop`, so the model walls users off from tastes that are actually very close.
- **Ignores most of the data.** Only genre, mood, and energy are scored. Valence, tempo, danceability, and acousticness are loaded but never used, and the profile's `likes_acoustic` flag is ignored entirely.
- **Shallow understanding of music.** It doesn't understand lyrics, language, era/release year, or popularity — just a few numeric features and category labels.
- **Energy now dominates.** After the reweight, energy closeness is the strongest signal, so it can over-favor songs with the "right" energy even when the genre or vibe is a poor fit.

More detail is in the [model card](model_card.md).

---

