# -*- coding: utf-8 -*-
# Regenere synthese_png/ (fiches 384x216 zoomees pour l'ecran fixe de la
# calculatrice) et synthese_jpg/ (une longue image par page, pour PC/tel).
# Source : Synthese(1).pdf (0_sources/) rendu en PNG 300dpi au prealable :
#   pdftoppm -png -r 300 "0_sources/Synthese(1).pdf" <SCRATCH>/p
#
# Deux etapes de recadrage :
#  1. retire la marge rose/rouge du cahier (ligne de reliure verticale)
#  2. pour le PNG, chaque bande est ENSUITE recadree serree sur son PROPRE
#     texte (pas la pleine largeur de page) : c'est ca qui fait le zoom.
import os
from PIL import Image, ImageFilter
import numpy as np

SCRATCH = "chemin/vers/synthese_hires"  # dossier des p-01.png .. p-18.png a 300dpi
OUT_PNG = "../synthese_png"
OUT_JPG = "../synthese_jpg"

SLUGS = {
    1: "travail-elementaire", 2: "premier-principe-ferme", 3: "premier-principe-ouvert",
    4: "coeff-calorimetriques", 5: "adiabatique-reversible", 6: "transformations-recap",
    7: "transfo-isochore", 8: "cycle-carnot", 9: "cycle-joule", 10: "rendement-formules",
    11: "rendement-moteur", 12: "calcul-rendement", 13: "puissance-utile", 14: "moteur-diesel",
    15: "moteur-essence", 16: "moteur-2temps-a", 17: "moteur-2temps-b", 18: "frigo-pac",
}

def find_margin_x(im, xmin=250, xmax=950, ymin=400, ymax=3000, frac=0.6):
    """Detecte la ligne verticale rose/rouge de marge du cahier (photo scannee)."""
    arr = np.array(im.convert("RGB")).astype(int)
    ymax = min(ymax, arr.shape[0])
    sub = arr[ymin:ymax, xmin:xmax, :]
    r, g, b = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    mask = (r > g + 5) & (b > g + 3) & (r > 180) & (g < 245)
    colsum = mask.sum(axis=0)
    x = int(np.argmax(colsum)) + xmin
    if colsum.max() < frac * (ymax - ymin):
        return None  # pas de ligne fiable trouvee (ex: page tapee a la machine)
    return x

def content_bbox_from(im, x_start, thresh=245, pad=15):
    g = np.array(im.convert("L"))[:, x_start:]
    mask = g < thresh
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not rows.any():
        return (x_start, 0, im.width, im.height)
    y0, y1 = np.where(rows)[0][[0, -1]]
    x0, x1 = np.where(cols)[0][[0, -1]]
    y0 = max(0, y0 - pad); y1 = min(im.height, y1 + pad)
    x0 = max(x_start, x_start + x0 - pad)
    x1 = min(im.width, x_start + x1 + pad)
    return (int(x0), int(y0), int(x1), int(y1))

def get_trimmed_bbox(im):
    mx = find_margin_x(im)
    x_start = (mx + 12) if mx is not None else 0
    return content_bbox_from(im, x_start)

def tight_bbox_region(im, x0, x1, sy0, sy1, thresh=245, pad_x=20, pad_y=10):
    """Re-crop une bande horizontale serree sur SON PROPRE texte (zoom)."""
    region = im.crop((x0, sy0, x1, sy1))
    g = np.array(region.convert("L"))
    mask = g < thresh
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not rows.any() or not cols.any():
        return (x0, sy0, x1, sy1)
    ry0, ry1 = np.where(rows)[0][[0, -1]]
    rx0, rx1 = np.where(cols)[0][[0, -1]]
    nx0 = max(x0, x0 + rx0 - pad_x)
    nx1 = min(x1, x0 + rx1 + pad_x)
    ny0 = max(sy0, sy0 + ry0 - pad_y)
    ny1 = min(sy1, sy0 + ry1 + pad_y)
    return (int(nx0), int(ny0), int(nx1), int(ny1))

def strip_bounds(y0, y1, cw, density, overlap=0.06):
    ch = y1 - y0
    target_h = cw * 9 / 16.0 * density
    n = max(1, round(ch / target_h))
    actual = ch / n
    ov = actual * overlap
    bounds = []
    for i in range(n):
        sy0 = y0 + i * actual - (ov if i > 0 else 0)
        sy1 = y0 + (i + 1) * actual + (ov if i < n - 1 else 0)
        bounds.append((max(y0, int(sy0)), min(y1, int(sy1))))
    return bounds

PNG_DENSITY = 0.45  # plus petit -> plus de bandes, plus de zoom par bande

def process_page_png(scratch_dir, pnum, slug, out_dir, density=PNG_DENSITY):
    im = Image.open(f"{scratch_dir}/p-{pnum:02d}.png").convert("RGB")
    x0, y0, x1, y1 = get_trimmed_bbox(im)
    cw = x1 - x0
    letters = "abcdefghijklmn"
    n = 0
    for i, (sy0, sy1) in enumerate(strip_bounds(y0, y1, cw, density)):
        tx0, ty0, tx1, ty1 = tight_bbox_region(im, x0, x1, sy0, sy1)
        crop = im.crop((tx0, ty0, tx1, ty1))
        mini = crop.resize((384, 216), Image.LANCZOS)
        mini = mini.filter(ImageFilter.UnsharpMask(radius=1.2, percent=130, threshold=2))
        mini.save(f"{out_dir}/S{pnum:02d}{letters[i]}-{slug}.png")
        n += 1
    return n

def process_page_jpg(scratch_dir, pnum, slug, out_dir):
    im = Image.open(f"{scratch_dir}/p-{pnum:02d}.png").convert("RGB")
    x0, y0, x1, y1 = get_trimmed_bbox(im)
    crop = im.crop((x0, y0, x1, y1))
    big_w = 1400
    big_h = int(big_w * crop.height / crop.width)
    big = crop.resize((big_w, big_h), Image.LANCZOS)
    big = big.filter(ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=2))
    big.save(f"{out_dir}/S{pnum:02d}-{slug}.jpg", quality=90)

if __name__ == "__main__":
    for p in range(1, 19):
        process_page_png(SCRATCH, p, SLUGS[p], OUT_PNG)
        process_page_jpg(SCRATCH, p, SLUGS[p], OUT_JPG)
