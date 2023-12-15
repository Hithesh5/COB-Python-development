import requests

def check_url_status(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return 1, "Available"
        else:
            return response.status_code, "Not Available"
    except requests.ConnectionError:
        return 0, "Not Available"

def main():
    # List of URLs to check
    urls = [
        "https://www.facebook.com",
        "https://www.whatsapp.com",
        "https://www.google.com"
    ]

    # Checking the status of each URL
    for url in urls:
        status_code, availability = check_url_status(url)
        print(f"URL: {url} - Status Code: {status_code}, Availability: {availability}")

if __name__ == "__main__":
    main()
