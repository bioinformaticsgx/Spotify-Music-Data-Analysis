
## Project introduction

In this project, we conducted data mining for 200000 tracks over the past 20 years, in order to analyze the trend of music industry development, and produce a predictive model for track popularity. 

## The purposes:

**1. Analyze the trend of music development over past 20 years. 

   For example:
   *Music has generally been louder than before? 
   Duration is longer than before? 
   What novel types of music have evolved popular in the past five years?


**2. Establish models to predict track popularity by machine learning algorithms.

 
   *What features are associated with popularity?
   What makes a song popular?




## Data Snippet

The information was pulled out from Spotify API and include: 
1. General numeric features (e.g. release time, popularity, artist popularity), 
2. Numeric physical properties (e.g. loudness, duration) 
3. Non-numeric ones (e.g. genres, album name, artist name)

One critical target variable is `track popularity`, which we used as indicator of popularity. It's provided by Spotify API, and calcuated by algorithms based on total number of plays the track has had and how recent those plays are.



### General pipeline and techniques:
```   
1. API extract and data snippet
2. Data clean and transform
3. Data visualization
4. Machine learning and modeling
```

### Result
### General trend of music over past 20 years

1. First, regardless of popularity, time series barplot for 16 different numeric features.
   Only loudness slightly change
   
   <p align="center">
   <img src="Figure/modified-boxplot-matrix.png" width="120%"/>
   </p>



### Popularity Analysis
### Association between track popularity and different numeric features.

1. What types of music do we listen these days?
   
   Barplot for number of different genres of tracks which are either popular or unpopular
   
   We define "popular songs" as those with track popularity score ranking at top 20 
 
   <p align="center">
   <img src="Figure/barplot-genres.png" width="80%"/>
   </p>
 
 


2. Barplot for number of different genres of tracks for the past four years. 

   
   <p align="center">
   <img src="Figure/stream-pop.png" width="80%"/>
   </p>

   <p align="center">
   <img src="Figure/stream-total.png" width="80%"/>
   </p>

3. Time-series analysis of popularity for different genres of music.

   <p align="center">
   <img src="Figure/year-type-popularity.png" width="80%"/>
   </p>



4. Which features are associated with track popularity? 
   Scatterplot between track popularity and features.
 
   <p align="center">
   <img src="Figure/modified-scatterplot-matrix.png" width="100%"/>
   </p>


5. Album popularity and artist popularity are two strong features linearly associated.
 
   <p align="center">
   <img src="Figure/album-artist-track.png" width="50%"/>
   </p>



### Modeling: Random Forest Regression
```
Before ML, correlation map for different features
```
   <p align="center">
   <img src="Figure/corr-map.png" width="80%"/>
   </p>

### Modeling: Random Forest Regression
```
1. xgbclassifier tune parameters
2. Which features are most predictive?
----MAKE wordle!
```

We define "popular songs" as those with track popularity score ranking at top 20 
 
   <p align="center">
   <img src="Figure/wordle.png" width="80%"/>
   </p>
 
