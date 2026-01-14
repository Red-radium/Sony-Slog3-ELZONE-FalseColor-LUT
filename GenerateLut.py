import math
from pathlib import Path
from typing import Tuple, List

# =========================
# 1) EL Zone colors
# =========================
EL_ZONE_COLORS_SRGB_ORDERED: List[Tuple[int, int, int]] = [
    (0, 0, 0),        # 0  clipping_black
    (99, 72, 153),    # 1  -6 and under
    (160, 126, 185),  # 2  -5
    (22, 114, 164),   # 3  -4
    (45, 174, 228),   # 4  -3
    (22, 165, 73),    # 5  -2
    (94, 187, 72),    # 6  -1
    (14, 200, 62),    # 7  -1/2
    (143, 138, 132),  # 8  0 (18% gray)
    (252, 229, 2),    # 9  +1/2
    (255, 248, 167),  # 10 +1
    (244, 113, 41),   # 11 +2
    (245, 166, 73),   # 12 +3
    (237, 30, 36),    # 13 +4
    (227, 126, 142),  # 14 +5
    (240, 190, 191),  # 15 +6 and over
    (255, 255, 255),  # 16 clipping_white
]

def srgb8_to_float(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    return (rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)

EL_ZONE_COLORS_FLOAT = [srgb8_to_float(c) for c in EL_ZONE_COLORS_SRGB_ORDERED]

# =========================
# 2) S-Log3 decode 
# =========================

LOG_CUTOFF_REFLECTION = 0.01125000

CODE_GRAY_18 = 420.0
LOG_SCALE = 261.5

REFLECTANCE_GRAY = 0.18
LOG_OFFSET = 0.01

TOE_CODE_BLACK = 95.0
TOE_CODE_CUTOFF = 171.2102946929  # code at reflection = 0.01125

def slog3_norm_to_reflection(slog3_norm: float) -> float:
    """
    S-Log3 normalized (0..1) -> Scene Linear Reflection
    Follows your screenshot exactly.
    """
    if slog3_norm >= (TOE_CODE_CUTOFF / 1023.0):
        # out = (10^((in*1023 - 420)/261.5))*(0.18+0.01) - 0.01
        return (10.0 ** ((slog3_norm * 1023.0 - CODE_GRAY_18) / LOG_SCALE)) * (REFLECTANCE_GRAY + LOG_OFFSET) - LOG_OFFSET
    else:
        # out = (in*1023 - 95)*0.01125/(171.2102946929 - 95)
        return (slog3_norm * 1023.0 - TOE_CODE_BLACK) * LOG_CUTOFF_REFLECTION / (TOE_CODE_CUTOFF - TOE_CODE_BLACK)

# =========================
# 3) Convert scene-linear luminance to "stops"
# =========================

def safe_log2(x: float, floor: float = 1e-12) -> float:
    return math.log(x if x > floor else floor, 2.0)

def linear_rgb_to_luma_rec709(r: float, g: float, b: float) -> float:
    # Rec.709 luma weights
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def luma_to_stops_relative_to_gray(luma: float) -> float:
    # EV relative to 18% gray
    return safe_log2(luma / REFLECTANCE_GRAY)

# =========================
# 4) EL Zone classification (whole-stop system with ±0.5 boundaries,
#    plus the special -1/2 and +1/2 zones like the standard bar)
# =========================

# Zone centers matching your palette order (excluding clip endpoints):
# -6, -5, -4, -3, -2, -1, -0.5, 0, +0.5, +1, +2, +3, +4, +5, +6
ZONE_CENTERS = [-6, -5, -4, -3, -2, -1, -0.5, 0, 0.5, 1, 2, 3, 4, 5, 6]

def stops_to_zone_index(ev: float) -> int:
    """
    Returns index into EL_ZONE_COLORS_FLOAT (0..16).

    0  = clipping_black
    1  = -6 and under
    ...
    15 = +6 and over
    16 = clipping_white
    """
    # Define boundaries between zone centers as midpoints.
    # We'll clamp anything below the first boundary to -6-and-under,
    # and anything above the last boundary to +6-and-over,
    # then add separate clipping cutoffs as optional extremes.

    # Boundaries in EV between successive centers
    boundaries = []
    for a, b in zip(ZONE_CENTERS[:-1], ZONE_CENTERS[1:]):
        boundaries.append((a + b) / 2.0)

    # Here: below -7.0 EV => black clip, above +7.0 EV => white clip
    if ev <= -7.0:
        return 0
    if ev >= +7.0:
        return 16

    # Determine which interval ev falls into
    # If ev < first boundary => -6 and under (index 1)
    if ev < boundaries[0]:
        return 1

    # If ev >= last boundary => +6 and over (index 15)
    if ev >= boundaries[-1]:
        return 15

    # Otherwise find the bin
    # Bin i corresponds to ZONE_CENTERS[i], and palette index is i+1
    for i in range(len(boundaries) - 1):
        if boundaries[i] <= ev < boundaries[i + 1]:
            return i + 1

    return 8  # 0 zone

# =========================
# 5) Build a 3D .cube LUT
# =========================

def apply_el_zone_false_color(
    r_norm: float,
    g_norm: float,
    b_norm: float,
    offset_ev: float = 0.0,
    make_plus6_white: bool = False,
) -> Tuple[float, float, float]:
    """
    If make_plus6_white=True:
      any EV that maps to +6 and over (index 15) OR clipping white (index 16)
      will output pure white (1.0, 1.0, 1.0).
    """
    r_lin = slog3_norm_to_reflection(r_norm)
    g_lin = slog3_norm_to_reflection(g_norm)
    b_lin = slog3_norm_to_reflection(b_norm)

    luma = linear_rgb_to_luma_rec709(r_lin, g_lin, b_lin)
    ev = luma_to_stops_relative_to_gray(luma)

    ev_effective = ev - offset_ev
    idx = stops_to_zone_index(ev_effective)

    if make_plus6_white and idx >= 15:
        return (1.0, 1.0, 1.0)

    return EL_ZONE_COLORS_FLOAT[idx]

def write_cube_3d(
    out_path: Path,
    size: int = 33,
    offset_ev: float = 0.0,
    title: str = "EL_ZONE_SLOG3_FALSE_COLOR",
    make_plus6_white: bool = False,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"# {title}\n")
        f.write(f"LUT_3D_SIZE {size}\n")

        for r_i in range(size):
            r = r_i / (size - 1)
            for g_i in range(size):
                g = g_i / (size - 1)
                for b_i in range(size):
                    b = b_i / (size - 1)

                    out_r, out_g, out_b = apply_el_zone_false_color(
                        r, g, b,
                        offset_ev=offset_ev,
                        make_plus6_white=make_plus6_white
                    )
                    f.write(f"{out_r:.6f} {out_g:.6f} {out_b:.6f}\n")

if __name__ == "__main__":
    # 1) Normal EL Zone LUT
    write_cube_3d(
        out_path=Path("EL_ZONE_SLOG3_false_color.cube"),
        size=33,
        offset_ev=0.0,
        title="EL_ZONE_SLOG3_FALSE_COLOR",
        make_plus6_white=False,
    )

    # 2) Shifted “to the right” by +1.7 EV, with +6 and over forced to pure white
    write_cube_3d(
        out_path=Path("EL_ZONE_SLOG3_false_color_offset_plus_1p7.cube"),
        size=33,
        offset_ev=1.7,
        title="EL_ZONE_SLOG3_FALSE_COLOR_OFFSET_PLUS_1P7EV_PLUS6WHITE",
        make_plus6_white=True,
    )

    print("Wrote:")
    print(" - EL_ZONE_SLOG3_false_color.cube")
    print(" - EL_ZONE_SLOG3_false_color_offset_plus_1p7.cube")
