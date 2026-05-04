import json
import requests


URL = "https://www.btkakademi.gov.tr/api/service/v1/public/51/cms/category/tree/course?language=tr"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}


def flatten_categories(nodes, parent_name=None):
    items = []

    for node in nodes:
        items.append(
            {
                "id": node.get("id"),
                "title": node.get("name"),
                "parent_category": parent_name,
                "image_url": node.get("imageUrl"),
                "thumbnail_url": node.get("thumbnailUrl"),
            }
        )

        children = node.get("children") or []
        if children:
            items.extend(flatten_categories(children, node.get("name")))

    return items


def main():
    print("Veri cekiliyor...")

    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        print("Request hatasi:", exc)
        return

    content_type = response.headers.get("Content-Type", "").lower()
    if "json" not in content_type:
        print("JSON donmedi. Ilk 500 karakter:")
        print(response.text[:500])
        return

    try:
        data = response.json()
    except ValueError as exc:
        print("JSON parse hatasi:", exc)
        print(response.text[:500])
        return

    if not isinstance(data, list):
        print("Beklenmeyen veri formati:", type(data).__name__)
        print(data)
        return

    all_items = flatten_categories(data)

    with open("btkakademi_course_category.json", "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    print(f"Toplam kategori/kurs kaydi: {len(all_items)}")
    print("Dosyaya kaydedildi: btkakademi_course_category.json")


if __name__ == "__main__":
    main()