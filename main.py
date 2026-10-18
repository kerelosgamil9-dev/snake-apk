import json, os, math
from datetime import datetime
from kivy.app import App
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, Ellipse, Line, Mesh
from kivy.metrics import dp
from random import choice, randint, uniform

try:
    import arabic_reshaper
    _reshaper = arabic_reshaper.ArabicReshaper({
        "delete_harakat": True,
        "support_ligatures": False,
        "use_unshaped_instead_of_isolated": True,
    })
    ARABIC_OK = True
except Exception:
    ARABIC_OK = False

FONT_OK = False
try:
    _font_dir = os.path.dirname(os.path.abspath(__file__))
    resource_add_path(_font_dir)
    _reg = os.path.join(_font_dir, "Cairo-Regular.ttf")
    _bold = os.path.join(_font_dir, "Cairo-Bold.ttf")
    if os.path.exists(_reg) and os.path.exists(_bold):
        LabelBase.register(name="Arabic", fn_regular=_reg, fn_bold=_bold)
        FONT_OK = True
except Exception:
    FONT_OK = False


def ar(text):
    if not ARABIC_OK:
        return text
    try:
        result_lines = []
        for line in text.split("\n"):
            tokens = line.split(" ")
            processed = []
            for tok in tokens:
                if not tok:
                    processed.append("")
                    continue
                has_ar = any('\u0600' <= c <= '\u06ff' for c in tok)
                if has_ar:
                    shaped = _reshaper.reshape(tok)
                    processed.append(shaped[::-1])
                else:
                    processed.append(tok)
            result_lines.append(" ".join(processed[::-1]))
        return "\n".join(result_lines)
    except Exception:
        return text


TEXTS = {
    "en": {
        "snake": "SNAKE", "score": "Score", "best": "Best",
        "menu": "MENU", "theme": "Theme: Night", "theme_day": "Theme: Day",
        "top5": "Top 5 Scores", "sound": "Sound", "vibration": "Vibration",
        "close": "Close", "language": "Language: AR",
        "on": "ON", "off": "OFF",
        "choose_diff": "Choose Difficulty", "speed": "Speed",
        "easy": "EASY\n(pass through walls)",
        "normal": "NORMAL\n(walls kill you)",
        "hard": "HARD\n(survive + bombs)",
        "gold_hint": "Gold apple = 50 pts!",
        "swipe": "Swipe your finger to steer",
        "choose_start": "Choose a difficulty to start",
        "game_over_r": "Game Over! Press R to restart",
        "game_over": "Game Over!", "choose_settings": "Choose settings",
        "no_scores": "No scores yet", "top5_title": "TOP 5",
        "tap_to_resume": "Tap to resume",
        "rules": "Game Rules", "rules_title": "GAME RULES",
        "rule_red": "+10 points", "rule_gold": "+50 points (HARD: +5 sec)",
        "rule_blue": "Slow down 5 sec", "rule_purple": "Pass through self 5 sec",
        "rule_bomb": "Lose 1 life", "rule_lives": "3 lives",
        "achievements": "Achievements", "achv_title": "ACHIEVEMENTS",
        "coins": "Coins", "unlocked": "Unlocked", "locked": "Locked",
        "new_achievement": "Achievement Unlocked!",
        "collect": "Collect",
        "shop": "Shop", "shop_title": "SHOP",
        "tab_skins": "Skins", "tab_colors": "Colors", "tab_helpers": "Helpers",
        "buy": "Buy", "equip": "Equip", "equipped": "Equipped",
        "owned": "Owned", "not_enough": "Not enough coins",
        "shield": "Shield", "slow": "Slow",
        "shield_desc": "Protects for 7 sec",
        "slow_desc": "Slows for 5 sec",
        "quantity": "Qty",
    },
    "ar": {
        "snake": "الثعبان", "score": "النقاط", "best": "الأفضل",
        "menu": "القائمة", "theme": "الثيم ليلي", "theme_day": "الثيم نهاري",
        "top5": "أعلى خمس نتائج", "sound": "الصوت", "vibration": "الاهتزاز",
        "close": "إغلاق", "language": "اللغة EN",
        "on": "تشغيل", "off": "إيقاف",
        "choose_diff": "اختر المستوى", "speed": "السرعة",
        "easy": "سهل", "normal": "عادي", "hard": "صعب",
        "gold_hint": "التفاحة الذهبية خمسين نقطة",
        "swipe": "اسحب بإصبعك", "choose_start": "اختر مستوى",
        "game_over_r": "انتهت اضغط R", "game_over": "انتهت اللعبة",
        "choose_settings": "الإعدادات", "no_scores": "لا توجد نتائج",
        "top5_title": "أعلى خمس", "tap_to_resume": "المس الشاشة للاستمرار",
        "rules": "قوانين اللعبة", "rules_title": "قوانين اللعبة",
        "rule_red": "عشر نقاط", "rule_gold": "خمسون نقطة",
        "rule_blue": "تبطيء خمس ثواني", "rule_purple": "عبور الذات خمس ثواني",
        "rule_bomb": "تخسر حياة", "rule_lives": "ثلاث حياوات",
        "achievements": "الإنجازات", "achv_title": "الإنجازات",
        "coins": "العملات",
        "unlocked": "مفتوح", "locked": "مقفول",
        "new_achievement": "إنجاز جديد",
        "collect": "اجمع",
        "shop": "المتجر", "shop_title": "المتجر",
        "tab_skins": "الأشكال", "tab_colors": "الألوان", "tab_helpers": "المساعدات",
        "buy": "اشتر", "equip": "استخدم", "equipped": "مستخدم",
        "owned": "مملوك", "not_enough": "عملات غير كافية",
        "shield": "درع", "slow": "ساعة",
        "shield_desc": "حماية سبع ثواني",
        "slow_desc": "تبطيء خمس ثواني",
        "quantity": "العدد",
    }
}


SKINS = [
    {"id": "classic", "name_en": "Classic", "name_ar": "كلاسيكي",
     "price": 0, "thickness": 0.37, "style": "normal"},
    {"id": "thin", "name_en": "Thin", "name_ar": "رقيق",
     "price": 80, "thickness": 0.22, "style": "normal"},
    {"id": "thick", "name_en": "Thick", "name_ar": "سميك",
     "price": 80, "thickness": 0.50, "style": "normal"},
    {"id": "round", "name_en": "Round", "name_ar": "دائري",
     "price": 100, "thickness": 0.38, "style": "round"},
]

COLORS = [
    {"id": "green", "name_en": "Green", "name_ar": "أخضر",
     "price": 0, "body": (0.15, 0.8, 0.3, 1),
     "head": (0.55, 1, 0.2, 1)},
    {"id": "blue", "name_en": "Blue", "name_ar": "أزرق",
     "price": 50, "body": (0.2, 0.55, 0.95, 1),
     "head": (0.4, 0.75, 1.0, 1)},
    {"id": "purple", "name_en": "Purple", "name_ar": "بنفسجي",
     "price": 50, "body": (0.6, 0.25, 0.9, 1),
     "head": (0.75, 0.45, 1.0, 1)},
    {"id": "red", "name_en": "Red", "name_ar": "أحمر",
     "price": 50, "body": (0.9, 0.2, 0.25, 1),
     "head": (1.0, 0.4, 0.4, 1)},
    {"id": "gold", "name_en": "Gold", "name_ar": "ذهبي",
     "price": 80, "body": (0.9, 0.7, 0.15, 1),
     "head": (1.0, 0.85, 0.3, 1)},
]


def _build_achievements():
    out = []
    score_data = [(50, 3), (100, 5), (200, 8), (400, 15), (500, 20),
                  (600, 25), (700, 30), (800, 40), (900, 50), (1000, 75)]
    for th, c in score_data:
        out.append({"id": f"score_{th}", "type": "score", "th": th, "coins": c,
                    "en": f"Reach a score of {th}", "ar": f"حقق نتيجة {th}", "icon": "star"})
    red_data = [(10, 5), (50, 10), (100, 20), (200, 35), (300, 50), (400, 70), (500, 100)]
    for th, c in red_data:
        out.append({"id": f"apple_red_{th}", "type": "apple_red", "th": th, "coins": c,
                    "en": f"Eat {th} red apples", "ar": f"كل {th} تفاحة حمراء", "icon": "red"})
    gold_data = [(10, 5), (30, 12), (70, 25), (100, 40), (150, 60)]
    for th, c in gold_data:
        out.append({"id": f"apple_gold_{th}", "type": "apple_gold", "th": th, "coins": c,
                    "en": f"Eat {th} gold apples", "ar": f"كل {th} تفاحة ذهبية", "icon": "gold"})
    blue_data = [(10, 5), (20, 7), (30, 10), (50, 20), (70, 30)]
    for th, c in blue_data:
        out.append({"id": f"apple_blue_{th}", "type": "apple_blue", "th": th, "coins": c,
                    "en": f"Eat {th} blue apples", "ar": f"كل {th} تفاحة زرقاء", "icon": "blue"})
    purple_data = [(10, 5), (20, 7), (30, 10), (50, 20), (70, 30)]
    for th, c in purple_data:
        out.append({"id": f"apple_purple_{th}", "type": "apple_purple", "th": th, "coins": c,
                    "en": f"Eat {th} purple apples", "ar": f"كل {th} تفاحة بنفسجية", "icon": "purple"})
    hard_data = [(20, 5), (50, 15), (70, 25), (100, 40), (150, 60)]
    for th, c in hard_data:
        out.append({"id": f"hard_{th}", "type": "hard_survival", "th": th, "coins": c,
                    "en": f"Score {th} in HARD mode", "ar": f"حقق {th} نقطة في الصعب", "icon": "hard"})
    return out


ACHIEVEMENTS = _build_achievements()


class Vibrator:
    def __init__(self):
        self.available = False
        self.enabled = True
        try:
            from plyer import vibrator
            self.vibrator = vibrator
            self.available = True
        except Exception:
            self.vibrator = None

    def buzz(self, duration=0.1):
        if self.available and self.enabled:
            try:
                self.vibrator.vibrate(duration)
            except Exception:
                pass


THEMES = {
    "dark": {"bg": (0.035, 0.055, 0.07, 1), "cell": (0.10, 0.15, 0.17, 1),
             "food": (0.95, 0.15, 0.2, 1), "gold": (1.0, 0.85, 0.2, 1)},
    "light": {"bg": (0.92, 0.94, 0.96, 1), "cell": (0.82, 0.86, 0.90, 1),
              "food": (0.95, 0.15, 0.2, 1), "gold": (1.0, 0.85, 0.2, 1)},
}
THEME_ORDER = ["dark", "light"]


def get_save_path():
    if platform == "android":
        try:
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), "snake_save.json")
        except Exception:
            return "snake_save.json"
    return "snake_save.json"


SAVE_PATH = get_save_path()


class SaveManager:
    def __init__(self, path=None):
        self.path = path or SAVE_PATH

    def load(self):
        defaults = {
            "high_score": 0, "speed": 5, "wrap": True,
            "theme": "dark", "sound_on": True, "vibration_on": True,
            "leaderboard": [], "language": "en",
            "achievements": {}, "counters": {}, "coins": 0,
            "hard_best": 0, "claimed": {},
            "owned_skins": ["classic"],
            "owned_colors": ["green"],
            "current_skin": "classic",
            "current_color": "green",
            "helpers": {"shield": 0, "slow": 0},
        }
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "claimed" not in data:
                data["claimed"] = {k: True for k, v in
                                   data.get("achievements", {}).items() if v}
            for k, v in defaults.items():
                data.setdefault(k, v)
            return data
        except Exception:
            return defaults

    def save(self, **kwargs):
        data = self.load()
        data.update(kwargs)
        try:
            tmp = self.path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(tmp, self.path)
        except Exception:
            pass

    def add_to_leaderboard(self, score):
        data = self.load()
        board = data.get("leaderboard", [])
        board.append({"score": score, "date": datetime.now().strftime("%Y-%m-%d")})
        board.sort(key=lambda x: x["score"], reverse=True)
        board = board[:5]
        self.save(leaderboard=board)
        return board


