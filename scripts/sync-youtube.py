"""
Automated YouTube Synchronization Engine for Sub-Record Studio
Channel: @subrecordstudio (ID: UCmWSNK21ZAIM4vgrrhiB6pQ)

Fetches latest uploads from YouTube RSS feed or YouTube Data API,
auto-categorizes by musical style / content type, merges with existing portfolio,
and writes to data/youtube-portfolio.json.
"""

import os
import json
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

CHANNEL_ID = "UCmWSNK21ZAIM4vgrrhiB6pQ"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "youtube-portfolio.json")

def categorize_video(title, description=""):
    combined = (title + " " + (description or "")).lower()

    if any(k in combined for k in ["compressor", "de-esser", "mixing kick", "fabfilter", "cara mixing", "vocal cewe", "tips"]):
        return "tutorial", "Audio Production Tips"
    elif any(k in combined for k in ["live at the living room", "the wedding of", "live cover", "live session", "live performance"]):
        return "live", "Live Performance & Session"
    elif any(k in combined for k in ["cover", "kover", "feat. binar", "feat. ruri", "feat. nadia nevita", "tembang", "protein"]):
        return "cover", "Cover Song"
    elif any(k in combined for k in ["official music video", "official lyric video", "single", "mengertilah", "pelabuhan", "khayalku", "abrakadabra", "sofa", "pulang sayang", "bersamanya", "sunflowers"]):
        return "original", "Original Song & Single"
    else:
        return "original", "Studio Showcase"

def detect_artist(title):
    tl = title.lower()
    if "cindy and the fairies" in tl or "cindy leivana and the fairies" in tl:
        return "Cindy and The Fairies"
    elif "cindy leivana" in tl:
        return "Cindy Leivana"
    elif "dhandy & dhanty" in tl or "dhandy" in tl:
        return "Dhandy & Dhanty"
    elif "kezhiki" in tl:
        return "KEZHIKI"
    elif "marrez" in tl:
        return "Marrez"
    elif "anton yoga" in tl:
        return "Anton Yoga"
    elif "binar" in tl:
        return "Sub-Record Studio ft. Binar"
    elif "nadia nevita" in tl:
        return "Sub-Record Studio ft. Nadia Nevita"
    elif "ruri" in tl:
        return "Sub-Record Studio ft. Ruri"
    else:
        return "Sub-Record Studio"

def fetch_rss_xml():
    # Try with curl.exe first (bypasses Python urllib SSL/header quirks on Windows)
    try:
        proc = subprocess.run(
            ["curl.exe", "-s", "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", RSS_URL],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15,
            check=False
        )
        if proc.returncode == 0 and len(proc.stdout) > 200 and b"<feed" in proc.stdout:
            return proc.stdout
    except Exception:
        pass

    # Fallback to urllib
    req = urllib.request.Request(
        RSS_URL,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()

def parse_xml_feed(xml_bytes):
    root = ET.fromstring(xml_bytes)
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'yt': 'http://www.youtube.com/xml/schemas/2015',
        'media': 'http://search.yahoo.com/mrss/'
    }

    fetched_videos = []
    for entry in root.findall('atom:entry', ns):
        vid = entry.find('yt:videoId', ns).text
        title = entry.find('atom:title', ns).text
        published = entry.find('atom:published', ns).text
        
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

        cat_key, cat_label = categorize_video(title, desc)
        artist = detect_artist(title)

        fetched_videos.append({
            "id": vid,
            "title": title,
            "artist": artist,
            "category": cat_key,
            "category_label": cat_label,
            "published": published,
            "formatted_date": formatted_date,
            "thumbnail": thumb,
            "youtube_url": f"https://www.youtube.com/watch?v={vid}",
            "embed_url": f"https://www.youtube.com/embed/{vid}?autoplay=1",
            "description": desc[:200] + ("..." if len(desc) > 200 else "")
        })

    return fetched_videos

def sync():
    os.makedirs(DATA_DIR, exist_ok=True)
    existing_videos = []
    existing_map = {}
    
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                existing_videos = data.get("videos", [])
                for v in existing_videos:
                    existing_map[v["id"]] = v
        except Exception as e:
            print(f"Notice: Could not read existing file ({e}). Starting fresh.")

    print(f"Connecting to YouTube RSS feed ({RSS_URL})...")
    new_found = 0
    try:
        xml_bytes = fetch_rss_xml()
        feed_videos = parse_xml_feed(xml_bytes)
        print(f"Fetched {len(feed_videos)} videos from YouTube RSS feed.")

        # Prepend new videos if not in map
        new_items = []
        for fv in feed_videos:
            if fv["id"] not in existing_map:
                new_items.append(fv)
                existing_map[fv["id"]] = fv
                new_found += 1
            else:
                # Update thumbnail or description if improved
                ex = existing_map[fv["id"]]
                if fv.get("description") and not ex.get("description"):
                    ex["description"] = fv["description"]

        merged_videos = new_items + existing_videos
    except Exception as e:
        print(f"Notice: Online RSS fetch could not complete ({e}). Retaining existing verified database.")
        merged_videos = existing_videos

    final_payload = {
        "channel_title": "Sub-Record Studio",
        "channel_url": "https://www.youtube.com/@subrecordstudio",
        "channel_id": CHANNEL_ID,
        "last_synced": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_videos": len(merged_videos),
        "new_videos_added": new_found,
        "categories": {
            "all": "Semua Portofolio",
            "original": "Original Song & Single",
            "live": "Live Session & Performance",
            "cover": "Cover Song",
            "tutorial": "Audio Production Tips"
        },
        "videos": merged_videos
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_payload, f, indent=2, ensure_ascii=False)

    print(f"Sync complete! Total videos in catalog: {len(merged_videos)} (+{new_found} new).")
    print(f"Data file updated: {OUTPUT_FILE}")

if __name__ == "__main__":
    sync()
