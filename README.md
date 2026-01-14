# SonySlog3-ELZONE-FalseColor-LUT

This repository contains **[EL Zone–style](https://www.elzonesystem.com/) false color LUTs for Sony S-Log3**, together with the **Python source code used to generate them**.  
The LUTs are intended for **exposure analysis only**, not for creative grading.

> 本仓库提供基于 Sony S-Log3 的 [EL Zone](https://www.elzonesystem.com/) 伪色 LUT，以及用于生成这些 LUT 的 Python 源代码，仅用于曝光监看。

## Included LUTs

### 1. `EL_ZONE_SLOG3_false_color.cube`
- Reference exposure placement  
- **0 EV = 18% middle gray**
- Standard EL Zone stop structure (−6 EV to +6 EV)
- Designed for neutral exposure evaluation in S-Log3
> 标准 EL Zone 伪色 LUT，0EV 对应 18% 灰，用于常规 S-Log3 曝光判断。

### 2. `EL_ZONE_SLOG3_false_color_offset_plus_1p7.cube`
- Exposure thresholds shifted by **+1.7 EV**
- EV labels remain unchanged; only the stop boundaries move
- **+6 EV and above are rendered as pure white**
- Useful for ETTR-style exposure and highlight protection checks
> 曝光阈值整体右移 +1.7EV，适合向右曝光监看，+6EV 以上直接显示为纯白。

## Source Code

### `GenerateLut.py`

The Python script:
- Implements exact Sony S-Log3 math as documented in [Sony’s technical whitepapers](https://pro.sony/s3/cms-static-content/uploadfile/06/1237494271406.pdf).
- Generates both LUT variants
- Allows modification of:
  - LUT resolution (e.g. 33³, 65³)
  - EV offset
  - Highlight handling behavior
> Python 脚本严格按照 [Sony 官方文档](https://pro.sony/s3/cms-static-content/uploadfile/06/1237494271406.pdf)实现 S-Log3 数学模型，可自定义 LUT 精度、EV 偏移和高光处理方式。
 
## Color Palette

The EL Zone colors were sampled from a reference EL Zone chart and interpreted in sRGB.
There is no official EL Zone RGB specification; the palette is illustrative and intended for clarity rather than colorimetry.
> 颜色取自 EL Zone 参考图表并提取sRGB，颜色仅用于区分曝光区间，不代表严格色度标准。

![picture](Images/ColorPalette.jpeg)

## Acknowledgements

- **EL Zone System**  
  The EL Zone exposure system was developed by **Ed Lachman, ASC**.  
  This project is an independent technical implementation and is not affiliated with the original creator.
  > EL Zone 曝光系统由摄影指导 Ed Lachman, ASC 提出，本项目为独立技术实现。

- **Inspiration**  
  This repository is heavily inspired by the work by [ShinKanji on NikonZR-ELZONE-LUT](https://github.com/ShinKanji/NikonZR-ELZONE-LUT)
  > 本项目受到[ShinKanji 的 NikonZR-ELZONE-LUT](https://github.com/ShinKanji/NikonZR-ELZONE-LUT)项目启发。

