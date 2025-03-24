import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = 'https://www.litcharts.com'

def get_play_links():
    url = f'{BASE_URL}/shakescleare/shakespeare-translations'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    play_links = []
    for a in soup.select('a[href^="/shakescleare/shakespeare-translations/"]'):
        play_links.append(BASE_URL + a['href'])
    return play_links

def extract_play_content(play_url):
    response = requests.get(play_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    original_texts = soup.select('.original-text .text')
    translated_texts = soup.select('.translation .text')
    data = []
    for original, translated in zip(original_texts, translated_texts):
        data.append({
            'Original Text': original.get_text(strip=True),
            'Modern Translation': translated.get_text(strip=True)
        })
    return data


all_data = []
play_links = get_play_links()
for link in play_links:
    play_data = extract_play_content(link)
    all_data.extend(play_data)

# Convert to DataFrame for tabular representation
df = pd.DataFrame(all_data)

df.to_csv('shakespeare_translations.csv', index=False)