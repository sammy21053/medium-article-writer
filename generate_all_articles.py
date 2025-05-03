import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import google.generativeai as genai
from datetime import datetime
import os

# === CONFIGURATION ===
GOOGLE_AI_STUDIO_API_KEY = "AIzaSyBjsWQjcfAaLqFCnquWEgtzeeKmoWh1nIE"
genai.configure(api_key=GOOGLE_AI_STUDIO_API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

run_date = datetime.now().strftime("%Y-%m-%d")
final_dir = f"outputs/{run_date}/final"
os.makedirs(final_dir, exist_ok=True)

def generate_articles():
    # Locate topics file
    topics_file = f"outputs/{run_date}/topics/{run_date}_topics.md"

    if not os.path.exists(topics_file):
        print("❌ Error: Topics file not found.")
        return

    # Read topics and keywords
    with open(topics_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    topics = []
    current_topic = None

    for line in lines:
        if line.startswith(("1.", "2.", "3.", "4.", "5.")):
            try:
                number, title = line.split(". ", 1)
                current_topic = {"title": title.strip(), "keywords": []}
                topics.append(current_topic)
            except ValueError:
                continue
        elif line.startswith("Keywords:") and current_topic:
            keywords = line.replace("Keywords:", "", 1).strip()
            current_topic["keywords"] = [k.strip() for k in keywords.split(",")]

    # Limit to 5 topics
    topics = topics[:5]

    if not topics:
        print("❌ No valid topics found in topics.md")
        return

    print(f"\n📄 Found {len(topics)} topics. Generating articles...\n")

    # Generate each article
    for i, entry in enumerate(topics, start=1):
        title = entry["title"]
        keywords = ", ".join(entry["keywords"]) if entry["keywords"] else "AI, technology, beginner-friendly"

        print(f"📝 Generating Article {i}: {title}")
        print(f"   Using keywords: {keywords}")

        prompt = f"""
        Write a 1000-word article in the style of Medium on the following topic:
        "{title}"

        Use these SEO keywords naturally throughout the article: {keywords}

        Keep the tone professional but beginner-friendly.
        Include subheadings, bullet points, real-world examples, and a strong conclusion.
        Use Markdown formatting (e.g., # for headers).
        write like a real blogger who explains things clearly.
        Avoid including any AI-generated prompts or feedback sections.
        """

        response = model.generate_content(prompt)

        padded_index = str(i).zfill(4)
        filename = f"{final_dir}/final_article_{padded_index}.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(response.text)

        print(f"✅ Saved: {filename}\n")

if __name__ == "__main__":
    generate_articles()