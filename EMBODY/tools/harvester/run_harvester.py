import argparse
from harvester_core import harvest_clip

parser = argparse.ArgumentParser()
parser.add_argument('--video_path', type=str, required=True)
parser.add_argument('--subtitle_path', type=str, required=True)
parser.add_argument('--output_dir', type=str, required=True)
args = parser.parse_args()

harvest_clip(
    video_path=args.video_path,
    subtitle_path=args.subtitle_path,
    output_dir=args.output_dir
)
