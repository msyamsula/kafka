from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select
import pandas as pd
from math import ceil
import time

connection = 'mysql+pymysql://root:agh765@V@localhost:3306/student_score'
engine = create_engine(connection, echo=False)

def calculate_average(student):
    query="SELECT * FROM students_result"
    df = pd.read_sql_query(query, engine)[['CATEGORY', 'SCORE', 'NAME']]
    student_df = df.loc[df['NAME']==student]

    if len(student_df)<3:
        print('please take another test (less than 3 test)')
        return -3

    last_3_test = student_df.tail(3)

    average = last_3_test['SCORE'].mean()
    
    print(last_3_test)
    rounded_average = ceil(average)
    return rounded_average

def calculate_ranking():
    time.sleep(5)
    query="SELECT * FROM students_average"
    df = pd.read_sql_query(query, engine)

    ranking = df['AVERAGE'].rank(method='first', ascending=False).astype('int64')
    df_rank = pd.DataFrame(ranking, index=df.index).rename(columns={'AVERAGE': 'ranking'})

    df_join = df.join(df_rank).sort_values(by=['ranking'])

    list_data=[]
    for index, row in df_join.iterrows():
        list_data.append({
            'student_id': row['STUDENT_ID'],
            'name': row['NAME'],
            'average': row['AVERAGE'],
            'ranking': row['ranking']
        })
    
    return list_data