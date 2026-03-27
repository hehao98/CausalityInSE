#!/usr/bin/env python3
"""Apply manual classifications to ray_citations.csv."""

import csv
import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(PROJECT_ROOT, "data", "ray_citations.csv")

# All manual classifications by row index
classifications = {
    # Batch 1 (rows 1-23)
    1: "neutral", 2: "neutral", 3: "causal", 5: "neutral", 6: "neutral",
    7: "neutral", 8: "causal", 9: "hedged", 10: "neutral", 11: "neutral",
    13: "neutral", 14: "hedged", 15: "neutral", 16: "neutral", 17: "causal",
    18: "causal", 19: "neutral", 20: "causal", 22: "neutral", 23: "neutral",
    # Batch 2 (rows 24-65)
    24: "neutral", 25: "neutral", 28: "neutral", 29: "neutral", 32: "neutral",
    33: "causal", 35: "neutral", 36: "neutral", 37: "neutral", 39: "hedged",
    40: "causal", 41: "neutral", 42: "neutral", 43: "neutral", 45: "neutral",
    47: "neutral", 50: "neutral", 51: "neutral", 52: "neutral", 53: "neutral",
    54: "causal", 55: "neutral", 56: "neutral", 57: "causal", 58: "neutral",
    59: "neutral", 60: "causal", 61: "neutral", 62: "causal", 65: "causal",
    # Batch 3 (rows 66-107)
    66: "neutral", 68: "neutral", 71: "causal", 72: "hedged", 73: "causal",
    75: "hedged", 77: "causal", 78: "neutral", 79: "causal", 80: "hedged",
    81: "neutral", 82: "neutral", 84: "neutral", 85: "neutral", 86: "neutral",
    87: "neutral", 88: "neutral", 89: "neutral", 90: "causal", 91: "causal",
    92: "neutral", 93: "neutral", 96: "neutral", 98: "neutral", 101: "neutral",
    102: "neutral", 103: "neutral", 104: "neutral", 105: "causal", 107: "neutral",
    # Batch 4 (rows 109-151)
    109: "neutral", 110: "neutral", 111: "neutral", 112: "neutral", 113: "neutral",
    114: "neutral", 115: "neutral", 117: "neutral", 118: "neutral", 119: "neutral",
    120: "hedged", 121: "causal", 122: "causal", 123: "neutral", 124: "hedged",
    125: "causal", 126: "causal", 127: "neutral", 128: "causal", 129: "neutral",
    130: "neutral", 131: "causal", 133: "causal", 134: "causal", 135: "hedged",
    136: "hedged", 139: "neutral", 140: "neutral", 142: "neutral", 143: "causal",
    144: "neutral", 145: "hedged", 148: "neutral", 150: "causal", 151: "causal",
    # Batch 5 (rows 152-200)
    152: "neutral", 153: "neutral", 154: "neutral", 156: "hedged", 157: "neutral",
    158: "neutral", 160: "neutral", 161: "neutral", 162: "neutral", 163: "causal",
    165: "neutral", 166: "causal", 168: "neutral", 169: "neutral", 170: "causal",
    172: "causal", 173: "causal", 174: "causal", 175: "causal", 176: "neutral",
    177: "neutral", 178: "critical", 179: "causal", 180: "neutral", 184: "neutral",
    185: "critical", 186: "neutral", 188: "neutral", 190: "hedged", 191: "causal",
    192: "neutral", 194: "critical", 196: "neutral", 198: "neutral", 200: "neutral",
    # Batch 6 (rows 201-252)
    201: "neutral", 202: "hedged", 203: "neutral", 207: "causal", 209: "neutral",
    210: "neutral", 211: "hedged", 212: "neutral", 215: "neutral", 216: "neutral",
    217: "neutral", 218: "neutral", 219: "neutral", 221: "neutral", 222: "hedged",
    223: "causal", 224: "neutral", 225: "neutral", 227: "neutral", 228: "causal",
    229: "causal", 231: "causal", 232: "hedged", 233: "causal", 234: "causal",
    235: "hedged", 236: "neutral", 237: "neutral", 238: "hedged", 239: "causal",
    240: "causal", 241: "causal", 244: "neutral", 245: "neutral", 246: "neutral",
    247: "neutral", 249: "neutral", 250: "hedged", 251: "neutral", 252: "neutral",
    # Batch 7 (rows 253-303)
    253: "causal", 254: "neutral", 255: "neutral", 256: "causal", 257: "hedged",
    258: "neutral", 259: "neutral", 260: "causal", 261: "neutral", 262: "critical",
    263: "hedged", 264: "hedged", 265: "hedged", 266: "hedged", 269: "causal",
    270: "causal", 271: "causal", 273: "neutral", 274: "critical", 275: "neutral",
    277: "hedged", 279: "neutral", 280: "critical", 282: "neutral", 283: "hedged",
    285: "neutral", 286: "neutral", 287: "neutral", 288: "neutral", 289: "causal",
    290: "causal", 293: "neutral", 294: "neutral", 296: "hedged", 298: "neutral",
    299: "neutral", 300: "neutral", 301: "neutral", 302: "causal", 303: "neutral",
    # Batch 8 (rows 306-354)
    306: "neutral", 307: "hedged", 308: "causal", 309: "causal", 311: "neutral",
    312: "neutral", 313: "neutral", 314: "hedged", 315: "neutral", 316: "neutral",
    317: "neutral", 318: "causal", 319: "neutral", 321: "neutral", 323: "causal",
    325: "neutral", 326: "neutral", 327: "causal", 329: "neutral", 330: "neutral",
    332: "neutral", 333: "neutral", 334: "neutral", 335: "causal", 336: "causal",
    338: "hedged", 339: "hedged", 340: "neutral", 341: "causal", 342: "neutral",
    343: "neutral", 345: "neutral", 347: "neutral", 348: "neutral", 349: "neutral",
    350: "neutral", 351: "neutral", 352: "neutral", 353: "hedged", 354: "critical",
    # Batch 9 (rows 355-406)
    355: "causal", 356: "neutral", 357: "neutral", 361: "neutral", 362: "neutral",
    363: "neutral", 364: "neutral", 366: "neutral", 367: "neutral", 368: "neutral",
    369: "neutral", 373: "causal", 374: "hedged", 375: "hedged", 376: "neutral",
    378: "causal", 379: "neutral", 380: "neutral", 381: "neutral", 382: "neutral",
    383: "neutral", 384: "causal", 385: "causal", 386: "neutral", 388: "causal",
    389: "causal", 390: "causal", 392: "neutral", 393: "neutral", 394: "neutral",
    395: "causal", 396: "neutral", 397: "causal", 398: "neutral", 399: "causal",
    400: "causal", 401: "neutral", 403: "causal", 404: "neutral", 406: "hedged",
    # Batch 10 (rows 407-450)
    407: "neutral", 408: "causal", 409: "causal", 410: "neutral", 412: "causal",
    414: "neutral", 415: "neutral", 418: "neutral", 419: "neutral", 420: "neutral",
    421: "neutral", 423: "neutral", 424: "neutral", 425: "neutral", 426: "neutral",
    427: "neutral", 428: "hedged", 429: "critical", 431: "neutral", 433: "neutral",
    434: "neutral", 435: "neutral", 436: "hedged", 437: "neutral", 440: "neutral",
    446: "neutral", 447: "hedged", 449: "neutral", 450: "hedged",
}

