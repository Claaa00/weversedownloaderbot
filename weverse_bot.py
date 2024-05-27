import requests
from bs4 import BeautifulSoup
import telebot

API_TOKEN = '7298752858:AAGpav50QxB8fanAdGgUy2SLMyCv97s9RCQ'
bot = telebot.TeleBot(API_TOKEN)

def download_media(url):
    if "instagram.com" in url:
        return get_instagram_media(url)
    elif "twitter.com" in url:
        return get_twitter_media(url)
    elif "weverse.io" in url:
        return get_weverse_media(url)
    else:
        return "Unsupported URL"

def get_instagram_media(url):
    # Scrape Instagram media (example implementation)
    return ["https://example.com/media1.jpg", "https://example.com/media2.mp4"], ["Example caption"]

def get_twitter_media(url):
    # Scrape Twitter media (example implementation)
    return ["https://example.com/media1.jpg"], ["Example tweet"]

def get_weverse_media(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    media_urls = []
    captions = []
    for img in soup.find_all('img'):
        media_urls.append(img['src'])
    for video in soup.find_all('video'):
        media_urls.append(video['src'])
    for caption in soup.find_all('p'):
        captions.append(caption.text)
    return media_urls, captions

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Send me a URL to download media.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    media_urls, captions = download_media(url)
    
    if not media_urls:
        bot.reply_to(message, "No media found.")
        return
    
    for media_url in media_urls:
        bot.send_message(message.chat.id, media_url)
    
    if captions:
        bot.send_message(message.chat.id, "\n".join(captions))

bot.polling()
