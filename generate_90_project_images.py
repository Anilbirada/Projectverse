"""
PROJECTVERSE - 90 Unique Project Image Generator
Generates exactly 90 bespoke 16:9 1200x675 WebP project artwork images:
- static/projects/bca/ (BCA001 to BCA015) - Deep Purple / Cyan Theme
- static/projects/bcom/ (BCOM001 to BCOM010) - Emerald Green / Navy Theme (Finance & Commerce)
- static/projects/btech/ (BTECH001 to BTECH025) - Electric Blue / Neon Indigo Theme (Engineering & AI)
- static/projects/mca/ (MCA001 to MCA015) - Royal Purple / Violet Theme (Enterprise & Multi-Agent)
- static/projects/mtech/ (MTECH001 to MTECH015) - Amber Gold / Dark Slate Theme (Postgraduate Research)
- static/projects/iit/ (IIT001 to IIT010) - Rose Crimson / Cyberpunk Deep Theme (Frontier Research)
"""
import os
import math
import random
import sqlite3
from PIL import Image, ImageDraw, ImageFont

DIRS = {
    "BCA": os.path.join("static", "projects", "bca"),
    "B.Com": os.path.join("static", "projects", "bcom"),
    "B.Tech": os.path.join("static", "projects", "btech"),
    "MCA": os.path.join("static", "projects", "mca"),
    "M.Tech": os.path.join("static", "projects", "mtech"),
    "IIT-Level / Research-Grade": os.path.join("static", "projects", "iit")
}

for d in DIRS.values():
    os.makedirs(d, exist_ok=True)

THEMES = {
    "BCA": {
        "bg_top": (10, 15, 35),
        "bg_bottom": (30, 20, 60),
        "accent": (0, 210, 255),
        "secondary": (168, 85, 247),
        "tag": "BCA CAPSTONE",
        "tag_bg": (124, 58, 237)
    },
    "B.Com": {
        "bg_top": (6, 30, 25),
        "bg_bottom": (15, 45, 40),
        "accent": (52, 211, 153),
        "secondary": (245, 158, 11),
        "tag": "B.COM ANALYTICS",
        "tag_bg": (16, 185, 129)
    },
    "B.Tech": {
        "bg_top": (8, 18, 42),
        "bg_bottom": (15, 30, 75),
        "accent": (56, 189, 248),
        "secondary": (99, 102, 241),
        "tag": "B.TECH ENGINEERING",
        "tag_bg": (14, 116, 144)
    },
    "MCA": {
        "bg_top": (18, 10, 45),
        "bg_bottom": (45, 20, 85),
        "accent": (192, 132, 252),
        "secondary": (0, 210, 255),
        "tag": "MCA ENTERPRISE",
        "tag_bg": (109, 40, 217)
    },
    "M.Tech": {
        "bg_top": (25, 20, 15),
        "bg_bottom": (50, 35, 20),
        "accent": (251, 191, 36),
        "secondary": (244, 63, 94),
        "tag": "M.TECH RESEARCH",
        "tag_bg": (180, 83, 9)
    },
    "IIT-Level / Research-Grade": {
        "bg_top": (30, 10, 25),
        "bg_bottom": (65, 15, 45),
        "accent": (251, 113, 133),
        "secondary": (168, 85, 247),
        "tag": "IIT-GRADE RESEARCH",
        "tag_bg": (190, 18, 60)
    }
}

