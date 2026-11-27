"""Invented 'Turismo Projects' app screen (1179x2556) with the real project photo, chip, CTA and a toast.
usage: python3 phone_ui.py <photos_dir> <out.png> pressed(0/1) toast(0..1)"""
import sys, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
PH, OUT, PRESSED, TOAST = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, "..", "fonts")
DMS = "/usr/share/fonts/opentype/inter/Inter-{}.otf"   # Inter: full Polish glyph set (DM Sans from the skill has no ę/ł/ń)
W, H = 1179, 2556; RED = (214, 44, 52)
im = Image.new("RGB", (W, H), (12, 12, 14)); d = ImageDraw.Draw(im)
f = lambda w, s: ImageFont.truetype(DMS.format({700: "Bold", 500: "Medium"}[w]), s)
lora = ImageFont.truetype(os.path.join(FD, "Lora.ttf"), 76); lora.set_variation_by_name("Medium")
# status bar + dynamic island
d.text((110, 62), "9:41", font=f(700, 52), fill=(255, 255, 255)); d.rounded_rectangle((W / 2 - 190, 40, W / 2 + 190, 150), 55, fill=(0, 0, 0))
d.rounded_rectangle((W - 240, 74, W - 140, 116), 12, outline=(255, 255, 255), width=4); d.rectangle((W - 234, 80, W - 160, 110), fill=(255, 255, 255))
# header with the logo
logo = Image.open(os.path.join(HERE, "..", "..", "brand", "turismo_logo_white.png")).convert("RGBA"); lw = 420
logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS); im.paste(logo, (80, 230), logo)
d.text((80, 360), "PROJECTS", font=f(700, 34), fill=(150, 150, 158), spacing=0)
# hero photo card (real photo _07)
ph = cv2.cvtColor(cv2.imread(os.path.join(PH, "C26_07.jpg")), cv2.COLOR_BGR2RGB); ch, cw = 1180, 1019
s = max(cw / ph.shape[1], ch / ph.shape[0]) * 1.35; cx, cy = 1180, 980
M = np.float32([[s, 0, cw / 2 - cx * s], [0, s, ch / 2 - cy * s]]); crop = cv2.warpAffine(ph, M, (cw, ch), flags=cv2.INTER_AREA)
card = Image.fromarray(crop); mask = Image.new("L", (cw, ch), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw - 1, ch - 1), 48, fill=255)
im.paste(card, (80, 450), mask)
d.text((80, 1680), "Mercedes-Benz", font=lora, fill=(255, 255, 255)); d.text((80, 1770), "S 560 4MATIC L", font=lora, fill=(255, 255, 255))
for i, (t, bg, fg) in enumerate((("C26", RED, (255, 255, 255)), ("Brushed Silver", (38, 38, 44), (255, 255, 255)), ("22 × 10.5J", (38, 38, 44), (255, 255, 255)))):
    x0 = [80, 260, 690][i]; w = d.textlength(t, font=f(700, 40)) + 70
    d.rounded_rectangle((x0, 1905, x0 + w, 1985), 40, fill=bg); d.text((x0 + 35, 1920), t, font=f(700, 40), fill=fg)
# CTA button (pressed = squish + darker + check)
bx0, by0, bx1, by1 = 80, 2140, W - 80, 2310
if PRESSED:
    k = 14; bx0 += k; bx1 -= k; by0 += 6; by1 -= 6
d.rounded_rectangle((bx0, by0, bx1, by1), 85, fill=(170, 30, 38) if PRESSED else RED)
lab = "Zapytanie wysłane ✓" if PRESSED else "Wyceń dla mojego auta"
tw = d.textlength(lab, font=f(700, 54)); d.text(((W - tw) / 2, (by0 + by1) / 2 - 36), lab, font=f(700, 54), fill=(255, 255, 255))
d.rounded_rectangle((W / 2 - 200, H - 40, W / 2 + 200, H - 28), 6, fill=(220, 220, 225))
# touch circle on the button
if PRESSED:
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov); tx, ty = W * 0.62, (by0 + by1) / 2
    od.ellipse((tx - 70, ty - 64, tx + 70, ty + 64), fill=(255, 255, 255, 90)); od.ellipse((tx - 150, ty - 150, tx + 150, ty + 150), outline=(255, 255, 255, 110), width=6)
    im.paste(ov, (0, 0), ov)
# toast notification (glass dark card from the top)
if TOAST > 0:
    ty0 = int(-300 + TOAST * 500); bg = im.crop((50, max(0, ty0), W - 50, max(1, ty0 + 260))).filter(ImageFilter.GaussianBlur(30))
    tl = Image.new("RGBA", (W - 100, 260), (0, 0, 0, 0)); tdl = ImageDraw.Draw(tl)
    tl.paste(bg.resize((W - 100, 260)), (0, 0)); m = Image.new("L", (W - 100, 260), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, W - 101, 259), 60, fill=255)
    over = Image.new("RGBA", (W - 100, 260), (40, 40, 46, 200)); tl = Image.alpha_composite(tl.convert("RGBA"), over)
    tdl = ImageDraw.Draw(tl); tdl.rounded_rectangle((36, 52, 186, 202), 36, fill=RED)
    icon = logo.resize((130, int(logo.height * 130 / logo.width))); tdl.text((0, 0), "", fill=0)
    tdl.text((92, 98), "T", font=f(700, 70), fill=(255, 255, 255), anchor="mm") if False else None
    mark = Image.open(os.path.join(HERE, "..", "..", "brand", "turismo_logo_white.png")).convert("RGBA").crop((19, 20, 1040, 541)).resize((112, 57))
    tl.paste(mark, (55, 98), mark)
    tdl.text((220, 50), "Daniel Chmielewski · Turismo Wheels", font=f(700, 40), fill=(255, 255, 255))
    tdl.text((220, 112), "Dziękuję! Twoje zapytanie dotarło.", font=f(500, 38), fill=(220, 220, 226))
    tdl.text((220, 166), "teraz", font=f(500, 32), fill=(150, 150, 158))
    im.paste(tl, (50, ty0), m)
im.save(OUT); print("UI", OUT)
