import os
import openai

ERAS = {
    "doomscroll_renaissance": {
        "name": "Doomscrolling Renaissance",
        "emoji": "\U0001f4dc\U0001f525",
        "colors": ["#1a0a00", "#ff4500", "#ff8c00"],
        "gradient": "linear-gradient(135deg, #1a0a00, #ff4500, #ff8c00)",
        "description": "You are chronically online and thriving in it. You know every drama within minutes. Your FYP knows you better than your therapist.",
        "tagline": "informed? more like weaponized",
        "aesthetic": "blue-lit face at 3am reading threads about the downfall of western civilization",
        "spirit_website": "X (formerly Twitter)",
        "spirit_animal": "Phoenix eating itself"
    },
    "delulu_influencer": {
        "name": "Delulu Influencer Era",
        "emoji": "\u2728\U0001f4f8",
        "colors": ["#2a1b38", "#e040fb", "#ff80ab"],
        "gradient": "linear-gradient(135deg, #2a1b38, #e040fb, #ff80ab)",
        "description": "You post like you have 10M followers but your most liked post is happy birthday mom. Still maintaining the aesthetic. Still believing in the grind.",
        "tagline": "fake it till you make it but like actually",
        "aesthetic": "ring light in a messy room posting like you are in a penthouse",
        "spirit_website": "TikTok",
        "spirit_animal": "Peacock in a parking lot"
    },
    "archive_mode": {
        "name": "Archive Mode",
        "emoji": "\U0001f516\U0001f5c3",
        "colors": ["#0d1b2a", "#1b998b", "#2ec4b6"],
        "gradient": "linear-gradient(135deg, #0d1b2a, #1b998b, #2ec4b6)",
        "description": "Your bookmarks folder has 4892 unread tabs. You save articles with the intention of becoming a completely new person. You do not become that person.",
        "tagline": "collecting information like a dragon hoarding gold",
        "aesthetic": "127 open tabs with i need to read this written in a note you never opened",
        "spirit_website": "Pocket / Pinterest",
        "spirit_animal": "Squirrel with 900 acorns and no winter prep"
    },
    "main_character_podcast": {
        "name": "Main Character Podcast Era",
        "emoji": "\U0001f399\ufe0f\U0001f485",
        "colors": ["#1a1a2e", "#e94560", "#f38181"],
        "gradient": "linear-gradient(135deg, #1a1a2e, #e94560, #f38181)",
        "description": "You narrate your life like you are hosting. Group chats get paragraphs. Your Spotify Wrapped is a TED talk waiting to happen. Everything is content.",
        "tagline": "sorry i missed your text i was recording a voice note to myself",
        "aesthetic": "talking to your phone camera at the mall like someone is watching",
        "spirit_website": "Substack / Podcasts",
        "spirit_animal": "Golden retriever who found a podcast microphone"
    },
    "ghost_protocol": {
        "name": "Ghost Protocol",
        "emoji": "\U0001f47b\U0001f573",
        "colors": ["#0a0a0a", "#4a4a6a", "#7a7a9a"],
        "gradient": "linear-gradient(135deg, #0a0a0a, #4a4a6a, #7a7a9a)",
        "description": "You are everywhere and nowhere. You read every message but reply to none. You know everything but say nothing. The internet best kept secret.",
        "tagline": "present in the mind, absent from the group chat",
        "aesthetic": "staring into the void while the void stares directly at their search history",
        "spirit_website": "Reddit (lurker account)",
        "spirit_animal": "Cat. Not even a ghost cat. Just a cat."
    },
    "parasocial_peak": {
        "name": "Parasocial Peak",
        "emoji": "\U0001f495\U0001f4fa",
        "colors": ["#2a0033", "#9b59b6", "#f1c40f"],
        "gradient": "linear-gradient(135deg, #2a0033, #9b59b6, #f1c40f)",
        "description": "You can name 37 YouTubers birthdays. You have felt emotions about people who do not know you exist. And honestly you would not change a thing.",
        "tagline": "they feel like friends. they are not your friends. you know this. it does not matter.",
        "aesthetic": "watching a 3-hour lore video at 2am and feeling personally attacked by the ending",
        "spirit_website": "YouTube / Twitch",
        "spirit_animal": "Koala clinging to a cardboard cutout"
    },
    "algorithm_slave": {
        "name": "Algorithm Slave",
        "emoji": "\U0001f916\U0001f300",
        "colors": ["#001a33", "#00b4d8", "#90e0ef"],
        "gradient": "linear-gradient(135deg, #001a33, #00b4d8, #90e0ef)",
        "description": "Your FYP controls your life and you have accepted it. You did not choose the scroll life. You got assigned a video about cleaning products and now your bathroom has 47 new items.",
        "tagline": "i watched a 40-minute tiktok about concrete. i do not even live near concrete.",
        "aesthetic": "falling down a rabbit hole about mushroom foraging when you set out to check the weather",
        "spirit_website": "TikTok / Instagram Reels",
        "spirit_animal": "Moth but the lamp is the algorithm"
    },
    "cottagecore_internet": {
        "name": "Cottagecore Internet",
        "emoji": "\U0001f338\U0001f375",
        "colors": ["#4a2c2a", "#98a8b3", "#d4b483"],
        "gradient": "linear-gradient(135deg, #4a2c2a, #98a8b3, #d4b483)",
        "description": "Your internet is Pinterest boards of sourdough, Instagram accounts of cabins, and 15 saved recipes you will never make. You dream of a quiet life but currently live above a gym.",
        "tagline": "soft life in a hard world",
        "aesthetic": "curating a digital garden while surrounded by the chaos of modern existence",
        "spirit_website": "Pinterest / GoodNotes",
        "spirit_animal": "Capybara in a garden"
    }
}

