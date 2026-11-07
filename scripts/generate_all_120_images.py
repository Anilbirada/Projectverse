"""
PROJECTVERSE - 120 Unique Project Image Generator
Creates 120 bespoke 1200x675 (16:9) WebP project images
60 in static/projects/bca/ (BCA001 to BCA060)
60 in static/projects/be/ (BE001 to BE060)
"""
import os
import math
import random
import sqlite3
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BCA_DIR = os.path.join("static", "projects", "bca")
BE_DIR = os.path.join("static", "projects", "be")
QR_DIR = os.path.join("static", "uploads", "qr")
SCREENSHOT_DIR = os.path.join("static", "uploads", "screenshots")
RESOURCES_DIR = os.path.join("static", "uploads", "resources")

for d in [BCA_DIR, BE_DIR, QR_DIR, SCREENSHOT_DIR, RESOURCES_DIR]:
    os.makedirs(d, exist_ok=True)

# Generate an official sample UPI QR Code image if not present
def generate_official_upi_qr():
    qr_path = os.path.join(QR_DIR, "official_upi_qr.png")
    if not os.path.exists(qr_path):
        img = Image.new("RGBA", (500, 500), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Border
        draw.rounded_rectangle([15, 15, 485, 485], radius=16, outline=(15, 23, 42), width=3)
        # Header banner
        draw.rectangle([16, 16, 484, 80], fill=(15, 23, 42))
        draw.text((120, 36), "PROJECTVERSE UPI", fill=(0, 210, 255))
        draw.text((120, 56), "Scan with any UPI App", fill=(200, 210, 230))
        
        # QR Code Finder Patterns (Top-Left, Top-Right, Bottom-Left)
        for fx, fy in [(60, 110), (330, 110), (60, 330)]:
            draw.rectangle([fx, fy, fx + 110, fy + 110], fill=(15, 23, 42))
            draw.rectangle([fx + 15, fy + 15, fx + 95, fy + 95], fill=(255, 255, 255))
            draw.rectangle([fx + 30, fy + 30, fx + 80, fy + 80], fill=(15, 23, 42))

        # QR Matrix Grid simulation
        random.seed(42)
        grid_size = 14
        cell_size = 12
        start_x, start_y = 60, 110
        for gx in range(28):
            for gy in range(25):
                px = start_x + gx * cell_size
                py = start_y + gy * cell_size
                # Avoid finder zones
                if (px < 190 and py < 240) or (px > 310 and py < 240) or (px < 190 and py > 310):
                    continue
                if random.random() > 0.45:
                    draw.rectangle([px, py, px + cell_size - 2, py + cell_size - 2], fill=(15, 23, 42))

        # Center Brand Logo in QR
        draw.rounded_rectangle([200, 215, 300, 285], radius=10, fill=(15, 23, 42), outline=(0, 210, 255), width=2)
        draw.text((215, 235), "PV", fill=(0, 210, 255))
        draw.text((210, 255), "UPI PAY", fill=(255, 255, 255))

        # Footer
        draw.rectangle([16, 435, 484, 484], fill=(241, 245, 249))
        draw.text((130, 450), "BHIM  |  GPay  |  PhonePe  |  Paytm", fill=(71, 85, 105))

        img.save(qr_path)
        print("Generated official UPI QR Code at:", qr_path)

# Generate a sample verified receipt screenshot for demo order
def generate_sample_receipt():
    rec_path = os.path.join(SCREENSHOT_DIR, "sample_receipt.png")
    if not os.path.exists(rec_path):
        img = Image.new("RGB", (600, 800), (248, 250, 252))
        draw = ImageDraw.Draw(img)
        # Header
        draw.rectangle([0, 0, 600, 160], fill=(16, 185, 129))
        draw.ellipse([260, 30, 340, 110], fill=(255, 255, 255))
        # Checkmark
        draw.line([(280, 70), (295, 85), (325, 55)], fill=(16, 185, 129), width=6)
        draw.text((210, 120), "Payment Successful", fill=(255, 255, 255))
        
        # Details Card
        draw.rounded_rectangle([40, 190, 560, 750], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.text((70, 220), "Paid to: PROJECTVERSE ACADEMIC", fill=(15, 23, 42))
        draw.text((70, 250), "UPI ID: projectverse@okaxis", fill=(100, 116, 139))
        draw.text((70, 300), "Amount: Rs 1,899.00", fill=(15, 23, 42))
        draw.line([(70, 340), (530, 340)], fill=(226, 232, 240), width=1)
        draw.text((70, 370), "UPI Transaction ID / UTR", fill=(100, 116, 139))
        draw.text((70, 400), "492817293810", fill=(15, 23, 42))
        draw.text((70, 450), "Project ID: BCA001", fill=(15, 23, 42))
        draw.text((70, 480), "Date: 06 Nov 2026, 07:15 PM", fill=(100, 116, 139))
        draw.text((70, 530), "Status: Completed (Instant)", fill=(16, 185, 129))
        
        img.save(rec_path)
        print("Generated sample receipt screenshot at:", rec_path)

# Generate a sample deliverable zip file
def generate_sample_deliverable_files():
    import zipfile
    for code in ["BCA001", "BE001"]:
        zip_path = os.path.join(RESOURCES_DIR, f"{code}_source_code.zip")
        if not os.path.exists(zip_path):
            with zipfile.ZipFile(zip_path, 'w') as zf:
                zf.writestr("README.md", f"# {code} - PROJECTVERSE Verified Source Code Package\n\nAcademic Project Deliverables\nComplete runnable code, database SQL schema, and documentation.\nVerified for academic demonstration.")
                zf.writestr("app/server.py", "# Clean application entrypoint\nprint('Starting Projectverse Verified Academic System...')\n")
                zf.writestr("database/schema.sql", "-- Academic Relational Schema\nCREATE TABLE records (id INT PRIMARY KEY, timestamp DATETIME);\n")
            print(f"Generated sample deliverable zip: {zip_path}")

# Distinct Domain Themes (Color Accents, Gradient stops, and Glyphs)
THEMES = {
    "Artificial Intelligence & Machine Learning": {
        "bg_top": (10, 17, 40), "bg_bot": (24, 18, 56),
        "primary": (0, 210, 255), "secondary": (168, 85, 247),
        "tag": "AI & MACHINE LEARNING", "type": "neural"
    },
    "Full Stack Web Development": {
        "bg_top": (15, 23, 42), "bg_bot": (13, 43, 62),
        "primary": (56, 189, 248), "secondary": (52, 211, 153),
        "tag": "FULL STACK WEB DEV", "type": "web"
    },
    "Python & Automation": {
        "bg_top": (17, 24, 39), "bg_bot": (35, 29, 64),
        "primary": (251, 191, 36), "secondary": (96, 165, 250),
        "tag": "PYTHON & AUTOMATION", "type": "code"
    },
    "Data Science & Business Intelligence": {
        "bg_top": (11, 23, 44), "bg_bot": (18, 30, 58),
        "primary": (244, 63, 94), "secondary": (59, 130, 246),
        "tag": "DATA SCIENCE & BI", "type": "chart"
    },
    "Mobile & Modern Applications": {
        "bg_top": (13, 27, 42), "bg_bot": (22, 50, 72),
        "primary": (45, 212, 191), "secondary": (129, 140, 248),
        "tag": "MOBILE & MODERN APPS", "type": "mobile"
    },
    "Cybersecurity, Cloud & Advanced Systems": {
        "bg_top": (8, 15, 30), "bg_bot": (20, 20, 48),
        "primary": (239, 68, 68), "secondary": (0, 210, 255),
        "tag": "CYBERSECURITY & CLOUD", "type": "shield"
    },
    "Advanced AI & Generative AI": {
        "bg_top": (15, 12, 41), "bg_bot": (34, 16, 68),
        "primary": (192, 132, 252), "secondary": (56, 189, 248),
        "tag": "ADVANCED & GENERATIVE AI", "type": "genai"
    },
    "Advanced Machine Learning & Deep Learning": {
        "bg_top": (10, 15, 36), "bg_bot": (20, 32, 60),
        "primary": (0, 229, 255), "secondary": (124, 58, 237),
        "tag": "DEEP LEARNING & CV", "type": "vision"
    },
    "Advanced Full Stack & Enterprise Development": {
        "bg_top": (15, 23, 42), "bg_bot": (30, 41, 59),
        "primary": (99, 102, 241), "secondary": (45, 212, 191),
        "tag": "ENTERPRISE ARCHITECTURE", "type": "enterprise"
    },
    "Cybersecurity & Blockchain": {
        "bg_top": (12, 18, 38), "bg_bot": (22, 20, 54),
        "primary": (245, 158, 11), "secondary": (99, 102, 241),
        "tag": "CYBER & BLOCKCHAIN", "type": "blockchain"
    },
    "Cloud Computing, IoT & Distributed Systems": {
        "bg_top": (10, 25, 47), "bg_bot": (18, 45, 75),
        "primary": (52, 211, 153), "secondary": (56, 189, 248),
        "tag": "CLOUD & IOT SYSTEMS", "type": "iot"
    },
    "Advanced Data Science & Emerging Technologies": {
        "bg_top": (14, 19, 44), "bg_bot": (32, 23, 62),
        "primary": (236, 72, 153), "secondary": (0, 210, 255),
        "tag": "EMERGING TECH & BIG DATA", "type": "graph"
    }
}

DEFAULT_THEME = {
    "bg_top": (10, 17, 40), "bg_bot": (20, 28, 55),
    "primary": (0, 210, 255), "secondary": (168, 85, 247),
    "tag": "ACADEMIC PROJECT", "type": "generic"
}

def draw_visual_motif(draw, theme_type, pri, sec, seed_val):
    random.seed(seed_val)
    cx, cy = 880, 337  # Right-hand focal area for visual illustration

    # Background ambient radial glow
    for r in range(240, 40, -20):
        alpha = int(25 * (1 - r / 240))
        glow_col = (pri[0] // 4, pri[1] // 4, pri[2] // 4)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=glow_col, width=2)

    if theme_type in ["neural", "genai"]:
        # Neural Network Interconnected Nodes
        layers = [3, 5, 6, 4, 2]
        layer_x = [cx - 180 + i * 90 for i in range(len(layers))]
        node_coords = []
        for li, (lx, num_nodes) in enumerate(zip(layer_x, layers)):
            spacing = 260 / (num_nodes + 1)
            layer_nodes = []
            for ni in range(num_nodes):
                ny = cy - 130 + (ni + 1) * spacing
                layer_nodes.append((lx, ny))
            node_coords.append(layer_nodes)

        # Draw synapses
        for li in range(len(node_coords) - 1):
            for n1 in node_coords[li]:
                for n2 in node_coords[li + 1]:
                    alpha_factor = random.random()
                    line_col = pri if alpha_factor > 0.4 else sec
                    draw.line([n1, n2], fill=(line_col[0] // 2, line_col[1] // 2, line_col[2] // 2), width=1)

        # Draw glowing node points
        for layer in node_coords:
            for nx, ny in layer:
                draw.ellipse([nx - 9, ny - 9, nx + 9, ny + 9], fill=(15, 23, 42), outline=pri, width=2)
                draw.ellipse([nx - 4, ny - 4, nx + 4, ny + 4], fill=pri)

    elif theme_type in ["vision"]:
        # Object detection / Computer Vision Bounding Boxes & Reticle
        draw.ellipse([cx - 150, cy - 150, cx + 150, cy + 150], outline=pri, width=2)
        draw.ellipse([cx - 110, cy - 110, cx + 110, cy + 110], outline=(pri[0]//2, pri[1]//2, pri[2]//2), width=1)
        # Crosshair lines
        draw.line([(cx - 170, cy), (cx + 170, cy)], fill=pri, width=1)
        draw.line([(cx, cy - 170), (cx, cy + 170)], fill=pri, width=1)
        # Bounding boxes
        boxes = [
            (cx - 110, cy - 90, cx - 10, cy + 50, "OBJECT [CONF: 98%]", pri),
            (cx + 15, cy - 60, cx + 130, cy + 80, "TARGET [YOLOv8]", sec)
        ]
        for bx1, by1, bx2, by2, label, col in boxes:
            draw.rectangle([bx1, by1, bx2, by2], outline=col, width=2)
            # Corner markers
            d = 12
            draw.line([(bx1, by1), (bx1 + d, by1)], fill=col, width=3)
            draw.line([(bx1, by1), (bx1, by1 + d)], fill=col, width=3)
            draw.line([(bx2, by2), (bx2 - d, by2)], fill=col, width=3)
            draw.line([(bx2, by2), (bx2, by2 - d)], fill=col, width=3)
            draw.rectangle([bx1, by1 - 18, bx1 + 130, by1], fill=(15, 23, 42))
            draw.text((bx1 + 4, by1 - 16), label, fill=col)

    elif theme_type in ["shield"]:
        # Cybersecurity Shield & Lock Key
        # Shield polygon
        pts = [
            (cx, cy - 130),
            (cx + 110, cy - 80),
            (cx + 90, cy + 60),
            (cx, cy + 135),
            (cx - 90, cy + 60),
            (cx - 110, cy - 80)
        ]
        draw.polygon(pts, fill=(15, 23, 42), outline=pri)
        # Inner shield
        inner_pts = [
            (cx, cy - 105),
            (cx + 85, cy - 65),
            (cx + 70, cy + 45),
            (cx, cy + 105),
            (cx - 70, cy + 45),
            (cx - 85, cy - 65)
        ]
        draw.polygon(inner_pts, outline=sec, width=2)
        # Lock in center
        draw.rounded_rectangle([cx - 30, cy - 15, cx + 30, cy + 45], radius=6, fill=pri)
        draw.arc([cx - 20, cy - 45, cx + 20, cy - 5], 180, 0, fill=pri, width=6)
        draw.ellipse([cx - 6, cy + 5, cx + 6, cy + 17], fill=(15, 23, 42))
        draw.line([(cx, cy + 16), (cx, cy + 28)], fill=(15, 23, 42), width=3)
        # Encryption rings
        for i in range(12):
            angle = i * (math.pi / 6)
            rx = int(cx + 140 * math.cos(angle))
            ry = int(cy + 140 * math.sin(angle))
            draw.point((rx, ry), fill=pri)

    elif theme_type in ["blockchain"]:
        # Linked Blockchain Blocks
        block_w, block_h = 100, 65
        b_coords = [
            (cx - 160, cy - 40),
            (cx - 30, cy - 40),
            (cx + 100, cy - 40)
        ]
        for idx, (bx, by) in enumerate(b_coords):
            draw.rounded_rectangle([bx, by, bx + block_w, by + block_h], radius=8, fill=(15, 23, 42), outline=pri, width=2)
            draw.text((bx + 12, by + 12), f"BLOCK #{idx+1}", fill=pri)
            draw.text((bx + 12, by + 32), f"HASH: {hex(seed_val + idx)[2:8]}..", fill=sec)
            # Connectors
            if idx < 2:
                cnx1 = bx + block_w
                cny = by + block_h // 2
                cnx2 = b_coords[idx + 1][0]
                draw.line([(cnx1, cny), (cnx2, cny)], fill=sec, width=3)
                draw.ellipse([cnx1 + 10, cny - 5, cnx1 + 20, cny + 5], fill=pri)

        # Verification check icon
        draw.ellipse([cx - 25, cy + 65, cx + 25, cy + 115], fill=pri)
        draw.line([(cx - 12, cy + 90), (cx - 4, cy + 98), (cx + 12, cy + 82)], fill=(15, 23, 42), width=4)

    elif theme_type in ["chart"]:
        # Data Analytics, Metrics & Trend Line
        # Grid box
        gx1, gy1, gx2, gy2 = cx - 150, cy - 110, cx + 150, cy + 110
        draw.rectangle([gx1, gy1, gx2, gy2], fill=(15, 23, 42), outline=(50, 65, 95), width=2)
        # Grid lines
        for y in range(gy1 + 35, gy2, 35):
            draw.line([(gx1, y), (gx2, y)], fill=(30, 42, 68), width=1)
        for x in range(gx1 + 45, gx2, 45):
            draw.line([(x, gy1), (x, gy2)], fill=(30, 42, 68), width=1)
        # Bar charts
        bar_x = gx1 + 20
        heights = [50, 85, 60, 110, 140, 95, 160]
        for h in heights:
            draw.rounded_rectangle([bar_x, gy2 - h, bar_x + 22, gy2 - 2], radius=4, fill=(pri[0]//2, pri[1]//2, pri[2]//2), outline=pri)
            bar_x += 38
        # Trend line
        trend_pts = [
            (gx1 + 30, gy2 - 60), (gx1 + 68, gy2 - 95), (gx1 + 106, gy2 - 70),
            (gx1 + 144, gy2 - 120), (gx1 + 182, gy2 - 150), (gx1 + 220, gy2 - 110),
            (gx1 + 258, gy2 - 180)
        ]
        for pi in range(len(trend_pts) - 1):
            draw.line([trend_pts[pi], trend_pts[pi + 1]], fill=sec, width=3)
            draw.ellipse([trend_pts[pi][0] - 4, trend_pts[pi][1] - 4, trend_pts[pi][0] + 4, trend_pts[pi][1] + 4], fill=(255, 255, 255))

    elif theme_type in ["iot"]:
        # IoT Smart Devices & Connected Hub
        # Center Gateway Hub
        draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(15, 23, 42), outline=pri, width=3)
        draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=pri)
        # Concentric sensor wave rings
        for r in [70, 110, 150]:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(pri[0]//3, pri[1]//3, pri[2]//3), width=1)
        # Peripheral sensor nodes
        angles = [0, math.pi/3, 2*math.pi/3, math.pi, 4*math.pi/3, 5*math.pi/3]
        labels = ["TEMP", "PRESSURE", "FLOW", "POWER", "VIBR", "GATEWAY"]
        for idx, ang in enumerate(angles):
            nx = int(cx + 120 * math.cos(ang))
            ny = int(cy + 120 * math.sin(ang))
            draw.line([(cx, cy), (nx, ny)], fill=sec, width=1)
            draw.rounded_rectangle([nx - 28, ny - 16, nx + 28, ny + 16], radius=6, fill=(15, 23, 42), outline=pri)
            draw.text((nx - 18, ny - 7), labels[idx], fill=pri)

    elif theme_type in ["enterprise", "web"]:
        # Modern Browser UI / Architecture Container
        wx1, wy1, wx2, wy2 = cx - 160, cy - 110, cx + 160, cy + 110
        draw.rounded_rectangle([wx1, wy1, wx2, wy2], radius=10, fill=(15, 23, 42), outline=pri, width=2)
        # Window title bar
        draw.rectangle([wx1, wy1, wx2, wy1 + 28], fill=(30, 41, 59))
        draw.ellipse([wx1 + 10, wy1 + 9, wx1 + 20, wy1 + 19], fill=(239, 68, 68))
        draw.ellipse([wx1 + 26, wy1 + 9, wx1 + 36, wy1 + 19], fill=(245, 158, 11))
        draw.ellipse([wx1 + 42, wy1 + 9, wx1 + 52, wy1 + 19], fill=(16, 185, 129))
        draw.text((wx1 + 65, wy1 + 8), "REST API // ARCHITECTURE", fill=(148, 163, 184))
        # Inner panels
        draw.rounded_rectangle([wx1 + 16, wy1 + 40, cx - 20, wy2 - 16], radius=6, fill=(20, 30, 50), outline=sec)
        draw.rounded_rectangle([cx - 5, wy1 + 40, wx2 - 16, wy2 - 16], radius=6, fill=(20, 30, 50), outline=pri)
        draw.text((wx1 + 26, wy1 + 55), "> GET /api/v1", fill=pri)
        draw.text((wx1 + 26, wy1 + 80), "> STATUS: 200 OK", fill=(52, 211, 153))
        draw.text((wx1 + 26, wy1 + 105), "> LATENCY: 24ms", fill=(148, 163, 184))
        # Right visual diagram
        draw.rectangle([cx + 15, wy1 + 55, wx2 - 35, wy1 + 90], fill=(30, 45, 75))
        draw.rectangle([cx + 15, wy1 + 105, wx2 - 35, wy1 + 140], fill=(30, 45, 75))

    elif theme_type in ["code"]:
        # Code Editor with Syntax Highlighting simulation
        wx1, wy1, wx2, wy2 = cx - 160, cy - 110, cx + 160, cy + 110
        draw.rounded_rectangle([wx1, wy1, wx2, wy2], radius=10, fill=(15, 23, 42), outline=pri, width=2)
        draw.rectangle([wx1, wy1, wx2, wy1 + 26], fill=(30, 41, 59))
        draw.ellipse([wx1 + 10, wy1 + 8, wx1 + 18, wy1 + 16], fill=(239, 68, 68))
        draw.ellipse([wx1 + 24, wy1 + 8, wx1 + 32, wy1 + 16], fill=(245, 158, 11))
        draw.ellipse([wx1 + 38, wy1 + 8, wx1 + 46, wy1 + 16], fill=(16, 185, 129))
        draw.text((wx1 + 60, wy1 + 6), "main.py - PROJECTVERSE", fill=(148, 163, 184))
        # Code lines simulation
        code_lines = [
            ("import", (244, 63, 94), " fastapi, pydantic, torch"),
            ("from", (244, 63, 94), " models import Predictor"),
            ("", (255, 255, 255), ""),
            ("def", (56, 189, 248), " execute_pipeline(data: dict):"),
            ("    result = ", (255, 255, 255), "Predictor.run(data)"),
            ("    return", (244, 63, 94), " {'status': 'success'}"),
            ("", (255, 255, 255), ""),
            ("# Automated Production Ready", (100, 116, 139), "")
        ]
        ly = wy1 + 38
        for kw, kw_col, rest in code_lines:
            if kw:
                draw.text((wx1 + 20, ly), kw, fill=kw_col)
                draw.text((wx1 + 20 + len(kw) * 8, ly), rest, fill=(226, 232, 240))
            else:
                draw.text((wx1 + 20, ly), rest, fill=kw_col)
            ly += 18

    else:
        # Generic Modern Tech Geometrics
        draw.polygon([(cx, cy - 120), (cx + 120, cy), (cx, cy + 120), (cx - 120, cy)], outline=pri, width=3)
        draw.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], outline=sec, width=2)
        draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=pri)

def create_project_image(code, title, category, subcategory, difficulty, price, out_path):
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Resolve Theme
    theme = THEMES.get(subcategory, DEFAULT_THEME)
    bg_top = theme["bg_top"]
    bg_bot = theme["bg_bot"]
    pri = theme["primary"]
    sec = theme["secondary"]

    # 1. Subtle smooth gradient background
    for y in range(H):
        ratio = y / H
        r = int(bg_top[0] * (1 - ratio) + bg_bot[0] * ratio)
        g = int(bg_top[1] * (1 - ratio) + bg_bot[1] * ratio)
        b = int(bg_top[2] * (1 - ratio) + bg_bot[2] * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # 2. Tech Cyber Grid Pattern overlay
    grid_spacing = 45
    for x in range(0, W, grid_spacing):
        draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 10), width=1)
    for y in range(0, H, grid_spacing):
        draw.line([(0, y), (W, y)], fill=(255, 255, 255, 10), width=1)

    # 3. Top branding bar
    # Subtle top header glow line
    draw.line([(0, 0), (W, 0)], fill=pri, width=4)
    # Brand tag
    draw.text((60, 45), "PROJECTVERSE", fill=(255, 255, 255))
    draw.text((185, 45), "// ACADEMIC PROJECT REPOSITORY", fill=(100, 116, 139))
    draw.text((W - 240, 45), "STARTING AT Rs 799", fill=pri)

    # 4. Project ID Glow Badge (Top-Left)
    draw.rounded_rectangle([60, 95, 190, 140], radius=8, fill=(15, 23, 42), outline=pri, width=2)
    draw.text((80, 107), code, fill=pri)

    # Category / Domain Badge
    domain_label = theme.get("tag", subcategory.upper())
    draw.rounded_rectangle([205, 95, 205 + len(domain_label) * 9 + 30, 140], radius=8, fill=(30, 41, 59), outline=sec, width=1)
    draw.text((220, 107), domain_label, fill=(226, 232, 240))

    # Difficulty Badge
    diff_x = 205 + len(domain_label) * 9 + 45
    draw.rounded_rectangle([diff_x, 95, diff_x + 130, 140], radius=8, fill=(15, 23, 42), outline=(148, 163, 184))
    draw.text((diff_x + 15, 107), f"* {difficulty.upper()}", fill=(148, 163, 184))

    # 5. Project Title (Wrapped neatly)
    # Title words split
    words = title.split(" ")
    lines = []
    cur_line = []
    for w in words:
        if len(" ".join(cur_line + [w])) <= 34:
            cur_line.append(w)
        else:
            lines.append(" ".join(cur_line))
            cur_line = [w]
    if cur_line:
        lines.append(" ".join(cur_line))

    ty = 180
    for idx, l in enumerate(lines[:3]):
        # Draw soft shadow
        draw.text((62, ty + 2), l, fill=(0, 0, 0))
        # Draw crisp title text
        draw.text((60, ty), l, fill=(255, 255, 255))
        ty += 42

    # 6. Technology & Deliverable Highlights Pills (Bottom-Left)
    pills = [
        "100% Verified Source Code",
        "IEEE Project Report Included",
        "Complete Database Schema",
        "Presentation & Viva Q&A"
    ]
    pill_y = 360
    for p in pills:
        draw.ellipse([60, pill_y + 4, 70, pill_y + 14], fill=pri)
        draw.text((80, pill_y), p, fill=(203, 213, 225))
        pill_y += 32

    # 7. Price & Guarantee Box (Bottom-Left)
    draw.rounded_rectangle([60, 520, 400, 615], radius=12, fill=(15, 23, 42), outline=pri, width=2)
    draw.text((80, 535), f"ACADEMIC ACCESS: Rs {price:,}", fill=(255, 255, 255))
    draw.text((80, 565), "Instant Unlock  |  Verified Deliverables", fill=pri)
    draw.text((80, 588), "Secure UPI Payment with Admin Verification", fill=(148, 163, 184))

    # 8. Right-Hand Unique Thematic Motif
    seed_number = int(code[3:]) if code.startswith("BCA") else int(code[2:]) + 100
    draw_visual_motif(draw, theme["type"], pri, sec, seed_number)

    # 9. Bottom Footer telemetry watermark
    draw.line([(60, 640), (W - 60, 640)], fill=(30, 41, 59), width=1)
    draw.text((60, 648), f"PROJECTVERSE ID: {code}  |  16:9 HD WEBP  |  DEPARTMENT OF {category}", fill=(100, 116, 139))
    draw.text((W - 320, 648), "OFFICIAL ACADEMIC REPOSITORY", fill=(100, 116, 139))

    # Save as high-quality WebP
    img.save(out_path, "WEBP", quality=90)

def generate_all_images():
    generate_official_upi_qr()
    generate_sample_receipt()
    generate_sample_deliverable_files()

    conn = sqlite3.connect("projectverse.db")
    cur = conn.cursor()
    cur.execute("SELECT project_code, title, academic_level, subcategory, difficulty, price, image_url FROM projects;")
    rows = cur.fetchall()
    conn.close()

    total = len(rows)
    print(f"Generating bespoke 1200x675 WebP images for all {total} projects...")
    
    count = 0
    for code, title, level, subcat, diff, price, img_url in rows:
        target_dir = BCA_DIR if level == "BCA" else BE_DIR
        out_path = os.path.join(target_dir, f"{code}.webp")
        create_project_image(code, title, level, subcat, diff, price, out_path)
        count += 1
        if count % 20 == 0 or count == total:
            print(f"Generated {count}/{total} images...")

    print("All 120 unique project images successfully generated!")

if __name__ == "__main__":
    generate_all_images()