with open(CSV_FILE, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

# Apply classifications
classified_count = 0
for idx, cls in classifications.items():
    rows[idx]["classification"] = cls
    rows[idx]["confidence"] = ""
    rows[idx]["representative_quote"] = ""
    rows[idx]["reason"] = "manual"
    classified_count += 1

# Mark no_context papers
no_ctx_count = 0
for row in rows:
    if row["contexts"] == "[]" and not row.get("classification"):
        row["classification"] = "no_context"
        row["reason"] = "No citation context available"
        no_ctx_count += 1

# Write back
fieldnames = list(rows[0].keys())
with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Summary
counts = {}
for row in rows:
    cls = row.get("classification") or "unclassified"
    counts[cls] = counts.get(cls, 0) + 1

print(f"Classified {classified_count} papers with contexts")
print(f"Marked {no_ctx_count} papers as no_context")
print()
print("Classification summary:")
for cat in ["causal", "hedged", "neutral", "critical", "no_context", "unclassified"]:
    if cat in counts:
        pct = 100 * counts[cat] / len(rows)
        print(f"  {cat:14s} {counts[cat]:4d} ({pct:5.1f}%)")
print(f"  Total: {len(rows)}")

# Among papers WITH contexts only
with_ctx = {k: v for k, v in counts.items() if k != "no_context"}
total_with_ctx = sum(with_ctx.values())
print(f"\nAmong {total_with_ctx} papers with citation contexts:")
for cat in ["causal", "hedged", "neutral", "critical"]:
    if cat in with_ctx:
        pct = 100 * with_ctx[cat] / total_with_ctx
        print(f"  {cat:14s} {with_ctx[cat]:4d} ({pct:5.1f}%)")
