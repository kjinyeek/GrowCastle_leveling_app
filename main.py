import json
import os
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path

APP_TITLE = "Grow Castle Leveling Calculator"

DEFAULT_CHARACTERS = [
    {"name": "Archer", "type": "Hero", "ratio": 0.00},
    {"name": "Hunter", "type": "Hero", "ratio": 0.00},
    {"name": "Elf", "type": "Hero", "ratio": 0.00},
    {"name": "Ice Mage", "type": "Hero", "ratio": 0.00},
    {"name": "Lightning Mage", "type": "Hero", "ratio": 0.00},
    {"name": "Fire Mage", "type": "Hero", "ratio": 0.00},
    {"name": "White Mage", "type": "Hero", "ratio": 0.00},
    {"name": "Ogre", "type": "Hero", "ratio": 0.00},
    {"name": "Necromancer", "type": "Hero", "ratio": 0.00},
    {"name": "Military Band (F)", "type": "Hero", "ratio": 0.00},
    {"name": "Military Band (M)", "type": "Hero", "ratio": 0.00},
    {"name": "Priest", "type": "Hero", "ratio": 0.00},
    {"name": "Tiny Giant", "type": "Hero", "ratio": 0.00},
    {"name": "Slinger", "type": "Hero", "ratio": 0.00},
    {"name": "Smith", "type": "Hero", "ratio": 0.00},
    {"name": "Voodoo", "type": "Hero", "ratio": 0.00},
    {"name": "Bazooka Man", "type": "Hero", "ratio": 0.00},
    {"name": "Knight", "type": "Hero", "ratio": 0.00},
    {"name": "Architect", "type": "Hero", "ratio": 0.00},
    {"name": "Lisa", "type": "Hero", "ratio": 0.00},
    {"name": "Alice", "type": "Hero", "ratio": 0.00},
    {"name": "Dorothy", "type": "Hero", "ratio": 0.00},
    {"name": "Druid", "type": "Hero", "ratio": 0.00},
    {"name": "Assassin", "type": "Hero", "ratio": 0.02},
    {"name": "Flying Orc", "type": "Hero", "ratio": 0.00},
    {"name": "Windy", "type": "Hero", "ratio": 0.00},
    {"name": "Angel", "type": "Hero", "ratio": 0.00},
    {"name": "Zeus", "type": "Hero", "ratio": 0.03},
    {"name": "Golem Master", "type": "Hero", "ratio": 0.00},
    {"name": "Succubus", "type": "Hero", "ratio": 0.00},
    {"name": "Elizabeth", "type": "Hero", "ratio": 0.00},
    {"name": "Orc Band", "type": "Hero", "ratio": 0.00},
    {"name": "Defender", "type": "Hero", "ratio": 0.00},
    {"name": "Goblin", "type": "Hero", "ratio": 0.00},
    {"name": "Alchemist", "type": "Hero", "ratio": 0.00},
    {"name": "Rogue", "type": "Hero", "ratio": 0.00},
    {"name": "Chrono", "type": "Hero", "ratio": 0.00},
    {"name": "Dark Skeleton", "type": "Hero", "ratio": 0.00},
    {"name": "Stone", "type": "Hero", "ratio": 0.00},
    {"name": "Poseidon", "type": "Hero", "ratio": 0.00},
    {"name": "Ice Sorceress", "type": "Hero", "ratio": 0.00},
    {"name": "Edward", "type": "Leader", "ratio": 0.00},
    {"name": "Solar", "type": "Leader", "ratio": 0.00},
    {"name": "Zero", "type": "Leader", "ratio": 0.00},
    {"name": "Thor", "type": "Leader", "ratio": 0.05},
    {"name": "Sara", "type": "Leader", "ratio": 0.00},
    {"name": "Tony", "type": "Leader", "ratio": 0.00},
    {"name": "Din", "type": "Leader", "ratio": 0.00},
    {"name": "Orc King", "type": "Leader", "ratio": 0.00},
    {"name": "Skeleton King", "type": "Leader", "ratio": 0.00},
    {"name": "Mechanic", "type": "Leader", "ratio": 0.00},
    {"name": "Troll King", "type": "Leader", "ratio": 0.00},
    {"name": "Town Archer", "type": "Extra", "ratio": 0.08},
    {"name": "Castle HP", "type": "Extra", "ratio": 0.07},
]

DEFAULT_SETTINGS = {
    "language": "en",
    "last_wave": "10000",
    "selected": ["Assassin", "Zeus", "Castle HP", "Thor", "Town Archer"],
    "characters": DEFAULT_CHARACTERS,
    "recommend_data": {},
    "recommend_extra_percent": 10
}

