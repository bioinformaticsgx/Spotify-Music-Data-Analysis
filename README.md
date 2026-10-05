# Spotify Music Data Analysis

Data mining and machine learning on ~200,000 Spotify tracks (1995–2017) to study how popular music changed over two decades and to predict whether a track lands in the top 20% of popularity.

## Goals

- Describe trends in audio features, genres, and catalog structure over ~20 years.
- Build a classifier that predicts **popular** vs **not popular** tracks from metadata, audio features, and bag-of-words text.

Popular is defined as track popularity at or above the **80th percentile**.

## Repository layout

```
Code/
  Spotify_Extract_API_Data.py   # Pull yearly track samples + audio/artist/album fields from the Spotify Web API
  Spotify-XGBClassifier.py      # Clean data, vectorize text, train XGBClassifier, report accuracy and feature importance
plot.r                          # ggplot2 / circlize snippets used for EDA figures
LICENSE                         # MIT
```

Figures referenced in the original analysis (boxplots, streamgraphs, correlation maps, and so on) lived under `Figure/`. Recreate them with `plot.r` and your cleaned CSV if those images are not in the clone.

## Pipeline

1. **Extract** — For each year from 1995 to 2017, search tracks (`q=year:YYYY`), then batch-fetch audio features, artists, and albums. Write one tab-separated CSV per year.
2. **Transform** — Drop missing rows, map `explicit` to 0/1, derive `year` from album release date, reduce genre lists to a modal token, and bag-of-words vectorize `artist_genres`, `artist_name`, `album_name`, and `song_name` (top 30 tokens each, English stopwords removed).
3. **Model** — Binary `class` from popularity quantile. Train/test split, 5-fold CV on the training set, compare SVM, random forest, and XGBoost.

Final modeling table in the original run: **215,868 tracks × 419 features**.

## Requirements

Python 3 with:

- `pandas`, `numpy`, `scipy`
- `requests`
- `scikit-learn`
- `xgboost`
- `nltk` (download `stopwords`)
- `matplotlib`, `seaborn` (optional plotting)

R (optional, for `plot.r`): `ggplot2`, `circlize`.

The extraction script uses `pandas` for merges but does not import it at the top of the file; add `import pandas as pd` before running it.

`Spotify-XGBClassifier.py` uses older sklearn paths (`sklearn.cross_validation`, `sklearn.grid_search`). On current scikit-learn, switch those to `sklearn.model_selection`.

## Spotify API setup

You need a [Spotify Developer](https://developer.spotify.com/documentation/web-api) app and a valid **OAuth access token**. Search, audio-features, artists, and albums endpoints all require authorization today.

Do **not** commit tokens. Load them from an environment variable, for example:

```python
import os
access_token = "Bearer " + os.environ["SPOTIFY_ACCESS_TOKEN"]
```

Pass that value in the `Authorization` header on every request (not only audio features).

Rate-limit politely; the extractor already sleeps ~0.3s between batch calls.

## How to run

**1. Extract yearly CSVs** (after adding pandas import, auth headers, and a writable output path):

```bash
python Code/Spotify_Extract_API_Data.py
```

This writes files named `{year}.csv` (tab-separated) in the working directory.

**2. Combine years** into one table (column layout must match the extractor: popularity, IDs, names, audio features, artist genres/popularity, album fields, etc.).

**3. Classify** — Point the CSV path in `Spotify-XGBClassifier.py` at your combined file (it currently hardcodes a local path), then:

```bash
python Code/Spotify-XGBClassifier.py
```

The script prints feature importances, mean ± std of CV accuracy on the train split, and hold-out test accuracy.

Example XGBoost settings used in the project:

```python
XGBClassifier(
    eval_metric="accuracy",
    learning_rate=0.1,
    n_estimators=100,
    max_depth=3,
    subsample=0.9,
    colsample_bytree=0.9,
)
```

## Reported model comparison

| Algorithm       | CV accuracy | Test accuracy |
| --------------- | ----------- | ------------- |
| SVM             | 0.8254      | 0.7911        |
| Random forest   | 0.8534      | 0.8379        |
| XGBClassifier   | 0.8901      | 0.8812        |

Strongest predictor was **album popularity**, then track number, year, and duration. Dropping album popularity still reached about **0.85** accuracy.

## Findings (summary)

- Recent releases, albums, and artists score higher with today’s listeners; catalogs lean toward newer material.
- **Loudness** and **energy** ticked up; **valence** and **acousticness** ticked down. Albums got **shorter** (lower typical track numbers).
- **Pop** dominates volume and hits. **House** and **indie** grew as recent genres; **rock** share contracted.
- Raw audio features barely correlate with track popularity; **album** and **artist** popularity do. Loudness↔energy, loudness↔acousticness, and speechiness↔explicit are the notable audio/metadata correlations.

Spotify’s API does not expose listener location, so geographic taste is out of scope.

## License

MIT. See [LICENSE](LICENSE).
