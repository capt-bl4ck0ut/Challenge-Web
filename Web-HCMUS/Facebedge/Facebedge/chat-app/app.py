from flask import Flask, render_template, request, jsonify
import re, os
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import base64
import random

FACEBED_URL = os.getenv('FACEBED_URL', 'http://localhost:9812')
app = Flask(__name__)

def get_facebook_image_data_url(url, headers=None):
  """
  Given a Facebook URL, fetch the Facebed service, extract the og:image,
  download the image, and return a data URL. Returns None on failure.
  """
  parsed = urlparse(url)
  # Build the full path including query
  full_path = parsed.path
  if parsed.query:
    full_path += '?' + parsed.query
  if not full_path.startswith('/'):
    full_path = '/' + full_path
  try:
    req = urllib.request.Request(FACEBED_URL + full_path)
    req.headers.update(headers)
    with urllib.request.urlopen(req) as response:
      html_data = response.read().decode("utf-8")
      soup = BeautifulSoup(html_data, "html.parser")
      meta = soup.find("meta", property="og:image")
      if meta and meta.get("content"):
        img_url = meta["content"]
        try:
          img_req = urllib.request.Request(img_url)
          img_req.headers.update(headers)
          with urllib.request.urlopen(img_req) as img_response:
            img_data = img_response.read()
            ext = img_url.split('.')[-1].lower()
            if ext in ['jpg', 'jpeg']:
              mime = 'image/jpeg'
            elif ext == 'png':
              mime = 'image/png'
            elif ext == 'gif':
              mime = 'image/gif'
            else:
              mime = 'application/octet-stream'
            b64 = base64.b64encode(img_data).decode('utf-8')
            return f'data:{mime};base64,{b64}'
        except Exception as e:
          return None
  except Exception as e:
    return None
  return None

def embed_url(match, headers=None):
  url = match.group(0)
  parsed = urlparse(url)
  # Facebook URL
  if parsed.netloc.endswith("facebook.com"):
    data_url = get_facebook_image_data_url(url, headers)
    if data_url:
      return f'<img src="{data_url}" alt="Facebook Embedded Image" class="embedded-image">'
    else:
      return f'<a href="{url}" target="_blank">{url}</a>'
  # Direct image URL
  if re.search(r'\.(jpg|jpeg|png|gif)$', url, re.IGNORECASE):
    return f'<img src="{url}" alt="Embedded Image" class="embedded-image">'
  # Fallback: link
  return f'<a href="{url}" target="_blank">{url}</a>'

RANDOM_RESPONSES = [
  "Nice message! 👍",
  "I see what you did there 😏",
  "That's interesting!",
  "Haha, good one! 😂",
  "Tell me more!",
  "Cool! 😎",
  "I'm just a bot, but I like your style.",
  "Did you know? Python is awesome 🐍",
  "Let's keep the chat going!",
  "Great share! 🚀",
  "What brings you here today?",
  "That made me smile!",
  "I'm always here to chat.",
  "You have a way with words!",
  "Let's vibe together!",
  "I appreciate your input.",
  "Keep those messages coming!",
  "You seem pretty cool.",
  "Is there anything else on your mind?",
  "I'm learning from you every day!",
  "That sounds awesome!",
  "You rock! 🤘",
  "Let's make this chat lively!",
  "I'm here for a good conversation.",
  "Your energy is contagious!",
  "I like your enthusiasm!",
  "Let's keep the good times rolling!",
  "You make this chat better!",
  "I'm always ready for more!",
  "That was insightful.",
  "You just made my day!"
]

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
  data = request.get_json()
  headers = dict(request.headers)
  headers.pop('Host', None)  # Remove Host header to avoid issues with Facebed
  headers.pop('Content-Length', None)  # Remove Content-Length header to avoid issues with Facebed
  headers.pop('Accept-Encoding', None)  # Remove Accept-Encoding header to avoid issues with Facebed
  message = data.get('message', '')
  url_regex = r'(https?://[^\s]+)'
  html = re.sub(url_regex, lambda m: embed_url(m, headers), message)
  # Pick a random response
  bot_response = random.choice(RANDOM_RESPONSES)
  return jsonify({'html': html, 'bot': bot_response})

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=1337, debug=True)

# Thank you Copilot!