OBSOLETE_CHARACTERS = {"Lightning Archer"}
COLORS = {
    "bg": "#f5f6fa",
    "card": "#ffffff",
    "card2": "#f0f2f7",
    "text": "#1f2937",
    "muted": "#8a94a6",
    "accent": "#2f80ed",
    "accent2": "#dbeafe",
    "danger": "#ef4444",
    "line": "#e6e9f2",
}

I18N = {
    "en": {
        "app_title": "Grow Castle Leveling Calculator",
        "saved_wave": "Saved wave",
        "targets": "Targets",
        "calculate": "Calculate",
        "edit": "Edit",
        "recommend": "Auto Recommend",
        "language": "Language",
        "main": "Main",
        "back_main": "Back to Main",
        "result_title": "Calculation Result",
        "name": "Name",
        "ratio": "Ratio",
        "level": "Level",
        "error": "Error",
        "edit_title": "Edit Settings",
        "save": "Save",
        "wave": "Wave",
        "wave_hint": "ex: 10000, 10k, 1.5m, 2b",
        "all_chars": "All Characters · double-click or drag",
        "selected_slots": "Selected Characters",
        "drop_hint": "Drag characters here.",
        "leveling_ratio": "Leveling Ratio",
        "damage_data": "Level / Damage Share",
        "remove": "Remove",
        "saved": "Saved",
        "saved_msg": "Settings have been saved.",
        "save_failed": "Save failed",
        "ratio_edit_title": "Edit Leveling Ratio",
        "ratio_edit_msg": "Enter {name}'s ratio as a percent.\nExample: 2 → 2% of wave\n\nCurrent: {current:.2f}%",
        "data_edit_title": "Edit Level and Damage Share",
        "data_edit_msg": "Enter current level and damage share for {name}.\nExample: level 32000 or 32k / damage share 35 or 35%",
        "current_level": "Current Level",
        "damage": "Damage Share (%)",
        "manual_ratio": "Manual Ratio",
        "recommend_data": "Recommendation Data",
        "edit_ratio_short": "Ratio",
        "edit_data_short": "Data",
        "recommend_title": "Recommended Leveling Ratio",
        "recommend_desc": "The target total ratio is p + x. p is the sum of current level-to-wave ratios, and x is the adjustable extra ratio below. The target total is distributed by efficiency: Damage Share (%) ÷ Current Level. Town Archer receives a 5x adjustment.",
        "logic_button": "Calculation Logic",
        "logic_title": "Calculation Logic",
        "logic_text": "1. Current ratio = Current Level ÷ Current Wave × 100.\n2. p = Sum of all selected characters' current ratios.\n3. y = p + x, where x is the extra target ratio controlled by the slider.\n4. Efficiency = Damage Share (%) ÷ Current Level.\n5. Town Archer efficiency is multiplied by 5. This is an app assumption based on the idea that Town Archer leveling is much more cost-efficient, so the same damage share per level is treated as about 5 times more valuable.\n6. Recommended Ratio = y × Character Efficiency ÷ Total Efficiency.\n7. Recommended Level = Current Wave × Recommended Ratio ÷ 100.",
        "need_data": "Enter wave, current level, and damage share data for at least two selected characters.",
        "recommended_ratio": "Recommended Ratio",
        "recommended_level": "Recommended Level",
        "extra_percent": "Extra target ratio x",
        "current_total_ratio": "Current total ratio p",
        "target_total_ratio": "Target total ratio y",
        "recommend_table_header": "Character                 Recommended Ratio     Recommended Level",
        "open_edit": "Edit Input Data",
        "creator": "Created by SL_jinyee",
    },
    "ko": {
        "app_title": "Grow Castle 레벨링 계산기",
        "saved_wave": "저장된 웨이브",
        "targets": "계산 대상",
        "calculate": "계산",
        "edit": "수정",
        "recommend": "자동 추천",
        "language": "언어",
        "main": "메인",
        "back_main": "메인으로",
        "result_title": "계산 결과",
        "name": "이름",
        "ratio": "비율",
        "level": "레벨",
        "error": "오류",
        "edit_title": "설정 수정",
        "save": "저장",
        "wave": "웨이브",
        "wave_hint": "예: 10000, 10k, 1.5m, 2b",
        "all_chars": "전체 캐릭터 · 더블클릭 또는 드래그",
        "selected_slots": "계산 대상 캐릭터",
        "drop_hint": "여기에 캐릭터를 드래그해서 넣으세요.",
        "leveling_ratio": "레벨링 비율",
        "damage_data": "레벨 / 데미지 비율",
        "remove": "삭제",
        "saved": "저장 완료",
        "saved_msg": "설정이 저장되었습니다.",
        "save_failed": "저장 실패",
        "ratio_edit_title": "레벨링 비율 수정",
        "ratio_edit_msg": "{name} 비율을 퍼센트로 입력하세요.\n예: 2 → 웨이브의 2%\n\n현재: {current:.2f}%",
        "data_edit_title": "레벨과 데미지 비율 수정",
        "data_edit_msg": "{name}의 현재 레벨과 데미지 비율을 입력하세요.\n예: 레벨 32000 또는 32k / 데미지 비율 35 또는 35%",
        "current_level": "현재 레벨",
        "damage": "데미지 비율(%)",
        "manual_ratio": "수동 비율",
        "recommend_data": "추천 데이터",
        "edit_ratio_short": "비율",
        "edit_data_short": "데이터",
        "recommend_title": "레벨링 비율 추천",
        "recommend_desc": "목표 총 비율은 p + x입니다. p는 현재 캐릭터들의 웨이브 대비 레벨 비율 총합이고, x는 아래 슬라이더로 조절하는 추가 비율입니다. 목표 총합은 효율(데미지 비율 ÷ 현재 레벨)에 따라 배분됩니다. Town Archer는 5배 보정을 적용합니다.",
        "logic_button": "계산 로직",
        "logic_title": "계산 로직",
        "logic_text": "1. 현재 비율 = 현재 레벨 ÷ 현재 웨이브 × 100.\n2. p = 선택된 모든 캐릭터의 현재 비율 합.\n3. y = p + x. x는 슬라이더로 조절하는 추가 목표 비율입니다.\n4. 효율 = 데미지 비율(%) ÷ 현재 레벨.\n5. Town Archer는 효율에 5배를 적용합니다. 이 값은 마을아처 레벨링이 일반 캐릭터보다 비용 효율이 훨씬 높다고 보는 앱의 가정이며, 같은 데미지 비율/레벨 값을 약 5배 더 가치 있게 반영하기 위한 보정입니다.\n6. 추천 비율 = y × 캐릭터 효율 ÷ 전체 효율 합.\n7. 추천 레벨 = 현재 웨이브 × 추천 비율 ÷ 100.",
        "need_data": "웨이브와 선택된 캐릭터 중 최소 2명의 레벨, 데미지 비율을 입력해야 합니다.",
        "recommended_ratio": "추천 비율",
        "recommended_level": "추천 레벨",
        "extra_percent": "추가 목표 비율 x",
        "current_total_ratio": "현재 총 비율 p",
        "target_total_ratio": "목표 총 비율 y",
        "recommend_table_header": "캐릭터                    추천 비율             추천 레벨",
        "open_edit": "입력값 수정",
        "creator": "Created by SL_jinyee",
    }
}


