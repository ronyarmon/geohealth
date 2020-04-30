def query (statements):
    import time
    import psycopg2
    import pandas as pd

    conn = psycopg2.connect(
        database="postgres",
        user="dashboard_user",
        password="healthgeo2020",
        host="prescribinguk.czm1h03t4mrp.eu-central-1.rds.amazonaws.com",
        port= '5432'
    )
    cur = conn.cursor()
    query_dfs=[]

    # Query each statement
    for query, statement in statements.items():
        start=time.time()
        cur.execute(statement)
        rows_fetched=cur.fetchall()

        # Store the feature values in a dataframe
        if query !='location':
            a,b = map(list, zip(*rows_fetched))
            query_df=pd.DataFrame(data=list(zip(a,b)),columns=['practice_code',query])

        # Store the location values in a dataframe
        else:
            a,b,c,d,e,f,g = map(list, zip(*rows_fetched))
            headers=['practice','practice_code','ccg','region','sub_region','longitudemerc','latitudemerc']
            query_df=pd.DataFrame(data=list(zip(a,b,c,d,e,f,g)),columns=headers)

        query_dfs.append(query_df)
        end=round ((time.time()-start),2)

    # Join location data to feature values     
    if len (query_dfs)>2:
        queries_df=query_dfs[0].merge(query_dfs[1], on='practice_code')\
        .merge(query_dfs[2], on='practice_code')
    else:
        queries_df=query_dfs[0].merge(query_dfs[1], on='practice_code')

    queries_df.to_csv('queries_df.csv',index=False)
    return queries_df
