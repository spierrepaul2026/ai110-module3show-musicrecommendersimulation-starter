# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders
My understanding of the real-world recommdenations is focusing on things in commmon. For example i believe it is important to focus on is the energy, valence and also tempo_BPM. My version will focus on energy valence and tempo_BPM (even though claude thinks BPM isn't as important) So we will make it a socre system then compare it from the person socre to the song score and based on that difference we will determine if it matches well with the person.


Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

songs.csv and user_prefs go in. load_songs() turns the CSV into song data. recommend_songs() loops through every song. score_song() scores each one against user_prefs. The list gets sorted, top k kept main.py prints the results.

The user profile store infomation of the users go to genres, the level of intense they like and how fast they like it.

The recommender compute a core by a grading system

Category	Max points	Share
genre	40	~40%
mood	25	~25%
energy	25	~25%
tempo_bpm	10	~10%
Core total	100	100%


You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```


Loaded songs: 20

================================================
  TOP RECOMMENDATIONS
================================================

1. Sunrise City — Neon Echo
   Score: 4.97
   Reasons:
     • matches your favorite genre (pop)
     • matches your mood (happy)
     • energy (0.82) closely matches yours

2. Gym Hero — Max Pulse
   Score: 3.30
   Reasons:
     • matches your favorite genre (pop)

3. Rooftop Lights — Indigo Parade
   Score: 2.94
   Reasons:
     • matches your mood (happy)
     • energy (0.76) closely matches yours

4. Groove Machine — Funk Factory
   Score: 1.50
   Reasons:
     • energy (0.80) closely matches yours

5. Night Drive Loop — Neon Echo
   Score: 1.42
   Reasons:
     • energy (0.75) closely matches yours


**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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

You will go deeper on this in your model card.

Loaded songs: 20

================================================
  TOP RECOMMENDATIONS — lofi / chill / energy 0.3
================================================

1. Library Rain — Paper Lanterns
   Score: 4.92
   Reasons:
     • matches your favorite genre (lofi)
     • matches your mood (chill)
     • energy (0.35) closely matches yours

2. Midnight Coding — LoRoom
   Score: 4.82
   Reasons:
     • matches your favorite genre (lofi)
     • matches your mood (chill)

3. Focus Flow — LoRoom
   Score: 3.35
   Reasons:
     • matches your favorite genre (lofi)

4. Spacewalk Thoughts — Orbit Bloom
   Score: 2.97
   Reasons:
     • matches your mood (chill)
     • energy (0.28) closely matches yours

5. Velvet Sorrow — Aria Bloom
   Score: 1.50
   Reasons:
     • energy (0.30) closely matches yours

================================================

================================================
  TOP RECOMMENDATIONS — pop / happy / energy 0.8
================================================

1. Sunrise City — Neon Echo
   Score: 4.97
   Reasons:
     • matches your favorite genre (pop)
     • matches your mood (happy)
     • energy (0.82) closely matches yours

2. Gym Hero — Max Pulse
   Score: 3.30
   Reasons:
     • matches your favorite genre (pop)

3. Rooftop Lights — Indigo Parade
   Score: 2.94
   Reasons:
     • matches your mood (happy)
     • energy (0.76) closely matches yours

4. Groove Machine — Funk Factory
   Score: 1.50
   Reasons:
     • energy (0.80) closely matches yours

5. Night Drive Loop — Neon Echo
   Score: 1.42
   Reasons:
     • energy (0.75) closely matches yours

================================================

================================================
  TOP RECOMMENDATIONS — rock / energetic / energy 0.9
================================================

1. Storm Runner — Voltline
   Score: 3.48
   Reasons:
     • matches your favorite genre (rock)
     • energy (0.91) closely matches yours

2. Neon Overdrive — Pulse Grid
   Score: 2.92
   Reasons:
     • matches your mood (energetic)
     • energy (0.95) closely matches yours

3. Groove Machine — Funk Factory
   Score: 2.85
   Reasons:
     • matches your mood (energetic)
     • energy (0.80) closely matches yours

4. Gym Hero — Max Pulse
   Score: 1.46
   Reasons:
     • energy (0.93) closely matches yours

5. Iron Veins — Sledgehammer
   Score: 1.38
   Reasons:
     • energy (0.98) closely matches yours



     ---------------



     Changed version with double energy half genre 

     Loaded songs: 20

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

4. Focus Flow — LoRoom
   Score: 3.70
   Reasons:
     • matches your favorite genre (lofi)

5. Velvet Sorrow — Aria Bloom
   Score: 3.00
   Reasons:
     • energy (0.30) closely matches yours

================================================

================================================
  TOP RECOMMENDATIONS — pop / happy / energy 0.8
================================================

1. Sunrise City — Neon Echo
   Score: 5.44
   Reasons:
     • matches your favorite genre (pop)
     • matches your mood (happy)
     • energy (0.82) closely matches yours

2. Rooftop Lights — Indigo Parade
   Score: 4.38
   Reasons:
     • matches your mood (happy)
     • energy (0.76) closely matches yours

3. Gym Hero — Max Pulse
   Score: 3.61
   Reasons:
     • matches your favorite genre (pop)

4. Groove Machine — Funk Factory
   Score: 3.00
   Reasons:
     • energy (0.80) closely matches yours

5. Night Drive Loop — Neon Echo
   Score: 2.85
   Reasons:
     • energy (0.75) closely matches yours

================================================

================================================
  TOP RECOMMENDATIONS — rock / energetic / energy 0.9
================================================

1. Neon Overdrive — Pulse Grid
   Score: 4.35
   Reasons:
     • matches your mood (energetic)
     • energy (0.95) closely matches yours

2. Groove Machine — Funk Factory
   Score: 4.20
   Reasons:
     • matches your mood (energetic)
     • energy (0.80) closely matches yours

3. Storm Runner — Voltline
   Score: 3.97
   Reasons:
     • matches your favorite genre (rock)
     • energy (0.91) closely matches yours

4. Gym Hero — Max Pulse
   Score: 2.91
   Reasons:
     • energy (0.93) closely matches yours

5. Iron Veins — Sledgehammer
   Score: 2.76
   Reasons:
     • energy (0.98) closely matches yours


---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this




Implement CLI-first music recommender simulation

Build out the core recommendation pipeline in recommender.py and wire it
into a working CLI-first simulation via main.py.

- load_songs: read data/songs.csv with the csv module, casting numeric
  columns (id, energy, tempo_bpm, valence, danceability, acousticness)
  to their proper types
- score_song: score a song against user prefs — +2.0 genre match,
  +1.5 mood match, and (1 - |energy diff|) * 1.5 for energy closeness,
  collecting human-readable reasons
- recommend_songs: score all songs and return the top k sorted highest
  to lowest, using a helper + list comprehension for a clean, idiomatic
  implementation
- main.py: run the full simulation end-to-end from the CLI, printing a
  clean ranked layout with title, artist, score, and per-song reasons
- add one-line docstrings to the Recommender stub methods

Verified working: `python3 src/main.py` loads 20 songs and prints the
top 5 recommendations with explanations.

