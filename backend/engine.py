import os
import random
import openai

ERAS = {
    "doomscroll_renaissance": {
        "name": "Doomscrolling Renaissance",
        "emoji": "📜🔥",
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
        "emoji": "✨📸",
        "colors": ["#2a1b38", "#e040fb", "#ff80ab"],
        "gradient": "linear-gradient(135deg, #2a1b38, #e040fb, #ff80ab)",
        "description": "You post like you have 10M followers but your most liked post is 'happy birthday mom.' Still maintaining the aesthetic. Still believing in the grind.",
        "tagline": "fake it till you make it — but like, actually",
        "aesthetic": "ring light in a messy room posting like you're in a penthouse",
        "spirit_website": "TikTok",
        "spirit_animal": "Peacock in a parking lot"
    },
    "archive_mode": {
        "name": "Archive Mode",
        "emoji": "🔖🗃️",
        "colors": ["#0d1b2a", "#1b998b", "#2ec4b6"],
        "gradient": "linear-gradient(135deg, #0d1b2a, #1b998b, #2ec4b6)",
        "description": "Your bookmarks folder has 4,892 unread tabs. You save articles with the intention of becoming a completely new person. You do not become that person.",
        "tagline": "collecting information like dragon hoarding gold",
        "aesthetic": "127 open tabs with 'i need to read this' written in a note you never opened",
        "spirit_website": "Pocket / Pinterest",
        "spirit_animal": "Squirrel with 900 acorns and no winter prep"
    },
    "main_character_podcast": {
        "name": "Main Character Podcast Era",
        "emoji": "🎙️💅",
        "colors": ["#1a1a2e", "#e94560", "#f38181"],
        "gradient": "linear-gradient(135deg, #1a1a2e, #e94560, #f38181)",
        "description": "You narrate your life like you're hosting. Group chats get paragraphs. Your Spotify Wrapped is a TED talk waiting to happen. Everything is content.",
        "tagline": "sorry i missed your text i was recording a voice note to myself",
        "aesthetic": "talking to your phone camera at the mall like someone is watching",
        "spirit_website": "Substack / Podcasts",
        "spirit_animal": "Golden retriever who found a podcast microphone"
    },
    "ghost_protocol": {
        "name": "Ghost Protocol",
        "emoji": "👻🕳️",
        "colors": ["#0a0a0a", "#4a4a6a", "#7a7a9a"],
        "gradient": "linear-gradient(135deg, #0a0a0a, #4a4a6a, #7a7a9a)",
        "description": "You are everywhere and nowhere. You read every message but reply to none. You know EVERYTHING but say NOTHING. The internet's best kept secret.",
        "tagline": "present in the mind, absent from the group chat",
        "aesthetic": "staring into the void while the void stares directly at their search history",
        "spirit_website": "Reddit (lurker account)",
        "spirit_animal": "Cat. Not even a ghost cat. Just a cat."
    },
    "parasocial_peak": {
        "name": "Parasocial Peak",
        "emoji": "💕📺",
        "colors": ["#2a0033", "#9b59b6", "#f1c40f"],
        "gradient": "linear-gradient(135deg, #2a0033, #9b59b6, #f1c40f)",
        "description": "You can name 37 YouTubers' birthdays. You've felt emotions about people who don't know you exist. And honestly you wouldn't change a thing.",
        "tagline": "they feel like friends. they are not your friends. you know this. it doesn't matter.",
        "aesthetic": "watching a 3-hour lore video at 2am and feeling personally attacked by the ending",
        "spirit_website": "YouTube / Twitch",
        "spirit_animal": "Koala clinging to a cardboard cutout"
    },
    "algorithm_slave": {
        "name": "Algorithm Slave",
        "emoji": "🤖🌀",
        "colors": ["#001a33", "#00b4d8", "#90e0ef"],
        "gradient": "linear-gradient(135deg, #001a33, #00b4d8, #90e0ef)",
        "description": "Your FYP controls your life and you've accepted it. You didn't choose the scroll life. You got assigned a video about cleaning products and now your bathroom has 47 new items.",
        "tagline": "i watched a 40-minute tiktok about concrete. i don't even live near concrete.",
        "aesthetic": "falling down a rabbit hole about mushroom foraging when you set out to check the weather",
        "spirit_website": "TikTok / Instagram Reels",
        "spirit_animal": "Moth but the lamp is the algorithm"
    },
    "cottagecore_internet": {
        "name": "Cottagecore Internet",
        "emoji": "🌸🍵",
        "colors": ["#4a2c2a", "#98a8b3", "#d4b483"],
        "gradient": "linear-gradient(135deg, #4a2c2a, #98a8b3, #d4b483)",
        "description": "Your internet is Pinterest boards of sourdough, Instagram accounts of cabins, and 15 saved recipes you will never make. You dream of a quiet life but currently live above a gym.",
        "tagline": "soft life in a hard world",
        "aesthetic": "curating a digital garden while surrounded by the chaos of modern existence",
        "spirit_website": "Pinterest / GoodNotes",
        "spirit_animal": "Capybara in a garden"
    }
}

