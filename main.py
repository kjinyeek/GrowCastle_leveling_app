
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
    {"name": "Lightning Archer", "type": "Extra", "ratio": 0.02},
]

DEFAULT_SETTINGS = {
    "last_wave": "10000",
    "selected": ["Assassin", "Lightning Archer", "Zeus", "Castle HP", "Thor", "Town Archer"],
    "characters": DEFAULT_CHARACTERS
}


def base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


BASE_DIR = base_dir()
SETTINGS_PATH = BASE_DIR / "settings.json"
ASSET_DIR = BASE_DIR / "assets" / "heroes"


def slug(name):
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in name).strip("_")


def deep_copy(obj):
    return json.loads(json.dumps(obj, ensure_ascii=False))


def load_settings():
    if not SETTINGS_PATH.exists():
        data = deep_copy(DEFAULT_SETTINGS)
        save_settings(data)
        return data

    try:
        data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except Exception:
        data = deep_copy(DEFAULT_SETTINGS)

    data.setdefault("last_wave", DEFAULT_SETTINGS["last_wave"])
    data.setdefault("selected", DEFAULT_SETTINGS["selected"])
    data.setdefault("characters", [])

    existing = {c.get("name"): c for c in data["characters"] if c.get("name")}
    for c in DEFAULT_CHARACTERS:
        if c["name"] not in existing:
            data["characters"].append(deep_copy(c))
        else:
            existing[c["name"]].setdefault("type", c["type"])
            existing[c["name"]].setdefault("ratio", c["ratio"])
    return data


def save_settings(data):
    SETTINGS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_number(text):
    text = str(text).strip().replace(",", "")
    if not text:
        raise ValueError("웨이브를 입력하세요.")

    multipliers = {"k": 1000, "m": 1000000, "b": 1000000000, "t": 1000000000000}
    last = text[-1].lower()

    if last in multipliers:
        if not text[:-1]:
            raise ValueError("숫자 부분이 없습니다.")
        return float(text[:-1]) * multipliers[last]

    return float(text)


def fmt(num):
    return f"{round(num):,}"


