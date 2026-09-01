# -*- coding: utf-8 -*-
# Regenere synthese_png/ (dense, pour l'ecran 384x216 fixe de la calculatrice)
# et synthese_jpg/ (UNE longue image par page/chapitre, pour PC/tel : on la
# fait defiler, pas besoin de la decouper).
# Source : Synthese(1).pdf (0_sources/) rendu en PNG 300dpi au prealable :
#   pdftoppm -png -r 300 "0_sources/Synthese(1).pdf" <SCRATCH>/p
#
# Les deux formats detectent et retirent la marge rouge/rose du cahier
# (ligne verticale de reliure) pour gagner de la place utile.
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

PNG_DENSITY = 0.68  # ecran calculatrice fixe (384x216) -> il faut des fiches petites/nombreuses
OVERLAP = 0.06       # recouvrement entre fiches voisines pour ne rien couper au bord

def strip_bounds(y0, y1, cw, density):
    ch = y1 - y0
    target_h = cw * 9 / 16.0 * density
    n = max(1, round(ch / target_h))
    actual = ch / n
    ov = actual * OVERLAP
    bounds = []
    for i in range(n):
        sy0 = y0 + i * actual - (ov if i > 0 else 0)
        sy1 = y0 + (i + 1) * actual + (ov if i < n - 1 else 0)
        bounds.append((max(y0, int(sy0)), min(y1, int(sy1))))
    return bounds

def process_page(pnum):
    slug = SLUGS[pnum]
    im = Image.open(f"{SCRATCH}/p-{pnum:02d}.png").convert("RGB")
    x0, y0, x1, y1 = get_trimmed_bbox(im)
    cw = x1 - x0
    letters = "abcdefghij"

    for i, (sy0, sy1) in enumerate(strip_bounds(y0, y1, cw, PNG_DENSITY)):
        crop = im.crop((x0, sy0, x1, sy1))
        mini = crop.resize((384, 216), Image.LANCZOS)
        mini = mini.filter(ImageFilter.UnsharpMask(radius=1.2, percent=130, threshold=2))
        mini.save(f"{OUT_PNG}/S{pnum:02d}{letters[i]}-{slug}.png")

    crop = im.crop((x0, y0, x1, y1))
    big_w = 1400
    big_h = int(big_w * crop.height / crop.width)
    big = crop.resize((big_w, big_h), Image.LANCZOS)
    big = big.filter(ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=2))
    big.save(f"{OUT_JPG}/S{pnum:02d}-{slug}.jpg", quality=90)

if __name__ == "__main__":
    for p in range(1, 19):
        process_page(p)
