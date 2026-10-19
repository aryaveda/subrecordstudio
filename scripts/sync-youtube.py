"""
Sync YouTube Videos for Sub-Record Studio
Channel: @subrecordstudio (ID: UCmWSNK21ZAIM4vgrrhiB6pQ)
Fetches YouTube RSS feed, auto-categorizes, and saves to data/youtube-portfolio.json.
Can be run locally or automated via GitHub Actions.
"""

import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

CHANNEL_ID = "UCmWSNK21ZAIM4vgrrhiB6pQ"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "youtube-portfolio.json")

def categorize_video(title, description=""):
    title_lower = title.lower()
    desc_lower = (description or "").lower()
    combined = title_lower + " " + desc_lower

    if any(k in combined for k in ["compressor", "de-esser", "mixing kick", "fabfilter", "cara mixing", "vocal cewe", "tips"]):
        return "tutorial", "Production Tips"
    elif any(k in combined for k in ["live at the living room", "the wedding of", "live cover", "live session", "live performance"]):
        return "live", "Live Performance"
    elif any(k in combined for k in ["cover by", "cover)", " cover", "pandangan pertama", "sesaat kau hadir", "listen"]):
        return "cover", "Cover Song"
    elif any(k in combined for k in ["official music video", "official lyric video", "single", "mengertilah", "pelabuhan", "khayalku", "abrakadabra", "sofa", "pulang sayang", "bersamanya", "sunflowers"]):
        return "original", "Original Song"
    else:
        return "original", "Studio Work"

def detect_artist(title):
    title_lower = title.lower()
    if "cindy leivana and the fairies" in title_lower or "cindy and the fairies" in title_lower:
        return "Cindy and The Fairies"
    elif "cindy leivana" in title_lower:
        return "Cindy Leivana"
    elif "kezhiki" in title_lower:
        return "KEZHIKI"
    elif "marrez" in title_lower:
        return "Marrez"
    elif "anton yoga" in title_lower:
        return "Anton Yoga"
    elif "dhandy & dhanty" in title_lower or "dhandy" in title_lower:
        return "Dhandy & Dhanty"
    elif "binar" in title_lower:
        return "Sub-Record Studio ft. Binar"
    else:
        return "Sub-Record Studio"

def fetch_rss_feed():
    req = urllib.request.Request(
        RSS_URL,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()

def parse_feed(xml_bytes):
    root = ET.fromstring(xml_bytes)
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'yt': 'http://www.youtube.com/xml/schemas/2015',
        'media': 'http://search.yahoo.com/mrss/'
    }

    videos = []
    for entry in root.findall('atom:entry', ns):
        vid = entry.find('yt:videoId', ns).text
        title = entry.find('atom:title', ns).text
        published = entry.find('atom:published', ns).text
        
        # Format date readable (e.g. 29 Aug 2026)
        try:
            dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
            formatted_date = dt.strftime("%d %b %Y")
        except Exception:
            formatted_date = published[:10]

        media_group = entry.find('media:group', ns)
        desc = ""
        thumb = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
        if media_group is not None:
            desc_el = media_group.find('media:description', ns)
            if desc_el is not None and desc_el.text:
                desc = desc_el.text.strip()
            thumb_el = media_group.find('media:thumbnail', ns)
            if thumb_el is not None and 'url' in thumb_el.attrib:
                thumb = thumb_el.attrib['url']

        category, category_label = categorize_video(title, desc)
        artist = detect_artist(title)

        videos.append({
            "id": vid,
            "title": title,
            "artist": artist,
            "category": category,
            "category_label": category_label,
            "published": published,
            "formatted_date": formatted_date,
            "thumbnail": thumb,
            "youtube_url": f"https://www.youtube.com/watch?v={vid}",
            "embed_url": f"https://www.youtube.com/embed/{vid}?autoplay=1",
            "description": desc[:250] + ("..." if len(desc) > 250 else "")
        })

    return videos

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Fetching latest videos from YouTube RSS: {RSS_URL}...")
    try:
        xml_data = fetch_rss_feed()
        videos = parse_feed(xml_data)
        print(f"Successfully parsed {len(videos)} videos from YouTube feed.")
    except Exception as e:
        print(f"Warning: Failed to fetch online RSS ({e}). Checking existing cache...")
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                videos = data.get("videos", [])
                print(f"Loaded {len(videos)} videos from existing cache.")
        else:
            videos = []

    # Sort videos newest first
    videos.sort(key=lambda x: x.get("published", ""), reverse=True)

    result = {
        "channel_title": "Sub-Record Studio",
        "channel_url": "https://www.youtube.com/@subrecordstudio",
        "channel_id": CHANNEL_ID,
        "last_synced": datetime.utcnow().isoformat() + "Z",
        "total_videos": len(videos),
        "categories": {
            "all": "Semua Portofolio",
            "original": "Original Song & Single",
            "live": "Live Session & Performance",
            "cover": "Cover Song",
            "tutorial": "Audio Production Tips"
        },
        "videos": videos
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Done! Saved portfolio data to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