SCORES = {k: 0 for k in ERAS}

TRAIT_LABELS = {
    "doomscroll_renaissance": "Doomscroller",
    "delulu_influencer": "Delulu",
    "archive_mode": "Archivist",
    "main_character_podcast": "Podcaster",
    "ghost_protocol": "Ghost",
    "parasocial_peak": "Parasocial",
    "algorithm_slave": "Algorithm'd",
    "cottagecore_internet": "Cottagecore"
}

ERA_KEYS_BY_QUESTION = [
    ["doomscroll_renaissance", "delulu_influencer", "archive_mode", "ghost_protocol"],
    ["doomscroll_renaissance", "parasocial_peak", "main_character_podcast", "delulu_influencer"],
    ["algorithm_slave", "doomscroll_renaissance", "delulu_influencer", "ghost_protocol"],
    ["ghost_protocol", "main_character_podcast", "parasocial_peak", "delulu_influencer"],
    ["delulu_influencer", "ghost_protocol", "archive_mode", "main_character_podcast"],
    ["parasocial_peak", "algorithm_slave", "cottagecore_internet", "doomscroll_renaissance"],
    ["main_character_podcast", "ghost_protocol", "cottagecore_internet", "archive_mode"],
    ["parasocial_peak", "algorithm_slave", "cottagecore_internet", "doomscroll_renaissance"],
]

AI_PROMPTS = [
    ("roast", "Write a SHORT fun roast (2 sentences max) about someone who got '{era}' as their internet era. Make it feel personal, funny, and slightly mean in a loving way. No generic stuff."),
    ("horoscope", "Write a SHORT internet horoscope (1-2 sentences) for this person's week ahead. Make it specific to their internet era. Funny, slightly unhinged."),
    ("advice", "Give one piece of SHORT absurd but relatable advice (1 sentence max) for someone in '{era}' era. Make it sound like a wellness guru who lost it."),
]

DEFAULTS = {
    "roast": "Your era tracks. Your screen time report is judging you.",
    "horoscope": "This week you'll discover a new app that consumes 47 percent of your life. You'll adapt.",
    "advice": "Close this app. You won't though. That's very on brand for you."
}


class InternetEraEngine:
    def __init__(self):
        key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""
        self.client = None
        self.model = os.environ.get("VIBE_MODEL", "openai/gpt-4o-mini")
        if key:
            self.client = openai.OpenAI(
                api_key=key,
                base_url=os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            )

    def score_answers(self, answers):
        scores = dict(SCORES)
        for qi, ai in enumerate(answers):
            if qi < len(ERA_KEYS_BY_QUESTION) and ai < 4:
                era = ERA_KEYS_BY_QUESTION[qi][ai]
                scores[era] += 1
        return scores

    def generate_ai_content(self, era_name):
        results = dict(DEFAULTS)
        if not self.client:
            return results
        for key, prompt in AI_PROMPTS:
            try:
                r = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt.format(era=era_name)}],
                    temperature=0.9,
                    max_tokens=150,
                )
                text = r.choices[0].message.content.strip().strip('"').strip("'")
                if text:
                    results[key] = text
            except Exception:
                pass
        return results

    def analyze(self, answers):
        scores = self.score_answers(answers)
        max_s = max(scores.values()) or 1
        winner = max(scores, key=scores.get)
        runner = max((k for k in scores if k != winner), key=lambda k: scores[k])
        data = ERAS[winner]
        ai = self.generate_ai_content(data["name"])
        return {
            "era_key": winner,
            "name": data["name"],
            "emoji": data["emoji"],
            "colors": data["colors"],
            "gradient": data["gradient"],
            "description": data["description"],
            "tagline": data["tagline"],
            "aesthetic": data["aesthetic"],
            "spirit_website": data["spirit_website"],
            "spirit_animal": data["spirit_animal"],
            "scores": {TRAIT_LABELS[k]: v for k, v in scores.items()},
            "runner_up": ERAS[runner],
            "total_score": sum(scores.values()),
            "roast": ai["roast"],
            "horoscope": ai["horoscope"],
            "advice": ai["advice"],
        }
