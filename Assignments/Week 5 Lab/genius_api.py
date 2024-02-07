

def genius(search_term, per_page=15):
    '''
    Collect data from the Genius API by searching for `search_term`.
    
    **Assumes ACCESS_TOKEN is loaded in environment.**
    '''
    genius_search_url = f"http://api.genius.com/search?q={search_term}&" + \
                        f"access_token={ACCESS_TOKEN}&per_page={per_page}"
    
    response = requests.get(genius_search_url)
    json_data = response.json()
    
    return json_data['response']['hits']

def genius_to_df(search_term, n_results_per_term=10):
    json_data = genius(search_term, per_page=n_results_per_term)
    hits = [hit['result'] for hit in json_data]
    df = pd.DataFrame(hits)

    # expand dictionary elements
    df_stats = df['stats'].apply(pd.Series)
    df_stats.rename(columns={c:'stat_' + c for c in df_stats.columns},
                    inplace=True)
    
    df_primary = df['primary_artist'].apply(pd.Series)
    df_primary.rename(columns={c:'primary_artist_' + c for c in df_primary.columns},
                      inplace=True)
    
    df = pd.concat((df, df_stats, df_primary), axis=1)
    
    return df
