import google.generativeai as genai
from datetime import datetime
import os
import sys

# ===== CONFIGURATION =====
GOOGLE_AI_STUDIO_API_KEY = "AIzaSyBjsWQjcfAaLqFCnquWEgtzeeKmoWh1nIE"
genai.configure(api_key=GOOGLE_AI_STUDIO_API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# ===== PATH SETUP =====
run_date = datetime.now().strftime("%Y-%m-%d")
topics_dir = f"outputs/{run_date}/topics"
os.makedirs(topics_dir, exist_ok=True)

# File paths
topics_file = f"{topics_dir}/{run_date}_topics.md"
used_topics_file = "outputs/used_topics.txt"

# ===== HELPER FUNCTIONS =====
def load_used_topics():
    if not os.path.exists(used_topics_file):
        return set()
    with open(used_topics_file, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.readlines())

def log_used_topic(topic):
    with open(used_topics_file, "a", encoding="utf-8") as f:
        f.write(topic.strip() + "\n")

# ===== MAIN: GENERATE TOPICS =====
def generate_topics(domain="AI"):
    used_topics = load_used_topics()

    prompt = f"""
    Suggest 5 engaging Medium-style article topics about {domain} for beginners.
    
    Make sure:
    - No topic should be repeated from these past topics:
      {', '.join(used_topics) if used_topics else 'None'}
      
    - Each topic should be unique and researchable
    - Include SEO keywords below each topic like this:
      1. [Topic Title]
         Keywords: keyword1, keyword2, keyword3

    Example format:
    1. How AI is Changing Education
       Keywords: AI in education, EdTech, Machine Learning in Schools
    """

    response = model.generate_content(prompt)
    raw_response = response.text.strip()

    # Save topics
    with open(topics_file, "w", encoding="utf-8") as f:
        f.write("# Generated Topics\n\n")
        f.write(raw_response)

    # Extract and save only titles to used_topics.txt
    lines = [line.strip() for line in raw_response.splitlines()]
    topics = []
    for line in lines:
        if line.startswith(("1.", "2.", "3.", "4.", "5.")):
            try:
                number, title = line.split(". ", 1)
                topic_title = title.splitlines()[0].strip()
                topics.append(topic_title)
            except Exception:
                continue

    for topic in topics:
        log_used_topic(topic)

    print(f"[SUCCESS] Generated 5 new topics in '{domain}' domain.")
    return raw_response

# ===== RUN SCRIPT =====
if __name__ == "__main__":
    selected_domain = sys.argv[1] if len(sys.argv) > 1 else "AI"
    generate_topics(selected_domain)