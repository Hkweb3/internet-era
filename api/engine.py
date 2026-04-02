import os
import json
import hashlib
import openai

ARCHETYPES = {
    "main_character": {
        "name": "Main Character Energy",
        "icon": "🌟",
        "desc": "You radiate confidence and purpose. People don't just notice you - they remember you. Your vibe is unapologetically authentic and magnetic.",
        "colors": ["#FF6B6B", "#FFA07A", "#FFD700"],
        "aesthetic": "golden hour cinematic"
    },
    "dark_academia": {
        "name": "Dark Academic",
        "icon": "📚",
        "desc": "Mysterious, intellectual, and deeply thoughtful. You're the person who reads at 2 AM and has profound conversations in coffee shops.",
        "colors": ["#2C1810", "#8B6914", "#DEB887"],
        "aesthetic": "candlelit library at midnight"
    },
    "soft_babygirl": {
        "name": "Soft & Ethereal",
        "icon": "🦋",
        "desc": "Gentle, dreamy, and deeply empathetic. You have a calming presence that makes people feel safe. Your energy is like a warm hug.",
        "colors": ["#DDA0DD", "#FFB6C1", "#E6E6FA"],
        "aesthetic": "pastel clouds at sunset"
    },
    "chaos_gremlin": {
        "name": "Chaos Gremlin",
        "icon": "👾",
        "desc": "Unpredictable, hilarious, and brilliantly chaotic. You're the friend who turns a normal Tuesday into an unforgettable story.",
        "colors": ["#00FF00", "#FF1493", "#4B0082"],
        "aesthetic": "neon signs in a rainstorm"
    },
    "golden_retriever": {
        "name": "Golden Retreiver Energy", 
        "color_palette": ["#FFD700", "#FFA500", "#FFFACD"],
        "icon": "🐕",
        "desc": "Eternally optimistic, endlessly loyal, perpetually excited. You bring joy to every room and make everyone feel like they're your favorite person.",
        "colors": ["#FFD700", "#FFA500", "#FFFACD"],
        "aesthetic": "sunflower field in June"
    },
    "villain_arc": {
        "name": "In Their Villain Era",
        "icon": "🖤",
        "desc": "Done with people-pleasing, unapologetically setting boundaries. You radiate 'I've been through the storm and emerged darker, wiser, and stronger'.",
        "colors": ["#1A1A1A", "#8B0000", "#4B0082"],
        "aesthetic": "thunderstorm over gothic architecture"
    },
    "cottagecore": {
        "name": "Cottagecore Soul",
        "icon": "🌿",
        "desc": "You want peace, simplicity, and connection to nature. Your vibe is sourdough starters, pressed flowers, and slow mornings with tea.",
        "colors": ["#8FBC8F", "#F5DEB3", "#DDA0DD"],
        "aesthetic": "sun-dappled forest meadow"
    },
    "corporate_meltdown": {
        "name": "Corporate Meltdown",
        "icon": "💼🔥",
        "desc": "Professionally unhinged. You're the person who sends emails at 3 AM with passive-aggressive perfection. Burnout chic is your aesthetic.",
        "colors": ["#708090", "#FF6347", "#2F4F4F"],
        "aesthetic": "fluorescent lighting meets existential crisis"
    },
    "y2k_dream": {
        "name": "Y2K Dream",
        "icon": "💿",
        "desc": "Nostalgic, trendy, and living in your own pop music video. Butterfly clips, bedazzled everything, and early 2000s energy in text form.",
        "colors": ["#FF69B4", "#00CED1", "#FFD700"],
        "aesthetic": "bedazzled flip phone in a pool"
    },
    "main_character_energy": {
        "name": "Main Character",
        "icon": "🌟", 
        "desc": "You radiate confidence and purpose. People don't just notice you - they remember you. Your vibe is unapologetically authentic and magnetic.",
        "colors": ["#FFD700", "#FFA500", "#FFF8DC"],
        "aesthetic": "golden hour, wind in hair, slow motion"
    },
    "delulu_queen": {
        "name": "Delulu Queen/King",
        "icon": "👑",
        "desc": "Delusionally optimistic and thriving for it. You see signs where there are none and somehow it works out. Your delulu is your superpower.",
        "colors": ["#FF69B4", "#FFB6C1", "#FFE4B5"],
        "aesthetic": "pink clouds and glitter"
    }
}

AURAS = {
    "electric_blue": {"name": "Electric Blue", "emoji": "⚡", "desc": "Magnetic energy - you light up any space"},
    "warm_gold": {"name": "Warm Gold", "emoji": "✨", "desc": "Nurturing warmth - healing energy"},
    "deep_purple": {"name": "Deep Purple", "emoji": "🔮", "desc": "Mystical depth - mysterious and wise"},
    "forest_green": {"name": "Forest Green", "emoji": "🌿", "desc": "Grounded growth - steady and evolving"},
    "sunset_orange": {"name": "Sunset Orange", "emoji": "🌅", "desc": "Creative fire - passionate and artistic"},
    "icy_white": {"name": "Icy White", "emoji": "❄️", "desc": "Clean precision - sharp mind"},
    "rose_pink": {"name": "Rose Pink", "emoji": "🌹", "desc": "Loving depth - romantic and empathetic"},
    "void_black": {"name": "Void Black", "emoji": "🖤", "desc": "Infinite depth - complex and layered"}
}

