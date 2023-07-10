import re
import pandas as pd
from components.utils import features

# making dataframe
def preprocessor(data):
    msg_pattern = '\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{1,2}\s\w{2}\s-\s' # this pattern is for 12 hour time format , change as per your requirement.
    message = re.split(msg_pattern, data)[1:]
    date_time = re.findall(msg_pattern,data)
    df = pd.DataFrame({'message' : message, 'date-time' : date_time})
    df['date-time'] = pd.to_datetime(df['date-time'], format='%d/%m/%Y, %I:%M %p - ')
    df['User'], df['Message'] = features(df)
    df.drop(['message'], axis = 1, inplace=True)

    df['day'] = df['date-time'].dt.day
    df['month'] = df['date-time'].dt.month
    df['month_name'] = df['date-time'].dt.month_name()
    df['day_name'] = df['date-time'].dt.day_name()
    df['year'] = df['date-time'].dt.year
    df['hour'] = df['date-time'].dt.hour
    df['minute'] = df['date-time'].dt.minute
    df['date'] = pd.to_datetime(df['year'] * 10000 + df['month'] * 100 + df['day'], format='%Y%m%d')

    return df