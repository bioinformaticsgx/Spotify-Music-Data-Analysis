import requests
import csv
import time
import json
import sys
import imp
imp.reload(sys)


print('start..')


def main():
    
    queries = ['1995','1996','1997','1998','1999','2000','2001',
              '2002','2003','2004','2005','2006','2007','2008',
              '2009','2010','2011','2012','2013','2014','2015','2016','2017']
              
    #queries = ['2017']
    # Query and request from API are different!
    # Number of track query need to make
    num_tracks_per_query = 10000

    for query in queries:
        
        ltrack = []
        song_ids = []
        artist_ids = []
        album_ids = []
        
        audioF = []
        artist_data = []
        album_data = []

        
        col1 = [   'popularity',
                   'song_id',     'artist_id',     'album_id', 
                   'song_name',   'artist_name',   'album_name', 
                   'explicit',    'disc_number',   'track_number']
        
        
        col2 =  [  'song_id', 'uri',
                   'tempo', 'type',
                   'key', 'loudness',
                   'mode', 'speechiness',
                   'liveness', 'valence',
                   'danceability', 'energy',
                   'track_href', 'analysis_url',
                   'duration_ms', 'time_signature',
                   'acousticness', 'instrumentalness' ]
        
        col3 =  [  'artist_id',  'artist_genres',  'artist_popularity']
        
        col4 =  [  'album_id',  'album_genres',   'album_popularity',  'album_release_date']
        
        n = 0 
        idx = 0
        
        while idx < num_tracks_per_query:  
            
            API_search_request(query, 'track', 50, idx, ltrack, song_ids, artist_ids, album_ids)   
            n +=1
            print(('\n>> this is No '+ str(n) + ' search End '))
            idx += 50 
            # Limit API requests to at most 3ish calls / second
            time.sleep(0.3)                                     
        
        print(len(song_ids))
        ## spotify API "search" option vs here track/audiofeature query
        for idx in range(0, len(song_ids), 50):
            API_get_audio_feature(song_ids[idx: idx+50], audioF)
            time.sleep(0.3)
        
        for idx in range(0, len(artist_ids), 50):
            API_get_artists(artist_ids[idx: idx+50], artist_data)
            time.sleep(0.3)
        
        for idx in range(0, len(album_ids), 20):
            API_get_albums(album_ids[idx: idx+20], album_data)
            time.sleep(0.3)    
        
        
        df1 = pd.DataFrame(ltrack, columns=col1)
        
        df2 = pd.DataFrame(audioF, columns=col2) 
        
        
        df3 = pd.DataFrame(artist_data, columns=col3)
        
        df4 = pd.DataFrame(album_data, columns=col4)
        
        df = df1.merge(df2, on='song_id', how='outer').merge(df3, on='artist_id', how='outer').merge(
             df4, on='album_id', how='outer')
        
        filename = query + '.csv'                      
        
        df.to_csv(filename, sep='\t')
        
        print ('finish')
        print (query)

def API_search_request(keywords, search_type, results_limit, results_offset, ltrack, song_ids, artist_ids, album_ids):

    off = str(results_offset)
    lim = str(results_limit)

    url = 'https://api.spotify.com/v1/search?q=year:'+ keywords +'&type=' + search_type +'&offset='+ off +'&limit=' + lim

    r = requests.get(url)

    if r: 
       j = r.json()
    else:
      return r


    litem = j['tracks']['items']
    #print(len(ll))
    try:
        for l in litem:
        
            if l['id'] not in song_ids:
                song_ids.append( l['id'] )

            if l['artists'][0]['id'] not in artist_ids:
                artist_ids.append( l['artists'][0]['id'] )

            if l['album']['id'] not in album_ids:
                album_ids.append(  l['album']['id'] )
        
        
            k =   [  l['popularity'],
        
                     l['id'], 
                     l['artists'][0]['id'],
                     l['album']['id'],

                     l['name'],
                     l['artists'][0]['name'],
                     l['album']['name'],

                     l['explicit'], 
                     l['disc_number'],
                     l['track_number']]
        
            ltrack.append(k)
    except:
         ValueError
      
   # f.close()
    #return j


def API_get_audio_feature(songids, audioF):
    
    #print(songids)
    #print '>> call art several'
    track_ids = ','.join(songids)

    url = 'https://api.spotify.com/v1/audio-features?ids=' + track_ids  
    ## access_token will expire soon
    access_token = (  'Bearer BQDAZNalQ6KCd8pRM0Exu3D-tzdeodFYL86pdq8kz'
                      'qN8i5gqeLMNeCgyPmZ1B3mgQ2YGd29tL06jxeNzOMkhmi4GM'
                      'QQLQ_ZfQUroBMRSMj10IOjEo-cX7YsfzH_v3eUlN4wXgDd4z'
                      'njNqrPu-MI9qRz3_jyb44urQ7J5TeOeWk4kvHKfD36TplacQ'
                      'DeYJe49DsaAQWuCSe5kdt1r7r0GqugSH85vOaa5qrqMaGbKM'
                      'DnZ-2aWzuLUE37Vh3U2MR3VEdgHPIxlQtC_vfTBwiMZZcY55'
                      'Q1aZuKSrGL9A6MC2hUi4CgRMD1mXwE9l8bLJQ')
    
    
    r = requests.get(url, headers={"Accept": "application/json" , "Authorization": access_token})
    
    if r: 
      j = r.json()
    else:
      return r
    
    # print(j)
    ll = j['audio_features']

    try:

        for l in ll:
            k =  [  l['id'],l['uri'],
                    l['tempo'],l['type'],
                    l['key'],l['loudness'],
                    l['mode'],l['speechiness'],
                    l['liveness'],l['valence'],
                    l['danceability'],l['energy'],
                    l['track_href'],l['analysis_url'],
                    l['duration_ms'],l['time_signature'],
                    l['acousticness'],l['instrumentalness'] ]

            audioF.append(k)
        
    except:
        ValueError
    
        

    #return j

def API_get_artists(artist_ids, artist_data):

    art_ids = ','.join(artist_ids)

    url = 'https://api.spotify.com/v1/artists?ids=' + art_ids

    r = requests.get(url)

    if r:
       j = r.json()
    else:
       #print 'for this specific art_ids, response reaches maximum, return'
       return r

    
    ll = j['artists']

    try:
        for l in ll:
        
            k = [  l['id'], 
                   l['genres'],
                   l['popularity'] ]

            artist_data.append(k)
    
    except:
        ValueError
    


def API_get_albums(album_ids, album_data):
   

    alb_ids = ','.join(album_ids)

    url = 'https://api.spotify.com/v1/albums?ids=' + alb_ids
    r = requests.get(url)

    if r:
       j = r.json()
    else:
       return r


    ll = j['albums']
    
    try:
        for l in ll:
            k = [  l['id'], 
                   l['genres'],
                   l['popularity'],
                   l['release_date'] ]

            album_data.append(k)
    
    except:
        ValueError


if __name__ == '__main__':
    main()

