# example usage: python main.py
# vapoursynth does not have audio support and processing multiple files is not really possible
# hacky script to make batch processing with audio and subtitle support
# make sure tmp_dir is also set in inference.py
# maybe should pass arguments instead of a text file instead
import glob
import os
import shutil

input_dir = "/workspace/tensorrt/input/"
tmp_dir = "tmp/"
output_dir = "/workspace/tensorrt/output/"
files = glob.glob(input_dir + "/**/*.webm", recursive=True)
files.sort()

for f in files:
    # creating folders if they dont exist
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
        os.mkdir(tmp_dir)

    # paths
    txt_path = os.path.join(tmp_dir, "tmp.txt")
    out_render_path = os.path.join(
        output_dir, os.path.splitext(os.path.basename(f))[0] + "_rendered.mkv"
    )
    mux_path = os.path.join(
        output_dir, os.path.splitext(os.path.basename(f))[0] + "_mux.mkv"
    )

    # only needed for dedup
    os.system(f"vspipe /workspace/tensorrt/parse.py --arg source={f} -p .")

    os.system(f"vspipe -c y4m inference_batch.py - | ffmpeg -i pipe: {out_render_path}")
    os.system(
        f"ffmpeg -y -loglevel error -i {f} -i {out_render_path}  -map 1 -map 0 -map -0:v -codec copy -max_interleave_delta 0 {mux_path}"
    )

    # directly muxing
    # os.system(
    #    f"vspipe -c y4m inference_batch.py - | ffmpeg -y -i {f} -thread_queue_size 4096 -i pipe: -map 1 -map 0 -map -0:v -max_interleave_delta 0 -crf 15 {mux_path}"
    # )

    # deleting temp files
    os.remove(txt_path)
