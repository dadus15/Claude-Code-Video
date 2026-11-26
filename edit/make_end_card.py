"""End card Turismo (1080x1920) wg youtube-edit/BRAND-TURISMO: biale tlo, granatowe logo, tagline z czerwonym STYLE."""
import sys
from PIL import Image, ImageDraw, ImageFont
FONT = "/root/.claude/skills/synced/5628d1e2-09fa-4684-99d7-f6f5adccad20_383ed38f-cdf3-40a8-92c9-21fa68bbbc10/youtube-edit/assets/fonts/DMSans-{}.ttf"
NAVY, RED, GREY = (10, 27, 43), (199, 34, 42), (95, 104, 115)
logo_path, out = sys.argv[1], sys.argv[2]
W, H = 1080, 1920
im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
def tracked(text, font, y, fill, track=0.16, x_center=W // 2, parts=None):
    # draw text with letter-spacing; parts = list of (text, color)
    parts = parts or [(text, fill)]
    sp = font.size * track
    widths = [sum(font.getlength(c) + sp for c in t) - sp for t, _ in parts]
    space = font.getlength(" ") + sp
    total = sum(widths) + space * (len(parts) - 1)
    x = x_center - total / 2
    for (t, col), w in zip(parts, widths):
        for c in t:
            d.text((x, y), c, font=font, fill=col); x += font.getlength(c) + sp
        x += space
logo = Image.open(logo_path).convert("RGBA")
lw = 760; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
im.paste(logo, ((W - lw) // 2 + 20, 640), logo)
f_tag = ImageFont.truetype(FONT.format(700), 58)
tracked(None, f_tag, 640 + logo.height + 90, NAVY, parts=[("UNLOCK", NAVY), ("YOUR", NAVY), ("STYLE", RED)])
y_rule = 640 + logo.height + 200
d.rectangle((W // 2 - 60, y_rule, W // 2 + 60, y_rule + 4), fill=RED)
f_model = ImageFont.truetype(FONT.format(500), 34)
tracked(None, f_model, y_rule + 40, GREY, track=0.12, parts=[("TURISMO FORGED V05", NAVY), ("·", RED), ("AUDI RS5", NAVY)])
f_cta = ImageFont.truetype(FONT.format(700), 44); f_mail = ImageFont.truetype(FONT.format(500), 32)
f_name = ImageFont.truetype(FONT.format(700), 40)
tracked(None, f_name, 1262, NAVY, track=0.08, parts=[("DANIEL", NAVY), ("CHMIELEWSKI", NAVY)])
tracked(None, f_cta, 1330, NAVY, track=0.06, parts=[("+48 501 404 861", NAVY)])
tracked(None, f_mail, 1400, GREY, track=0.02, parts=[("daniel.chmielewski@turismo-wheels.com", GREY)])
im.save(out); print(out, im.size)