def tr(lang, key):
    return I18N.get(lang, I18N["en"]).get(key, I18N["en"].get(key, key))


def base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


def resource_dir():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


BASE_DIR = base_dir()
RESOURCE_DIR = resource_dir()
SETTINGS_PATH = BASE_DIR / "settings.json"
ASSET_DIR = RESOURCE_DIR / "assets" / "heroes"


def slug(name):
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in name).strip("_")


def deep_copy(obj):
    return json.loads(json.dumps(obj, ensure_ascii=False))


def clean_settings(data):
    data["characters"] = [
        c for c in data.get("characters", [])
        if c.get("name") not in OBSOLETE_CHARACTERS
    ]
    valid_names = {c.get("name") for c in data.get("characters", []) if c.get("name")}
    data["selected"] = [
        name for name in data.get("selected", [])
        if name in valid_names and name not in OBSOLETE_CHARACTERS
    ]
    data.setdefault("recommend_data", {})
    for bad in list(OBSOLETE_CHARACTERS):
        data["recommend_data"].pop(bad, None)
    return data


def load_settings():
    if not SETTINGS_PATH.exists():
        data = deep_copy(DEFAULT_SETTINGS)
        save_settings(data)
        return data
    try:
        data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except Exception:
        data = deep_copy(DEFAULT_SETTINGS)

    data.setdefault("language", "en")
    if data.get("language") not in ("en", "ko"):
        data["language"] = "en"
    data.setdefault("last_wave", DEFAULT_SETTINGS["last_wave"])
    data.setdefault("selected", DEFAULT_SETTINGS["selected"])
    data.setdefault("characters", [])
    data.setdefault("recommend_data", {})
    data.setdefault("recommend_extra_percent", 10)

    existing = {c.get("name"): c for c in data["characters"] if c.get("name")}
    for c in DEFAULT_CHARACTERS:
        if c["name"] not in existing:
            data["characters"].append(deep_copy(c))
        else:
            existing[c["name"]].setdefault("type", c["type"])
            existing[c["name"]].setdefault("ratio", c["ratio"])
    data = clean_settings(data)
    save_settings(data)
    return data


