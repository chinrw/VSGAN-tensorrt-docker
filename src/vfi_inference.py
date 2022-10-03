import itertools
import numpy as np
import vapoursynth as vs
import functools
from pytorch_msssim import ssim, ms_ssim, SSIM, MS_SSIM
from .dedup import PSNR
from .rife import RIFE
from .IFRNet import IFRNet
from .GMFupSS import GMFupSS
from .eisai import EISAI
from .film import FILM
from .M2M import M2M
from .sepconv_enhanced import sepconv
import torch 

# https://github.com/HolyWu/vs-rife/blob/master/vsrife/__init__.py
def vfi_inference(
    clip: vs.VideoNode,
    skip_framelist=[],
) -> vs.VideoNode:
    core = vs.core

    def frame_to_tensor(frame: vs.VideoFrame):
        return np.stack(
            [np.asarray(frame[plane]) for plane in range(frame.format.num_planes)]
        )

    def tensor_to_frame(f: vs.VideoFrame, array) -> vs.VideoFrame:
        for plane in range(f.format.num_planes):
            d = np.asarray(f[plane])
            np.copyto(d, array[plane, :, :])
        return f

    def tensor_to_clip(clip: vs.VideoNode, image) -> vs.VideoNode:
        clip = core.std.BlankClip(
            clip=clip, width=image.shape[-1], height=image.shape[-2]
        )
        return core.std.ModifyFrame(
            clip=clip,
            clips=clip,
            selector=lambda n, f: tensor_to_frame(f.copy(), image),
        )

    # select desired model
    model_inference = RIFE(scale=1, fastmode=False, ensemble=True, model_version="rife46", fp16=False)
    #model_inference = IFRNet(model="small", fp16=False)
    #model_inference = GMFupSS()
    #model_inference = EISAI() # 960x540
    #model_inference = FILM(model_choise="vgg")
    #model_inference = M2M()
    #model_inference = sepconv()

    def execute(n: int, clip: vs.VideoNode) -> vs.VideoNode:
        if (
            (n % 2 == 0)
            or n == 0
            or n in skip_framelist
            or n == clip.num_frames - 1
        ):
            return clip

        I0 = frame_to_tensor(clip.get_frame(n - 1))
        I1 = frame_to_tensor(clip.get_frame(n + 1))
        
        I0 = torch.Tensor(I0).unsqueeze(0).to("cuda", non_blocking=True)
        I1 = torch.Tensor(I1).unsqueeze(0).to("cuda", non_blocking=True)

        # clamping because vs does not give tensors in range 0-1, results in nan in output
        I0 = torch.clamp(I0, min=0, max=1)
        I1 = torch.clamp(I1, min=0, max=1)

        middle = model_inference.execute(I0, I1)

        return tensor_to_clip(clip=clip, image=middle)

    clip = core.std.Interleave([clip, clip])
    return core.std.FrameEval(
        core.std.BlankClip(clip=clip, width=clip.width, height=clip.height),
        functools.partial(execute, clip=clip),
    )