SCORES = {
    "doomscroll_renaissance": 0,
    "delulu_influencer": 0,
    "archive_mode": 0,
    "main_character_podcast": 0,
    "ghost_protocol": 0,
    "parasocial_peak": 0,
    "algorithm_slave": 0,
    "cottagecore_internet": 0
}

QUESTIONS = [
    {
        "question": "It's 11 PM. You're in bed. What's actually happening?",
        "options": [
            {"text": "📱 3 apps open: X, Discord, and something I saved at 6 PM to 'read later'", "era": "doomscroll_renaissance"},
            {"text": "📸 Taking 47th attempt at something aesthetic for tomorrow's post", "era": "delulu_influencer"},
            {"text": "🔖 Found a 25-minute essay. Bookmarked it. Will never read it.", "era": "archive_mode"},
            {"text": "🛌 Actually sleeping. Who am I? A ghost. Nobody's texting me.", "era": "ghost_protocol"}
        ]
    },
    {
        "question": "A celebrity you follow gets cancelled. Your immediate response?",
        "options": [
            {"text": "📋 I've already read their entire post history from 2014 and built a timeline", "era": "doomscroll_renaissance"},
            {"text": "💭 'I still stan fr' ... I'm not saying this out loud though", "era": "parasocial_peak"},
            {"text": "🤔 'Hot take: this is nuanced' — already drafting my Substack post", "era": "main_character_podcast"},
            {"text": "💅 Unrelated but this reminds me I have a brand deal to post about", "era": "delulu_influencer"}
        ]
    },
    {
        "question": "Your screen time app just sent the weekly report. You look and see:",
        "options": [
            {"text": "⏰ 6h 23m on TikTok. The algorithm showed me one video about sourdough and I've been here since", "era": "algorithm_slave"},
            {"text": "📊 4h 15m but if you count time 'just checking' Instagram, it's more like 8", "era": "doomscroll_renaissance"},
            {"text": "📱 5h and the top app is 'Notes' because I'm writing ideas for content", "era": "delulu_influencer"},
            {"text": "🤔 1h 12m. My screen time app is lying to me or I am dissociating efficiently", "era": "ghost_protocol"}
        ]
    },
    {
        "question": "Your group chat sends a message. What happens:",
        "options": [
            {"text": "📕 Read it. Understood it fully. Will never, ever respond.", "era": "ghost_protocol"},
            {"text": "🎙️ I send a 4-minute voice note explaining my perspective on a simple question", "era": "main_character_podcast"},
            {"text": "💬 Reply instantly. I was already there. I'm always there.", "era": "parasocial_peak"},
            {"text": "📱 I check it. I don't respond because I'm busy curating my own group chat's vibe", "era": "delulu_influencer"}
        ]
    },
    {
        "question": "You're at a restaurant. Food arrives. What do you do?",
        "options": [
            {"text": "📸 30 seconds of photos, 15 angles, adjusting the lighting. The meal can wait.", "era": "delulu_influencer"},
            {"text": "🍽️ Just eat. My friends know I don't do the food pic thing.", "era": "ghost_protocol"},
            {"text": "🗒️ 'Wait, I need to save the recipe for later.' I have 2,847 saved recipes.", "era": "archive_mode"},
            {"text": "😭 'Okay so when I was here last month...' I'm telling the full story. Everyone stays.", "era": "main_character_podcast"}
        ]
    },
    {
        "question": "What does your Spotify 'Wrapped' usually reveal about you?",
        "options": [
            {"text": "🎧 I listened to one album 892 times. It was a podcast about true crime.", "era": "parasocial_peak"},
            {"text": "🤖 My top genre is 'YouTube background' and 'lofi beats to not think to'", "era": "algorithm_slave"},
            {"text": "🎵 It's mostly indie artists with under 1000 monthly listeners. I'm better.", "era": "cottagecore_internet"},
            {"text": "🎭 My top song is from a TikTok trend I hate but listened to 400 times anyway", "era": "doomscroll_renaissance"}
        ]
    },
    {
        "question": "Someone asks 'how are you?' over text. You:",
        "options": [
            {"text": "📝 'Honestly? Let me tell you...' [proceeds to send 900 words]", "era": "main_character_podcast"},
            {"text": "👀 Leave it on read. They'll figure it out.", "era": "ghost_protocol"},
            {"text": "🌻 'living my best life!' (this is a lie. everything is fine. everything is terrible.)", "era": "cottagecore_internet"},
            {"text": "🤔 Type 'good! you?' then delete it and write the definitive answer to their question", "era": "archive_mode"}
        ]
    },
    {
        "question": "Pick the homepage that would actually make you stay:",
        "options": [
            {"text": "📺 YouTube: 47 recommended videos, 3 of them 2-hour longform documentaries", "era": "parasocial_peak"},
            {"text": "🔍 Google: 89 open tabs, half of them from last week, zero closed", "era": "algorithm_slave"},
            {"text": "📌 Pinterest: 500 boards including 'aesthetic i will never achieve'", "era": "cottagecore_internet"},
            {"text": "📰 X: The timeline knows your opinions better than you do", "era": "doomscroll_renaissance"}
        ]
    }
]

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

