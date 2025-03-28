import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

nfx = pd.read_csv(r'C:/Namit/Unified Mentor Internship/Netflix/netflix1.csv')
nfx.info()
nfx.dtypes
nfx.describe()
nfx.isnull().sum()                           #no null values
duplicates = nfx[nfx.duplicated()]           #no duplicates

#total of "Not Given" values in director and country column
director_count = (nfx['director'] == 'Not Given').sum()
country_count = (nfx['country'] == 'Not Given').sum()


#Typecasting
nfx['type'] = nfx['type'].astype(str)
nfx['title'] = nfx['title'].astype(str)
nfx['director'] = nfx['director'].astype(str)
nfx['country'] = nfx['country'].astype(str)
nfx['listed_in'] = nfx['listed_in'].astype(str)


#the "date_added column contains multiple date formats. 
#Use Pandas to infer the format by setting "dayfirst=True" and using "errors='coerce'" to handle any invalid dates.
nfx['date_added'] = pd.to_datetime(nfx['date_added'], dayfirst=False , errors='coerce')
nfx['date_added'] = nfx['date_added'].dt.strftime('%Y-%m-%d')

def convert_duration(duration):
    if 'Season' in duration:
        return int(duration.split()[0])
    elif 'min' in duration:
        return int(duration.split()[0])
    return None

nfx['duration'] = nfx['duration'].apply(convert_duration)


#Exploratory Data Analysis
#Count the number of Movies and TV shows
type_counts = nfx['type'].value_counts()

plt.figure(figsize=(8, 6))
sns.barplot(x=type_counts.index, y=type_counts.values, palette='Set2')
plt.title('Distribution of Content by Type')
plt.xlabel('Type')
plt.ylabel('Count')
plt.show()


#Most common genres
nfx['genres'] = nfx['listed_in'].apply(lambda x: x.split(','))
all_genres = sum(nfx['genres'], [])
genre_counts = pd.Series(all_genres).value_counts().head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='Set3')
plt.title('Most Common Genres on Netflix')
plt.xlabel('Count')
plt.ylabel('Genre')
plt.show()


#Content added over time
nfx['year_added'] = nfx['date_added'].dt.year
nfx['month_added'] = nfx['date_added'].dt.month

plt.figure(figsize=(12, 6))
sns.countplot(x='year_added', nfx=nfx, palette='coolwarm')
plt.title('Content Added Over Time')
plt.xlabel('Year')
plt.ylabel('Count')
plt.show()


#Top 10 directors
top_directors = nfx['director'].value_counts().head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=top_directors.values, y=top_directors.index, palette='coolwarm')
plt.title('Top 10 directors with most titles')
plt.xlabel('Titles')
plt.ylabel('Directors')
plt.show()


#Ratings frequency of TV shows and Movies
nfx['rating'].value_counts()
ratings= nfx['rating'].value_counts().reset_index().sort_values(by='count', ascending=False)

plt.bar(ratings['rating'], ratings['count'])
plt.xticks(rotation=45, ha='right')
plt.xlabel('Rating types')
plt.ylabel('Rating frequency')
plt.suptitle("Ratings on Netflix", fontsize=16)
plt.show()


#Top 10 countries with most content on netflix
nfx['country'].value_counts()
countries= nfx['country'].value_counts().reset_index().sort_values(by='count', ascending=False)[:10]

plt.bar(countries['country'], countries['count'])
plt.xticks(rotation=45, ha='right')
plt.xlabel('Country')
plt.ylabel('Frequency')
plt.suptitle('Top 10 countries with most content')
plt.show()