class AppleIcon(Widget):
    def __init__(self, apple_type="red", **kwargs):
        super().__init__(**kwargs)
        self.apple_type = apple_type
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *args):
        self.canvas.clear()
        if self.width <= 0 or self.height <= 0:
            return
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        size = min(self.width, self.height) * 0.85
        with self.canvas:
            if self.apple_type == "gold":
                bcol = (1.0, 0.85, 0.2, 1); dcol = (0.7, 0.55, 0.1, 1)
            elif self.apple_type == "blue":
                bcol = (0.30, 0.60, 1.0, 1); dcol = (0.15, 0.3, 0.6, 1)
            elif self.apple_type == "purple":
                bcol = (0.70, 0.30, 1.0, 1); dcol = (0.4, 0.15, 0.6, 1)
            elif self.apple_type == "star":
                pts = []
                for i in range(10):
                    a = math.pi / 2 + i * math.pi / 5
                    r = size * 0.45 if i % 2 == 0 else size * 0.2
                    pts.extend([cx + math.cos(a) * r, cy + math.sin(a) * r])
                Color(1, 0.85, 0.2, 1)
                Line(points=pts + pts[:2], width=max(2, size * 0.08))
                return
            elif self.apple_type == "coin":
                Color(0.65, 0.45, 0.05, 1)
                Ellipse(pos=(cx - size * 0.45, cy - size * 0.45),
                        size=(size * 0.9, size * 0.9))
                Color(1.0, 0.82, 0.15, 1)
                Ellipse(pos=(cx - size * 0.39, cy - size * 0.39),
                        size=(size * 0.78, size * 0.78))
                Color(0.85, 0.62, 0.08, 1)
                Line(circle=(cx, cy, size * 0.27), width=max(1.2, size * 0.04))
                Color(1, 0.95, 0.6, 0.9)
                Line(points=[cx - size * 0.1, cy - size * 0.12,
                             cx - size * 0.1, cy + size * 0.12],
                     width=max(1.5, size * 0.06))
                return
            elif self.apple_type == "hard":
                Color(1, 0.3, 0.4, 1)
                Ellipse(pos=(cx - size * 0.4, cy - size * 0.4),
                        size=(size * 0.8, size * 0.8))
                Color(1, 1, 1, 1)
                Line(points=[cx, cy, cx, cy + size * 0.2],
                     width=max(2, size * 0.08))
                Line(points=[cx, cy, cx + size * 0.15, cy],
                     width=max(2, size * 0.08))
                return
            elif self.apple_type == "bomb":
                Color(0.18, 0.18, 0.22, 1)
                Ellipse(pos=(cx - size * 0.42, cy - size * 0.42),
                        size=(size * 0.84, size * 0.84))
                Color(0.65, 0.65, 0.7, 0.85)
                Ellipse(pos=(cx - size * 0.17, cy - size * 0.13),
                        size=(size * 0.18, size * 0.15))
                Color(0.6, 0.4, 0.2, 1)
                Line(points=[cx, cy + size * 0.42,
                             cx + size * 0.13, cy + size * 0.63],
                     width=max(2, size * 0.06))
                Color(1, 0.65, 0.1, 1)
                Ellipse(pos=(cx + size * 0.07, cy + size * 0.58),
                        size=(size * 0.18, size * 0.18))
                return
            elif self.apple_type == "shield":
                Color(0.2, 0.5, 0.9, 1)
                Ellipse(pos=(cx - size * 0.4, cy - size * 0.4), size=(size * 0.8, size * 0.8))
                Color(1, 1, 1, 0.9)
                Line(circle=(cx, cy, size * 0.28), width=max(2, size * 0.08))
                return
            elif self.apple_type == "slow":
                Color(0.15, 0.25, 0.45, 1)
                Ellipse(pos=(cx - size * 0.4, cy - size * 0.4), size=(size * 0.8, size * 0.8))
                Color(0.95, 0.95, 0.98, 1)
                Ellipse(pos=(cx - size * 0.3, cy - size * 0.3), size=(size * 0.6, size * 0.6))
                Color(0.15, 0.25, 0.45, 1)
                Line(points=[cx, cy, cx, cy + size * 0.2], width=max(2, size * 0.06), cap='round')
                Line(points=[cx, cy, cx + size * 0.15, cy], width=max(2, size * 0.06), cap='round')
                return
            else:
                bcol = (0.95, 0.15, 0.2, 1); dcol = (0.55, 0.1, 0.15, 1)
            Color(0, 0, 0, 0.25)
            Ellipse(pos=(cx - size * 0.35, cy - size * 0.45),
                    size=(size * 0.7, size * 0.2))
            Color(*dcol)
            Ellipse(pos=(cx - size * 0.45, cy - size * 0.42),
                    size=(size * 0.9, size * 0.85))
            Color(*bcol)
            Ellipse(pos=(cx - size * 0.4, cy - size * 0.38),
                    size=(size * 0.8, size * 0.76))
            Color(1, 1, 1, 0.85)
            Ellipse(pos=(cx - size * 0.13, cy + size * 0.05),
                    size=(size * 0.2, size * 0.24))
            Color(1, 1, 1, 0.55)
            Ellipse(pos=(cx - size * 0.05, cy + size * 0.18),
                    size=(size * 0.09, size * 0.1))
            Color(0.35, 0.2, 0.1, 1)
            Rectangle(pos=(cx - size * 0.03, cy + size * 0.38),
                      size=(size * 0.06, size * 0.22))
            Color(0.3, 0.7, 0.25, 1)
            Ellipse(pos=(cx + size * 0.02, cy + size * 0.42),
                    size=(size * 0.24, size * 0.14))


class LivesIcon(Widget):
    def __init__(self, count=3, **kwargs):
        super().__init__(**kwargs)
        self.count = count
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *args):
        self.canvas.clear()
        if self.width <= 0 or self.height <= 0:
            return
        n = self.count
        size = min(self.height * 0.85, self.width / (n + 1))
        if size < 5:
            return
        gap = size * 1.15
        total_w = gap * n
        start_x = self.x + (self.width - total_w) / 2 + gap * 0.05
        cy = self.y + self.height / 2
        with self.canvas:
            for i in range(n):
                cx = start_x + i * gap + size / 2
                self._draw_heart(cx, cy, size)

    def _draw_heart(self, cx, cy, size):
        p = size / 7
        rows = [(5, 1, 2), (5, 4, 2), (4, 0, 7), (3, 0, 7),
                (2, 1, 5), (1, 2, 3), (0, 3, 1)]
        base_x = cx - size / 2
        base_y = cy - size * 0.45
        Color(0.55, 0.05, 0.12, 1)
        for (y_lvl, sx, cnt) in rows:
            for i in range(cnt):
                x = base_x + (sx + i) * p
                y = base_y + y_lvl * p
                Rectangle(pos=(x - p * 0.15, y - p * 0.15), size=(p * 1.3, p * 1.3))
        Color(0.95, 0.15, 0.25, 1)
        for (y_lvl, sx, cnt) in rows:
            for i in range(cnt):
                x = base_x + (sx + i) * p
                y = base_y + y_lvl * p
                Rectangle(pos=(x, y), size=(p, p))
        Color(1, 0.85, 0.85, 0.95)
        Rectangle(pos=(base_x + p, base_y + 4 * p), size=(p, p))


class RefreshIcon(Widget):
    """أيقونة إعادة التشغيل: سهمين بيلفوا حوالين بعض، مرسومة بالكامل
    بتعليمات الجرافيكس (مفيش إيموجي ولا نص)."""

    def __init__(self, color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.icon_color = color
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *args):
        self.canvas.clear()
        if self.width <= 0 or self.height <= 0:
            return
        cx, cy = self.x + self.width / 2, self.y + self.height / 2
        radius = min(self.width, self.height) * 0.38
        thickness = max(2, radius * 0.22)
        with self.canvas:
            Color(*self.icon_color)
            Line(circle=(cx, cy, radius, 25, 145), width=thickness, cap='square')
            Line(circle=(cx, cy, radius, 205, 325), width=thickness, cap='square')
            self._arrowhead(cx, cy, radius, 145, thickness)
            self._arrowhead(cx, cy, radius, 325, thickness)

    def _arrowhead(self, cx, cy, radius, angle_deg, thickness):
        angle = math.radians(angle_deg)
        # point on the circle where the arc ends
        base_x = cx + radius * math.cos(angle)
        base_y = cy + radius * math.sin(angle)
        # tangent direction = direction of travel along the arc
        # (Kivy draws circle arcs counter-clockwise as the angle increases)
        tan_x = -math.sin(angle)
        tan_y = math.cos(angle)
        # radial direction = points away from the circle's center
        rad_x = math.cos(angle)
        rad_y = math.sin(angle)

        length = thickness * 2.6
        width = thickness * 1.6

        apex_x = base_x + tan_x * length * 0.6
        apex_y = base_y + tan_y * length * 0.6
        back_x = base_x - tan_x * length * 0.5
        back_y = base_y - tan_y * length * 0.5

        p1x, p1y = apex_x, apex_y
        p2x, p2y = back_x + rad_x * width, back_y + rad_y * width
        p3x, p3y = back_x - rad_x * width, back_y - rad_y * width

        Mesh(
            vertices=[p1x, p1y, 0, 0, p2x, p2y, 0, 0, p3x, p3y, 0, 0],
            indices=[0, 1, 2],
            mode='triangle_fan'
        )


class SkinPreview(Widget):
    """معاينة بصرية احترافية ومضبوطة داخل أبعاد المربع المخصص في المتجر"""
    def __init__(self, item_data, kind="skins", **kwargs):
        super().__init__(**kwargs)
        self.item_data = item_data
        self.kind = kind
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *args):
        self.canvas.clear()
        if self.width <= 0 or self.height <= 0:
            return
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2

        with self.canvas:
            if self.kind == "skins":
                thick = self.item_data.get("thickness", 0.37)
                style = self.item_data.get("style", "normal")
                # حساب نصف قطر يتناسب بوضوح مع الفرق في السمك
                r = dp(11) * (thick / 0.37)
                
                # لون الجسم والألوان
                bcol = (0.15, 0.8, 0.3, 1)
                hcol = (0.55, 1.0, 0.2, 1)

                # رسم ذيل وجسم مصغر مع رأس وعينين
                Color(*bcol)
                Ellipse(pos=(cx - dp(20) - r, cy - r), size=(2 * r, 2 * r))
                Ellipse(pos=(cx - dp(8) - r, cy - r), size=(2 * r, 2 * r))

                if style == "round":
                    Color(0.3, 0.9, 0.4, 0.8)
                    Line(circle=(cx - dp(8), cy, r), width=dp(1.2))

                # رأس الثعبان
                hr = r * 1.15
                Color(*hcol)
                Ellipse(pos=(cx + dp(6) - hr, cy - hr), size=(2 * hr, 2 * hr))

                # عين الثعبان للمعاينة
                Color(0.05, 0.1, 0.05, 1)
                Ellipse(pos=(cx + dp(8), cy + hr * 0.2), size=(dp(3.5), dp(3.5)))
                Color(1, 1, 1, 0.9)
                Ellipse(pos=(cx + dp(9), cy + hr * 0.3), size=(dp(1.2), dp(1.2)))

            elif self.kind == "colors":
                bcol = self.item_data.get("body", (0.15, 0.8, 0.3, 1))
                hcol = self.item_data.get("head", (0.55, 1, 0.2, 1))
                r = dp(11)

                Color(*bcol)
                Ellipse(pos=(cx - dp(18) - r, cy - r), size=(2 * r, 2 * r))
                Ellipse(pos=(cx - dp(6) - r, cy - r), size=(2 * r, 2 * r))

                hr = r * 1.15
                Color(*hcol)
                Ellipse(pos=(cx + dp(6) - hr, cy - hr), size=(2 * hr, 2 * hr))

                Color(0.05, 0.1, 0.05, 1)
                Ellipse(pos=(cx + dp(8), cy + hr * 0.2), size=(dp(3.5), dp(3.5)))
                Color(1, 1, 1, 0.9)
                Ellipse(pos=(cx + dp(9), cy + hr * 0.3), size=(dp(1.2), dp(1.2)))