SYSTEM_PROMPT = """You are a Vibe Analyzer - an AI that reads someone's text and generates a detailed personality analysis.
Analyze the writing style, tone, vocabulary, word choices, emoji usage (if any), and overall energy.

Output ONLY valid JSON matching this exact structure:
{
    "archetype": "one_of_the_archetype_keys",
    "vibe_score": {
        "authenticity": 0-100,
        "chaos": 0-100, 
        "intellect": 0-100,
        "warmth": 0-100,
        "intensity": 0-100
    },
    "aesthetic": "one poetic phrase describing their aesthetic",
    "red_flags": ["flag1", "flag2", "flag3"],
    "green_flags": ["flag1", "flag2", "flag3"],
    "famous_match": "a celebrity/public figure match",
    "famous_match_reason": "why they match",
    "quote": "a quote that perfectly captures their vibe",
    "energy": "a 2-3 word description of their energy",
    "aura": "a description of their aura color/quality"
}

Rules:
- Be specific and personal, not generic
- Red/green flags should be funny but accurate
- Make it feel like a friend who gets them
- Keep quotes short and punchy
- Be genuinely insightful about their writing style and personality signals"""

class VibeAnalyzer:
    def __init__(self):
        api_key=os.env...EY") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("No API key found. Set OPENROUTER_API_KEY or OPENAI_API_KEY")
        
        self.client = openai.OpenAI(
            api_key=***
            base_url=os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        )
        self.model = os.environ.get("VIBE_MODEL", "openai/gpt-4o-mini")
    
    def analyze(self, text: str, name: str) -> dict:
        """Generate full vibe analysis from text"""
        
        # Truncate if too long
        if len(text) > 5000:
            text = text[:5000] + "..."
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Analyze this person's vibe: {text}"}
            ],
            temperature=0.8,
            max_tokens=***
            response_format={"type": "json_object"}
        )
        
        try:
            raw = json.loads(response.choices[0].message.content)
            
            # Get archetype data
            arch_key = raw.get("archetype", "main_character")
            archetype_data = self._get_archetype(arch_key)
            
            # Determine aura
            aura_key = self._match_aura(raw.get("aura", ""), archetype_data)
            aura = AURAS[aura_key]
            
            return {
                "archetype": archetype_data["name"],
                "archetype_icon": archetype_data["icon"],
                "archetype_desc": archetype_data["desc"],
                "vibe_score": raw.get("vibe_score", {
                    "authenticity": 75, "chaos": 50, 
                    "intellect": 65, "warmth": 70, "intensity": 60
                }),
                "colors": archetype_data["colors"],
                "aesthetic": raw.get("aesthetic", archetype_data.get("aesthetic", "beautiful chaos")),
                "red_flags": raw.get("red_flags", ["probably overthinks everything"]),
                "green_flags": raw.get("green_flags", ["great friend to have"]),
                "famous_match": raw.get("famous_match", "someone iconic"),
                "famous_match_reason": raw.get("famous_match_reason", "you share that special something"),
                "quote": raw.get("quote", "\"the vibe is immaculate\""),
                "aura": aura["name"],
                "aura_emoji": aura["emoji"],
                "energy": raw.get("energy", "undeniably vibey")
            }
            
        except json.JSONDecodeError:
            return self._fallback_result(name)
    
    def _get_archetype(self, key: str) -> dict:
        """Map archetype key to full archetype data"""
        # Normalize key
        key = key.lower().replace(" ", "_").replace("-", "_")
        
        for ak, av in ARCHETYPES.items():
            if ak in key or key in ak:
                return av
        
        return ARCHETYPES["main_character_energy"]
    
    def _match_aura(self, aura_desc: str, archetype: dict) -> str:
        """Map aura description to aura key"""
        desc = aura_desc.lower()
        
        for ak, av in AURAS.items():
            if av["name"].lower() in desc or ak.lower().replace("_", " ") in desc:
                return ak
        
        # Default based on archetype vibe
        default_map = {
            "villain_arc": "void_black",
            "golden_retriever": "warm_gold", 
            "chaos_gremlin": "electric_blue",
            "soft_babygirl": "rose_pink"
        }
        
        for ak in default_map:
            if ak in archetype.get("name", "").lower():
                return default_map[ak]
        
        return "warm_gold"
    
    def _fallback_result(self, name: str) -> dict:
        """Fallback if AI analysis fails"""
        return {
            "archetype": "Main Character Energy",
            "archetype_icon": "🌟",
            "archetype_desc": f"{name}, your vibe is giving main character energy.",
            "vibe_score": {
                "authenticity": 85, "chaos": 45,
                "intellect": 70, "warmth": 80, "intensity": 65
            },
            "colors": ["#FFD700", "#FFA500", "#FFF8DC"],
            "aesthetic": "golden hour energy",
            "red_flags": [
                "probably overthinks every text they send",
                "has 47 browser tabs open at all times"
            ],
            "green_flags": [
                "incredibly self-aware",
                "makes every group chat better"
            ],
            "famous_match": "Zendaya",
            "famous_match_reason": "effortlessly cool with depth",
            "quote": "\"the vibe is immaculate\"",
            "aura": "Warm Gold",
            "aura_emoji": "✨",
            "energy": "undeniably vibey"
        }
