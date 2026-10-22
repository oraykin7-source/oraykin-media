"""Prepare a photo for an @oraykin Instagram post.

Default (house style since 16.10.2026): full-bleed 4:5, 1080x1350, no frame.
The image is center-cropped to 4:5 and scaled to fill the canvas. Enhancement
is gentle: autocontrast, slight saturation, slight contrast, unsharp mask.

Usage:
    python3 scripts/frame.py <src> <dst>              # full-bleed 4:5
    python3 scripts/frame.py <src> <dst> --frame 54   # old style: white frame

--frame N keeps the pre-16.10 look (image fit inside a white border of N px)
for regenerating old material. No EXIF is written, so location metadata is
dropped.
"""
import argparse
from PIL import Image, ImageEnhance, ImageOps, ImageFilter


def enhance(im):
    im = ImageOps.exif_transpose(im).convert('RGB')
    im = ImageOps.autocontrast(im, cutoff=0.5)
    im = ImageEnhance.Color(im).enhance(1.12)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.5, percent=60, threshold=3))
    return im


def crop_to_ratio(im, W, H):
    """Center-crop so the image has exactly the W:H aspect ratio."""
    if im.width * H > im.height * W:          # too wide
        w = round(im.height * W / H)
        x0 = (im.width - w) // 2
        return im.crop((x0, 0, x0 + w, im.height))
    if im.width * H < im.height * W:          # too tall
        h = round(im.width * H / W)
        y0 = (im.height - h) // 2
        return im.crop((0, y0, im.width, y0 + h))
    return im


def fullbleed(src, dst, W=1080, H=1350):
    """Full-bleed 4:5: center crop to W:H and scale to fill. No border."""
    im = enhance(Image.open(src))
    im = crop_to_ratio(im, W, H).resize((W, H), Image.LANCZOS)
    im.save(dst, quality=95)


def frame(src, dst, W=1080, H=1350, pad=54):
    """Legacy style: fit the whole image inside a white frame of `pad` px."""
    im = enhance(Image.open(src))
    box_w, box_h = W - 2 * pad, H - 2 * pad
    r = min(box_w / im.width, box_h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    c = Image.new('RGB', (W, H), 'white')
    c.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    c.save(dst, quality=95)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--frame', type=int, default=0, metavar='PX',
                    help='white frame width in px (legacy look); 0 = full-bleed')
    a = ap.parse_args()
    if a.frame > 0:
        frame(a.src, a.dst, pad=a.frame)
    else:
        fullbleed(a.src, a.dst)