def save_settings(data):
    SETTINGS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_number(text):
    text = str(text).strip().replace(",", "")
    if not text:
        raise ValueError("empty")
    value = text.lower()
    result = 0.0
    units = [("t", 1_000_000_000_000), ("b", 1_000_000_000), ("m", 1_000_000), ("k", 1_000), ("조", 1_000_000_000_000), ("억", 100_000_000), ("만", 10_000)]
    consumed = False
    for unit, mult in units:
        if unit in value:
            parts = value.split(unit, 1)
            num = float(parts[0]) if parts[0] else 0.0
            result += num * mult
            value = parts[1]
            consumed = True
    if value:
        result += float(value)
    if consumed:
        return result
    return float(text)


def parse_optional(text):
    text = str(text).strip()
    if not text:
        return 0.0
    return parse_number(text)


def parse_damage_share(text):
    text = str(text).strip().replace(",", "")
    if not text:
        return 0.0
    if text.endswith("%"):
        text = text[:-1].strip()
    value = float(text)
    if value < 0:
        raise ValueError("damage share must be positive")
    return value


def fmt_percent(num):
    return f"{num:g}%"


def fmt(num):
    return f"{round(num):,}"


def round100(num):
    return round(num / 100) * 100


class ScrollFrame(tk.Frame):
    def __init__(self, parent, width=300, height=380, **kwargs):
        super().__init__(parent, **kwargs)
        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0, bg=COLORS["bg"])
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=COLORS["bg"])
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self._resize_inner)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _resize_inner(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("980x700")
        self.root.minsize(940, 660)
        self.data = load_settings()
        self.lang = self.data.get("language", "en")
        self.image_cache = {}
        self.drag_name = None
        ASSET_DIR.mkdir(parents=True, exist_ok=True)
        self.show_main()

    def t(self, key):
        return tr(self.lang, key)

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=COLORS["bg"])

    def get_char(self, name):
        for c in self.data["characters"]:
            if c["name"] == name:
                return c
        return None

    def char_image(self, name, size=56):
        key = (name, size)
        if key in self.image_cache:
            return self.image_cache[key]
        path = ASSET_DIR / f"{slug(name)}.png"
        if path.exists():
            try:
                img = tk.PhotoImage(file=str(path))
                if img.width() > size or img.height() > size:
                    factor = max(1, __import__("math").ceil(max(img.width() / size, img.height() / size)))
                    img = img.subsample(factor, factor)
                self.image_cache[key] = img
                return img
            except Exception:
                pass
        ph = tk.PhotoImage(width=size, height=size)
        ph.put("#eef2ff", to=(0, 0, size, size))
        ph.put("#c7d2fe", to=(3, 3, size-3, size-3))
        ph.put("#ffffff", to=(7, 7, size-7, size-7))
        self.image_cache[key] = ph
        return ph

    def set_language(self, lang):
        self.lang = lang
        self.data["language"] = lang
        save_settings(self.data)
        self.show_main()

    def pill_button(self, parent, text, command, primary=False, width=15):
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            font=("Malgun Gothic", 12, "bold" if primary else "normal"),
            bg=COLORS["accent"] if primary else COLORS["card"],
            fg="white" if primary else COLORS["text"],
            activebackground="#1d6fd1" if primary else COLORS["card2"],
            activeforeground="white" if primary else COLORS["text"],
            relief="flat",
            bd=0,
            padx=18,
            pady=12,
            cursor="hand2",
        )

    def topbar(self, parent, title):
        header = tk.Frame(parent, bg=COLORS["bg"], pady=8)
        header.pack(fill="x")
        tk.Label(header, text=title, bg=COLORS["bg"], fg=COLORS["text"], font=("Malgun Gothic", 22, "bold")).pack(side="left")
        self.pill_button(header, self.t("back_main"), self.show_main, width=12).pack(side="right", padx=4)
        return header

    def show_main(self):
        self.clear()
        container = tk.Frame(self.root, bg=COLORS["bg"], padx=48, pady=34)
        container.pack(fill="both", expand=True)

        langbar = tk.Frame(container, bg=COLORS["bg"])
        langbar.pack(fill="x")
        tk.Label(langbar, text=self.t("language"), bg=COLORS["bg"], fg=COLORS["muted"], font=("Malgun Gothic", 10)).pack(side="right", padx=(8, 0))
        lang_var = tk.StringVar(value=self.lang)
        opt = tk.OptionMenu(langbar, lang_var, "en", "ko", command=lambda v: self.set_language(v))
        opt.config(bg=COLORS["card"], fg=COLORS["text"], relief="flat", bd=0, highlightthickness=0)
        opt.pack(side="right")

        card = tk.Frame(container, bg=COLORS["card"], padx=42, pady=42)
        card.pack(fill="both", expand=True, pady=(20, 10))

        tk.Label(card, text=self.t("app_title"), font=("Malgun Gothic", 26, "bold"), bg=COLORS["card"], fg=COLORS["text"]).pack(pady=(0, 22))
        try:
            wave = fmt(parse_number(self.data.get("last_wave", "0")))
        except Exception:
            wave = self.data.get("last_wave", "")
        info = tk.Frame(card, bg=COLORS["card"])
        info.pack(pady=6)
        tk.Label(info, text=f"{self.t('saved_wave')}: {wave}", font=("Malgun Gothic", 13), bg=COLORS["card"], fg=COLORS["muted"]).grid(row=0, column=0, padx=12)
        tk.Label(info, text=f"{self.t('targets')}: {len(self.data.get('selected', []))}", font=("Malgun Gothic", 13), bg=COLORS["card"], fg=COLORS["muted"]).grid(row=0, column=1, padx=12)

        btns = tk.Frame(card, bg=COLORS["card"])
        btns.pack(pady=42)
        self.pill_button(btns, self.t("calculate"), self.show_calc, primary=True, width=18).grid(row=0, column=0, padx=10, pady=8)
        self.pill_button(btns, self.t("edit"), self.show_edit, width=18).grid(row=0, column=1, padx=10, pady=8)
        self.pill_button(btns, self.t("recommend"), self.show_recommend, width=18).grid(row=1, column=0, columnspan=2, padx=10, pady=8)

        tk.Label(container, text=self.t("creator"), bg=COLORS["bg"], fg="#b8bfcc", font=("Malgun Gothic", 9)).pack(anchor="se", pady=(4, 0))

    def show_calc(self):
        self.clear()
        body = tk.Frame(self.root, bg=COLORS["bg"], padx=28, pady=18)
        body.pack(fill="both", expand=True)
        self.topbar(body, self.t("result_title"))
        panel = tk.Frame(body, bg=COLORS["card"], padx=24, pady=24)
        panel.pack(fill="both", expand=True, pady=(12, 0))
        text = tk.Text(panel, font=("Consolas", 13), height=20, bg="#fbfcff", fg=COLORS["text"], relief="flat", padx=16, pady=16)
        text.pack(fill="both", expand=True)
        try:
            wave = parse_number(self.data["last_wave"])
            text.insert("end", f"Wave: {fmt(wave)}\n\n")
            text.insert("end", f"{self.t('name'):<28} {self.t('ratio'):>10} {self.t('level'):>14}\n")
            text.insert("end", "-" * 58 + "\n")
            for name in self.data.get("selected", []):
                c = self.get_char(name)
                if not c:
                    continue
                ratio = float(c.get("ratio", 0))
                text.insert("end", f"{name:<28} {ratio*100:>9.2f}% {fmt(wave*ratio):>14}\n")
        except Exception as e:
            text.insert("end", f"{self.t('error')}: {e}")

    def show_edit(self):
        self.clear()
        body = tk.Frame(self.root, bg=COLORS["bg"], padx=24, pady=14)
        body.pack(fill="both", expand=True)
        header = tk.Frame(body, bg=COLORS["bg"], pady=4)
        header.pack(fill="x")
        tk.Label(header, text=self.t("edit_title"), font=("Malgun Gothic", 22, "bold"), bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left")
        self.pill_button(header, self.t("save"), self.save_edit, primary=True, width=10).pack(side="right", padx=5)
        self.pill_button(header, self.t("back_main"), self.show_main, width=12).pack(side="right", padx=5)

        wavebar = tk.Frame(body, bg=COLORS["card"], padx=18, pady=14)
        wavebar.pack(fill="x", pady=(12, 12))
        tk.Label(wavebar, text=self.t("wave"), font=("Malgun Gothic", 11, "bold"), bg=COLORS["card"], fg=COLORS["text"]).pack(side="left")
        self.wave_entry = tk.Entry(wavebar, font=("Malgun Gothic", 12), width=24, relief="flat", bg=COLORS["card2"])
        self.wave_entry.pack(side="left", padx=10, ipady=7)
        self.wave_entry.insert(0, self.data.get("last_wave", ""))
        tk.Label(wavebar, text=self.t("wave_hint"), fg=COLORS["muted"], bg=COLORS["card"], font=("Malgun Gothic", 9)).pack(side="left")

        pane = tk.Frame(body, bg=COLORS["bg"])
        pane.pack(fill="both", expand=True)
        left = tk.Frame(pane, bg=COLORS["card"], padx=12, pady=12)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right = tk.Frame(pane, bg=COLORS["card"], padx=12, pady=12)
        right.pack(side="left", fill="both", expand=True, padx=(10, 0))
        tk.Label(left, text=self.t("all_chars"), bg=COLORS["card"], fg=COLORS["text"], font=("Malgun Gothic", 12, "bold")).pack(anchor="w", pady=(0, 8))
        tk.Label(right, text=self.t("selected_slots"), bg=COLORS["card"], fg=COLORS["text"], font=("Malgun Gothic", 12, "bold")).pack(anchor="w", pady=(0, 8))

        self.left_scroll = ScrollFrame(left, width=420, height=440, bg=COLORS["bg"])
        self.left_scroll.pack(fill="both", expand=True)
        self.selected_drop = tk.Frame(right, bg=COLORS["card2"])
        self.selected_drop.pack(fill="both", expand=True)
        self.selected_drop.bind("<Enter>", lambda e: self.selected_drop.configure(bg=COLORS["accent2"]) if self.drag_name else None)
        self.selected_drop.bind("<Leave>", lambda e: self.selected_drop.configure(bg=COLORS["card2"]))
        self.render_all()
        self.render_selected()

    def icon_card(self, parent, char):
        frame = tk.Frame(parent, bg=COLORS["card"], relief="flat", bd=0, padx=9, pady=8)
        img = self.char_image(char["name"], 50)
        icon_bg = tk.Frame(frame, bg=COLORS["card2"], width=60, height=60)
        icon_bg.pack_propagate(False)
        icon_bg.pack(side="left")
        icon = tk.Label(icon_bg, image=img, bg=COLORS["card2"])
        icon.image = img
        icon.pack(expand=True)
        text = tk.Frame(frame, bg=COLORS["card"])
        text.pack(side="left", padx=10, fill="x", expand=True)
        name = tk.Label(text, text=char["name"], bg=COLORS["card"], fg=COLORS["text"], font=("Malgun Gothic", 10, "bold"), anchor="w")
        name.pack(fill="x")
        meta = tk.Label(text, text=f"{char['type']} · {char.get('ratio', 0)*100:.2f}%", bg=COLORS["card"], fg=COLORS["muted"], font=("Malgun Gothic", 9), anchor="w")
        meta.pack(fill="x")
        for w in (frame, icon, icon_bg, name, meta, text):
            w.bind("<ButtonPress-1>", lambda e, n=char["name"]: self.start_drag(n))
            w.bind("<ButtonRelease-1>", lambda e, n=char["name"]: self.end_drag(n))
            w.bind("<Double-Button-1>", lambda e, n=char["name"]: self.add_selected(n))
        return frame

    def render_all(self):
        for w in self.left_scroll.inner.winfo_children():
            w.destroy()
        for c in self.data["characters"]:
            card = self.icon_card(self.left_scroll.inner, c)
            if c["name"] in self.data.get("selected", []):
                card.configure(bg="#f7f8fb")
            card.pack(fill="x", padx=4, pady=4)

    def render_selected(self):
        for w in self.selected_drop.winfo_children():
            w.destroy()
        selected = self.data.get("selected", [])
        if not selected:
            tk.Label(self.selected_drop, text=self.t("drop_hint"), bg=COLORS["card2"], fg=COLORS["muted"], font=("Malgun Gothic", 13)).pack(expand=True)
            return
        for idx, name in enumerate(selected):
            c = self.get_char(name)
            if not c:
                continue
            rec = self.data.setdefault("recommend_data", {}).get(name, {})
            card = tk.Frame(self.selected_drop, bg=COLORS["card"], relief="flat", bd=0, width=285, height=132)
            card.grid(row=idx//2, column=idx%2, padx=8, pady=8, sticky="n")
            card.grid_propagate(False)
            img = self.char_image(name, 54)
            icon_bg = tk.Frame(card, bg=COLORS["card2"], width=66, height=66)
            icon_bg.place(x=10, y=12)
            icon_bg.pack_propagate(False)
            icon = tk.Label(icon_bg, image=img, bg=COLORS["card2"])
            icon.image = img
            icon.pack(expand=True)
            tk.Label(card, text=name, bg=COLORS["card"], fg=COLORS["text"], font=("Malgun Gothic", 10, "bold")).place(x=88, y=12)
            tk.Label(card, text=f"{self.t('manual_ratio')}: {c.get('ratio', 0)*100:.2f}%", bg=COLORS["card"], fg=COLORS["muted"], font=("Malgun Gothic", 9)).place(x=88, y=38)
            level_text = rec.get("level", "-") or "-"
            dmg_text = rec.get("damage", "-") or "-"
            tk.Label(card, text=f"{self.t('recommend_data')}: {self.t('current_level')} {level_text} / {self.t('damage')} {dmg_text}", bg=COLORS["card"], fg=COLORS["muted"], font=("Malgun Gothic", 8), wraplength=185, justify="left").place(x=88, y=60)
            self.pill_button(card, self.t("edit_ratio_short"), lambda n=name: self.edit_ratio(n), width=7).place(x=12, y=92, width=72, height=28)
            self.pill_button(card, self.t("edit_data_short"), lambda n=name: self.edit_damage_data(n), width=7).place(x=90, y=92, width=72, height=28)
            self.pill_button(card, "X", lambda n=name: self.remove_selected(n), width=3).place(x=168, y=92, width=40, height=28)

    def start_drag(self, name):
        self.drag_name = name

    def end_drag(self, name):
        if not self.drag_name:
            return
        x, y = self.root.winfo_pointerx(), self.root.winfo_pointery()
        target = self.root.winfo_containing(x, y)
        inside = False
        while target is not None:
            if target == self.selected_drop:
                inside = True
                break
            target = target.master
        if inside:
            self.add_selected(name)
        self.drag_name = None
        if hasattr(self, "selected_drop"):
            self.selected_drop.configure(bg=COLORS["card2"])

    def add_selected(self, name):
        self.data.setdefault("selected", [])
        if name not in self.data["selected"]:
            self.data["selected"].append(name)
        self.render_all()
        self.render_selected()

    def remove_selected(self, name):
        if name in self.data.get("selected", []):
            self.data["selected"].remove(name)
        self.render_all()
        self.render_selected()

    def edit_ratio(self, name):
        c = self.get_char(name)
        if not c:
            return
        current_percent = float(c.get("ratio", 0)) * 100
        value = simpledialog.askfloat(
            self.t("ratio_edit_title"),
            self.t("ratio_edit_msg").format(name=name, current=current_percent),
            initialvalue=current_percent,
            minvalue=0
        )
        if value is None:
            return
        c["ratio"] = value / 100
        self.render_all()
        self.render_selected()

    def edit_damage_data(self, name):
        recs = self.data.setdefault("recommend_data", {})
        current = recs.get(name, {})
        win = tk.Toplevel(self.root)
        win.title(self.t("data_edit_title"))
        win.configure(bg=COLORS["bg"])
        win.geometry("420x260")
        win.transient(self.root)
        win.grab_set()
        tk.Label(win, text=self.t("data_edit_msg").format(name=name), bg=COLORS["bg"], fg=COLORS["text"], font=("Malgun Gothic", 10), wraplength=360, justify="left").pack(padx=24, pady=(22, 14), anchor="w")
        form = tk.Frame(win, bg=COLORS["bg"])
        form.pack(fill="x", padx=24)
        tk.Label(form, text=self.t("current_level"), bg=COLORS["bg"], fg=COLORS["muted"], font=("Malgun Gothic", 10)).grid(row=0, column=0, sticky="w", pady=6)
        level_e = tk.Entry(form, font=("Malgun Gothic", 12), relief="flat", bg=COLORS["card"])
        level_e.grid(row=0, column=1, sticky="ew", padx=8, ipady=6)
        level_e.insert(0, current.get("level", ""))
        tk.Label(form, text=self.t("damage"), bg=COLORS["bg"], fg=COLORS["muted"], font=("Malgun Gothic", 10)).grid(row=1, column=0, sticky="w", pady=6)
        damage_e = tk.Entry(form, font=("Malgun Gothic", 12), relief="flat", bg=COLORS["card"])
        damage_e.grid(row=1, column=1, sticky="ew", padx=8, ipady=6)
        damage_e.insert(0, current.get("damage", ""))
        form.columnconfigure(1, weight=1)
        def apply():
            try:
                level = level_e.get().strip()
                damage = damage_e.get().strip()
                if level:
                    parse_number(level)
                if damage:
                    parse_damage_share(damage)
                recs[name] = {"level": level, "damage": damage}
                save_settings(self.data)
                win.destroy()
                self.render_selected()
            except Exception as e:
                messagebox.showerror(self.t("error"), str(e), parent=win)
        self.pill_button(win, self.t("save"), apply, primary=True, width=12).pack(pady=18)

    def recommendation_rows(self, extra_percent=None):
        rows = []
        try:
            wave = parse_number(self.data.get("last_wave", DEFAULT_SETTINGS["last_wave"]))
        except Exception:
            wave = 0
        if wave <= 0:
            return [], 0, 0, 0
        if extra_percent is None:
            extra_percent = float(self.data.get("recommend_extra_percent", 10))
        for name in self.data.get("selected", []):
            c = self.get_char(name)
            rec = self.data.setdefault("recommend_data", {}).get(name, {})
            if not c or not rec:
                continue
            try:
                level = parse_optional(rec.get("level", ""))
                damage = parse_damage_share(rec.get("damage", ""))
            except Exception:
                continue
            if level <= 0 or damage <= 0:
                continue
            current_ratio = (level / wave) * 100
            efficiency = damage / level
            if name == "Town Archer":
                efficiency *= 5
            rows.append({"name": name, "level": level, "damage": damage, "current_ratio": current_ratio, "efficiency": efficiency})
        if len(rows) < 2:
            return [], 0, 0, wave
        p_total = sum(r["current_ratio"] for r in rows)
        y_total = p_total + float(extra_percent)
        total_efficiency = sum(r["efficiency"] for r in rows)
        for r in rows:
            share = r["efficiency"] / total_efficiency if total_efficiency else 0
            r["recommend_ratio"] = y_total * share
            r["recommended_level"] = wave * r["recommend_ratio"] / 100
        return rows, p_total, y_total, wave

    def show_logic_popup(self):
        messagebox.showinfo(self.t("logic_title"), self.t("logic_text"))

    def show_recommend(self):
        self.clear()
        body = tk.Frame(self.root, bg=COLORS["bg"], padx=28, pady=18)
        body.pack(fill="both", expand=True)
        header = self.topbar(body, self.t("recommend_title"))
        self.pill_button(header, self.t("open_edit"), self.show_edit, primary=True, width=12).pack(side="right", padx=4)
        panel = tk.Frame(body, bg=COLORS["card"], padx=24, pady=20)
        panel.pack(fill="both", expand=True, pady=(12, 0))
        tk.Label(panel, text=self.t("recommend_desc"), bg=COLORS["card"], fg=COLORS["muted"], font=("Malgun Gothic", 10), wraplength=820, justify="left").pack(anchor="w", pady=(0, 8))
        self.pill_button(panel, self.t("logic_button"), self.show_logic_popup, width=12).pack(anchor="w", pady=(0, 12))

        control = tk.Frame(panel, bg=COLORS["card"])
        control.pack(fill="x", pady=(0, 12))
        extra_var = tk.DoubleVar(value=float(self.data.get("recommend_extra_percent", 10)))
        extra_label = tk.Label(control, text=f"{self.t('extra_percent')}: {extra_var.get():.1f}%", bg=COLORS["card"], fg=COLORS["text"], font=("Malgun Gothic", 10, "bold"))
        extra_label.pack(anchor="w")

        text = tk.Text(panel, font=("Consolas", 12), bg="#fbfcff", fg=COLORS["text"], relief="flat", padx=16, pady=16)
        text.pack(fill="both", expand=True)

        def render_result(*_):
            value = float(extra_var.get())
            self.data["recommend_extra_percent"] = value
            save_settings(self.data)
            extra_label.config(text=f"{self.t('extra_percent')}: {value:.1f}%")
            rows, p_total, y_total, wave = self.recommendation_rows(value)
            text.delete("1.0", "end")
            if not rows:
                text.insert("end", self.t("need_data") + "\n\n")
                text.insert("end", "Edit → selected character card → Data → enter Current Level and Damage Share (%).")
                return
            ordered = sorted(rows, key=lambda r: r["recommend_ratio"], reverse=True)
            text.insert("end", f"Wave: {fmt(wave)}\n")
            text.insert("end", f"{self.t('current_total_ratio')}: {p_total:.2f}%\n")
            text.insert("end", f"{self.t('target_total_ratio')}: {y_total:.2f}%\n\n")
            text.insert("end", self.t("recommend_table_header") + "\n")
            text.insert("end", "-" * 72 + "\n")
            for r in ordered:
                text.insert("end", f"{r['name']:<24} {r['recommend_ratio']:>10.2f}% {fmt(round100(r['recommended_level'])):>18}\n")

        scale = tk.Scale(control, from_=0, to=100, orient="horizontal", resolution=0.5, variable=extra_var, command=render_result, bg=COLORS["card"], fg=COLORS["muted"], troughcolor=COLORS["accent2"], highlightthickness=0, relief="flat", length=520)
        scale.pack(fill="x", pady=(4, 0))
        render_result()

    def save_edit(self):
        try:
            wave = self.wave_entry.get().strip()
            parse_number(wave)
            self.data["last_wave"] = wave
            self.data["language"] = self.lang
            save_settings(self.data)
            messagebox.showinfo(self.t("saved"), self.t("saved_msg"))
        except Exception as e:
            messagebox.showerror(self.t("save_failed"), str(e))


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
