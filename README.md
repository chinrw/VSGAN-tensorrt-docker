# VSGAN-tensorrt-docker

Repository to use super resolution models and video frame interpolation models and also trying to speed them up with TensorRT. This repository contains the fastest inference code that you can find, at least I am trying to archive that. Not all codes can use TensorRT due to various reasons, but I try to add that if it works. Further model architectures are planned to be added later on.

Table of contents
=================

<!--ts-->
   * [Usage](#usage)
   * [Usage example](#usage-example)
   * [Individual examples](#individual-examples)
   * [vs-mlrt (C++ TRT)](#vs-mlrt)
   * [Deduplicated inference](#deduplicated)
   * [Shot Boundary Detection](#shot-boundry)
   * [multi-gpu](#multi-gpu)
   * [ddfi](#ddfi)
   * [VFR (variable refresh rate)](#vfr)
   * [Benchmarks](#benchmarks)
   * [License](#license)
<!--te-->

-------

Currently working networks:
- [Rife4 with HolyWu/vs-rife](https://github.com/HolyWu/vs-rife/) and [hzwer/Practical-RIFE](https://github.com/hzwer/Practical-RIFE) ([rife4.0](https://drive.google.com/file/d/1mUK9iON6Es14oK46-cCflRoPTeGiI_A9/view) [rife4.1](https://drive.google.com/file/d/1CPJOzo2CHr8AN3GQCGKOKMVXIdt1RBR1/view) [rife4.2](https://drive.google.com/file/d/1JpDAJPrtRJcrOZMMlvEJJ8MUanAkA-99/view)
[rife4.3](https://drive.google.com/file/d/1xrNofTGMHdt9sQv7-EOG0EChl8hZW_cU/view) [rife4.4](https://drive.google.com/file/d/1eI24Kou0FUdlHLkwXfk-_xiZqKaZZFZX/view) [rife4.5](https://drive.google.com/file/d/17Bl_IhTBexogI9BV817kTjf7eTuJEDc0/view) [rife4.6](https://drive.google.com/file/d/1EAbsfY7mjnXNa6RAsATj2ImAEqmHTjbE/view) [rife4.7.1](https://drive.google.com/file/d/1s2zMMIJrUAFLexktm1rWNhlIyOYJ3_ju/view) [rife4.8.1](https://drive.google.com/file/d/1wZa3SyegLPUwBQWmoDLM0MumWd2-ii63/view)
[rife4.9.2](https://drive.google.com/file/d/1UssCvbL8N-ty0xIKM5G5ZTEgp9o4w3hp/view) [rife4.10.1](https://drive.google.com/file/d/1WNot1qYBt05LUyY1O9Uwwv5_K8U6t8_x/view) [rife4.11.1](https://drive.google.com/file/d/1Dwbp4qAeDVONPz2a10aC2a7-awD6TZvL/view) [rife4.12.2](https://drive.google.com/file/d/1ZHrOBL217ItwdpUBcBtRE3XBD-yy-g2S/view) [rife4.12 lite](https://drive.google.com/file/d/1KoEJ5x6aisxOpkhdNptsGUrL3yf4iy8b/view) [rife4.13.2](https://drive.google.com/file/d/1mj9lH6Be7ztYtHAr1xUUGT3hRtWJBy_5/view) [rife4.13 lite](https://drive.google.com/file/d/1l3lH9QxQQeZVWtBpdB22jgJ-0kmGvXra/view) [rife4.14](https://drive.google.com/file/d/1BjuEY7CHZv1wzmwXSQP9ZTj0mLWu_4xy/view) [rife4.14 lite](https://drive.google.com/file/d/1eULia_onOtRXHMAW9VeDL8N2_7z8J1ba/view) [rife4.15](https://drive.google.com/file/d/1xlem7cfKoMaiLzjoeum8KIQTYO-9iqG5/view) [rife4.17](https://drive.google.com/file/d/1962p_lEWo_kLTEynarNaRYRNVdaiQG2k/view) [rife4.18](https://drive.google.com/file/d/1octn-UVuEjXa_HlsIUbNeLTTvYCKbC_s/view) [rife4.19-beta](https://drive.google.com/file/d/1Wf09iMyTrvVdG7oG3blVAEHDdLU2dhW2/view) [rife4.20](https://drive.google.com/file/d/11n3YR7-qCRZm9RDdwtqOTsgCJUHPuexA/view) [rife4.21](https://drive.google.com/file/d/1l5u6G8vEkPAT7cYYWwzB6OG8vwBYrxiS/view) [rife4.22](https://drive.google.com/file/d/1qh2DSA9a1eZUTtZG9U9RQKO7N7OaUJ0_/view)) and v2 with [WolframRhodium](https://github.com/WolframRhodium)
- Model based shot boundary detection with [rwightman/pytorch-image-models](https://github.com/rwightman/pytorch-image-models), [snap-research/EfficientFormer (EfficientFormerV2)](https://github.com/snap-research/EfficientFormer), [wentaozhu/AutoShot](https://github.com/wentaozhu/AutoShot), [abhijay9/ShiftTolerant-LPIPS](https://github.com/abhijay9/ShiftTolerant-LPIPS) and [photosynthesis-team/piq](https://github.com/photosynthesis-team/piq)
- [Real-ESRGAN / SRVGGNetCompact](https://github.com/xinntao/Real-ESRGAN)
- [SAFMN](https://github.com/sunny2109/SAFMN)
- [DPIR](https://github.com/cszn/DPIR)
- [Waifu2x](https://github.com/AmusementClub/vs-mlrt/releases/download/model-20211209/waifu2x_v3.7z)
- [real-cugan](https://drive.google.com/drive/folders/1jAJyBf2qKe2povySwsGXsVMnzVyQzqDD)
- [apisr](https://github.com/kiteretsu77/apisr)
- [AnimeJaNai](https://github.com/the-database/mpv-upscale-2x_animejanai)
- [ModernSpanimation](https://github.com/TNTwise/Models/releases/tag/2x_ModernSpanimationV1)
- [AniScale](https://github.com/Sirosky/Upscale-Hub)
- [Anime1080Fixer by zarxrax](https://mega.nz/file/EAs2XZwA#-YrO3QSP8Waz2l5JVtrSew2Dk4gbT0xE0uA5hc5CYRo)

Onnx files can be found [here](https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/tag/models).

Also used:
- TensorRT C++ inference and python script usage with [AmusementClub/vs-mlrt](https://github.com/AmusementClub/vs-mlrt)
- ddfi with [Mr-Z-2697/ddfi-rife](https://github.com/Mr-Z-2697/ddfi-rife) (auto dedup-duplication, not an arch)
- custom ffmpeg with [styler00dollar/ffmpeg-static-arch-docker](https://github.com/styler00dollar/ffmpeg-static-arch-docker)
- lsmash with [AkarinVS/L-SMASH-Works](https://github.com/AkarinVS/L-SMASH-Works)
- bestsource with [vapoursynth/bestsource](https://github.com/vapoursynth/bestsource)
- trt precision check and upscale frame skip with [mafiosnik777/enhancr](https://github.com/mafiosnik777/enhancr)
- temporal fix with [pifroggi/vs_temporalfix](https://github.com/pifroggi/vs_temporalfix)
- color fix with [pifroggi/vs_colorfix](https://github.com/pifroggi/vs_colorfix)
- rife with [HolyWu/vs-rife](https://github.com/HolyWu/vs-rife)

<div id='usage'/>

## Usage
The following docker requires the latest Nvidia driver (560+). After that, follow the following steps:

**WARNING FOR PEOPLE WITHOUT `AVX512`: Instead of using `styler00dollar/vsgan_tensorrt:latest`, which I build with my 7950x and thus with all AVX, use `styler00dollar/vsgan_tensorrt:latest_no_avx512` in `compose.yaml` to avoid `Illegal instruction (core dumped)` which is mentioned in [this issue](https://github.com/styler00dollar/VSGAN-tensorrt-docker/issues/48).**

**AND AS A FINAL INFO, `Error opening input file pipe:` IS NOT A REAL ERROR MESSAGE. That means invalid data got piped into ffmpeg and can be piped error messages for example. To see the actual error messages and what got piped, you can use `vspipe -c y4m inference.py -`.**

Quickstart:
```bash
# if you have Windows, install Docker Desktop https://www.docker.com/products/docker-desktop/

# if you have Arch, install the following dependencies
yay -S docker nvidia-docker nvidia-container-toolkit docker-compose docker-buildx

# run the docker with docker-compose
# you need to be inside the vsgan folder with cli before running the following step, git clone repo and cd into it
# go into the vsgan folder, inside that folder should be compose.yaml, run this command
# you can adjust folder mounts in the yaml file
docker-compose run --rm vsgan_tensorrt
```
There are now multiple containers to choose from, if you don't want the default, then edit `compose.yaml`
and set a different tag `image: styler00dollar/vsgan_tensorrt:x` prior to running `docker-compose run --rm vsgan_tensorrt`.
- `latest`: Default docker with everything. Trying to keep everything updated and fixed.
- `latest_no_avx512` is for cpus without avx512 support, otherwise it just crashes if you try to run avx512 binaries on cpus without such support. Use this if your cpu does not support all instruction sets.
- `minimal`: Bare minimum to run `ffmpeg`, `mlrt` and a few video readers.

| docker image  | compressed download | extracted container | short description |
| ------------- | ------------------- | ------------------- | ----------------- |
| styler00dollar/vsgan_tensorrt:latest | 10gb | 19gb | default latest with trt10.7
| styler00dollar/vsgan_tensorrt:latest_no_avx512 | 10gb | 19gb | trt10.7 without avx512
| styler00dollar/vsgan_tensorrt:trt9.3 | 8gb | 15gb | trt9.3 [use `bfdb96a` with this docker](https://github.com/styler00dollar/VSGAN-tensorrt-docker/commit/bfdb96a329682af19d093ecb990f67e823ea2e89)
| styler00dollar/vsgan_tensorrt:trt9.3_no_avx512 | 8gb | 15gb | trt9.3 without avx512 [use `bfdb96a` with this docker](https://github.com/styler00dollar/VSGAN-tensorrt-docker/commit/bfdb96a329682af19d093ecb990f67e823ea2e89)
| styler00dollar/vsgan_tensorrt:minimal | 6gb | 10gb | trt10.6 + ffmpeg + mlrt + ffms2 + lsmash + bestsource

Piping usage:
```
vspipe -c y4m inference.py - | ffmpeg -i pipe: example.mkv -y
```
If docker does not want to start, try this before you use docker:
```bash
sudo systemctl start docker
```
Linux docker autostart:
```
sudo systemctl enable --now docker
```
The following stuff is for people who want to run things from scratch.
Manual ways of downloading the docker image:
```
# Download prebuild image from dockerhub (recommended)
docker pull styler00dollar/vsgan_tensorrt:latest

# if you have `unauthorized: authentication required` problems, download the docker with
git clone https://github.com/NotGlop/docker-drag
cd docker-drag
python docker_pull.py styler00dollar/vsgan_tensorrt:latest
docker load -i styler00dollar_vsgan_tensorrt.tar
```
Manually building docker image from scratch:
```
# Build docker manually (only required if you want to build from scratch)
# This step is not needed if you already downloaded the docker and is only needed if yo
# want to build it from scratch. Keep in mind that you need to set env variables in windows differently and
# this command will only work in linux. Run that inside that directory
DOCKER_BUILDKIT=1 sudo docker build -t styler00dollar/vsgan_tensorrt:latest .
# If you want to rebuild from scratch or have errors, try to build without cache
DOCKER_BUILDKIT=1 sudo docker build --no-cache -t styler00dollar/vsgan_tensorrt:latest .
```
Manually run docker:
```
# you need to be inside the vsgan folder with cli before running the following step, git clone repo and cd into it
# the folderpath before ":" will be mounted in the path which follows afterwards
# contents of the vsgan folder should appear inside /workspace/tensorrt

sudo docker run --privileged --gpus all -it --rm -v /home/vsgan_path/:/workspace/tensorrt styler00dollar/vsgan_tensorrt:latest

# Windows is mostly similar, but the path needs to be changed slightly:
Example for C://path
docker run --privileged --gpus all -it --rm -v /mnt/c/path:/workspace/tensorrt styler00dollar/vsgan_tensorrt:latest
docker run --privileged --gpus all -it --rm -v //c/path:/workspace/tensorrt styler00dollar/vsgan_tensorrt:latest
```
<div id='usage-example'/>

## Usage example

Small minimalistic example of how to configure inference. If you only want to process one video, then edit video path in `inference.py`
```
video_path = "test.mkv"
```
and then afterwards edit `inference_config.py`.

Small example for upscaling with TensorRT:

```python
import sys
import os

sys.path.append("/workspace/tensorrt/")
import vapoursynth as vs

core = vs.core
vs_api_below4 = vs.__api_version__.api_major < 4
core.num_threads = 8

core.std.LoadPlugin(path="/usr/local/lib/libvstrt.so")


def inference_clip(video_path="", clip=None):
    clip = core.bs.VideoSource(source=video_path)

    clip = vs.core.resize.Bicubic(clip, format=vs.RGBH, matrix_in_s="709")  # RGBS means fp32, RGBH means fp16
    clip = core.trt.Model(
        clip,
        engine_path="/workspace/tensorrt/2x_AnimeJaNai_V2_Compact_36k_op18_fp16_clamp.engine",  # read readme on how to build engine
        num_streams=2,
    )
    clip = vs.core.resize.Bicubic(clip, format=vs.YUV420P8, matrix_s="709")  # you can also use YUV420P10 for example

    return clip
```

Small example for rife interpolation with TensorRT without scene change detection:

```python
import sys
import vapoursynth as vs
from vsrife import rife

sys.path.append("/workspace/tensorrt/")
core = vs.core
core.num_threads = 4

core.std.LoadPlugin(path="/usr/local/lib/libvstrt.so")


def inference_clip(video_path):
    clip = core.bs.VideoSource(source=video_path)

    clip = core.resize.Bicubic(
        clip, format=vs.RGBS, matrix_in_s="709"
    )  # RGBS means fp32, RGBH means fp16

    # interpolation
    clip = rife(clip, trt=True, model="4.22", sc=False)

    clip = core.resize.Bicubic(clip, format=vs.YUV420P8, matrix_s="709")
    return clip
```

More examples in `custom_scripts/`.

Then use the commands above to render. For example:
```
vspipe -c y4m inference.py - | ffmpeg -i pipe: example.mkv
```

Video will be rendered without sound and other attachments. You can add that manually to the ffmpeg command.

To process videos in batch and copy their properties like audio and subtitle to another file, you need to use `main.py`. Edit filepaths and file extention:
```python
input_dir = "/workspace/tensorrt/input/"
output_dir = "/workspace/tensorrt/output/"
files = glob.glob(input_dir + "/**/*.webm", recursive=True)
```
and configure `inference_config.py` like wanted. Afterwards just run
```
python main.py
```

<div id='individual-examples'/>

## Individual examples

More parameter documentation can be found in the plugin repositories.

- Video Reader: [ffms2](https://github.com/FFMS/ffms2/blob/master/doc/ffms2-vapoursynth.md) [lsmash](https://github.com/HomeOfAviSynthPlusEvolution/L-SMASH-Works/blob/master/VapourSynth/README.md) [bestsource](https://github.com/vapoursynth/bestsource)
```python
core.std.LoadPlugin(path="/usr/lib/x86_64-linux-gnu/libffms2.so")
clip = core.ffms2.Source(source=video_path)
clip = core.lsmas.LWLibavSource(source=video_path)
clip = core.bs.VideoSource(source=video_path) # recommended
```

- Convert colorspace: [descale](https://github.com/Irrational-Encoding-Wizardry/descale) [vs](http://www.vapoursynth.com/doc/functions/video/resize.html)
```python
clip = core.descale.Debilinear(clip, 1280, 720)
clip = core.resize.Bicubic(clip, format=vs.RGBS, matrix_in_s="709")
clip = core.resize.Bicubic(clip, width=1280, height=720,, format=vs.RGBS, matrix_in_s="709")
```

- Clamp 0-1
```python
clip = core.akarin.Expr(clip, "x 0 1 clamp")
clip = clip.std.Expr("x 0 max 1 min")
clip = core.std.Limiter(clip, max=1, planes=[0,1,2])
```

- Metrics: [vmaf](https://github.com/HomeOfVapourSynthEvolution/VapourSynth-VMAF)
```python
clip = core.vmaf.Metric(clip, offs1, feature=2)
```

- Scene Detect
```python
clip = core.misc.SCDetect(clip=clip, threshold=0.100)

from src.scene_detect import scene_detect
clip = scene_detect(clip, fp16=True, thresh=0.85, model=12)
```

- TensorRT inference: [vstrt](https://github.com/AmusementClub/vs-mlrt/tree/master/vstrt)
```python
core.std.LoadPlugin(path="/usr/local/lib/libvstrt.so")
clip = core.trt.Model(
    clip,
    engine_path="/workspace/tensorrt/cugan.engine",
    tilesize=[854, 480],
    overlap=[0, 0],
    num_streams=4,
)
```

- dpir inference: [vstrt](https://github.com/AmusementClub/vs-mlrt/tree/master/vstrt)
```python
core.std.LoadPlugin(path="/usr/local/lib/libvstrt.so")
strength = 10.0
noise_level = clip.std.BlankClip(format=vs.GRAYS, color=strength / 100)
clip = core.trt.Model(
    [clip, noise_level],
    engine_path="dpir.engine",
    tilesize=[1280, 720],
    num_streams=2,
)
```

- ORT inference: [vs-mlrt](https://github.com/AmusementClub/vs-mlrt/tree/master/vsort)
```python
core.std.LoadPlugin(path="/usr/local/lib/libvsort.so")
clip = core.ort.Model(clip, "/workspace/tensorrt/2x_ModernSpanimationV2_clamp_op20_fp16_onnxslim.onnx", provider="CUDA", fp16=True, num_streams=2)
```

- Rife: [vs-rife](https://github.com/styler00dollar/vs-rife)
```python
from vsrife import rife
clip = rife(clip, trt=True, model="4.22", sc=False)
```

- Sharpening: [awarpsharp2](https://github.com/dubhater/vapoursynth-awarpsharp2) [cas](https://github.com/HomeOfVapourSynthEvolution/VapourSynth-CAS)
```python
core.std.LoadPlugin(path="/usr/local/lib/x86_64-linux-gnu/libawarpsharp2.so")
clip = core.warp.AWarpSharp2(clip, thresh=128, blur=2, type=0, depth=[16, 8, 8], chroma=0, opt=True, planes=[0,1,2], cplace="mpeg1")
clip = core.cas.CAS(clip, sharpness=0.5)
```

- Color fix: [colorfix](https://github.com/pifroggi/vs_colorfix)
```python
import vs_colorfix
clip = vs_colorfix.average(clip, ref, radius=10, planes=[0, 1, 2], fast=False)
```

- Temporal fix: [temporalfix](https://github.com/pifroggi/vs_temporalfix) (very slow)
```python
core.std.LoadPlugin(path="/usr/local/lib/x86_64-linux-gnu/libmvtools.so")
core.std.LoadPlugin(path="/usr/local/lib/x86_64-linux-gnu/libfillborders.so")
core.std.LoadPlugin(path="/usr/local/lib/x86_64-linux-gnu/libmotionmask.so")
core.std.LoadPlugin(path="/usr/local/lib/x86_64-linux-gnu/libtemporalmedian.so")
from vs_temporalfix import vs_temporalfix
clip = vs_temporalfix(clip, strength=400, tr=6, exclude="[10 20]", debug=False)
```

- Line darken: [linedarken](https://github.com/Selur/VapoursynthScriptsInHybrid/blob/550cc72221848732fa36a5dfb9ad5f98a308dd6e/havsfunc.py#L5217)
```python
from src.utils import FastLineDarkenMOD
clip = FastLineDarkenMOD(clip)
```

<div id='vs-mlrt'/>
  
## vs-mlrt (C++ TRT)
You need to convert onnx models into engines. You need to do that on the same system where you want to do inference. Download onnx models from [here]( https://github.com/AmusementClub/vs-mlrt/releases/download/v7/models.v7.7z) or from [my Github page](https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/tag/models). Inside the docker, you do one of the following commands:
  
Good default choice:
```
trtexec --bf16 --fp16 --onnx=model.onnx --minShapes=input:1x3x8x8 --optShapes=input:1x3x720x1280 --maxShapes=input:1x3x1080x1920 --saveEngine=model.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5
```
If you have the vram to fit the model multiple times, add `--infStreams`.
```
trtexec --bf16 --fp16 --onnx=model.onnx --minShapes=input:1x3x8x8 --optShapes=input:1x3x720x1280 --maxShapes=input:1x3x1080x1920 --saveEngine=model.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5 --infStreams=4
```
DPIR (color) needs 4 channels.
```
trtexec --bf16 --fp16 --onnx=model.onnx --minShapes=input:1x4x8x8 --optShapes=input:1x4x720x1280 --maxShapes=input:1x4x1080x1920 --saveEngine=model.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5
```

**Warning:** Rife with TensorRT is broken without workarounds in every implementation (mlrt, torch_tensorrt, onnxruntime trt,...), even with fp32, and results in wobbly lines and artefacts during panning scenes. Unless Nvidia fixes it, it will stay broken with every onnx. [HolyWu/vs-rife](https://github.com/HolyWu/vs-rife) fixed it by adding torch decompositions in vsrife to prevent TensorRT from using grid sample. HolyWu also added encode cache to avoid repeating `self.encode`. Testing showed that vsrife is not a lot slower than mlrt, so I don't recommend using rife onnx.

Rife v1 needs 8 channels.
```
trtexec --bf16 --fp16 --onnx=model.onnx --minShapes=input:1x8x64x64 --optShapes=input:1x8x720x1280 --maxShapes=input:1x8x1080x1920 --saveEngine=model.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5
```
Rife v2 needs 7 channels. Set the same shape everywhere to avoid build errors.
```
trtexec --bf16 --fp16 --onnx=model.onnx --minShapes=input:1x7x1080x1920 --optShapes=input:1x7x1080x1920 --maxShapes=input:1x7x1080x1920 --saveEngine=model.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5
```
My Shuffle Span has a static shape and needs dynamic conv to be in fp32 for lower precision to work.
```
trtexec --bf16 --fp16 --onnx=sudo_shuffle_span_op20_10.5m_1080p_onnxslim.onnx --saveEngine=sudo_shuffle_span_op20_10.5m_1080p_onnxslim.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5 --infStreams=4 --layerPrecisions=/dynamic/Conv:fp32 --precisionConstraints=obey
```
Put that engine path into `inference_config.py`.

**Warnings**:
- Only add `--bf16` if your GPU supports it, otherwise remove it. If model looks broken, remove `--fp16`.
- Cugan with 3x scale requires same MIN/OPT/MAX shapes.
- rvpV2 needs 6 channels, but does not support variable shapes.
- If you use the FP16 onnx you need to use `RGBH` colorspace, if you use FP32 onnx you need to use `RGBS` colorspace in `inference_config.py` .
- Engines are system specific, don't use across multiple systems.
- Don't use reuse engines for different GPUs.
- If you run out of memory, then you need to adjust the resolutions in that command. If your video is bigger than what you can input in the command, use tiling.
- If you get segfault, reduce `builderOptimizationLevel`. Change can change it down to 1 to speed up the engine building, but may result in worse speeds.
- If you set min, opt and max to the same resolution, it might result in a faster engine.

<div id='deduplicated'/>

## Deduplicated inference
Calculate similarity between frames with [HomeOfVapourSynthEvolution/VapourSynth-VMAF](https://github.com/HomeOfVapourSynthEvolution/VapourSynth-VMAF) and skip similar frames in interpolation tasks. The properties in the clip will then be used to skip similar frames.

```python
from vsrife import rife


# calculate metrics
def metrics_func(clip):
    offs1 = core.std.BlankClip(clip, length=1) + clip[:-1]
    offs1 = core.std.CopyFrameProps(offs1, clip)
    return core.vmaf.Metric(clip, offs1, 2)

def inference_clip(video_path):
    interp_scale = 2
    clip = core.bs.VideoSource(source=video_path)

    # ssim
    clip_metric = vs.core.resize.Bicubic(
        clip, width=224, height=224, format=vs.YUV420P8, matrix_s="709"  # resize before ssim for speedup
    )
    clip_metric = metrics_func(clip_metric)
    clip_orig = core.std.Interleave([clip] * interp_scale)

    # interpolation
    clip = rife(clip, trt=True, model="4.22", sc=False)

    # skip frames based on calculated metrics
    # in this case if ssim > 0.999, then copy frame
    clip = core.akarin.Select([clip, clip_orig], clip_metric, "x.float_ssim 0.999 >")

    return clip
```

There are multiple different metrics that can be used, but be aware that you may need to adjust the threshold metric value in `vfi_inference.py`, since they work differently. SSIM has a maximum of 1 and PSNR has a maximum of infinity. I would recommend leaving the defaults unless you know what you do.
```python
# 0 = PSNR, 1 = PSNR-HVS, 2 = SSIM, 3 = MS-SSIM, 4 = CIEDE2000
return core.vmaf.Metric(clip, offs1, 2)
```

<div id='shot-boundry'/>

## Shot Boundary Detection

Detection is implemented in various different ways. To use traditional scene change you can do:

```python
clip_sc = core.misc.SCDetect(
  clip=clip,
  threshold=0.100
)
```
Afterwards you can call `clip = core.akarin.Select([clip, clip_orig], clip_sc, "x._SceneChangeNext 1 0 ?")` to apply it.

Or use models like this. Adjust thresh to a value between 0 and 1, higher means to ignore with less confidence.

```python
clip_sc = scene_detect(
    clip,
    fp16=True,
    thresh=0.5,
    model=3,
)
```

**Warning: Keep in mind that different models may require a different thresh to be good.**

The rife models mean, that flow gets used as an additional input into the classification model. That should increase stability without major speed decrease. Models that are not linked will be converted later.

Available onnx files:
- efficientnetv2_b0 (256px) ([fp16](https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/sc_efficientnetv2b0_17957_256_CHW_6ch_clamp_softmax_op17_fp16_sim.onnx) [fp32](https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/sc_efficientnetv2b0_17957_256_CHW_6ch_clamp_softmax_op17_sim.onnx))
- efficientnetv2_b0+rife46 (256px) ([fp16](https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/sc_efficientnetv2b0+rife46_flow_1362_256_CHW_6ch_clamp_softmax_op17_fp16_sim.onnx) [fp32](https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/sc_efficientnetv2b0+rife46_flow_1362_256_CHW_6ch_clamp_softmax_op17_sim.onnx))
- efficientformerv2_s0 (224px) ([fp16](https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/sc_efficientformerv2_s0_12263_224_CHW_6ch_clamp_softmax_op17_fp16_sim.onnx) [fp32](https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/sc_efficientformerv2_s0_12263_224_CHW_6ch_clamp_softmax_op17_sim.onnx))
- efficientformerv2_s0+rife46 (224px) ([fp16](https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/sc_efficientformerv2_s0+rife46_flow_84119_224_CHW_6ch_clamp_softmax_op17_fp16.onnx) [fp32](https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/sc_efficientformerv2_s0+rife46_flow_84119_224_CHW_6ch_clamp_softmax_op17.onnx))
- swinv2_small (256px) ([fp16](https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/sc_swinv2_small_window16_10412_256_CHW_6ch_clamp_softmax_op17_fp16.onnx) [fp32](https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/sc_swinv2_small_window16_10412_256_CHW_6ch_clamp_softmax_op17.onnx))
- swinv2_small+rife46 (256px) ([fp16](https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/sc_swinv2_small_window16+rife46_flow_1814_256_84119_224_CHW_6ch_clamp_softmax_op17_fp16.onnx) [fp32](https://github.com/styler00dollar/VSGAN-tensorrt-docker/releases/download/models/sc_swinv2_small_window16+rife46_flow_1814_256_84119_224_CHW_6ch_clamp_softmax_op17.onnx))

Other models I trained but are not available due to various reasons:
- hornet_tiny_7x7
- renset50
- STAM
- volo_d1
- tf_efficientnetv2_xl_in21k
- resnext50_32x4d
- nfnet_f0
- swsl_resnet18
- poolformer_m36
- densenet121
- TimeSformer
- maxvit_small
- maxvit_small+rife46
- regnetz_005
- repvgg_b0
- resnetrs50
- resnetv2_50
- rexnet_100

Interesting observations:
- Applying means/stds seemingly worsened results, despite people doing that as standard practise.
- Applying image augmentation worsened results.
- Training with higher batchsize made detections a little more stable, but maybe that was placebo and a result of more finetuning.

Comparison to traditional methods:
- [wwxd](https://github.com/dubhater/vapoursynth-wwxd) and [scxvid](https://github.com/dubhater/vapoursynth-scxvid) suffer from overdetection (at least in drawn animation).
- The json that [master-of-zen/Av1an](https://github.com/master-of-zen/Av1an) produces with `--sc-only --sc-method standard --scenes test.json` returns too little scene changes. Changing the method does not really influence a lot. Not reliable enough for vfi.
- I can't be bothered to [Breakthrough/PySceneDetect](https://github.com/Breakthrough/PySceneDetect) get working with vapousynth with FrameEval and by default it only works with video or image sequence as input. I may try in the future, but I don't understand why I cant just input two images.
- `misc.SCDetect` seemed like the best traditional vapoursynth method that does currently exist, but I thought I could try to improve. It struggles harder with similar colors and tends to skip more changes compared to methods.

Decided to only do scene change inference with ORT with TensorRT backend to keep code small and optimized.

Example usage:
```python
from src.scene_detect import scene_detect
from vsrife import rife

core.std.LoadPlugin(path="/usr/local/lib/libvstrt.so")


clip_sc = scene_detect(
    clip,
    fp16=True,
    thresh=0.5,
    model=3,
)

clip = rife(clip, trt=True, model="4.22", sc=False)

clip_orig = core.std.Interleave([clip_orig] * 2)  # 2 means interpolation factor here
clip = core.akarin.Select([clip, clip_orig], clip_sc, "x._SceneChangeNext 1 0 ?")
```

<div id='multi-gpu'/>

### multi-gpu

Thanks to tepete who figured it out, there is also a way to do inference on multipe GPUs.

```python
stream0 = core.std.SelectEvery(core.trt.Model(clip, engine_path="models/engines/model.engine", num_streams=2, device_id=0), cycle=3, offsets=0)
stream1 = core.std.SelectEvery(core.trt.Model(clip, engine_path="models/engines/model.engine", num_streams=2, device_id=1), cycle=3, offsets=1)
stream2 = core.std.SelectEvery(core.trt.Model(clip, engine_path="models/engines/model.engine", num_streams=2, device_id=2), cycle=3, offsets=2)
clip = core.std.Interleave([stream0, stream1, stream2])
```

<div id='ddfi'/>

## ddfi

To quickly explain what ddfi is, the repository [Mr-Z-2697/ddfi-rife](https://github.com/Mr-Z-2697/ddfi-rife) deduplicates frames and interpolates between frames. Normally, frames which are duplicated can create a stuttering visual effect and to mitigate that, a higher interpolation factor is used on scenes which have a duplicated frames to compensate.

Visual examples from that repository:

https://user-images.githubusercontent.com/74594146/142829178-ff08b96f-9ca7-45ab-82f0-4e95be045f2d.mp4

Example usage is in `custom_scripts/ddfi_rife_dedup_scene_change/`. As a quick summary, you need to do two processing passes. One pass to calculate metrics and another to use interpolation combined with VFRToCFR. You need to use `deduped_vfi.py` similar to how you used `main.py`.

<div id='vfr'/>

## VFR
**Warning**: Using variable refresh rate video input will result in desync errors. To check if a video is do
```bash
ffmpeg -i video_Name.mp4 -vf vfrdet -f null -
```
and look at the final line. If it is not zero, then it means it is variable refresh rate. Example:
```bash
[Parsed_vfrdet_0 @ 0x56518fa3f380] VFR:0.400005 (15185/22777) min: 1801 max: 3604)
```
To go around this issue, specify `fpsnum` and `fpsden` in `inference_config.py`
```
clip = core.ffms2.Source(source='input.mkv', fpsnum = 24000, fpsden = 1001, cache=False)
```
or convert everything to constant framerate with ffmpeg.
```bash
ffmpeg -i video_input.mkv -fps_mode cfr -crf 10 -c:a copy video_out.mkv
```
or use my `vfr_to_cfr.py` to process a folder.

<div id='benchmarks'/>

## Benchmarks

- Used `vspipe -c y4m inference.py - | ffmpeg -i pipe: -f null /dev/null -y` and a 5000 frame h264 default settings ffmpeg encoded video for all benchmarks.
- All benchmarks done on Linux.

| model                 | scale | gpu  | arch          | fps 720 | fps 1080 | vram 720 | vram 1080   | backend                                                                  | batch | level | streams   | threads   | onnx      | onnxslim / onnxsim | onnx shape  | trtexec shape | precision | usage                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------------- | ----- | ---- | ------------- | ------- | -------- | -------- | ----------- | ------------------------------------------------------------------------ | ----- | ----- | --------- | --------- | --------- | ------------------ | ----------- | ------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AnimeJaNai V2         | 2x    | 4090 | Compact       | 87.54   | 39.44    | 1.7gb    | 2.7gb       | trt 10.7 (trtexec+mlrt)                                                  | 1     | 5     | 3         | 4         | fp16 op18 | -		               | dynamic     | dynamic       | RGBH      | trtexec --bf16 --fp16 --onnx=2x_AnimeJaNai_V2_Compact_36k_op18_fp16_clamp.onnx --minShapes=input:1x3x8x8 --optShapes=input:1x3x720x1280 --maxShapes=input:1x3x1080x1920 --saveEngine=2x_AnimeJaNai_V2_Compact_36k_op18_fp16_clamp.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5 --infStreams=3               |
| AnimeJaNai V2         | 2x    | 4090 | Compact       | 136.47  | 61.26    | 6.4gb    | 13.2gb      | trt 10.7 (trtexec+mlrt)                                                  | 2     | 5     | 10        | 10        | fp16 op18 | -		               | dynamic     | dynamic       | RGBH      | trtexec --bf16 --fp16 --onnx=2x_AnimeJaNai_V2_Compact_36k_op18_fp16_clamp_batch2.onnx --minShapes=input:1x6x8x8 --optShapes=input:1x6x720x1280 --maxShapes=input:1x6x1080x1920 --saveEngine=2x_AnimeJaNai_V2_Compact_36k_op18_fp16_clamp_batch2.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5 --infStreams=3 |
| ModernSpanimation V2  | 2x    | 4090 | Span          | 111.96  | 44.21    | 3.2gb    | 6.2gb       | trt 10.7 (trtexec+mlrt)                                                  | 1     | 5     | 3         | 4         | fp16 op20 | onnxslim           | dynamic     | dynamic       | RGBH      | trtexec --bf16 --fp16 --onnx=2x_ModernSpanimationV2_clamp_op20_fp16_onnxslim.onnx --minShapes=input:1x3x8x8 --optShapes=input:1x3x720x1280 --maxShapes=input:1x3x1080x1920 --saveEngine=2x_ModernSpanimationV2_clamp_op20_fp16_onnxslim.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5 --infStreams=3         |
| sudo shuffle span     | 2x    | 4090 | span (custom) | 96.06   | 42.63    | 5.5gb    | 11.1gb      | trt 10.7 (trtexec+mlrt)                                                  | 1     | 5     | 3         | 4         | fp16 op20 | onnxslim           | static      | -             | RGBH      | trtexec --bf16 --fp16 --onnx=2x_sudo_shuffle_span_10.5m_1080p_clamp_op20_fp16_onnxslim.onnx --saveEngine=2x_sudo_shuffle_span_10.5m_1080p_clamp_op20_fp16_onnxslim.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5 --infStreams=3 --layerPrecisions=/dynamic/Conv:fp32 --precisionConstraints=obey             |
| cugan                 | 2x    | 4090 | cugan         | 47.51   | 21.34    | 6.2gb    | 12.7gb      | trt 10.7 (trtexec+mlrt)                                                  | 1     | 5     | 3         | 4         | fp16 op20 | -                  | dynamic     | dynamic       | RGBH      | trtexec --bf16 --fp16 --onnx=cugan_pro-denoise3x-up2x_op18_fp16_clamp_colorfix.onnx --minShapes=input:1x3x8x8 --optShapes=input:1x3x720x1280 --maxShapes=input:1x3x1080x1920 --saveEngine=cugan_pro-denoise3x-up2x_op18_fp16_clamp_colorfix.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5 --infStreams=3     |
| dpir                  | 1x    | 4090 | dpir (4ch)    | 51.46   | 22.92    | 2.7gb    | 4.8gb       | trt 10.7 (trtexec+mlrt)                                                  | 1     | 5     | 3         | 4         | fp32 op9  | -                  | dynamic     | dynamic       | RGBS      | trtexec --bf16 --fp16 --onnx=dpir_drunet_color.onnx --minShapes=input:1x4x8x8 --optShapes=input:1x4x720x1280 --maxShapes=input:1x4x1080x1920 --saveEngine=dpir_drunet_color.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5 --infStreams=3                                                                     |
| vsrife 4.18           | 2x    | 4090 | rife (4.18)   | 305.19  | 136.87   | 1.9gb    | 2.8gb       | torch 20241231+cu126 (holywu vsrife)                                     | 1     | 5     | -         | 8         | -         | -                  | -           | -             | RGBH      | rife(clip, trt=False, sc=False)                                                                                                                                                                                                                                                                                                                                                               |
| vsrife 4.18           | 2x    | 4090 | rife (4.18)   | 651.55  | 298.91   | 2.4gb    | 2.1gb       | trt 10.7, torch 20241231+cu126, torch_trt 20250102+cu126 (holywu vsrife) | 1     | 5     | -         | 8         | -         | -                  | -           | static        | RGBH      | rife(clip, trt=True, trt_static_shape=True, model="4.18", trt_optimization_level=5, sc=False)                                                                                                                                                                                                                                                                                                 |
| rife 4.18v2           | 2x    | 4090 | rife (4.18)   | 393.04  | 193.56   | 1.6gb    | 2.3gb       | trt 10.7 (trtexec+mlrt)                                                  | 1     | 5     | 3         | 8         | fp16 op20 | onnxslim           | dynamic     | static        | RGBH      | trtexec --bf16 --fp16 --onnx=rife418_v2_ensembleFalse_op20_fp16_clamp_onnxslim.onnx --minShapes=input:1x7x1080x1920 --optShapes=input:1x7x1080x1920 --maxShapes=input:1x7x1080x1920 --saveEngine=rife418_v2_ensembleFalse_op20_fp16_clamp_onnxslim.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5             |
| vsrife 4.22           | 2x    | 4090 | rife (4.22)   | 284.04  | 131.54   | 1.9gb    | 2.9gb       | torch 20241231+cu126 (holywu vsrife)                                     | 1     | 5     | -         | 8         | -         | -                  | -           | -             | RGBH      | rife(clip, trt=False, sc=False)                                                                                                                                                                                                                                                                                                                                                               |
| vsrife 4.22           | 2x    | 4090 | rife (4.22)   | 529.35  | 244.01   | 1.6gb    | 2.2gb       | trt 10.7, torch 20241231+cu126, torch_trt 20250102+cu126 (holywu vsrife) | 1     | 5     | -         | 8         | -         | -                  | -           | static        | RGBH      | rife(clip, trt=True, trt_static_shape=True, model="4.18", trt_optimization_level=5, sc=False)                                                                                                                                                                                                                                                                                                 |
| rife 4.22v2           | 2x    | 4090 | rife (4.22)   | 379.43  | 191.50   | 1.6gb    | 2.5gb       | trt 10.7 (trtexec+mlrt)                                                  | 1     | 5     | 3         | 8         | fp16 op20 | onnxslim           | dynamic     | static        | RGBH      | trtexec --bf16 --fp16 --onnx=rife422_v2_ensembleFalse_op20_fp16_clamp_onnxslim.onnx --minShapes=input:1x7x1080x1920 --optShapes=input:1x7x1080x1920 --maxShapes=input:1x7x1080x1920 --saveEngine=rife422_v2_ensembleFalse_op20_fp16_clamp_onnxslim.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5             |

Experimental testing:

| model                 | scale | gpu  | arch                       | fps 720 | fps 1080 | vram 720 | vram 1080   | backend                | batch | level | streams   | threads   | onnx      | onnxslim / onnxsim | onnx shape  | trtexec shape | precision | usage                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------------- | ----- | ---- | -------------------------- | ------- | -------- | -------- | ----------- | ---------------------- | ----- | ----- | --------- | --------- | --------- | ------------------ | ----------- | ------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| moesr                 | 2x    | 4090 | moesr (dysample)           | 3.99    | ~1.8     | 4.6gb    | 9.6gb       | trt10.7 (trtexec+mlrt) | 1     | 5     | 3         | 4         | fp16 op20 | -                  | dynamic     | dynamic       | RGBH      | trtexec --bf16 --fp16 --onnx=moesr_dysample_fp16_op20.onnx --minShapes=input:1x3x8x8 --optShapes=input:1x3x720x1280 --maxShapes=input:1x3x1080x1920 --saveEngine=moesr_dysample_fp16_op20.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5 --infStreams=3                                                       |
| mosr                  | 2x    | 4090 | mosr (dysample)            | 9.93    | 4.39     | 3.7gb    | 7.6gb       | trt10.7 (trtexec+mlrt) | 1     | 5     | 3         | 4         | fp16 op20 | -                  | dynamic     | dynamic       | RGBH      | trtexec --bf16 --fp16 --onnx=mosr_dysample_fp16_op20.onnx --minShapes=input:1x3x8x8 --optShapes=input:1x3x720x1280 --maxShapes=input:1x3x1080x1920 --saveEngine=mosr_dysample_fp16_op20.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5 --infStreams=3                                                         |
| safmn-l               | 2x    | 4090 | safmn (safmn-l + dysample) | 9.02    | 3.99     | 5.5gb    | 11.1gb      | trt10.7 (trtexec+mlrt) | 1     | 5     | 3         | 4         | fp16 op20 | -                  | static      | -             | RGBH      | trtexec --bf16 --fp16 --onnx=safmn_l_fp16_op20_clamp_1080_clamp.onnx --saveEngine=safmn_l_fp16_op20_clamp_1080_clamp.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5 --infStreams=3                                                                                                                            |
| rcan                  | 2x    | 4090 | rcan                       | 3.11    | ~1.4     | 4.6gb    | 9.3gb       | trt10.7 (trtexec+mlrt) | 1     | 5     | 3         | 4         | fp16 op20 | -                  | dynamic     | dynamic       | RGBH      | trtexec --bf16 --fp16 --onnx=rcan_op20_fp16_clamp.onnx --minShapes=input:1x3x8x8 --optShapes=input:1x3x720x1280 --maxShapes=input:1x3x1080x1920 --saveEngine=rcan_op20_fp16_clamp.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5 --infStreams=3                                                               |
| cfsr                  | 2x    | 4090 | cfsr                       | 15.64   | 6.95     | 3.2gb    | 6.2gb       | trt10.7 (trtexec+mlrt) | 1     | 5     | 3         | 4         | fp16 op20 | -                  | dynamic     | dynamic       | RGBH      | trtexec --bf16 --fp16 --onnx=rcan_op20_fp16_clamp.onnx --minShapes=input:1x3x8x8 --optShapes=input:1x3x720x1280 --maxShapes=input:1x3x1080x1920 --saveEngine=rcan_op20_fp16_clamp.engine --tacticSources=+CUDNN,-CUBLAS,-CUBLAS_LT --skipInference --useCudaGraph --noDataTransfers --builderOptimizationLevel=5 --infStreams=3                                                               |

<div id='license'/>

## License

This code uses code from other repositories, but the code I wrote myself is under BSD3.