class ScrollFrame(tk.Frame):
    def __init__(self, parent, width=300, height=380, **kwargs):
        super().__init__(parent, **kwargs)
        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas)

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
        self.root.geometry("920x640")
        self.root.minsize(920, 640)

        self.data = load_settings()
        self.image_cache = {}
        self.drag_name = None

        ASSET_DIR.mkdir(parents=True, exist_ok=True)
        self.show_main()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def get_char(self, name):
        for c in self.data["characters"]:
            if c["name"] == name:
                return c
        return None

    def char_image(self, name, size=52):
        key = (name, size)
        if key in self.image_cache:
            return self.image_cache[key]

        path = ASSET_DIR / f"{slug(name)}.png"
        if path.exists():
            try:
                img = tk.PhotoImage(file=str(path))
                if img.width() > size or img.height() > size:
                    factor = max(1, int(max(img.width() / size, img.height() / size)))
                    img = img.subsample(factor, factor)
                self.image_cache[key] = img
                return img
            except Exception:
                pass

        ph = tk.PhotoImage(width=size, height=size)
        ph.put("#e8eef8", to=(0, 0, size, size))
        ph.put("#9eb7db", to=(2, 2, size-2, size-2))
        ph.put("#f7f9fd", to=(5, 5, size-5, size-5))
        self.image_cache[key] = ph
        return ph

    def icon_card(self, parent, char):
        frame = tk.Frame(parent, bg="white", relief="solid", bd=1, padx=6, pady=6)
        img = self.char_image(char["name"])
        icon = tk.Label(frame, image=img, bg="white")
        icon.image = img
        icon.pack(side="left")

        text = tk.Frame(frame, bg="white")
        text.pack(side="left", padx=8, fill="x", expand=True)

        name = tk.Label(text, text=char["name"], bg="white", font=("Malgun Gothic", 10, "bold"), anchor="w")
        name.pack(fill="x")
        meta = tk.Label(text, text=f"{char['type']} · {char.get('ratio', 0)*100:.2f}%", bg="white", fg="#666", font=("Malgun Gothic", 9), anchor="w")
        meta.pack(fill="x")

        for w in (frame, icon, name, meta, text):
            w.bind("<ButtonPress-1>", lambda e, n=char["name"]: self.start_drag(n))
            w.bind("<ButtonRelease-1>", lambda e, n=char["name"]: self.end_drag(n))
            w.bind("<Double-Button-1>", lambda e, n=char["name"]: self.add_selected(n))

        return frame

    def show_main(self):
        self.clear()
        container = tk.Frame(self.root, padx=40, pady=40)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Grow Castle Leveling Calculator", font=("Malgun Gothic", 24, "bold")).pack(pady=20)

        try:
            wave = fmt(parse_number(self.data.get("last_wave", "0")))
        except Exception:
            wave = self.data.get("last_wave", "")

        tk.Label(container, text=f"저장된 웨이브: {wave}", font=("Malgun Gothic", 14)).pack(pady=4)
        tk.Label(container, text=f"계산 대상: {len(self.data.get('selected', []))}개", font=("Malgun Gothic", 11), fg="#777").pack(pady=4)

        btns = tk.Frame(container)
        btns.pack(pady=50)

        tk.Button(btns, text="계산", width=16, height=3, font=("Malgun Gothic", 18, "bold"), command=self.show_calc).grid(row=0, column=0, padx=22)
        tk.Button(btns, text="수정", width=16, height=3, font=("Malgun Gothic", 18, "bold"), command=self.show_edit).grid(row=0, column=1, padx=22)

        tk.Label(container, text="캐릭터 아이콘 포함 버전입니다. 비율과 웨이브는 settings.json에 저장됩니다.", font=("Malgun Gothic", 10), fg="#777").pack(pady=20)

    def show_calc(self):
        self.clear()
        top = tk.Frame(self.root, padx=24, pady=18)
        top.pack(fill="x")
        tk.Label(top, text="계산 결과", font=("Malgun Gothic", 22, "bold")).pack(side="left")
        tk.Button(top, text="메인으로", command=self.show_main, font=("Malgun Gothic", 11)).pack(side="right")

        body = tk.Frame(self.root, padx=24)
        body.pack(fill="both", expand=True)

        text = tk.Text(body, font=("Consolas", 13), height=20)
        text.pack(fill="both", expand=True)

        try:
            wave = parse_number(self.data["last_wave"])
            text.insert("end", f"Wave: {fmt(wave)}\n\n")
            text.insert("end", "Name                         Ratio        Level\n")
            text.insert("end", "-" * 55 + "\n")
            for name in self.data.get("selected", []):
                c = self.get_char(name)
                if not c:
                    continue
                ratio = float(c.get("ratio", 0))
                text.insert("end", f"{name:<28} {ratio*100:>6.2f}% {fmt(wave*ratio):>13}\n")
        except Exception as e:
            text.insert("end", f"오류: {e}")

    def show_edit(self):
        self.clear()

        header = tk.Frame(self.root, padx=20, pady=12)
        header.pack(fill="x")
        tk.Label(header, text="설정 수정", font=("Malgun Gothic", 20, "bold")).pack(side="left")
        tk.Button(header, text="저장", command=self.save_edit, font=("Malgun Gothic", 11, "bold"), width=10).pack(side="right", padx=5)
        tk.Button(header, text="메인으로", command=self.show_main, font=("Malgun Gothic", 11), width=10).pack(side="right")

        wavebar = tk.Frame(self.root, padx=20)
        wavebar.pack(fill="x")
        tk.Label(wavebar, text="웨이브", font=("Malgun Gothic", 11)).pack(side="left")
        self.wave_entry = tk.Entry(wavebar, font=("Malgun Gothic", 12), width=24)
        self.wave_entry.pack(side="left", padx=8)
        self.wave_entry.insert(0, self.data.get("last_wave", ""))
        tk.Label(wavebar, text="예: 10000, 10k, 1.5m, 2b", fg="#777", font=("Malgun Gothic", 9)).pack(side="left")

        pane = tk.Frame(self.root, padx=20, pady=14)
        pane.pack(fill="both", expand=True)

        left = tk.LabelFrame(pane, text="전체 캐릭터 · 더블클릭 또는 드래그", font=("Malgun Gothic", 11, "bold"))
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = tk.LabelFrame(pane, text="계산 대상 칸", font=("Malgun Gothic", 11, "bold"))
        right.pack(side="left", fill="both", expand=True, padx=(10, 0))

        self.left_scroll = ScrollFrame(left, width=420, height=440)
        self.left_scroll.pack(fill="both", expand=True, padx=8, pady=8)

        self.selected_drop = tk.Frame(right, bg="#f2f5fa")
        self.selected_drop.pack(fill="both", expand=True, padx=8, pady=8)
        self.selected_drop.bind("<Enter>", lambda e: self.selected_drop.configure(bg="#deecff") if self.drag_name else None)
        self.selected_drop.bind("<Leave>", lambda e: self.selected_drop.configure(bg="#f2f5fa"))

        self.render_all()
        self.render_selected()

    def render_all(self):
        for w in self.left_scroll.inner.winfo_children():
            w.destroy()

        for c in self.data["characters"]:
            card = self.icon_card(self.left_scroll.inner, c)
            if c["name"] in self.data.get("selected", []):
                card.configure(bg="#e9e9e9")
            card.pack(fill="x", padx=5, pady=3)

    def render_selected(self):
        for w in self.selected_drop.winfo_children():
            w.destroy()

        selected = self.data.get("selected", [])
        if not selected:
            tk.Label(self.selected_drop, text="여기에 캐릭터를 드래그해서 넣으세요.", bg="#f2f5fa", fg="#777", font=("Malgun Gothic", 13)).pack(expand=True)
            return

        for idx, name in enumerate(selected):
            c = self.get_char(name)
            if not c:
                continue
            card = tk.Frame(self.selected_drop, bg="white", relief="solid", bd=1, width=250, height=82)
            card.grid(row=idx//2, column=idx%2, padx=8, pady=8, sticky="n")
            card.grid_propagate(False)

            img = self.char_image(name, 48)
            icon = tk.Label(card, image=img, bg="white")
            icon.image = img
            icon.place(x=8, y=15)

            tk.Label(card, text=name, bg="white", font=("Malgun Gothic", 10, "bold")).place(x=65, y=10)
            tk.Label(card, text=f"{c.get('ratio', 0)*100:.2f}%", bg="white", fg="#666", font=("Malgun Gothic", 10)).place(x=65, y=38)

            tk.Button(card, text="✎", width=2, command=lambda n=name: self.edit_ratio(n)).place(x=195, y=6)
            tk.Button(card, text="X", width=2, command=lambda n=name: self.remove_selected(n)).place(x=220, y=6)

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
            self.selected_drop.configure(bg="#f2f5fa")

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
            "레벨링 비율 수정",
            f"{name} 비율을 퍼센트로 입력하세요.\n예: 2 → 웨이브의 2%\n\n현재: {current_percent:.2f}%",
            initialvalue=current_percent,
            minvalue=0
        )
        if value is None:
            return
        c["ratio"] = value / 100
        self.render_all()
        self.render_selected()

    def save_edit(self):
        try:
            wave = self.wave_entry.get().strip()
            parse_number(wave)
            self.data["last_wave"] = wave
            save_settings(self.data)
            messagebox.showinfo("저장 완료", "설정이 저장되었습니다.")
        except Exception as e:
            messagebox.showerror("저장 실패", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
