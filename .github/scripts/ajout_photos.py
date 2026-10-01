#!/usr/bin/env python3
"""Ajoute les photos listées dans photos-a-ajouter.json (Commons, 3200 px)."""
import json, os, sys, urllib.parse, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = {"User-Agent": "homeselect-photos-sync/1.0 (contact@home-select.fr)"}

with open(os.path.join(REPO, "photos-a-ajouter.json"), encoding="utf-8") as f:
    picks = json.load(f)
with open(os.path.join(REPO, "manifest.json"), encoding="utf-8") as f:
    manifest = json.load(f)

def jpeg_size(buf):
    """Dimensions d'un JPEG (marqueurs SOF)."""
    i = 2
    while i + 9 < len(buf):
        if buf[i] != 0xFF:
            i += 1
            continue
        m = buf[i + 1]
        if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h = buf[i + 5] * 256 + buf[i + 6]
            w = buf[i + 7] * 256 + buf[i + 8]
            return w, h
        if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
            i += 2
            continue
        seg = buf[i + 2] * 256 + buf[i + 3]
        i += 2 + seg
    return None, None

existants = {v["slug"] for v in manifest["villes"]}
for p in picks:
    if p["slug"] in existants:
        print(f"skip {p['slug']} (déjà dans le manifeste)")
        continue
    url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(p["titre"].replace(" ", "_")) + "?width=3200"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        buf = r.read()
    if not buf.startswith(b"\xff\xd8"):
        sys.exit(f"ECHEC {p['slug']}: pas un JPEG ({len(buf)} octets)")
    w, h = jpeg_size(buf)
    if not w or w < 1600:
        sys.exit(f"ECHEC {p['slug']}: largeur {w}")
    dest = os.path.join(REPO, "photos", f"{p['slug']}.jpg")
    with open(dest, "wb") as f:
        f.write(buf)
    manifest["villes"].append({
        "slug": p["slug"], "nom": p["nom"], "region": p["region"],
        "fichier": f"photos/{p['slug']}.jpg", "largeur": w, "hauteur": h,
        "octets": len(buf), "source": p["source"],
        "licence": {"nom": p["licence"]}, "credit": p["credit"],
    })
    print(f"OK {p['slug']}: {w}x{h}, {len(buf)} octets, {p['licence']}")

manifest["nbVilles"] = len(manifest["villes"])
with open(os.path.join(REPO, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("manifeste mis à jour :", len(manifest["villes"]), "villes")
