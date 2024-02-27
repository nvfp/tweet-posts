
def hsl_to_hex(h, s, l):
    """
    Params:
    - h: hue (0-360)
    - s: saturation (0-1)
    - l: lightness (0-1)
    """
    h /= 360
    s, l = min(1, max(0, s)), min(1, max(0, l))
    if s == 0:
        r = g = b = int(l * 255)
    else:
        def hue_to_rgb(p, q, t):
            if t < 0:
                t += 1
            if t > 1:
                t -= 1
            if t < 1/6:
                return p + (q - p) * 6 * t
            if t < 1/2:
                return q
            if t < 2/3:
                return p + (q - p) * (2/3 - t) * 6
            return p
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = int(hue_to_rgb(p, q, h + 1/3) * 255)
        g = int(hue_to_rgb(p, q, h) * 255)
        b = int(hue_to_rgb(p, q, h - 1/3) * 255)
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def get_ffmpeg_drawtext_filter(text, x, y, fcolor, fsize, font):
    text = text.replace("'", '`')
    return (
        f"drawtext="
        f"text='{text}':"
        f"x={x}:"
        f"y={y}:"
        f"fontcolor={fcolor}:"
        f"fontsize={fsize}:"
        f"fontfile={font}"
    )