AI_PROMPTS = {
    "roast": "Write a SHORT fun roast (2 sentences max) about someone who got '{era_name}' as their internet era. Make it feel personal, funny, and slightly mean in a loving way. No generic stuff.",
    "horoscope": "Write a SHORT internet horoscope (1-2 sentences) for this person's week ahead. Make it specific to their internet era. Funny, slightly unhinged.",
    "advice": "Give one piece of SHORT absurd but relatable advice (1 sentence max) for someone in '{era_name}' era. Make it sound like a wellness guru who lost it."
}

class InternetEraEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        if not self.api_key:
            self.api_key = os.environ.get("OPENAI_API_KEY", "")
        
        self.model = os.environ.get("VIBE_MODEL", "openai/gpt-4o-mini")
        self.client = None
        if self.api_key:
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url=os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
            )

    def score_answers(self, answers: list[int]) -> dict:
        """Score quiz answers and determine the era"""
        scores = dict(SCORES)
        
        for q_idx, a_idx in enumerate(answers):
            if q_idx < len(QUESTIONS):
                era_key = QUESTIONS[q_idx]["options"][a_idx]["era"]
                scores[era_key] += 1
        
        winner = max(scores, key=scores.get)
        data = ERAS[winner]
        
        runner_up = max((k for k in scores if k != winner), key=lambda k: scores[k])
        
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
            "runner_up": ERAS[runner_up],
            "total_score": sum(scores.values())
        }

    def generate_ai_content(self, era_name: str) -> dict:
        """Generate roast, horoscope, and advice using AI"""
        if not self.client:
            return {
                "roast": f"You got {era_name} and honestly it tracks. Your search history would make a therapist retire early.",
                "horoscope": "This week: you'll discover a new app that consumes 47% of your life. You'll adapt. You always do.",
                "advice": "Close your eyes. Now open them. Check your phone again. Yeah. This is your life."
            }
        
        results = {}
        for key, prompt in AI_PROMPTS.items():
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt.format(era_name=era_name)}
                    ],
                    temperature=0.9,
                    max_tokens=150
                )
                results[key] = response.choices[0].message.content.strip().strip('"').strip("'")
            except Exception:
                results[key] = None
        
        # Fallback for any failed calls
        defaults = {
            "roast": f"You got {era_name} and honestly your screen time report is judging you.",
            "horoscope": "This week the algorithm will show you something that changes everything. It will be a recipe you'll never make.",
            "advice": f"The healthiest thing you could do right now is close this app. You won't though. That's very {era_name} of you."
        }
        
        for key in AI_PROMPTS:
            if not results.get(key):
                results[key] = defaults[key]
        
        return results

    def analyze(self, answers: list[int]) -> dict:
        """Full analysis pipeline"""
        scores = self.score_answers(answers)
        content = self.generate_ai_content(scores["name"])
        
        return {**scores, **content}
