import requests
from bs4 import BeautifulSoup
from datetime import datetime


def extract_event_dates(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the main content area
        content_area = soup.find(class_="l-content")
        if not content_area:
            print("Could not find class='l-content'")
            return []

        # Find all event detail containers within the content area
        event_details = content_area.find_all(class_="l-event__itemDetail")

        current_date = datetime.now().date()
        alerts = []

        print(f"Checking events against current date: {current_date}")

        for detail in event_details:
            # Extract status
            status_tag = detail.find(class_="l-event__itemTag")
            status_text = status_tag.get_text(strip=True) if status_tag else ""

            # Extract date
            date_tag = detail.find(class_="l-event__itemDate")
            if not date_tag:
                continue

            date_text = date_tag.get_text(strip=True)

            # Extract title (sibling of detail)
            title_tag = detail.find_next_sibling(class_="l-event__itemTitle")
            title_text = title_tag.get_text(strip=True) if title_tag else "No Title"

            # Parse date
            try:
                # Handle potential non-date text like "今すぐ視聴可能" or "定期開催" by skipping or handling specific cases
                # Assuming standard format YYYY.MM.DD based on request
                event_date = datetime.strptime(date_text, "%Y.%m.%d").date()

                # Check condition: Date is in the past AND status is NOT "開催終了"
                if event_date < current_date and status_text != "開催終了":
                    alerts.append(
                        {
                            "date": date_text,
                            "status": status_text,
                            "title": title_text,
                            "message": f'"{date_text}" "{title_text}" は開催日を過ぎています。',
                        }
                    )

            except ValueError:
                # print(f"Skipping non-date text: {date_text}")
                continue

        return alerts

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


if __name__ == "__main__":
    target_url = "https://phoneappli.net/event/"
    print(f"Scanning {target_url} for alerts...")
    alerts = extract_event_dates(target_url)

    if alerts:
        print("\n!!! ALERTS FOUND !!!")
        for alert in alerts:
            print(alert["message"])
    else:
        print("\nNo alerts found. All past events seem to be marked correctly.")
