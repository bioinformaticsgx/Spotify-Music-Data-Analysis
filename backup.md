
## Project Introduction


With the rise of Spotify, iTune, Youtube, etc, streaming services have contributed majority of music industry revenues. And understanding what makes streaming music popular could hugely impact decision-making for music business.

In this project, we conducted data mining for 200000 tracks extracted by Spotify API, in order to analyze the trend of music industry development, and produce a predictive model for track popularity.


<span style="color:red"></span>

## Project Goals

**Analyze the trend of music development over past 20 years.** 

**Establish models to predict track popularity by machine learning algorithms.**




## Data Extraction and Transformation

**Spotify has provided amazing API resources:**

   [Spotify API link](https://developer.spotify.com/web-api/track-endpoints/)

**We randomly extracted data for 10000 tracks per year for the past 20 years.**
```python
url = 'https://api.spotify.com/v1/search?q=year:'+ keywords +'&type=' + search_type +'&offset='+ off +'&limit=' + lim
requests.get(url).json()
```

**Then acquire audio feature data by track_id; Access_token is required for this.**

```python
url = 'https://api.spotify.com/v1/audio-features?ids=' + track_ids
requests.get(url, headers={"Authorization": access_token})
```

**Get items from complicated nested list**
For example,
```python
str = j['tracks']['items']['popularity']
```


**Vectorization of text (e.g. genres or name) by bag-of-words model.**

```python
vectorizer = CountVectorizer(analyzer='word',max_features=100)
WordVec = vectorizer.fit_transform(dicname[name]).toarray().tolist()
```

**Then merge into Pandas Dataframe and start feature engineering.**

Examples of feature engineering:
```python
## Remove NaN
df = df.dropna()

## Convert categorical features into numeric
df['explicit'] = df['explicit'].map( {True: 1, False: 0} ).astype(int) 

## New 'year' feature 
df['year'] = [x.split('-')[0] for x in df['album_release_date']]

## Simplify genre names by choosing the most common word
def reduce_genres(gen):
    genre = re.sub("[^a-zA-Z0-9]"," ",gen).lower().split()
    ...
    mode1 = str(stats.mode(genre)).split('[')[1].split(']')[0]
    return mode1
    
```

**Final cleaned data include:**

⋅⋅⋅1. General numeric features *(e.g. release time, track popularity, artist popularity)*

⋅⋅⋅2. Numeric physical properties *(e.g. loudness, duration)*

⋅⋅⋅3. Vectorized Non-numeric ones *(e.g. genres, album name, artist name)*

**Critical features include:**

⋅⋅⋅A. <span style="color:red">Track Popularity</span>
   
   Major indicator of song popularity and later used for correlation and data training in this project. It reflects "hotness"    by today's music listeners, calculated by total number of plays.

⋅⋅⋅B. <span style="color:red">Year</span>
   
   Used extensively for time-series analysis to demonstrate the trend of music evolution in the project.




## Exploratory Data Analysis and Data Visualization

### General trend of numeric features of songs over past 20 years

   Time-series boxplot for 16 different numeric features. (Purple lines reflect mean) 
   
   We could easily find recent tracks, album and artists are favored by today's listeners.
   
   **Loudness** and **energy** have slightly _increased_; while **valence** and **acousticness** _decreased_.
   
   **Track number** has been _lower_ in recent 10 years, indicating album is _smaller_ nowadays.
   
   
   <p align="center">
   <img src="Figure/modified-boxplot-matrix.png" width="90%"/>
   </p>



### Popularity Analysis by Genres

**First, we define "popular songs" as those with track popularity score ranking at *top 20%* of all tracks.**

**_What genres of tracks are prefered by listeners today?_**
   
Barplot for number of different genres of tracks, either popular or unpopular.

Easily we can see `pop` music dominate music industry; followed by `rock`, `country`, `metal`, `hip`, etc.

These genres are produced in large quantity with certain proportion at top 20%.

Some genres have very small percentage that would become popular, like `classical`, `soul`, `punk` and `jazz`.
   
 
   <p align="center">
   <img src="Figure/modified-bar-plot.png" width="80%"/>
   </p>
 

**_When were these popular tracks of different genres released?_**

We generated year-by-year streamplot, which illustrates time-dependent trend.

The upper panel is for only popular tracks; while lower for total tracks.

Clearly we could see `house` is brandnew genre, not exploading until 2010; followed by `indie`, which started to expand around 2005. `Mexican` music has been always there but only became popular from 2012.

For `rock`, the whole market has dramatically shrinked; while `latin` and `metal` shrinked much slowly.


   
   <p align="center">
   <img src="Figure/stream-pop.png" width="60%"/>
   </p>

   <p align="center">
   <img src="Figure/stream-total.png" width="60%"/>
   </p>



## Predictive Modeling by Gradient Boosting

Before machine learning step, chord diagram generated for correlation between numeric features.

We could see some strong pair correlations, such as **loudness** and **energy**, **loudness** and **acousticness**, **speechiness** and **explicit**.

   <p align="center">
   <img src="Figure/corr-map.png" width="60%"/>
   </p>


We dropped all non-numeric features, and our final dataframe is (215868 tracks X 419 features) for data training.

Various machine learning algorithms have been tried and gradient boosting classifier by *XGBoost* show the best accuracy score. 

|  Algorithms   | CV Accu     | Test Accu    | 
| ------------- |:---------:  |  ---------:  | 
| SVM           |   0.8254    |    0.7911    |
| Random Forest |   0.8534    |    0.8379    |  
| XGBClassifier |   0.8901    |    0.8812    |

(Accu = Accuracy)

We also tuned our parameters for **XGBClassifier**, with optimal as below:

```python
clf  =  XGBClassifier(
        eval_metric = 'accuracy',
        learning_rate = 0.1,
        n_estimators = 100,
        max_depth = 3,
        subsample = 0.9,
        colsample_bytree = 0.9,
        silent = False )
 ```

**_Which features are most predictive?_**

We converted the importance-weight list into wordle.

We could see **album popularity** dominates all other features, followed by **track number**, **year** and **duration**.
```python
importance = clf.feature_importances_
```
 
   <p align="center">
   <img src="Figure/wordle.png" width="60%"/>
   </p>
 

Since album popularity is quite similar and highly correlated to track popularity, we removed this feature and trained data again, our model still could achieve a high accuracy around 0.85.

## Summary and Discussion
Here's the insight we've learned about music trend based on big data analysis:

1.**Recent music is still largely favored**, indicating customers' music "psychology" leaning towards trying novel tracks. 

2.Some physical features of music with high popularity have slightly changed, including **energy/loudness** slightly increased, and **valence** slightly decreased. It'll be interesting to see if such small trend will continue.

Also, track number has been lower, indicating **smaller album** in music industry nowadays.

3.`Pop music` undoubtedly dominates the music market, in both production quantity and popularity quantity; while some other genres like `soul` and `classical` have almost zero percentage of being top 20% popular, most probably because they are minority music favored by a small population.

4.Important change: `indie` and `house` are brandnew genres and novel trend! While `rock`, which used to be prosperous, has now shrinked dramatically. 

5.There's basically NO correlation between track popularity and numeric physical features; yet, there's strong correlation among track, album and artist popularity, which is not suprising; and there's also slight correlation between track popularity and track number, which is also not surprising, as most popular songs are usually the first in the album.

6.We established a machine learning model, which could successfully predict track popularity. Ensemble methods are extremely good for analyzing multi-feature data with non-linear relationship, plus XGBoost has recently dominated data science field with extreme superiority, so we choose XGBClassifier to train our data, and achieved very excellent accuracy score for both cross-validated and test data. The best predictive feature is album popularity.

In general, we've analyzed Spotify API data, and have discovered some very interesting trends for today's music market, and also provide a high-quality model for track popularity prediction. Hopefully this could provide some insight into today and future's music market and industry.
