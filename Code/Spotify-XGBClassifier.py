import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model
from sklearn import svm
import seaborn as sns
from xgboost import XGBClassifier
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.grid_search import GridSearchCV
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer



def bagwords (df):
       
    
    listname = ['artist_genres', 'artist_name', 'album_name', 'song_name']
    
  
    dicname = {name: [] for name in listname}
    dicname['song_id'] = []
    
    listid = []
    
    dicdf = {}
    vol = {}
    print(df.shape)
 
        
    for name in listname:
        
        for idx in range(df[name].size):
            
            l = df[name][idx]
          
            r = names_to_words(l)
            
            dicname[name].append(r) 
            
      
            
        
        vectorizer = CountVectorizer(analyzer='word',max_features=30)
        feature = vectorizer.fit_transform(dicname[name]).toarray().tolist()
        vol[name] = vectorizer.get_feature_names()
        
        
        dicdf[name] = pd.DataFrame({name: feature}) 
        
        dicdf[name] = dicdf[name][name].apply(pd.Series)
        ### dicdf[name] already lose column tag name, but change into 0 1 2 
        
        l = len(dicdf[name].columns)
        
        dicdf[name].columns = [(name + '_' +vol[name][x]) for x in range(l)]
        
        print('good')
     
   
    
    for idx in range(df['song_id'].size):
        sid = df['song_id'][idx]
        listid.append(sid)
       
            
        dicdf['song_id'] = pd.DataFrame({'song_id':listid}) 

        
            
            
        
    result = pd.concat(dicdf.values(), axis =1)
    
    return result
    


def names_to_words(names):
    words = re.sub("[^a-zA-Z0-9]"," ",names).lower().split()
    
    words = [i for i in words if i not in set(stopwords.words("english"))]
    ## Need join as string for countvectorizer!
    return (" ".join(words))

def reduce_genres(gen):
    genre = re.sub("[^a-zA-Z0-9]"," ",gen).lower().split()
    genre = [i for i in genre if i not in set(stopwords.words("english"))]
    mode1 = str(stats.mode(genre)).split('[')[1].split(']')[0]
    return mode1
    

print('Start!')

## general dataframe transform
df = pd.read_csv('/Users/Guang/bigdi.csv', sep='\t')

df = df.dropna()

df = df.drop(['album_genres'],axis =1 )


df['explicit'] = df['explicit'].map( {True: 1, False: 0} ).astype(int) 

z = df['popularity'].quantile(0.8)
df['class'] = df['popularity'].apply(lambda x: 1 if x >= z else 0)

df = df[(df.astype(str)['artist_genres'] != '[]')].reset_index()

df['reduced_genres'] = df['artist_genres'].apply(lambda x: reduce_genres(x))

df['year'] = [x.split('-')[0] for x in df['album_release_date']]

#df.to_csv('bigdiwithyear.csv', sep='\t')


### bag of words: text items vectorization

df1 = bagwords( df )

df = df.merge(df1, on='song_id', how='outer')

df.shape


df = df.drop(['Unnamed: 0', 'song_id', 'artist_id','album_id','song_name',
            'artist_name','album_name','uri', 'type', 'track_href',
            'analysis_url','artist_genres','album_release_date','popularity',
            'class','index','reduced_genres'],axis=1)   

#df.to_csv('bigdichorddiagram.csv', sep='\t')

#df[(df['popularity'] >= df['popularity'].quantile(0.8))]['loudness'].mean()#value_counts(dropna=False)



#training
Y = df['class'].values

X = df.values     

X_train, X_test, Y_train, Y_test = train_test_split(X, Y)


#clf = XGBClassifier()
#clf = RandomForestRegressor(n_estimators=200,max_features=18)

clf  =  XGBClassifier(
        eval_metric = 'accuracy',
        learning_rate = 0.1,
        n_estimators = 100,
        max_depth = 3,
        subsample = 0.9,
        colsample_bytree = 0.9,
        silent = False
        )

#clf = RandomForestClassifier(n_estimators=100,max_features=17)  

#clf = svm.SVC()        
        
clf.fit(X_train,Y_train)

print('good')

importance = clf.feature_importances_

dfi = pd.DataFrame(importance, index=df.columns, columns=["Importance"])
dfi = dfi.sort_values(['Importance'],ascending=False)
print(dfi)
#dfi.plot(kind='bar',color='Purple')



Ascores_Train = cross_val_score(clf, X_train, Y_train, cv=5)
Ascores_Test = clf.score(X_test,Y_test)


print('lala')
print(Ascores_Train.mean()) 
print(Ascores_Train.std()) 
print(Ascores_Test) 




# Predicted_Train = cross_val_predict(clf, X_train, Y_train, cv=5)
# MSE_Train = mean_squared_error(Y_train, Predicted_Train)
# print('MSE for training data is:')
# print(MSE_Train)


# Predicted_Test = clf.predict(X_test)
# MSE_Test = mean_squared_error(Y_test, Predicted_Test)
# print('MSE for test data is:')
# print(MSE_Test)
