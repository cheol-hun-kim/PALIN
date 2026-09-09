from PIL import Image, ImageDraw, ImageFont
import os

for size in [192, 512]:
    img = Image.new('RGB', (size, size), '#0a0a0f')
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    r = int(size * 0.4)
    for i in range(r, 0, -1):
        ratio = i / r
        cr = int(99 + (16 - 99) * ratio)
        cg = int(102 + (185 - 102) * ratio)
        cb = int(241 + (129 - 241) * ratio)
        draw.ellipse([cx - i, cy - i, cx + i, cy + i], fill=(cr, cg, cb))
    try:
        font = ImageFont.truetype('arial.ttf', int(size * 0.45))
    except Exception:
        font = ImageFont.load_default()
    draw.text((cx, cy), 'P', fill='white', anchor='mm', font=font)
    out = os.path.join('static', f'icon-{size}.png')
    img.save(out)
    print(f'Created {out}')
