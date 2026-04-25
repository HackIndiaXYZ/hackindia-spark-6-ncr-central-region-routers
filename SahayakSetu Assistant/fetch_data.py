from firecrawl import FirecrawlApp
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("FIRECRAWL_API_KEY")

app = FirecrawlApp(api_key=api_key)

# 🔥 UPDATED URL LIST (HIGH QUALITY SOURCES)
urls = [
    # 🌍 GLOBAL EMERGENCY
    "https://www.redcross.org/get-help/how-to-prepare-for-emergencies/types-of-emergencies.html",
    "https://www.cdc.gov/disasters/index.html",
    "https://www.who.int/news-room/fact-sheets",

    # 🏥 MEDICAL (GENERAL + EMERGENCY)
    "https://medlineplus.gov/emergencymedicalservices.html",
    "https://www.nhs.uk/conditions/",
    "https://www.mayoclinic.org/first-aid",

    # 🇮🇳 INDIA
    "https://www.mohfw.gov.in/",
    "https://ndma.gov.in/",

    # 🚑 FIRST AID
    "https://www.maxhealthcare.in/blogs/first-aid-tips",
    "https://www.apolloshinefoundation.org/emergency-care/",

    # 🚒 FIRE
    "https://www.ready.gov/home-fires",
    "https://www.nfpa.org/Public-Education/Fire-causes-and-risks",

    # 🚗 ACCIDENT
    "https://www.cdc.gov/motorvehiclesafety/index.html",

    # 🧠 LIMITED MENTAL HEALTH
    "https://www.nimhans.ac.in/"
]

all_docs = []

# 🔥 CLEAN TEXT
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# 🔥 CATEGORY DETECTION (FIXED — NO "doctor" BIAS)
def detect_category(text):
    t = text.lower()

    if any(k in t for k in ["fire", "burn", "smoke", "flame"]):
        return "fire"
    elif any(k in t for k in ["bleeding", "injury", "wound", "fracture", "pain", "unconscious", "cpr"]):
        return "medical"
    elif any(k in t for k in ["earthquake", "flood", "storm", "cyclone", "disaster"]):
        return "natural_disaster"
    elif any(k in t for k in ["accident", "crash", "collision", "vehicle"]):
        return "accident"
    elif any(k in t for k in ["attack", "theft", "crime", "violence"]):
        return "crime"
    else:
        return "general"

# 🔥 SUBTYPE DETECTION (NEW 🔥)
def detect_subtype(text):
    t = text.lower()

    if any(k in t for k in ["mental", "depression", "anxiety", "stress"]):
        return "mental_health"
    elif any(k in t for k in ["first aid", "cpr", "bleeding", "injury", "emergency care"]):
        return "first_aid"
    else:
        return "general"

# 🔥 SMART SPLIT
def smart_split(text, chunk_size=400):
    sentences = text.split(".")
    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) < chunk_size:
            current += sentence + "."
        else:
            chunks.append(current.strip())
            current = sentence + "."

    if current:
        chunks.append(current.strip())

    return chunks

# 🔥 MAIN LOOP
for url in urls:
    try:
        data = app.scrape(url)

        content = data.markdown if hasattr(data, "markdown") else ""

        if not content:
            print(f"⚠️ No content: {url}")
            continue

        content = clean_text(content)
        chunks = smart_split(content)

        for chunk in chunks:
            category = detect_category(chunk)
            subtype = detect_subtype(chunk)

            doc = {
                "category": category,
                "subtype": subtype,
                "text": f"[{category}] {chunk}",
                "source": url
            }

            all_docs.append(doc)

        print(f"✅ Processed: {url} | chunks: {len(chunks)}")

    except Exception as e:
        print(f"❌ Error: {url} → {e}")

# 🔥 SAVE FILE
with open("firecrawl_data.json", "w") as f:
    json.dump(all_docs, f, indent=2)

print(f"🔥 Total docs saved: {len(all_docs)}")