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
**Status:** *Not recommended for practical exposure monitoring*

**状态**：*不建议实战使用*

This LUT applies a global EV offset to the EL Zone mapping, effectively remapping higher exposure levels into lower EV color zones.  
As a result, regions that are already close to or entering overexposure may no longer be clearly indicated by the EL Zone clipping warning colors (e.g. pink/white), which can obscure real highlight clipping and reduce the reliability of exposure judgement.
For practical use, EL Zone should be treated as a **fixed reference system**. ETTR is better achieved by using the **0EV LUT** and pushing exposure toward the highlight limit without clipping, rather than by shifting the EL Zone reference itself.

This LUT is retained for **technical comparison and analysis only**, and is **not recommended** for on-set or real-world exposure monitoring.

> 该版本通过整体 EV 偏移改变了 EL Zone 的参考系，本质上会将高曝光区域重新映射到较低的伪色区间，导致真实过曝区域在伪色中不再被清晰标记，从而降低曝光判断的可靠性。  
> 在实际拍摄中，更合理的做法是将 EL Zone 作为**固定参考系**使用，通过 0EV 版本在不裁切高光的前提下向右曝光，而不是整体平移伪色区间。因此该 LUT 仅保留作为技术对照与分析用途，不建议实战使用。




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

