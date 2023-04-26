from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "tranquil-lotus-368022",
  "private_key_id": "daa92497696493c69edc1d026cece9a41bbcef88",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDJMCuonJEv9S4K\nO5T+vXbSsxwHHkGv4Z9MEvF2CeBamFIOMQIKhCv2lkPplAxn/JejISLH5Dg7mzEn\na0tjwjd+oFTqxgcetCSGmzhIVGBpuSTcB6WXU+RF3d04zwta90jFcKbL+Wjj2pBk\ni5+2hwL7XMmubeSxixKYOeQBIIYblBkLbwuQ9aANog2s9JnnYlYErZwYVzOQn3op\n+E+nmyG1yD1cXZWeqcO1rX9tnMqemWZOzQwzN6vljbRHGN5ekuDL7CYWN6bIzbfS\nZ3x+7fRQuYC/6FeX50g1cugb6yWoQP2Uc1lvbLkABL+fmZrHnCsvtFGLEPIpfht1\nWq0H6AQHAgMBAAECggEAFYm6ospgIKo2y5GlWcAewF+8WGa80X9t9k7w2pokEo7L\n+gj1FvsfWb6sdo0K5vb7pNMfThb4jikHEhlCcOOR3VR8wsWAbaELZ/2mANhHmgng\nEE4hRBoPDgu6ayJ/LLXcbIaq1JtWx03Wt2zbJEc/4nkEfk/1c6xXyUQpTJWWxczc\nUzyj6hF/dM7VqponsHZZX+9xkAgBX/tZ6IqlKjGV8XaWAr8jmMjzYwTBZ6l952zc\nEedqtE/27f1VDqbYLgxvMYYWqwEHly7IjmoQ8bGtpUjc+xgRivbhymBWSUj0eFp2\nJS3b2bvbDfy9Kn9Ia4r4nLz9NjC1cHdX+52I1i95gQKBgQDxHzgsVOjAITskTXAg\nI8IXimbjqS0QW4WurcR4aIyxYhybdEvRuEqfzlugmiCBKErUmxdCfmufxW1UIIS0\n3f89TaLe02/bgMA+D7g2CM7QcwyW4/HRWCqRdz7bPHjmlRuwv7vUXAhsmpHIV5+5\nsK6SzO0VCjldUlNsGpZ9fseqSQKBgQDVmidum040ozJHUFhQgppWxK6VbMWr0a5O\nHcBUlqxanVtgw2S5+ljbqI4iGETp+drY+MOhlExd7u5ZSqHsm44xbuocT6Kgp9tH\nEkdheKcxChlrUf/88X3H617vn4wED/lHAYYmg35lJBHwTabfPCsJEkzbeZ7Rzjwu\nzwjpooK7zwKBgEXQ5FLxwvLerGE2iuDDec+XI3OH6KRz26FYbyruGs7BucbJRarT\n0cez2JQIDKFZKVGmFnYKZN8+KwnQ4Jv+K4l0kVQzpI/KF9/gbVY39qokpeCK39nd\nzXWRMYIJYHhjdEEZQymZ/FZ16wA3XuhFYEbhT0RoUXPUApOqnyh3LRkBAoGAQgGt\nBcUAWcvEkb0GTXrObtnAiXRfcUUOdB1Ffd5BzI6r2i8HRWFTbC2eHnMZeKQ5OKtG\n6PuGzdAz32vstc0sF6KKvczuGG9Gl6PSYxCBuenBCSUB0gxeLhVR9QJ8phS5l3Ol\nHOmteVu4H2YflwRk2BzLm1bt+S+d8WkQ/AG4HIkCgYEA2Jf+C2gZ+n8r5Pv/IwKl\npy8T7KKyBJsrG7MrXHDdMlInyzeKtASJRWYeTs4THssYrF5SsJk82YczddZ/B3nK\nCRpv+ahkoUvSoa//+Ij5hs+AW/cKEfa0/wUo0K7jJ2ZrxqO51kV4yJpTKL7j3s9O\nfTSrUjgeSbrgogcoBqLQuag=\n-----END PRIVATE KEY-----\n",
  "client_email": "tranquil-lotus-368022@appspot.gserviceaccount.com",
  "client_id": "111055234042344578014",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/tranquil-lotus-368022%40appspot.gserviceaccount.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('artists_names')
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
