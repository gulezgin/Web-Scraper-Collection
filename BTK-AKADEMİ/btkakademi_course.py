import json
import time

import requests


URL = "https://www.btkakademi.gov.tr/api/service/v1/public/51/catalog/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Referer": "https://www.btkakademi.gov.tr/portal/tr/catalog",
}
PAGE_SIZE = 12


def build_payload(offset):
    return {
        "firstResult": offset,
        "maxResults": PAGE_SIZE,
        "sortField": "recent",
        "sortOrder": "ASCENDING",
        "filter": {
            "documentType": "course",
            "categoryIds": [],
            "courseTypes": [],
            "localeIds": [],
            "courseLevels": [],
            "searchTerm": "",
            "demanded": None,
        },
    }


def course_url(course_id, title):
    slug = (
        title.lower()
        .replace("ı", "i")
        .replace("ğ", "g")
        .replace("ü", "u")
        .replace("ş", "s")
        .replace("ö", "o")
        .replace("ç", "c")
    )
    slug = "".join(ch if ch.isalnum() else "-" for ch in slug)
    slug = "-".join(part for part in slug.split("-") if part)
    return f"https://www.btkakademi.gov.tr/portal/course/{slug}/{course_id}"


def main():
    all_courses = []
    offset = 0
    total_records = None

    while True:
        print(f"Kurslar cekiliyor... offset={offset}")

        try:
            response = requests.post(
                URL,
                headers=HEADERS,
                json=build_payload(offset),
                timeout=20,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            print("Request hatasi:", exc)
            break

        content_type = response.headers.get("Content-Type", "").lower()
        if "json" not in content_type:
            print("JSON donmedi. Ilk 500 karakter:")
            print(response.text[:500])
            break

        try:
            data = response.json()
        except ValueError as exc:
            print("JSON parse hatasi:", exc)
            print(response.text[:500])
            break

        documents = data.get("documents") or []
        total_records = data.get("totalRecords", total_records)

        if not documents:
            print("Veri bitti.")
            break

        for doc in documents:
            all_courses.append(
                {
                    "id": doc.get("id"),
                    "title": doc.get("title"),
                    "description": doc.get("description"),
                    "learning_type": doc.get("learningType"),
                    "learning_level": doc.get("learningLevel"),
                    "duration": doc.get("duration"),
                    "attendee_count": doc.get("attendeeCount"),
                    "view_count": doc.get("viewCount"),
                    "like_count": doc.get("likes"),
                    "comment_count": doc.get("commentCount"),
                    "has_certificate": doc.get("hasCertificate"),
                    "has_post_test": doc.get("hasPostTest"),
                    "category_ids": doc.get("categoryIds", []),
                    "image": doc.get("image"),
                    "thumbnail": doc.get("thumbnail"),
                    "trainer": doc.get("trainer", {}),
                    "url": course_url(doc.get("id"), doc.get("title", "")),
                }
            )

        offset += len(documents)

        if total_records is not None and offset >= total_records:
            break

        time.sleep(0.5)

    with open("btkakademi_course.json", "w", encoding="utf-8") as f:
        json.dump(all_courses, f, ensure_ascii=False, indent=2)

    print(f"Toplam kurs: {len(all_courses)}")
    if total_records is not None:
        print(f"Beklenen toplam: {total_records}")
    print("Dosyaya kaydedildi: btk_courses.json")


if __name__ == "__main__":
    main()