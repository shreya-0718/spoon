from datetime import datetime
import random
import time
import httpx
import schedule

def get_spoonful_of_thought() -> str:
    try:
        r = httpx.get("https://zenquotes.io/api/random", timeout=5)
        data = r.json()[0]
        quote = data["q"]
        author = data["a"]
        return f'“{quote}” — {author}'
    except Exception:
        fallback_thoughts = [
            "You are made of stardust and silence.",
            "Even the moon takes time to wax and wane.",
            "A single spoon can hold an entire sky.",
            "You are not behind. You are becoming.",
        ]
        return random.choice(fallback_thoughts)

def main():
    text = get_spoonful_of_thought()
    httpx.post(
        "https://ntfy.sh/spoon-signals",  # Replace with your actual ntfy.sh topic
        data=text.encode("utf-8"),
        headers={
            "Title": "Spoonful of Thought",
            "Tags": "thought_balloon,tea",
        },
    )
    print(f'Posted: "{text}"')

if __name__ == "__main__":
    main()
    schedule.every(1).minutes.do(main)  # You can change this to .minutes for testing
    while True:
        schedule.run_pending()
        time.sleep(1)