class SnakeBoard(Widget):
    def __init__(self, theme="dark", **kwargs):
        super().__init__(**kwargs)
        self.cols = 15
        self.rows = 20
        self.score = 0
        self.high_score = 0
        self.running = True
        self.paused = True
        self.waiting_to_resume = False
        self.wrap = True
        self.hard_mode = False
        self.lives = 3
        self.bombs = []
        self.bomb_event = None
        self.survival_event = None
        self.growth_event = None
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.direction_locked = False
        self.snake = [(5, 10), (4, 10), (3, 10)]
        self.food = (9, 10)
        self.bonus_foods = []
        self.bonus_event = None
        self.bonus_spawn_counter = 0.0
        self.bonus_spawn_interval = 5.0
        self.eat_flash = 0.0
        self.hit_flash = 0.0
        self.dying = False
        self.death_index = 0
        self.theme_name = theme
        self.theme = THEMES.get(theme, THEMES["dark"])
        self.eat_sound = None
        self.over_sound = None
        self.click_sound = None
        self.sound_on = True
        self.vibrator = Vibrator()
        self.on_new_high_score = None
        self.on_game_over = None
        self.on_level_up = None
        self.on_resume_tap = None
        self.on_eat_apple = None
        self.on_achv_check = None
        self.touch_start = None
        self.min_swipe_px = dp(20)
        self.touch_dot = None
        self._current_speed = 5
        self.tongue_phase = 0.0
        self.tongue_out = 0.0
        self.particles = []
        self.popups = []
        self.slow_active = False
        self.slow_timer = None
        self.ghost_active = False
        self.ghost_timer = None
        self.ghost_phase = 0.0

        self.current_skin = SKINS[0]
        self.current_color = COLORS[0]
        self.shield_active = False
        self.shield_timer = None
        self.shield_phase = 0.0

        Clock.schedule_interval(self._animate, 0.05)
        self.bind(pos=self.draw, size=self.draw)
        self.update_event = Clock.schedule_interval(self.update, 0.15)
        Clock.schedule_once(self.load_sounds, 0.1)

    def set_skin(self, skin):
        self.current_skin = skin
        self.draw()

    def set_color(self, color):
        self.current_color = color
        self.draw()

    def activate_shield(self):
        if self.shield_timer:
            self.shield_timer.cancel()
        self.shield_active = True
        self.shield_phase = 0.0
        self.shield_timer = Clock.schedule_once(self._shield_end, 7.0)

    def _shield_end(self, dt):
        self.shield_active = False
        self.shield_timer = None

    def break_shield(self):
        if self.shield_timer:
            self.shield_timer.cancel()
            self.shield_timer = None
        self.shield_active = False

    def _animate(self, dt):
        self.tongue_phase += dt * 4
        self.tongue_out = (math.sin(self.tongue_phase) + 1) / 2
        if self.ghost_active:
            self.ghost_phase += dt * 8
        if self.shield_active:
            self.shield_phase += dt * 10
        new_p = []
        for p in self.particles:
            p["life"] -= dt
            if p["life"] > 0:
                p["x"] += p["vx"] * dt
                p["y"] += p["vy"] * dt
                p["vy"] -= 400 * dt
                new_p.append(p)
        self.particles = new_p
        new_pop = []
        for pop in self.popups:
            pop["life"] -= dt
            if pop["life"] > 0:
                pop["y"] += 60 * dt
                new_pop.append(pop)
        self.popups = new_pop
        if (self.running and not self.paused and self.width > 0) or self.particles or self.popups:
            if self.width > 0:
                self.draw()

    def add_popup(self, x, y, color):
        self.popups.append({
            "x": x, "y": y, "color": color,
            "life": 1.2, "max_life": 1.2,
            "start_size": 10, "end_size": 60
        })

    def add_burst(self, x, y, count, color):
        for _ in range(count):
            angle = uniform(0, 2 * math.pi)
            speed = uniform(120, 280)
            self.particles.append({
                "x": x, "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": uniform(0.5, 0.9),
                "max_life": 0.9,
                "size": uniform(3, 5),
                "color": color,
            })

    def _bomb_tick(self, dt):
        new_bombs = []
        for bx, by, tleft in self.bombs:
            if tleft - dt > 0:
                new_bombs.append((bx, by, tleft - dt))
        self.bombs = new_bombs
        self._spawn_bomb()

    def _spawn_bomb(self):
        if not self.hard_mode or len(self.bombs) >= 15:
            return
        for _ in range(3):
            if len(self.bombs) >= 15:
                break
            occupied = set(self.snake)
            if not self.hard_mode:
                occupied |= {self.food}
            occupied |= {(bx, by) for bx, by, _ in self.bombs}
            occupied |= {tuple(b["pos"]) for b in self.bonus_foods}
            empty = [(x, y) for x in range(self.cols) for y in range(self.rows)
                     if (x, y) not in occupied]
            if not empty:
                return
            hx, hy = self.snake[0]
            far = [(x, y) for (x, y) in empty if abs(x - hx) + abs(y - hy) >= 2]
            if not far:
                far = empty
            bx, by = choice(far)
            self.bombs.append((bx, by, 4.0))

    def _survival_tick(self, dt):
        if not self.running or self.paused:
            return
        if not self.hard_mode:
            return
        self.score += 1
        if self.score > self.high_score:
            old = self.high_score
            self.high_score = self.score
            if self.on_new_high_score:
                self.on_new_high_score(self.high_score)
            if self.on_level_up and (self.score // 100) > (old // 100):
                self.on_level_up(self.score)
        if self.on_achv_check:
            self.on_achv_check("score", self.score)
            self.on_achv_check("hard_survival", self.score)

    def _growth_tick(self, dt):
        if not self.running or self.paused:
            return
        if not self.hard_mode:
            return
        if self.snake:
            self.snake.append(self.snake[-1])

    def _bonus_tick(self, dt):
        new_bonus = []
        for b in self.bonus_foods:
            b["time"] -= dt
            if b["time"] > 0:
                new_bonus.append(b)
        self.bonus_foods = new_bonus
        self.bonus_spawn_counter += dt
        if self.bonus_spawn_counter >= self.bonus_spawn_interval:
            self.bonus_spawn_counter = 0.0
            self._try_spawn_bonus()

    def _try_spawn_bonus(self):
        if not self.running or self.paused:
            return
        if len(self.bonus_foods) >= 2:
            return
        r = randint(1, 100)
        bonus_type = None
        if self.score > 450:
            if r <= 25:
                bonus_type = "purple"
            elif r <= 60:
                bonus_type = "blue"
            elif r <= 90:
                bonus_type = "gold"
        elif self.score > 400:
            if r <= 35:
                bonus_type = "blue"
            elif r <= 75:
                bonus_type = "gold"
        else:
            if r <= 50:
                bonus_type = "gold"
        if bonus_type is None:
            return
        occupied = set(self.snake)
        if not self.hard_mode:
            occupied |= {self.food}
        occupied |= {tuple(b["pos"]) for b in self.bonus_foods}
        occupied |= {(bx, by) for bx, by, _ in self.bombs}
        empty = [(x, y) for x in range(self.cols) for y in range(self.rows)
                 if (x, y) not in occupied]
        if not empty:
            return
        hx, hy = self.snake[0]
        far = [(x, y) for (x, y) in empty if abs(x - hx) + abs(y - hy) >= 3]
        if not far:
            far = empty
        pos = choice(far)
        self.bonus_foods.append({
            "pos": pos,
            "type": bonus_type,
            "time": 3.0,
            "max_time": 3.0
        })

    def activate_slow(self):
        if self.slow_timer:
            self.slow_timer.cancel()
            self.slow_timer = None
        self.slow_active = True
        self.set_speed(self._current_speed)
        self.slow_timer = Clock.schedule_once(self._slow_end, 5.0)

    def _slow_end(self, dt):
        self.slow_active = False
        self.slow_timer = None
        self.set_speed(self._current_speed)

    def activate_ghost(self):
        if self.ghost_timer:
            self.ghost_timer.cancel()
            self.ghost_timer = None
        self.ghost_active = True
        self.ghost_timer = Clock.schedule_once(self._ghost_end, 5.0)

    def _ghost_end(self, dt):
        self.ghost_active = False
        self.ghost_timer = None

    def set_theme(self, name):
        if name in THEMES:
            self.theme_name = name
            self.theme = THEMES[name]
            self.draw()

    def load_sounds(self, *args):
        d = os.path.dirname(os.path.abspath(__file__))
        for fname, attr in [("eat.wav", "eat_sound"),
                             ("gameover.wav", "over_sound"),
                             ("click.wav", "click_sound")]:
            try:
                p = os.path.join(d, fname)
                if os.path.exists(p):
                    setattr(self, attr, SoundLoader.load(p))
            except Exception:
                pass

    def play_eat(self):
        if self.sound_on and self.eat_sound:
            try:
                self.eat_sound.stop()
                self.eat_sound.play()
            except Exception:
                pass

    def play_gameover(self):
        if self.sound_on and self.over_sound:
            try:
                self.over_sound.stop()
                self.over_sound.play()
            except Exception:
                pass

    def play_click(self):
        if self.sound_on and self.click_sound:
            try:
                self.click_sound.stop()
                self.click_sound.play()
            except Exception:
                pass

    def on_touch_down(self, touch):
        if self.waiting_to_resume:
            self.waiting_to_resume = False
            self.paused = False
            if self.on_resume_tap:
                self.on_resume_tap()
        if self.dying:
            return True
        if self.collide_point(*touch.pos):
            self.touch_start = touch.pos
            with self.canvas.after:
                Color(1, 1, 1, 0.35)
                self.touch_dot = Ellipse(
                    pos=(touch.x - dp(12), touch.y - dp(12)),
                    size=(dp(24), dp(24)))
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.touch_start and self.touch_dot:
            self.touch_dot.pos = (touch.x - dp(12), touch.y - dp(12))
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.touch_dot:
            self.canvas.after.remove(self.touch_dot)
            self.touch_dot = None
        if self.touch_start is None or self.dying:
            return super().on_touch_up(touch)
        dx = touch.x - self.touch_start[0]
        dy = touch.y - self.touch_start[1]
        self.touch_start = None
        if abs(dx) < self.min_swipe_px and abs(dy) < self.min_swipe_px:
            return super().on_touch_up(touch)
        if abs(dx) > abs(dy):
            d = (1, 0) if dx > 0 else (-1, 0)
        else:
            d = (0, 1) if dy > 0 else (0, -1)
        self.set_direction(d)
        return True

    def set_speed(self, speed):
        interval = max(0.05, 0.35 - speed * 0.028)
        if self.slow_active:
            interval *= 2.2
        if self.update_event:
            self.update_event.cancel()
        self.update_event = Clock.schedule_interval(self.update, interval)

    def speed_up_gradually(self, target, steps=5):
        self._current_speed = target
        self.set_speed(target)

    def random_food(self):
        if self.hard_mode:
            return
        occupied = set(self.snake)
        occupied |= {(bx, by) for bx, by, _ in self.bombs}
        occupied |= {tuple(b["pos"]) for b in self.bonus_foods}
        empty = [(x, y) for x in range(self.cols) for y in range(self.rows)
                 if (x, y) not in occupied]
        if not empty:
            self.running = False
            return
        self.food = choice(empty)

    def set_mode(self, wrap, hard=False):
        self.wrap = wrap
        self.hard_mode = hard
        self.paused = False
        self.waiting_to_resume = False
        self.shield_active = False
        if self.shield_timer:
            self.shield_timer.cancel()
            self.shield_timer = None
        if hard:
            self.lives = 3
            self.bombs = []
            if self.bomb_event:
                self.bomb_event.cancel()
            self.bomb_event = Clock.schedule_interval(self._bomb_tick, 2.0)
            if self.survival_event:
                self.survival_event.cancel()
            self.survival_event = Clock.schedule_interval(self._survival_tick, 1.0)
            if self.growth_event:
                self.growth_event.cancel()
            self.growth_event = Clock.schedule_interval(self._growth_tick, 5.0)
        else:
            self.lives = 0
            self.bombs = []
            if self.bomb_event:
                self.bomb_event.cancel()
                self.bomb_event = None
            if self.survival_event:
                self.survival_event.cancel()
                self.survival_event = None
            if self.growth_event:
                self.growth_event.cancel()
                self.growth_event = None
        if self.bonus_event:
            self.bonus_event.cancel()
        self.bonus_event = Clock.schedule_interval(self._bonus_tick, 0.1)
        self.bonus_spawn_counter = 0.0
        self.bonus_foods = []

    def set_direction(self, d):
        if self.direction_locked or self.dying:
            return
        dx, dy = self.direction
        nx, ny = d
        if (dx + nx, dy + ny) == (0, 0):
            return
        self.next_direction = d
        self.direction_locked = True

    def restart(self, *args):
        self.score = 0
        self.running = True
        self.dying = False
        self.death_index = 0
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.direction_locked = False
        self.snake = [(5, 10), (4, 10), (3, 10)]
        self.eat_flash = 0.0
        self.hit_flash = 0.0
        self.bombs = []
        self.bonus_foods = []
        self.bonus_spawn_counter = 0.0
        self.waiting_to_resume = False
        self.particles = []
        self.popups = []
        self.shield_active = False
        if self.shield_timer:
            self.shield_timer.cancel()
            self.shield_timer = None
        if self.slow_timer:
            self.slow_timer.cancel()
            self.slow_timer = None
        self.slow_active = False
        if self.ghost_timer:
            self.ghost_timer.cancel()
            self.ghost_timer = None
        self.ghost_active = False
        if self.hard_mode:
            self.lives = 3
        self.random_food()
        self.draw()

    def update(self, dt):
        if not self.running or self.paused or self.width <= 0:
            return
        if self.eat_flash > 0:
            self.eat_flash = max(0.0, self.eat_flash - dt * 4)
        if self.hit_flash > 0:
            self.hit_flash = max(0.0, self.hit_flash - dt * 4)
        self.direction_locked = False
        self.direction = self.next_direction
        dx, dy = self.direction
        x, y = self.snake[0]

        if self.wrap or self.shield_active:
            head = ((x + dx) % self.cols, (y + dy) % self.rows)
        else:
            head = (x + dx, y + dy)
            if not (0 <= head[0] < self.cols and 0 <= head[1] < self.rows):
                self.game_over()
                return

        bomb_hit = None
        for i, (bx, by, tl) in enumerate(self.bombs):
            if head == (bx, by):
                bomb_hit = i
                break

        if bomb_hit is not None:
            self.bombs.pop(bomb_hit)
            self.vibrator.buzz(0.25)
            if self.shield_active:
                self.break_shield()
                self.hit_flash = 1.0
                return
            self.hit_flash = 1.0
            self.lives -= 1
            if self.lives <= 0:
                self.game_over()
                return
            return

        bonus_eaten = None
        for i, b in enumerate(self.bonus_foods):
            if head == tuple(b["pos"]):
                bonus_eaten = (i, b)
                break

        red_eaten = (not self.hard_mode) and (head == self.food)
        eating = red_eaten or (bonus_eaten is not None)
        body = self.snake if eating else self.snake[:-1]

        if head in body:
            if not self.ghost_active and not self.shield_active:
                self.game_over()
                return
            if self.shield_active and not self.ghost_active:
                self.break_shield()

        self.snake.insert(0, head)
        cell = min(self.width / self.cols, self.height / self.rows)
        ox = self.x + (self.width - cell * self.cols) / 2
        oy = self.y + (self.height - cell * self.rows) / 2

        if red_eaten:
            self.score += 10
            self.eat_flash = 1.0
            if cell > 0:
                fpx = ox + head[0] * cell + cell / 2
                fpy = oy + head[1] * cell + cell / 2
                self.add_popup(fpx, fpy, (0.5, 1.0, 0.4, 1))
                self.add_burst(fpx, fpy, 10, (1.0, 0.3, 0.3, 1))
            self.play_eat()
            self.vibrator.buzz(0.06)
            self.random_food()
            if self.on_eat_apple:
                self.on_eat_apple("apple_red")
            if self.score > self.high_score:
                old = self.high_score
                self.high_score = self.score
                if self.on_new_high_score:
                    self.on_new_high_score(self.high_score)
                if self.on_level_up and (self.score // 100) > (old // 100):
                    self.on_level_up(self.score)
            if self.on_achv_check:
                self.on_achv_check("score", self.score)

        if bonus_eaten is not None:
            i, b = bonus_eaten
            btype = b["type"]
            if btype == "gold":
                if self.hard_mode:
                    self.score += 5
                else:
                    self.score += 50
                if self.score > self.high_score:
                    old = self.high_score
                    self.high_score = self.score
                    if self.on_new_high_score:
                        self.on_new_high_score(self.high_score)
                    if self.on_level_up and (self.score // 100) > (old // 100):
                        self.on_level_up(self.score)
                if cell > 0:
                    fpx = ox + b["pos"][0] * cell + cell / 2
                    fpy = oy + b["pos"][1] * cell + cell / 2
                    self.add_popup(fpx, fpy, (1.0, 0.85, 0.2, 1))
                    self.add_burst(fpx, fpy, 16, (1.0, 0.85, 0.2, 1))
                if self.on_eat_apple:
                    self.on_eat_apple("apple_gold")
                if self.on_achv_check:
                    self.on_achv_check("score", self.score)
            elif btype == "blue":
                if not self.hard_mode:
                    self.score += 20
                    if self.score > self.high_score:
                        old = self.high_score
                        self.high_score = self.score
                        if self.on_new_high_score:
                            self.on_new_high_score(self.high_score)
                        if self.on_level_up and (self.score // 100) > (old // 100):
                            self.on_level_up(self.score)
                self.activate_slow()
                if cell > 0:
                    fpx = ox + b["pos"][0] * cell + cell / 2
                    fpy = oy + b["pos"][1] * cell + cell / 2
                    self.add_popup(fpx, fpy, (0.3, 0.6, 1.0, 1))
                    self.add_burst(fpx, fpy, 16, (0.3, 0.6, 1.0, 1))
                if self.on_eat_apple:
                    self.on_eat_apple("apple_blue")
                if self.on_achv_check:
                    self.on_achv_check("score", self.score)
            elif btype == "purple":
                if not self.hard_mode:
                    self.score += 30
                    if self.score > self.high_score:
                        old = self.high_score
                        self.high_score = self.score
                        if self.on_new_high_score:
                            self.on_new_high_score(self.high_score)
                        if self.on_level_up and (self.score // 100) > (old // 100):
                            self.on_level_up(self.score)
                self.activate_ghost()
                if cell > 0:
                    fpx = ox + b["pos"][0] * cell + cell / 2
                    fpy = oy + b["pos"][1] * cell + cell / 2
                    self.add_popup(fpx, fpy, (0.7, 0.3, 1.0, 1))
                    self.add_burst(fpx, fpy, 16, (0.7, 0.3, 1.0, 1))
                if self.on_eat_apple:
                    self.on_eat_apple("apple_purple")
                if self.on_achv_check:
                    self.on_achv_check("score", self.score)
            self.eat_flash = 1.0
            self.play_eat()
            self.vibrator.buzz(0.06)
            self.bonus_foods.pop(i)

        if not eating:
            self.snake.pop()
        self.draw()

    def game_over(self):
        self.running = False
        self.dying = True
        self.death_index = len(self.snake) - 1
        self.play_gameover()
        self.vibrator.buzz(0.4)
        if self.bomb_event:
            self.bomb_event.cancel()
            self.bomb_event = None
        if self.bonus_event:
            self.bonus_event.cancel()
            self.bonus_event = None
        if self.survival_event:
            self.survival_event.cancel()
            self.survival_event = None
        if self.growth_event:
            self.growth_event.cancel()
            self.growth_event = None
        if self.shield_timer:
            self.shield_timer.cancel()
            self.shield_timer = None
        self.shield_active = False
        if self.on_game_over:
            self.on_game_over(self.score)
        Clock.schedule_interval(self._death_step, 0.05)

    def _death_step(self, dt):
        if self.death_index < 0:
            self.dying = False
            return False
        self.death_index -= 1
        self.draw()
        return True

    def _chaikin(self, pts, it=2):
        for _ in range(it):
            if len(pts) < 3:
                return pts
            new = [pts[0]]
            for i in range(len(pts) - 1):
                p, q = pts[i], pts[i + 1]
                new.append((0.75 * p[0] + 0.25 * q[0], 0.75 * p[1] + 0.25 * q[1]))
                new.append((0.25 * p[0] + 0.75 * q[0], 0.25 * p[1] + 0.75 * q[1]))
            new.append(pts[-1])
            pts = new
        return pts

    def _resample(self, pts, step):
        if len(pts) < 2:
            return list(pts), 0.0
        seg = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
               for i in range(len(pts) - 1)]
        total = sum(seg)
        if total <= 0:
            return [pts[0]], 0.0
        k = max(1, int(total / step))
        out = []
        i, acc = 0, 0.0
        for j in range(k + 1):
            target = total * j / k
            while i < len(seg) - 1 and acc + seg[i] < target:
                acc += seg[i]
                i += 1
            f = 0.0 if seg[i] <= 0 else min(1.0, max(0.0, (target - acc) / seg[i]))
            out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f,
                        pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f))
        return out, total

    def _draw_snake(self, visible, ox, oy, cell, ga):
        t = self.theme
        bc = self.current_color["body"]
        hc = self.current_color["head"]
        R = cell * self.current_skin["thickness"]
        is_round = self.current_skin["style"] == "round"
        n = len(visible)
        flash, hit = self.eat_flash, self.hit_flash
        pts = [(ox + sx * cell + cell / 2, oy + sy * cell + cell / 2)
               for sx, sy in visible]
        tail_r = cell * 0.07

        def col(m, lift=0.0):
            return (min(1, bc[0] * m + 0.4 * flash + 0.5 * hit + lift * 0.30),
                    min(1, bc[1] * m + 0.4 * flash + lift * 0.30),
                    min(1, bc[2] * m + 0.4 * flash + lift * 0.12))

        def circ(cx, cy, r):
            Ellipse(pos=(cx - r, cy - r), size=(2 * r, 2 * r))

        runs, cur = [], [0]
        for i in range(1, n):
            if (abs(visible[i][0] - visible[i - 1][0]) > 1 or
                    abs(visible[i][1] - visible[i - 1][1]) > 1):
                runs.append(cur)
                cur = [i]
            else:
                cur.append(i)
        runs.append(cur)

        step = cell * (0.13 if n <= 40 else 0.22)
        it = 2 if n <= 40 else 1
        fancy = n <= 70
        last = len(runs) - 1
        taper_cells = 3.2

        for ri, run in enumerate(runs):
            sm = self._chaikin([pts[i] for i in run], it)
            P, total = self._resample(sm, step)
            m = len(P)
            if m == 0:
                continue
            taper_len = min(cell * taper_cells, total * 0.9)
            items = []
            for j in range(m):
                s = total * j / (m - 1) if m > 1 else 0.0
                d_tail = total - s
                r = R
                if ri == last and taper_len > 0 and d_tail < taper_len:
                    f = max(0.0, d_tail / taper_len)
                    f = f * f * (3 - 2 * f)
                    r = tail_r + (R - tail_r) * f
                g = run[0] + (s / total if total > 0 else 0.0) * (len(run) - 1)
                items.append((P[j][0], P[j][1], r, g / max(1, n - 1)))

            Color(0, 0, 0, 0.22 * ga)
            for x, y, r, pg in items:
                circ(x + 1, y - cell * 0.07, r + cell * 0.03)
            Color(*col(0.30), ga)
            for x, y, r, pg in items:
                circ(x, y, r + cell * 0.05)
            for x, y, r, pg in items:
                Color(*col(1.0 - 0.30 * pg), ga)
                circ(x, y, r)
            if fancy and not is_round:
                for x, y, r, pg in items:
                    Color(*col(1.0 - 0.30 * pg, 0.9), ga)
                    circ(x, y + r * 0.22, r * 0.52)
            gap = cell * 0.95
            acc = gap * 0.55
            for j in range(1, m):
                acc += math.hypot(P[j][0] - P[j - 1][0], P[j][1] - P[j - 1][1])
                if acc >= gap:
                    acc = 0.0
                    x, y, r, pg = items[j]
                    if r > cell * 0.16:
                        Color(*col(0.42 - 0.12 * pg), 0.92 * ga)
                        circ(x, y, r * 0.46)

        if self.dying:
            return

        hx, hy = pts[0]
        dx, dy = self.direction
        px, py = -dy, dx
        hcol = hc
        if flash > 0:
            hcol = tuple(min(1.0, c + 0.4 * flash) for c in hcol[:3])
        if hit > 0:
            hcol = (min(1.0, hcol[0] + 0.5 * hit), hcol[1], hcol[2])

        head_cx = hx + dx * cell * 0.04
        head_cy = hy + dy * cell * 0.04
        head_len = cell * 1.02
        head_wid = cell * 0.88
        ew, eh = (head_len, head_wid) if dx != 0 else (head_wid, head_len)

        Color(0.015, 0.10, 0.035, 0.95 * ga)
        Ellipse(pos=(head_cx - ew * 0.53, head_cy - eh * 0.53),
                size=(ew * 1.06, eh * 1.06))
        Color(hcol[0] * 0.72, hcol[1] * 0.78, hcol[2] * 0.72, ga)
        Ellipse(pos=(head_cx - ew / 2, head_cy - eh / 2), size=(ew, eh))
        Color(hcol[0], hcol[1], hcol[2], ga)
        Ellipse(pos=(head_cx - ew * 0.46, head_cy - eh * 0.46),
                size=(ew * 0.92, eh * 0.92))

        Color(min(1, hcol[0] + 0.18), min(1, hcol[1] + 0.12),
              min(1, hcol[2] + 0.12), 0.72 * ga)
        Ellipse(pos=(head_cx - ew * 0.28 - px * cell * 0.03,
                     head_cy - eh * 0.28 - py * cell * 0.03),
                size=(ew * 0.56, eh * 0.34))

        eye_forward = cell * 0.13
        eye_side = cell * 0.245
        eye_r = cell * 0.145
        for side in (-1, 1):
            ex = hx + dx * eye_forward + px * eye_side * side
            ey = hy + dy * eye_forward + py * eye_side * side
            Color(0.04, 0.20, 0.07, ga)
            Ellipse(pos=(ex - eye_r * 1.12, ey - eye_r * 1.12),
                    size=(eye_r * 2.24, eye_r * 2.24))
            Color(0.96, 1.0, 0.82, ga)
            Ellipse(pos=(ex - eye_r, ey - eye_r),
                    size=(eye_r * 2, eye_r * 2))
            pupil_x = ex + dx * eye_r * 0.30
            pupil_y = ey + dy * eye_r * 0.30
            pupil_w = eye_r * 0.72
            pupil_h = eye_r * 0.92
            Color(0.025, 0.07, 0.025, ga)
            Ellipse(pos=(pupil_x - pupil_w / 2, pupil_y - pupil_h / 2),
                    size=(pupil_w, pupil_h))
            Color(1, 1, 1, 0.95 * ga)
            circ(pupil_x - dx * eye_r * 0.16 - px * eye_r * 0.12,
                 pupil_y - dy * eye_r * 0.16 - py * eye_r * 0.12,
                 eye_r * 0.16)

        Color(0.035, 0.16, 0.045, ga)
        for side in (-1, 1):
            nx = hx + dx * cell * 0.39 + px * cell * 0.075 * side
            ny = hy + dy * cell * 0.39 + py * cell * 0.075 * side
            circ(nx, ny, cell * 0.025)

        if self.tongue_out > 0.3:
            tongue_len = cell * (0.10 + self.tongue_out * 0.20)
            mx = hx + dx * cell * 0.43
            my = hy + dy * cell * 0.43
            tx, ty = mx + dx * tongue_len, my + dy * tongue_len
            Color(0.88, 0.08, 0.16, ga)
            Line(points=[mx, my, tx, ty], width=max(1, cell * 0.022), cap='round')
            fork = cell * 0.075
            for side in (-1, 1):
                Line(points=[tx, ty,
                             tx + dx * fork * 0.45 + px * fork * side,
                             ty + dy * fork * 0.45 + py * fork * side],
                     width=max(1, cell * 0.018), cap='round')

    def draw(self, *args):
        self.canvas.clear()
        cell = min(self.width / self.cols, self.height / self.rows)
        if cell <= 0:
            return
        ox = self.x + (self.width - cell * self.cols) / 2
        oy = self.y + (self.height - cell * self.rows) / 2
        t = self.theme
        with self.canvas:
            Color(*t["bg"])
            Rectangle(pos=(self.x, self.y), size=self.size)
            Color(*t["cell"])
            for x in range(self.cols):
                for y in range(self.rows):
                    Rectangle(pos=(ox + x * cell, oy + y * cell),
                              size=(cell - 1, cell - 1))
            for bx, by, tl in self.bombs:
                b_cx = ox + bx * cell + cell / 2
                b_cy = oy + by * cell + cell / 2
                b_sz = cell * 1.0
                Color(0.18, 0.18, 0.22, 1)
                Ellipse(pos=(b_cx - b_sz / 2, b_cy - b_sz / 2),
                        size=(b_sz, b_sz))
                Color(0.65, 0.65, 0.7, 0.85)
                Ellipse(pos=(b_cx - b_sz * 0.2, b_cy - b_sz * 0.15),
                        size=(b_sz * 0.22, b_sz * 0.18))
                Color(0.6, 0.4, 0.2, 1)
                Line(points=[b_cx, b_cy + b_sz / 2,
                             b_cx + b_sz * 0.15, b_cy + b_sz * 0.75],
                     width=cell * 0.06)
                Color(1, 0.65, 0.1, 1)
                Ellipse(pos=(b_cx + b_sz * 0.08, b_cy + b_sz * 0.68),
                        size=(b_sz * 0.22, b_sz * 0.22))
            if not self.hard_mode:
                fx, fy = self.food
                acx = ox + fx * cell + cell / 2
                acy = oy + fy * cell + cell / 2
                asz = cell * 1.05
                bcol = t["food"]
                dcol = (bcol[0] * 0.55, bcol[1] * 0.15, bcol[2] * 0.2, 1)
                Color(0, 0, 0, 0.25)
                Ellipse(pos=(acx - asz * 0.4, oy + fy * cell + 1),
                        size=(asz * 0.8, cell * 0.22))
                Color(*bcol)
                Ellipse(pos=(acx - asz * 0.42, acy - asz * 0.4),
                        size=(asz * 0.84, asz * 0.8))
                Color(dcol[0], dcol[1], dcol[2], 0.45)
                Ellipse(pos=(acx - asz * 0.38, acy - asz * 0.28),
                        size=(asz * 0.32, asz * 0.55))
                Color(1, 1, 1, 0.85)
                Ellipse(pos=(acx - asz * 0.14, acy + asz * 0.06),
                        size=(asz * 0.2, asz * 0.26))
                Color(1, 1, 1, 0.55)
                Ellipse(pos=(acx - asz * 0.05, acy + asz * 0.2),
                        size=(asz * 0.09, asz * 0.11))
                stem_top = acy + asz * 0.48
                Color(0.35, 0.2, 0.1, 1)
                Rectangle(pos=(acx - cell * 0.035, stem_top - cell * 0.05),
                          size=(cell * 0.07, cell * 0.24))
                Color(0.3, 0.7, 0.25, 1)
                Ellipse(pos=(acx + cell * 0.02, stem_top + cell * 0.04),
                        size=(cell * 0.26, cell * 0.15))
            for b in self.bonus_foods:
                bxc, byc = b["pos"]
                b_cx = ox + bxc * cell + cell / 2
                b_cy = oy + byc * cell + cell / 2
                b_type = b["type"]
                time_left = b["time"]
                blink = 1.0
                if time_left < 1.0:
                    blink = 0.5 + 0.5 * (math.sin(time_left * 25) + 1) / 2
                if b_type == "gold":
                    bcol2 = (1.0, 0.85, 0.2, 1)
                    glow = (1.0, 0.85, 0.2, 0.35 * blink)
                elif b_type == "blue":
                    bcol2 = (0.30, 0.60, 1.0, 1)
                    glow = (0.3, 0.6, 1.0, 0.35 * blink)
                else:
                    bcol2 = (0.70, 0.30, 1.0, 1)
                    glow = (0.7, 0.3, 1.0, 0.35 * blink)
                asz2 = cell * 1.05
                Color(*glow)
                Ellipse(pos=(b_cx - asz2 * 0.65, b_cy - asz2 * 0.65),
                        size=(asz2 * 1.3, asz2 * 1.3))
                Color(0, 0, 0, 0.25)
                Ellipse(pos=(b_cx - asz2 * 0.4, b_cy - asz2 * 0.45 + 3),
                        size=(asz2 * 0.8, cell * 0.22))
                Color(bcol2[0], bcol2[1], bcol2[2], blink)
                Ellipse(pos=(b_cx - asz2 * 0.42, b_cy - asz2 * 0.4),
                        size=(asz2 * 0.84, asz2 * 0.8))
                dcol2 = (bcol2[0] * 0.5, bcol2[1] * 0.5, bcol2[2] * 0.7, 0.45)
                Color(dcol2[0], dcol2[1], dcol2[2], 0.45 * blink)
                Ellipse(pos=(b_cx - asz2 * 0.38, b_cy - asz2 * 0.28),
                        size=(asz2 * 0.32, asz2 * 0.55))
                Color(1, 1, 1, 0.85 * blink)
                Ellipse(pos=(b_cx - asz2 * 0.14, b_cy + asz2 * 0.06),
                        size=(asz2 * 0.2, asz2 * 0.26))
                Color(1, 1, 1, 0.55 * blink)
                Ellipse(pos=(b_cx - asz2 * 0.05, b_cy + asz2 * 0.2),
                        size=(asz2 * 0.09, asz2 * 0.11))
                stem_top = b_cy + asz2 * 0.48
                Color(0.35, 0.2, 0.1, blink)
                Rectangle(pos=(b_cx - cell * 0.035, stem_top - cell * 0.05),
                          size=(cell * 0.07, cell * 0.24))
                Color(0.3, 0.7, 0.25, blink)
                Ellipse(pos=(b_cx + cell * 0.02, stem_top + cell * 0.04),
                        size=(cell * 0.26, cell * 0.15))
            ghost_alpha = (0.45 + 0.25 * (math.sin(self.ghost_phase) + 1) / 2
                           if self.ghost_active else 1.0)
            if self.snake:
                visible = (self.snake if not self.dying
                           else self.snake[:self.death_index + 1])
                if visible:
                    self._draw_snake(visible, ox, oy, cell, ghost_alpha)
                    if self.shield_active:
                        hx, hy = self.snake[0]
                        hcx = ox + hx * cell + cell / 2
                        hcy = oy + hy * cell + cell / 2
                        pulse = 0.5 + 0.5 * math.sin(self.shield_phase)
                        shield_r = cell * (0.75 + 0.15 * pulse)
                        Color(0.4, 0.7, 1.0, 0.35 + 0.25 * pulse)
                        Line(circle=(hcx, hcy, shield_r),
                             width=max(2, cell * 0.06))
                        Color(1, 0.9, 0.3, 0.25 + 0.15 * pulse)
                        Line(circle=(hcx, hcy, shield_r * 0.85),
                             width=max(2, cell * 0.04))
            for p in self.particles:
                alpha = max(0.0, p["life"] / p["max_life"])
                c = p["color"]
                Color(c[0], c[1], c[2], alpha)
                s = p["size"]
                Ellipse(pos=(p["x"] - s, p["y"] - s), size=(s * 2, s * 2))
            for pop in self.popups:
                prog = 1.0 - (pop["life"] / pop["max_life"])
                alpha = max(0.0, pop["life"] / pop["max_life"])
                size = pop["start_size"] + (pop["end_size"] - pop["start_size"]) * prog
                c = pop["color"]
                Color(c[0], c[1], c[2], alpha * 0.3)
                Ellipse(pos=(pop["x"] - size * 1.4, pop["y"] - size * 1.4),
                        size=(size * 2.8, size * 2.8))
                Color(c[0], c[1], c[2], alpha * 0.7)
                Ellipse(pos=(pop["x"] - size, pop["y"] - size),
                        size=(size * 2, size * 2))
                Color(1, 1, 1, alpha * 0.95)
                Ellipse(pos=(pop["x"] - size * 0.4, pop["y"] - size * 0.4),
                        size=(size * 0.8, size * 0.8))


class HelperButton(Button):
    def __init__(self, icon_type="shield", count=0, font_name="Roboto", **kwargs):
        super().__init__(**kwargs)
        self.icon_type = icon_type
        self.count = count
        self.font_name_custom = font_name
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)

        self.box = BoxLayout(orientation="vertical", spacing=dp(2), padding=(0, dp(4), 0, dp(4)))
        self.icon = AppleIcon(apple_type=self.icon_type, size_hint_y=0.65)
        self.lbl = Label(text=f"x{self.count}", font_size="12sp", color=(1, 1, 1, 1), size_hint_y=0.35)
        self.lbl.font_name = self.font_name_custom

        self.box.add_widget(self.icon)
        self.box.add_widget(self.lbl)
        self.add_widget(self.box)

        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.box.pos = self.pos
        self.box.size = self.size

    def update_count(self, count, font_name="Roboto"):
        self.count = count
        self.lbl.text = f"x{self.count}"
        self.lbl.font_name = font_name


class SnakeGame(App):
    def build(self):
        self.title = "Snake Game"
        self.icon = "icon.png"
        self.saver = SaveManager()
        self.saved = self.saver.load()
        self.lang = self.saved.get("language", "en")

        root = BoxLayout(orientation="vertical", padding=dp(6), spacing=dp(4))

        top_bar = BoxLayout(orientation="horizontal", size_hint_y=0.07, spacing=dp(6))
        self.title_label = Label(text="[b]SNAKE[/b]", markup=True,
                                  font_size="22sp", color=(0.5, 1, 0.2, 1),
                                  halign="left", valign="middle", size_hint_x=0.30)
        top_bar.add_widget(self.title_label)
        self.lives_widget = LivesIcon(count=0, size_hint_x=0.20)
        top_bar.add_widget(self.lives_widget)
        self.info = Label(text="Score: 0    Best: 0",
                          font_size="14sp", halign="right", valign="middle",
                          size_hint_x=0.50, padding=(0, 0, dp(65), 0))
        top_bar.add_widget(self.info)
        root.add_widget(top_bar)

        self.board = SnakeBoard(theme=self.saved.get("theme", "dark"), size_hint_y=0.78)
        self.board.high_score = self.saved["high_score"]
        self.board.on_new_high_score = self.on_new_high_score
        self.board.on_game_over = self.on_game_over
        self.board.on_level_up = self.on_level_up
        self.board.sound_on = self.saved.get("sound_on", True)
        self.board.vibrator.enabled = self.saved.get("vibration_on", True)
        self.board._current_speed = self.saved.get("speed", 5)

        skin = next((s for s in SKINS if s["id"] == self.saved.get("current_skin", "classic")), SKINS[0])
        color = next((c for c in COLORS if c["id"] == self.saved.get("current_color", "green")), COLORS[0])
        self.board.set_skin(skin)
        self.board.set_color(color)

        self.board.on_resume_tap = self.on_resume_tap
        self.board.on_eat_apple = self.on_eat_apple
        self.board.on_achv_check = self.on_achv_check
        root.add_widget(self.board)

        self.helper_bar = BoxLayout(
            orientation="horizontal",
            size_hint_y=0.09,
            spacing=dp(12),
            padding=(dp(40), 0, dp(40), 0)
        )

        self.shield_btn = HelperButton(icon_type="shield", count=0, font_name=self.get_font())
        self.shield_btn.bind(on_press=self.on_shield_pressed)
        self.helper_bar.add_widget(self.shield_btn)

        self.slow_btn = HelperButton(icon_type="slow", count=0, font_name=self.get_font())
        self.slow_btn.bind(on_press=self.on_slow_pressed)
        self.helper_bar.add_widget(self.slow_btn)

        root.add_widget(self.helper_bar)

        self.status = Label(
            text="Choose a difficulty to start",
            font_size="12sp",
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=0.05
        )
        root.add_widget(self.status)

        menu_btn = Button(
            text="|||",
            font_size="18sp",
            size_hint=(None, None),
            size=(dp(44), dp(40)),
            pos_hint={"right": 0.99, "top": 0.99},
            background_normal="",
            background_color=(0.15, 0.22, 0.28, 0.9),
            background_down=""
        )
        menu_btn.bind(on_press=self.on_btn_menu)

        restart = Button(
            text="",
            size_hint=(None, None),
            size=(dp(48), dp(48)),
            pos_hint={"right": 0.98, "y": 0.02},
            background_normal="",
            background_color=(0, 0, 0, 0),
            background_down=""
        )
        restart.bind(on_press=self.on_btn_restart)

        restart_icon = RefreshIcon(
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(34), dp(34))
        )

        def _position_restart_icon(*a):
            restart_icon.center = restart.center

        restart.bind(pos=_position_restart_icon, size=_position_restart_icon)
        restart.add_widget(restart_icon)
        _position_restart_icon()

        Clock.schedule_interval(self.refresh, 0.1)

        self.root_layout = FloatLayout()
        self.root_layout.add_widget(root)
        self.root_layout.add_widget(menu_btn)
        self.root_layout.add_widget(restart)
        self.root_layout.add_widget(self.build_mode_overlay())

        self.swipe_hint = Label(
            text="",
            font_size="13sp",
            color=(1, 1, 1, 0.7),
            size_hint=(None, None),
            size=(dp(240), dp(24)),
            pos_hint={"center_x": 0.5, "y": 0.10}
        )
        self.root_layout.add_widget(self.swipe_hint)
        Clock.schedule_once(self.hide_swipe_hint, 5)

        self.apply_language()
        self.refresh_helpers()
        return self.root_layout

    def refresh_helpers(self):
        data = self.saver.load()
        helpers = data.get("helpers", {})
        f = self.get_font()
        self.shield_btn.update_count(helpers.get("shield", 0), f)
        self.slow_btn.update_count(helpers.get("slow", 0), f)

    def on_shield_pressed(self, *a):
        self.board.play_click()
        if not self.board.running or self.board.paused or self.board.dying:
            return
        if self.board.shield_active:
            return
        data = self.saver.load()
        count = data.get("helpers", {}).get("shield", 0)
        if count <= 0:
            return
        helpers = data.get("helpers", {})
        helpers["shield"] = count - 1
        self.saver.save(helpers=helpers)
        self.board.activate_shield()
        self.refresh_helpers()

    def on_slow_pressed(self, *a):
        self.board.play_click()
        if not self.board.running or self.board.paused or self.board.dying:
            return
        if self.board.slow_active:
            return
        data = self.saver.load()
        count = data.get("helpers", {}).get("slow", 0)
        if count <= 0:
            return
        helpers = data.get("helpers", {})
        helpers["slow"] = count - 1
        self.saver.save(helpers=helpers)
        self.board.activate_slow()
        self.refresh_helpers()

    def on_eat_apple(self, kind):
        data = self.saver.load()
        counters = data.get("counters", {})
        counters[kind] = counters.get(kind, 0) + 1
        self.saver.save(counters=counters)
        self.on_achv_check(kind, counters[kind])

    def on_achv_check(self, kind, value):
        data = self.saver.load()
        ach = data.get("achievements", {})
        new_unlocked = []
        for a in ACHIEVEMENTS:
            if a["type"] != kind:
                continue
            if ach.get(a["id"]):
                continue
            if value >= a["th"]:
                ach[a["id"]] = True
                new_unlocked.append(a)
        if new_unlocked:
            self.saver.save(achievements=ach)
            for a in new_unlocked:
                self.show_achv_notification(a)
        if kind == "hard_survival":
            d = self.saver.load()
            if value > d.get("hard_best", 0):
                self.saver.save(hard_best=value)

    def show_achv_notification(self, a):
        ov = FloatLayout(size_hint=(1, 1))
        box = BoxLayout(
            orientation="vertical",
            size_hint=(0.9, None),
            height=dp(80),
            pos_hint={"center_x": 0.5, "top": 0.92},
            padding=dp(8),
            spacing=dp(4)
        )
        with box.canvas.before:
            Color(0.1, 0.15, 0.12, 0.95)
            rect = Rectangle(pos=box.pos, size=box.size)
        box.bind(
            pos=lambda *a: setattr(rect, "pos", box.pos),
            size=lambda *a: setattr(rect, "size", box.size)
        )
        f = self.get_font()
        L = self.tr
        title = Label(
            text=L("new_achievement"),
            font_size="14sp",
            color=(0.5, 1, 0.2, 1),
            size_hint_y=0.4
        )
        title.font_name = f
        box.add_widget(title)
        name = a["ar"] if self.lang == "ar" else a["en"]
        sub_line = name
        if self.lang == "ar":
            sub_line = ar(sub_line)
        sub = Label(
            text=sub_line,
            font_size="13sp",
            color=(1, 1, 1, 1),
            size_hint_y=0.6
        )
        sub.font_name = f
        box.add_widget(sub)
        ov.add_widget(box)
        self.root_layout.add_widget(ov)
        Clock.schedule_once(lambda dt: self.root_layout.remove_widget(ov), 3.0)

    def on_btn_menu(self, *a):
        self.board.play_click()
        self.show_menu()

    def on_btn_restart(self, *a):
        self.board.play_click()
        self.show_overlay()

    def on_btn_theme(self, btn):
        self.board.play_click()
        self.toggle_theme(btn)

    def on_btn_lang(self, ov):
        self.board.play_click()
        self.toggle_language(ov)

    def on_btn_top5(self, ov):
        self.board.play_click()
        self.show_leaderboard(ov)

    def on_btn_rules(self, ov):
        self.board.play_click()
        self.show_rules(ov)

    def on_btn_achv(self, ov):
        self.board.play_click()
        self.show_achievements(ov)

    def on_btn_shop(self, ov):
        self.board.play_click()
        self.show_shop(ov)

    def on_btn_sound(self, btn):
        self.board.play_click()
        self.toggle_sound(btn)

    def on_btn_vibration(self, btn):
        self.board.vibrator.enabled = not self.board.vibrator.enabled
        self.saver.save(vibration_on=self.board.vibrator.enabled)
        L = self.tr
        btn.text = f"{L('vibration')}: {L('on') if self.board.vibrator.enabled else L('off')}"
        btn.background_color = (0.15, 0.5, 0.35, 1) if self.board.vibrator.enabled else (0.4, 0.2, 0.2, 1)
        if self.board.vibrator.enabled:
            self.board.vibrator.buzz(0.15)

    def on_btn_close_menu(self, ov):
        self.board.play_click()
        self.close_menu_pause(ov)

    def on_btn_mode(self, mode):
        self.board.play_click()
        self.choose_mode(mode)

    def on_btn_close_rules(self, rlo):
        self.board.play_click()
        self.root_layout.remove_widget(rlo)

    def on_btn_close_lb(self, lbo):
        self.board.play_click()
        self.root_layout.remove_widget(lbo)

    def on_btn_close_achv(self, alo):
        self.board.play_click()
        self.root_layout.remove_widget(alo)

    def on_btn_close_shop(self, slo):
        self.board.play_click()
        self.root_layout.remove_widget(slo)

    def on_resume_tap(self):
        self.swipe_hint.text = self.tr("swipe")
        self.swipe_hint.opacity = 0.7
        Clock.schedule_once(self.hide_swipe_hint, 3)

    def t(self, key):
        return TEXTS.get(self.lang, TEXTS["en"]).get(key, key)

    def tr(self, key):
        text = self.t(key)
        if self.lang == "ar":
            return ar(text)
        return text

    def get_font(self):
        if self.lang == "ar" and FONT_OK:
            return "Arabic"
        return "Roboto"

    def apply_language(self):
        f = self.get_font()
        if self.lang == "en":
            self.title_label.font_name = "Roboto"
            self.title_label.text = "[b]SNAKE[/b]"
        else:
            self.title_label.font_name = f
            self.title_label.text = ar("الثعبان")
        self.status.font_name = f
        self.info.font_name = f
        self.swipe_hint.font_name = f
        self.swipe_hint.text = self.tr("swipe")
        self.update_mode_overlay_texts()
        self.refresh_helpers()
        self.refresh(0)

    def update_mode_overlay_texts(self):
        L = self.tr
        f = self.get_font()
        if hasattr(self, "mode_title_label"):
            self.mode_title_label.font_name = f
            self.mode_title_label.text = L("choose_diff")
        if hasattr(self, "easy_btn"):
            self.easy_btn.font_name = f
            self.easy_btn.text = L("easy")
        if hasattr(self, "normal_btn"):
            self.normal_btn.font_name = f
            self.normal_btn.text = L("normal")
        if hasattr(self, "hard_btn"):
            self.hard_btn.font_name = f
            self.hard_btn.text = L("hard")
        if hasattr(self, "gold_hint_label"):
            self.gold_hint_label.font_name = f
            self.gold_hint_label.text = L("gold_hint")
        if hasattr(self, "speed_label"):
            self.speed_label.font_name = f
            self.speed_label.text = f"{L('speed')}: {int(self.speed_slider.value)}"

    def on_new_high_score(self, v):
        self.saver.save(high_score=v)

    def on_game_over(self, score):
        if score > 0:
            self.saver.add_to_leaderboard(score)
        if self.board.hard_mode:
            d = self.saver.load()
            if score > d.get("hard_best", 0):
                self.saver.save(hard_best=score)
            self.on_achv_check("hard_survival", score)

    def on_level_up(self, score):
        level = min(10, 3 + score // 100)
        self.board.speed_up_gradually(level, steps=5)

    def show_menu(self, *a):
        self.board.paused = True
        self.board.waiting_to_resume = False
        ov = FloatLayout(size_hint=(1, 1))
        with ov.canvas.before:
            Color(0.02, 0.03, 0.04, 0.94)
            bg = Rectangle(pos=ov.pos, size=ov.size)
        ov.bind(
            pos=lambda *a: setattr(bg, "pos", ov.pos),
            size=lambda *a: setattr(bg, "size", ov.size)
        )
        panel = BoxLayout(
            orientation="vertical",
            spacing=dp(4),
            padding=dp(10),
            size_hint=(0.88, 0.95),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        L = self.tr
        f = self.get_font()
        coins_val = self.saver.load().get("coins", 0)

        title = Label(
            text=L("menu"),
            font_size="20sp",
            color=(0.5, 1, 0.2, 1),
            size_hint_y=0.06
        )
        title.font_name = f
        panel.add_widget(title)

        coins_anchor = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint_y=0.06
        )
        coins_anchor.add_widget(self.coin_badge(coins_val, fs="16sp", h=dp(26)))
        panel.add_widget(coins_anchor)

        shop_btn = Button(
            text=L("shop"),
            font_size="14sp",
            background_normal="",
            background_color=(0.75, 0.45, 0.1, 1),
            size_hint_y=0.10
        )
        shop_btn.font_name = f
        shop_btn.bind(on_press=lambda *a: self.on_btn_shop(ov))
        panel.add_widget(shop_btn)

        tb = Button(
            text="",
            font_size="14sp",
            background_normal="",
            background_color=(0.25, 0.35, 0.55, 1),
            size_hint_y=0.10
        )
        tb.font_name = f
        tb.text = L("theme") if self.board.theme_name == "dark" else L("theme_day")
        tb.bind(on_press=lambda *a: self.on_btn_theme(tb))
        panel.add_widget(tb)

        lgb = Button(
            text=L("language"),
            font_size="14sp",
            background_normal="",
            background_color=(0.4, 0.3, 0.5, 1),
            size_hint_y=0.10
        )
        lgb.font_name = f
        lgb.bind(on_press=lambda *a: self.on_btn_lang(ov))
        panel.add_widget(lgb)

        ab = Button(
            text=L("achievements"),
            font_size="14sp",
            background_normal="",
            background_color=(0.55, 0.4, 0.1, 1),
            size_hint_y=0.10
        )
        ab.font_name = f
        ab.bind(on_press=lambda *a: self.on_btn_achv(ov))
        panel.add_widget(ab)

        lb = Button(
            text=L("top5"),
            font_size="14sp",
            background_normal="",
            background_color=(0.6, 0.5, 0.15, 1),
            size_hint_y=0.10
        )
        lb.font_name = f
        lb.bind(on_press=lambda *a: self.on_btn_top5(ov))
        panel.add_widget(lb)

        rb = Button(
            text=L("rules"),
            font_size="14sp",
            background_normal="",
            background_color=(0.3, 0.55, 0.45, 1),
            size_hint_y=0.10
        )
        rb.font_name = f
        rb.bind(on_press=lambda *a: self.on_btn_rules(ov))
        panel.add_widget(rb)

        sb = Button(
            text="",
            font_size="14sp",
            background_normal="",
            background_color=(0.15, 0.5, 0.35, 1) if self.board.sound_on else (0.4, 0.2, 0.2, 1),
            size_hint_y=0.08
        )
        sb.font_name = f
        sb.text = f"{L('sound')}: {L('on') if self.board.sound_on else L('off')}"
        sb.bind(on_press=lambda *a: self.on_btn_sound(sb))
        panel.add_widget(sb)

        vb = Button(
            text="",
            font_size="14sp",
            background_normal="",
            background_color=(0.15, 0.5, 0.35, 1) if self.board.vibrator.enabled else (0.4, 0.2, 0.2, 1),
            size_hint_y=0.08
        )
        vb.font_name = f
        vb.text = f"{L('vibration')}: {L('on') if self.board.vibrator.enabled else L('off')}"
        vb.bind(on_press=lambda *a: self.on_btn_vibration(vb))
        panel.add_widget(vb)

        cb = Button(
            text=L("close"),
            font_size="14sp",
            background_normal="",
            background_color=(0.5, 0.2, 0.2, 1),
            size_hint_y=0.08
        )
        cb.font_name = f
        cb.bind(on_press=lambda *a: self.on_btn_close_menu(ov))
        panel.add_widget(cb)

        ov.add_widget(panel)
        self.root_layout.add_widget(ov)

    def show_shop(self, parent_ov):
        L = self.tr
        f = self.get_font()

        slo = FloatLayout(size_hint=(1, 1))
        with slo.canvas.before:
            Color(0.04, 0.05, 0.08, 0.98)
            bgr = Rectangle(pos=slo.pos, size=slo.size)
        slo.bind(
            pos=lambda *a: setattr(bgr, "pos", slo.pos),
            size=lambda *a: setattr(bgr, "size", slo.size)
        )

        outer = BoxLayout(
            orientation="vertical",
            spacing=dp(6),
            padding=dp(10),
            size_hint=(0.95, 0.92),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        head = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40)
        )
        ttl = Label(
            text=L("shop_title"),
            font_size="22sp",
            color=(1, 0.85, 0.2, 1)
        )
        ttl.font_name = f
        head.add_widget(ttl)

        coins_val = self.saver.load().get("coins", 0)
        coin_anchor = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint_x=None,
            width=dp(110)
        )
        coin_anchor.add_widget(self.coin_badge(coins_val, fs="18sp", h=dp(28)))
        head.add_widget(coin_anchor)
        outer.add_widget(head)

        tabs = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(44),
            spacing=dp(4)
        )

        self.shop_tab = getattr(self, "shop_tab", "skins")

        def set_tab(name):
            self.shop_tab = name
            if slo.parent:
                self.root_layout.remove_widget(slo)
            self.show_shop(parent_ov)

        tabs_btns = [
            ("tab_skins", "skins"),
            ("tab_colors", "colors"),
            ("tab_helpers", "helpers"),
        ]
        for key, val in tabs_btns:
            b = Button(
                text=L(key),
                font_size="14sp",
                background_normal="",
                background_color=(0.2, 0.4, 0.7, 1) if self.shop_tab == val else (0.15, 0.2, 0.25, 1)
            )
            b.font_name = f
            b.bind(on_press=lambda inst, v=val: set_tab(v))
            tabs.add_widget(b)
        outer.add_widget(tabs)

        sv = ScrollView(size_hint=(1, 1))
        list_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(6),
            padding=dp(4)
        )
        list_box.bind(minimum_height=list_box.setter("height"))

        data = self.saver.load()

        if self.shop_tab == "skins":
            owned = data.get("owned_skins", ["classic"])
            current = data.get("current_skin", "classic")
            for item in SKINS:
                list_box.add_widget(self._shop_item_row(
                    item, "skins", owned, current, slo))

        elif self.shop_tab == "colors":
            owned = data.get("owned_colors", ["green"])
            current = data.get("current_color", "green")
            for item in COLORS:
                list_box.add_widget(self._shop_item_row(
                    item, "colors", owned, current, slo))

        else:
            helpers = data.get("helpers", {"shield": 0, "slow": 0})
            list_box.add_widget(self._helper_row(
                "shield", helpers.get("shield", 0), data.get("coins", 0), slo))
            list_box.add_widget(self._helper_row(
                "slow", helpers.get("slow", 0), data.get("coins", 0), slo))

        sv.add_widget(list_box)
        outer.add_widget(sv)

        close_btn = Button(
            text=L("close"),
            font_size="15sp",
            background_normal="",
            background_color=(0.5, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(44)
        )
        close_btn.font_name = f
        close_btn.bind(on_press=lambda *a: self.on_btn_close_shop(slo))
        outer.add_widget(close_btn)

        slo.add_widget(outer)
        self.root_layout.add_widget(slo)

    def _shop_item_row(self, item, kind, owned_list, current_id, parent_slo):
        L = self.tr
        f = self.get_font()
        row = BoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(60),
            padding=dp(4)
        )
        with row.canvas.before:
            Color(0.10, 0.13, 0.18, 1)
            rct = Rectangle(pos=row.pos, size=row.size)
        row.bind(
            pos=lambda i, v, r=rct: setattr(r, "pos", i.pos),
            size=lambda i, v, r=rct: setattr(r, "size", i.size)
        )

        preview = SkinPreview(item_data=item, kind=kind, size_hint_x=None, width=dp(64))
        row.add_widget(preview)

        name_lbl = Label(
            text=(item["name_ar"] if self.lang == "ar" else item["name_en"]),
            font_size="14sp",
            color=(1, 1, 1, 1),
            halign="left",
            valign="middle",
            size_hint_x=0.40
        )
        if self.lang == "ar":
            name_lbl.text = ar(name_lbl.text)
        name_lbl.font_name = f
        name_lbl.bind(size=lambda i, v: setattr(i, "text_size", (v[0], None)))
        row.add_widget(name_lbl)

        is_owned = item["id"] in owned_list
        is_current = (item["id"] == current_id)

        if is_owned:
            if is_current:
                status_lbl = Label(
                    text=L("equipped"),
                    font_size="13sp",
                    color=(0.4, 1, 0.4, 1)
                )
                status_lbl.font_name = f
                row.add_widget(status_lbl)
            else:
                eq_btn = Button(
                    text=L("equip"),
                    font_size="13sp",
                    background_normal="",
                    background_color=(0.2, 0.5, 0.7, 1),
                    size_hint_x=None,
                    width=dp(80)
                )
                eq_btn.font_name = f
                eq_btn.bind(
                    on_press=lambda inst, i_=item, k_=kind, s_=parent_slo:
                    self._equip_item(i_, k_, s_)
                )
                row.add_widget(eq_btn)
        else:
            price_anchor = AnchorLayout(
                anchor_x="center",
                anchor_y="center",
                size_hint_x=None,
                width=dp(70)
            )
            price_anchor.add_widget(self.coin_badge(
                item["price"], fs="13sp", h=dp(20)))
            row.add_widget(price_anchor)

            buy_btn = Button(
                text=L("buy"),
                font_size="13sp",
                background_normal="",
                background_color=(0.9, 0.6, 0.1, 1),
                color=(0, 0, 0, 1),
                size_hint_x=None,
                width=dp(75)
            )
            buy_btn.font_name = f
            buy_btn.bind(
                on_press=lambda inst, i_=item, k_=kind, s_=parent_slo:
                self._buy_item(i_, k_, s_)
            )
            row.add_widget(buy_btn)

        return row

    def _helper_row(self, kind, count, coins, parent_slo):
        L = self.tr
        f = self.get_font()
        row = BoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(70),
            padding=dp(6)
        )
        with row.canvas.before:
            Color(0.10, 0.13, 0.18, 1)
            rct = Rectangle(pos=row.pos, size=row.size)
        row.bind(
            pos=lambda i, v, r=rct: setattr(r, "pos", i.pos),
            size=lambda i, v, r=rct: setattr(r, "size", i.size)
        )

        icon = AppleIcon(apple_type=kind, size_hint_x=None, width=dp(56))
        row.add_widget(icon)

        info_box = BoxLayout(
            orientation="vertical",
            size_hint_x=1
        )
        name_lbl = Label(
            text=(L("shield") if kind == "shield" else L("slow")),
            font_size="15sp",
            color=(1, 1, 1, 1),
            halign="left",
            valign="middle"
        )
        name_lbl.font_name = f
        name_lbl.bind(size=lambda i, v: setattr(i, "text_size", (v[0], None)))
        info_box.add_widget(name_lbl)

        desc_lbl = Label(
            text=(L("shield_desc") if kind == "shield" else L("slow_desc")),
            font_size="11sp",
            color=(0.7, 0.7, 0.7, 1),
            halign="left",
            valign="middle"
        )
        desc_lbl.font_name = f
        desc_lbl.bind(size=lambda i, v: setattr(i, "text_size", (v[0], None)))
        info_box.add_widget(desc_lbl)

        qty_text = f"{count}"
        qty_lbl = Label(
            text=f"{L('quantity')}: {qty_text}",
            font_size="12sp",
            color=(0.6, 1, 0.6, 1),
            halign="left",
            valign="middle"
        )
        qty_lbl.font_name = f
        qty_lbl.bind(size=lambda i, v: setattr(i, "text_size", (v[0], None)))
        info_box.add_widget(qty_lbl)
        row.add_widget(info_box)

        buy_btn = Button(
            text=f"+1\n{L('buy')}",
            font_size="13sp",
            background_normal="",
            background_color=(0.9, 0.6, 0.1, 1),
            color=(0, 0, 0, 1),
            size_hint_x=None,
            width=dp(80)
        )
        buy_btn.font_name = f
        buy_btn.bind(
            on_press=lambda inst, k_=kind, s_=parent_slo:
            self._buy_helper(k_, s_)
        )
        row.add_widget(buy_btn)

        return row

    def _buy_item(self, item, kind, parent_slo):
        self.board.play_click()
        data = self.saver.load()
        coins = data.get("coins", 0)
        if coins < item["price"]:
            return
        coins -= item["price"]
        if kind == "skins":
            owned = data.get("owned_skins", ["classic"])
            if item["id"] not in owned:
                owned.append(item["id"])
            self.saver.save(coins=coins, owned_skins=owned,
                            current_skin=item["id"])
            self.board.set_skin(item)
        else:
            owned = data.get("owned_colors", ["green"])
            if item["id"] not in owned:
                owned.append(item["id"])
            self.saver.save(coins=coins, owned_colors=owned,
                            current_color=item["id"])
            self.board.set_color(item)
        if parent_slo and parent_slo.parent:
            self.root_layout.remove_widget(parent_slo)
        self.show_shop(None)

    def _equip_item(self, item, kind, parent_slo):
        self.board.play_click()
        if kind == "skins":
            self.saver.save(current_skin=item["id"])
            self.board.set_skin(item)
        else:
            self.saver.save(current_color=item["id"])
            self.board.set_color(item)
        if parent_slo and parent_slo.parent:
            self.root_layout.remove_widget(parent_slo)
        self.show_shop(None)

    def _buy_helper(self, kind, parent_slo):
        self.board.play_click()
        data = self.saver.load()
        coins = data.get("coins", 0)
        cost = 10
        if coins < cost:
            return
        coins -= cost
        helpers = data.get("helpers", {"shield": 0, "slow": 0})
        helpers[kind] = helpers.get(kind, 0) + 1
        self.saver.save(coins=coins, helpers=helpers)
        if parent_slo and parent_slo.parent:
            self.root_layout.remove_widget(parent_slo)
        self.show_shop(None)
        self.refresh_helpers()

    def show_leaderboard(self, parent_ov):
        L = self.tr
        f = self.get_font()
        lbo = FloatLayout(size_hint=(1, 1))
        with lbo.canvas.before:
            Color(0.05, 0.05, 0.1, 0.98)
            bgr = Rectangle(pos=lbo.pos, size=lbo.size)
        lbo.bind(
            pos=lambda *a: setattr(bgr, "pos", lbo.pos),
            size=lambda *a: setattr(bgr, "size", lbo.size)
        )
        panel = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(20),
            size_hint=(0.85, 0.6),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        ttl = Label(
            text=L("top5_title"),
            font_size="24sp",
            color=(1, 0.85, 0.2, 1),
            size_hint_y=0.15
        )
        ttl.font_name = f
        panel.add_widget(ttl)
        board = self.saver.load().get("leaderboard", [])
        if not board:
            nl = Label(
                text=L("no_scores"),
                font_size="16sp",
                color=(0.7, 0.7, 0.7, 1),
                size_hint_y=0.5
            )
            nl.font_name = f
            panel.add_widget(nl)
        else:
            for i, e in enumerate(board, 1):
                m = {1: "1st", 2: "2nd", 3: "3rd"}.get(i, f"{i}th")
                row = Label(
                    text=f"{m}   {e['score']}   ({e.get('date', '')})",
                    font_size="17sp",
                    color=(1, 1, 1, 1),
                    size_hint_y=0.12
                )
                row.font_name = f
                panel.add_widget(row)
        cb = Button(
            text=L("close"),
            font_size="16sp",
            background_normal="",
            background_color=(0.2, 0.5, 0.3, 1),
            size_hint_y=0.15
        )
        cb.font_name = f
        cb.bind(on_press=lambda *a: self.on_btn_close_lb(lbo))
        panel.add_widget(cb)
        lbo.add_widget(panel)
        self.root_layout.add_widget(lbo)

    def _rule_row(self, icon_type, text, text_color):
        row = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=0.13)
        icon = AppleIcon(apple_type=icon_type, size_hint_x=0.15)
        row.add_widget(icon)
        f = self.get_font()
        lbl = Label(
            text=text,
            font_size="14sp",
            color=text_color,
            halign="left",
            valign="middle",
            size_hint_x=0.85
        )
        lbl.font_name = f
        lbl.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0], None)))
        row.add_widget(lbl)
        return row

    def _lives_row(self, text, text_color):
        row = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=0.13)
        icon = LivesIcon(count=3, size_hint_x=0.15)
        row.add_widget(icon)
        f = self.get_font()
        lbl = Label(
            text=text,
            font_size="14sp",
            color=text_color,
            halign="left",
            valign="middle",
            size_hint_x=0.85
        )
        lbl.font_name = f
        lbl.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0], None)))
        row.add_widget(lbl)
        return row

    def show_rules(self, parent_ov):
        L = self.tr
        f = self.get_font()
        rlo = FloatLayout(size_hint=(1, 1))
        with rlo.canvas.before:
            Color(0.04, 0.06, 0.08, 0.98)
            bgr = Rectangle(pos=rlo.pos, size=rlo.size)
        rlo.bind(
            pos=lambda *a: setattr(bgr, "pos", rlo.pos),
            size=lambda *a: setattr(bgr, "size", rlo.size)
        )
        panel = BoxLayout(
            orientation="vertical",
            spacing=dp(4),
            padding=dp(14),
            size_hint=(0.92, 0.88),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        ttl = Label(
            text=L("rules_title"),
            font_size="22sp",
            color=(0.5, 1, 0.2, 1),
            size_hint_y=0.09
        )
        ttl.font_name = f
        panel.add_widget(ttl)
        panel.add_widget(self._rule_row("red", L("rule_red"), (1.0, 0.5, 0.5, 1)))
        panel.add_widget(self._rule_row("gold", L("rule_gold"), (1.0, 0.85, 0.2, 1)))
        panel.add_widget(self._rule_row("blue", L("rule_blue"), (0.4, 0.7, 1.0, 1)))
        panel.add_widget(self._rule_row("purple", L("rule_purple"), (0.75, 0.4, 1.0, 1)))
        panel.add_widget(self._rule_row("bomb", L("rule_bomb"), (1.0, 0.6, 0.3, 1)))
        panel.add_widget(self._lives_row(L("rule_lives"), (1.0, 0.4, 0.5, 1)))
        cb = Button(
            text=L("close"),
            font_size="15sp",
            background_normal="",
            background_color=(0.5, 0.2, 0.2, 1),
            size_hint_y=0.1
        )
        cb.font_name = f
        cb.bind(on_press=lambda *a: self.on_btn_close_rules(rlo))
        panel.add_widget(cb)
        rlo.add_widget(panel)
        self.root_layout.add_widget(rlo)

    def coin_badge(self, amount, fs="16sp", h=dp(24), prefix=""):
        box = BoxLayout(
            orientation="horizontal",
            spacing=dp(4),
            size_hint=(None, None),
            height=h
        )
        lbl = Label(
            text=f"{prefix}{amount}",
            font_size=fs,
            color=(1, 0.85, 0.2, 1),
            size_hint=(None, 1),
            width=dp(10)
        )
        lbl.bind(texture_size=lambda i, v: setattr(i, "width", v[0]))
        icon = AppleIcon(apple_type="coin", size_hint=(None, 1), width=h)
        box.add_widget(lbl)
        box.add_widget(icon)
        box.bind(minimum_width=box.setter("width"))
        return box

    def claim_achievement(self, a, alo):
        self.board.play_click()
        data = self.saver.load()
        claimed = data.get("claimed", {})
        if claimed.get(a["id"]) or not data.get("achievements", {}).get(a["id"]):
            return
        claimed[a["id"]] = True
        self.saver.save(claimed=claimed,
                        coins=data.get("coins", 0) + a["coins"])
        if alo and alo.parent:
            self.root_layout.remove_widget(alo)
        self.show_achievements(None)

    def _visible_achievements(self, claimed):
        groups = {}
        for a in ACHIEVEMENTS:
            groups.setdefault(a["type"], []).append(a)
        out = []
        for lst in groups.values():
            lst = sorted(lst, key=lambda x: x["th"])
            nxt = next((x for x in lst if not claimed.get(x["id"])), lst[-1])
            out.append(nxt)
        return out

    def show_achievements(self, parent_ov):
        L = self.tr
        f = self.get_font()
        data = self.saver.load()
        achv = data.get("achievements", {})
        claimed = data.get("claimed", {})
        counters = data.get("counters", {})
        coins = data.get("coins", 0)

        alo = FloatLayout(size_hint=(1, 1))
        with alo.canvas.before:
            Color(0.04, 0.05, 0.08, 0.98)
            bgr = Rectangle(pos=alo.pos, size=alo.size)
        alo.bind(
            pos=lambda *a: setattr(bgr, "pos", alo.pos),
            size=lambda *a: setattr(bgr, "size", alo.size)
        )

        outer = BoxLayout(
            orientation="vertical",
            spacing=dp(6),
            padding=dp(12),
            size_hint=(0.95, 0.9),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        ttl = Label(
            text=L("achv_title"),
            font_size="20sp",
            color=(1, 0.85, 0.2, 1)
        )
        ttl.font_name = f
        head = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40)
        )
        head.add_widget(ttl)
        head_coins = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint_x=None,
            width=dp(100)
        )
        head_coins.add_widget(self.coin_badge(coins, fs="18sp", h=dp(28)))
        head.add_widget(head_coins)
        outer.add_widget(head)

        sv = ScrollView(size_hint=(1, 1))
        list_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(4),
            padding=dp(4)
        )
        list_box.bind(minimum_height=list_box.setter("height"))

        for a in self._visible_achievements(claimed):
            unlocked = achv.get(a["id"], False)
            if a["type"] == "score":
                cur = data.get("high_score", 0)
            elif a["type"] == "hard_survival":
                cur = data.get("hard_best", 0)
            else:
                cur = counters.get(a["type"], 0)
            th = a["th"]

            row = BoxLayout(
                orientation="horizontal",
                spacing=dp(6),
                size_hint_y=None,
                height=dp(56)
            )
            bg_color = (0.15, 0.22, 0.18, 1) if unlocked else (0.12, 0.12, 0.14, 1)
            with row.canvas.before:
                Color(*bg_color)
                bg_rect = Rectangle(pos=row.pos, size=row.size)
            row.bind(
                pos=lambda inst, val, r=bg_rect: setattr(r, "pos", inst.pos),
                size=lambda inst, val, r=bg_rect: setattr(r, "size", inst.size)
            )

            icon = AppleIcon(apple_type=a["icon"], size_hint_x=None, width=dp(48))
            row.add_widget(icon)

            name_text = a["ar"] if self.lang == "ar" else a["en"]
            status_icon = "[V]" if unlocked else "[X]"
            info_text = f"{status_icon} {name_text}"
            if unlocked:
                sub_text = L("unlocked")
            else:
                sub_text = f"{cur}/{th}"
                if self.lang == "ar":
                    sub_text = ar(sub_text)
            if self.lang == "ar":
                info_text = ar(info_text)

            info_box = BoxLayout(orientation="vertical", size_hint_x=1)
            name_lbl = Label(
                text=info_text,
                font_size="13sp",
                color=(1, 1, 1, 1) if unlocked else (0.7, 0.7, 0.7, 1),
                halign="left",
                valign="middle"
            )
            name_lbl.font_name = f
            name_lbl.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0], None)))
            info_box.add_widget(name_lbl)

            sub_lbl = Label(
                text=sub_text,
                font_size="11sp",
                color=(0.5, 1, 0.2, 1) if unlocked else (0.6, 0.6, 0.6, 1),
                halign="left",
                valign="middle"
            )
            sub_lbl.font_name = f
            sub_lbl.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0], None)))
            info_box.add_widget(sub_lbl)
            row.add_widget(info_box)

            reward = AnchorLayout(
                anchor_x="center",
                anchor_y="center",
                size_hint_x=None,
                width=dp(64)
            )
            reward.add_widget(self.coin_badge(a["coins"], fs="13sp",
                                              h=dp(20), prefix="+"))
            row.add_widget(reward)

            if unlocked and not claimed.get(a["id"]):
                cbtn = Button(
                    text=L("collect"),
                    font_size="14sp",
                    background_normal="",
                    background_color=(0.9, 0.7, 0.1, 1),
                    color=(0, 0, 0, 1),
                    size_hint=(None, None),
                    size=(dp(80), dp(40)),
                    pos_hint={"center_y": 0.5}
                )
                cbtn.font_name = f
                cbtn.bind(
                    on_press=lambda inst, ach_=a, alo_=alo:
                    self.claim_achievement(ach_, alo_)
                )
                row.add_widget(cbtn)

            list_box.add_widget(row)

        sv.add_widget(list_box)
        outer.add_widget(sv)

        cb = Button(
            text=L("close"),
            font_size="15sp",
            background_normal="",
            background_color=(0.5, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(44)
        )
        cb.font_name = f
        cb.bind(on_press=lambda *a: self.on_btn_close_achv(alo))
        outer.add_widget(cb)
        alo.add_widget(outer)
        self.root_layout.add_widget(alo)

    def close_menu_pause(self, ov):
        if ov.parent:
            self.root_layout.remove_widget(ov)
        if self.board.running and not self.board.dying:
            self.board.paused = True
            self.board.waiting_to_resume = True
            self.swipe_hint.text = self.tr("tap_to_resume")
            self.swipe_hint.opacity = 1
            Clock.schedule_once(self.hide_swipe_hint, 5)

    def toggle_language(self, ov):
        self.lang = "ar" if self.lang == "en" else "en"
        self.saver.save(language=self.lang)
        self.apply_language()
        self.root_layout.remove_widget(ov)

    def toggle_theme(self, btn):
        cur = self.board.theme_name
        idx = THEME_ORDER.index(cur) if cur in THEME_ORDER else 0
        new = THEME_ORDER[(idx + 1) % len(THEME_ORDER)]
        self.board.set_theme(new)
        self.saver.save(theme=new)
        btn.text = self.tr("theme") if new == "dark" else self.tr("theme_day")

    def toggle_sound(self, btn):
        self.board.sound_on = not self.board.sound_on
        self.saver.save(sound_on=self.board.sound_on)
        L = self.tr
        btn.text = f"{L('sound')}: {L('on') if self.board.sound_on else L('off')}"
        btn.background_color = (0.15, 0.5, 0.35, 1) if self.board.sound_on else (0.4, 0.2, 0.2, 1)

    def hide_swipe_hint(self, dt):
        self.swipe_hint.opacity = 0

    def build_mode_overlay(self):
        L0 = TEXTS["en"]
        self.overlay = FloatLayout(size_hint=(1, 1))
        with self.overlay.canvas.before:
            Color(0.02, 0.03, 0.04, 0.92)
            self.overlay_bg = Rectangle(pos=self.overlay.pos, size=self.overlay.size)
        self.overlay.bind(
            pos=lambda *a: setattr(self.overlay_bg, "pos", self.overlay.pos),
            size=lambda *a: setattr(self.overlay_bg, "size", self.overlay.size)
        )
        panel = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(18),
            size_hint=(0.85, 0.75),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.mode_title_label = Label(
            text=L0["choose_diff"],
            font_size="22sp",
            color=(1, 1, 1, 1),
            size_hint_y=0.1
        )
        panel.add_widget(self.mode_title_label)

        self.speed_label = Label(
            text=f"{L0['speed']}: {self.saved['speed']}",
            font_size="16sp",
            color=(1, 1, 1, 1),
            size_hint_y=0.07
        )
        panel.add_widget(self.speed_label)

        self.speed_slider = Slider(
            min=1, max=10,
            value=self.saved["speed"],
            step=1,
            size_hint_y=0.09
        )
        self.speed_slider.bind(
            value=lambda i, v: setattr(
                self.speed_label, "text", f"{self.tr('speed')}: {int(v)}")
        )
        panel.add_widget(self.speed_slider)

        self.easy_btn = Button(
            text=L0["easy"],
            font_size="15sp",
            background_normal="",
            background_color=(0.2, 0.6, 0.3, 1),
            halign="center",
            size_hint_y=0.16
        )
        self.easy_btn.bind(on_press=lambda *a: self.on_btn_mode("easy"))
        panel.add_widget(self.easy_btn)

        self.normal_btn = Button(
            text=L0["normal"],
            font_size="15sp",
            background_normal="",
            background_color=(0.6, 0.25, 0.2, 1),
            halign="center",
            size_hint_y=0.16
        )
        self.normal_btn.bind(on_press=lambda *a: self.on_btn_mode("normal"))
        panel.add_widget(self.normal_btn)

        self.hard_btn = Button(
            text=L0["hard"],
            font_size="15sp",
            background_normal="",
            background_color=(0.5, 0.1, 0.5, 1),
            halign="center",
            size_hint_y=0.16
        )
        self.hard_btn.bind(on_press=lambda *a: self.on_btn_mode("hard"))
        panel.add_widget(self.hard_btn)

        self.gold_hint_label = Label(
            text=L0["gold_hint"],
            font_size="11sp",
            color=(1, 0.85, 0.3, 1),
            size_hint_y=0.08
        )
        panel.add_widget(self.gold_hint_label)

        self.overlay.add_widget(panel)
        return self.overlay

    def choose_mode(self, mode):
        sp = self.speed_slider.value
        self.board._current_speed = sp
        self.board.set_speed(sp)
        if mode == "easy":
            self.board.set_mode(True, hard=False)
        elif mode == "normal":
            self.board.set_mode(False, hard=False)
        elif mode == "hard":
            self.board.set_mode(False, hard=True)
        self.board.restart()
        self.saver.save(speed=int(sp))
        if self.overlay.parent:
            self.root_layout.remove_widget(self.overlay)

    def show_overlay(self, *a):
        self.board.paused = True
        self.board.waiting_to_resume = False
        if not self.overlay.parent:
            self.root_layout.add_widget(self.overlay)

    def refresh(self, dt):
        L = self.tr
        f = self.get_font()
        info_txt = f"{L('score')}: {self.board.score}    {L('best')}: {self.board.high_score}"
        self.info.font_name = f
        self.info.text = info_txt

        if self.board.hard_mode and self.board.lives > 0 and self.board.running:
            if self.lives_widget.count != self.board.lives:
                self.lives_widget.count = self.board.lives
                self.lives_widget._redraw()
        else:
            if self.lives_widget.count != 0:
                self.lives_widget.count = 0
                self.lives_widget._redraw()

        if self.board.waiting_to_resume:
            return

        self.status.font_name = f
        if self.board.dying:
            self.status.text = L("game_over")
        elif self.board.paused:
            self.status.text = L("choose_start")
        elif not self.board.running:
            self.status.text = L("game_over_r")
        else:
            self.status.text = L("swipe")

    def on_pause(self):
        try:
            self.saver.save(
                high_score=self.board.high_score,
                speed=int(self.speed_slider.value),
                theme=self.board.theme_name,
                sound_on=self.board.sound_on,
                vibration_on=self.board.vibrator.enabled,
                language=self.lang
            )
        except Exception:
            pass
        self.board.paused = True
        return True

    def on_resume(self):
        pass

    def on_stop(self):
        try:
            self.saver.save(
                high_score=self.board.high_score,
                speed=int(self.speed_slider.value),
                theme=self.board.theme_name,
                sound_on=self.board.sound_on,
                vibration_on=self.board.vibrator.enabled,
                language=self.lang
            )
        except Exception:
            pass


if __name__ == "__main__":
    SnakeGame().run()
