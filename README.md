# SonySlog3-ELZONE-FalseColor-LUT

This repository contains **EL Zone–style false color LUTs for Sony S-Log3**, together with the **Python source code used to generate them**.  
The LUTs are intended for **exposure analysis only**, not for creative grading.

## Included LUTs

### 1. `EL_ZONE_SLOG3_false_color.cube`
- Reference exposure placement  
- **0 EV = 18% middle gray**
- Standard EL Zone stop structure (−6 EV to +6 EV)
- Designed for neutral exposure evaluation in S-Log3

### 2. `EL_ZONE_SLOG3_false_color_offset_plus_1p7.cube`
- Exposure thresholds shifted by **+1.7 EV**
- EV labels remain unchanged; only the stop boundaries move
- **+6 EV and above are rendered as pure white**
- Useful for ETTR-style exposure and highlight protection checks

## Source Code

### `GenerateLut.py`

The Python script:
- Implements exact Sony S-Log3 math as documented in [Sony’s technical whitepapers](https://pro.sony/s3/cms-static-content/uploadfile/06/1237494271406.pdf).
- Generates both LUT variants
- Allows modification of:
  - LUT resolution (e.g. 33³, 65³)
  - EV offset
  - Highlight handling behavior
 
## Color Palette

The EL Zone colors were sampled from a reference EL Zone chart and interpreted in sRGB.
There is no official EL Zone RGB specification; the palette is illustrative and intended for clarity rather than colorimetry.

![picture](Images/ColorPalette.jpeg)

## Acknowledgements

- **EL Zone System**  
  The EL Zone exposure system was developed by **Ed Lachman, ASC**.  
  This project is an independent technical implementation and is not affiliated with the original creator.

- **Inspiration**  
  This repository is heavily inspired by the work by [ShinKanji on NikonZR-ELZONE-LUT](https://github.com/ShinKanji/NikonZR-ELZONE-LUT)

