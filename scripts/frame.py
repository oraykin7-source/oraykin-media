import sys
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
def enhance(im):
    im = ImageOps.exif_transpose(im).convert('RGB')
    im = ImageOps.autocontrast(im, cutoff=0.5)
    im = ImageEnhance.Color(im).enhance(1.12)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.5, percent=60, threshold=3))
    return im
def frame(src, dst, W=1080, H=1350, pad=54):
    im = enhance(Image.open(src))
    box_w, box_h = W-2*pad, H-2*pad
    r = min(box_w/im.width, box_h/im.height)
    im = im.resize((round(im.width*r), round(im.height*r)), Image.LANCZOS)
    c = Image.new('RGB', (W,H), 'white')
    c.paste(im, ((W-im.width)//2, (H-im.height)//2))
    c.save(dst, quality=95)
if __name__=='__main__':
    frame(sys.argv[1], sys.argv[2])
