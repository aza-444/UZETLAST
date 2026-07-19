import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

topics = {
    "Deklaratsiya": "Customs_declaration",
    "Sertifikat": "Certificate",
    "Ruxsatnomalar": "License",
    "Yuk tushirish-ortish va tashish xizmatlari": "Forklift",
    "Omborlar elektr ta'minoti bilan ta'minlangan, 24/7 monitoring, qo'riqlash xizmati mavjud": "Security_camera",
    "O'rta va yirik hajmdagi yuk tashish xizmatlari": "Semi-trailer_truck",
    "Avtokran": "Mobile_crane",
    "Tezkor yetkazish": "Delivery_van",
    "Xavfsiz tashuv": "Armored_car"
}

results = {}

for name, search_term in topics.items():
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={search_term}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_info in pages.items():
            if "original" in page_info:
                results[name] = page_info["original"]["source"]
                break
    except Exception as e:
        print(f"Error for {name}: {e}")

print(json.dumps(results, indent=2))