def generate_artwork(project_code, title, level, domain, output_path):
    width, height = 1200, 675
    theme = THEMES.get(level, THEMES["B.Tech"])

    # Base gradient image
    img = Image.new("RGB", (width, height), theme["bg_top"])
    draw = ImageDraw.Draw(img)

    # Vertical gradient
    r1, g1, b1 = theme["bg_top"]
    r2, g2, b2 = theme["bg_bottom"]
    for y in range(height):
        ratio = y / height
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Abstract technical pattern / grid
    grid_color = (255, 255, 255, 12)
    for x in range(0, width, 50):
        draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 12), width=1)
    for y in range(0, height, 50):
        draw.line([(0, y), (width, y)], fill=(255, 255, 255, 12), width=1)

    # Ambient glowing geometric circuits
    random.seed(sum(ord(c) for c in project_code))
    for _ in range(6):
        cx = random.randint(100, width - 100)
        cy = random.randint(100, height - 100)
        radius = random.randint(30, 120)
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=theme["accent"], width=2)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=theme["accent"])

    # Diagonal accent banner lines
    draw.line([(0, height - 80), (width, height - 200)], fill=theme["secondary"], width=2)
    draw.line([(0, height - 60), (width, height - 180)], fill=theme["accent"], width=3)

    # Top Brand Ribbon
    draw.rectangle([60, 45, width - 60, 50], fill=theme["accent"])

    # Watermark Brand Logo Top-Right
    draw.text((width - 260, 65), "PROJECTVERSE", fill=(255, 255, 255))
    draw.text((width - 260, 85), "ACADEMIC MARKETPLACE", fill=theme["accent"])

    # Project Level Badge (Top Left)
    draw.rounded_rectangle([60, 65, 250, 105], radius=8, fill=theme["tag_bg"])
    draw.text((80, 75), theme["tag"], fill=(255, 255, 255))

    # Unique Project Code Pill
    draw.rounded_rectangle([265, 65, 400, 105], radius=8, fill=(15, 23, 42), outline=theme["accent"], width=2)
    draw.text((290, 75), project_code, fill=theme["accent"])

    # Domain Pill
    draw.rounded_rectangle([60, 120, 360, 155], radius=6, fill=(30, 41, 59))
    draw.text((75, 130), f"Domain: {domain}", fill=(203, 213, 225))

    # Main Project Title Box
    title_box_top = 220
    draw.rounded_rectangle([60, title_box_top, width - 60, title_box_top + 260], radius=16, fill=(15, 23, 42, 230), outline=(51, 65, 85), width=2)

    # Accent Left Border on Title Box
    draw.rounded_rectangle([60, title_box_top, 72, title_box_top + 260], radius=8, fill=theme["accent"])

    # Title Formatting (Word wrap)
    words = title.split()
    lines = []
    current_line = []
    for word in words:
        if len(" ".join(current_line + [word])) <= 34:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))

    # Render Title Text
    y_text = title_box_top + 40
    for line in lines[:3]:
        # Draw shadow
        draw.text((102, y_text + 2), line, fill=(0, 0, 0))
        # Draw text
        draw.text((100, y_text), line, fill=(255, 255, 255))
        y_text += 45

    # Features Subtitle inside Title Box
    draw.text((100, title_box_top + 195), "Verified IEEE Specification • 3NF Database • Full Source Code • Viva Preparation", fill=theme["accent"])

    # Bottom Footer Bar
    draw.rectangle([0, height - 60, width, height], fill=(10, 15, 30))
    draw.text((60, height - 42), "PROJECTVERSE 2026 • Verified Academic Deliverables • 100% University Compliant", fill=(148, 163, 184))
    draw.text((width - 260, height - 42), "Instant Access via UPI", fill=theme["accent"])

    # Save as WebP
    img.save(output_path, "WEBP", quality=88)

def generate_all():
    conn = sqlite3.connect("projectverse.db")
    cur = conn.cursor()
    cur.execute("SELECT project_code, title, academic_level, domain, image_url FROM projects ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()

    print(f"Generating bespoke 1200x675 WebP artworks for {len(rows)} projects...")
    count = 0
    for code, title, level, domain, img_url in rows:
        # Resolve target path from img_url e.g. /static/projects/bca/BCA001.webp -> static/projects/bca/BCA001.webp
        clean_rel = img_url.lstrip("/")
        generate_artwork(code, title, level, domain, clean_rel)
        count += 1
        if count % 15 == 0 or count == len(rows):
            print(f"Generated {count}/{len(rows)} images...")

    print("All 90 bespoke project artwork images generated successfully in WebP format!")

if __name__ == "__main__":
    generate_all()
