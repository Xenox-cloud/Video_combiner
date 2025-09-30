import shutil
from pathlib import Path
from moviepy.editor import VideoFileClip, concatenate_videoclips

try:
    import win32api
except ImportError:
    win32api = None

def safe_short_path(file: Path) -> str:
    """Return Windows short path for ffmpeg compatibility."""
    if win32api:
        return win32api.GetShortPathName(str(file))
    return str(file)

def clean_filename(name: str) -> str:
    """Replace problematic characters in filename."""
    name = name.replace(" ", "-").replace("+", "_")
    return name

def combine_videos_in_folder(folder: Path):
    """Combine all mp4 videos in a single folder."""
    # Skip folder if it already contains combined.mp4
    if any(f.name.lower() == "combined.mp4" for f in folder.iterdir()):
        print(f"⏭ Skipping folder (already combined): {folder}")
        return

    video_files = sorted([f for f in folder.iterdir() if f.suffix.lower() == ".mp4"])
    if not video_files:
        return  # No videos here

    print(f"🎬 Combining videos in folder: {folder}")

    # Temp folder on same drive
    temp_folder = folder / "temp_combiner"
    temp_folder.mkdir(exist_ok=True)

    clips = []
    for file in video_files:
        new_name = clean_filename(file.name)
        temp_file = temp_folder / new_name
        shutil.copy(file, temp_file)
        short_file = safe_short_path(temp_file)
        clips.append(VideoFileClip(short_file))

    # Combine videos
    final_clip = concatenate_videoclips(clips)
    combined_video_path = folder / "combined.mp4"
    final_clip.write_videofile(str(combined_video_path))
    print(f"✅ Combined video saved in folder: {folder}")

    # Clean temp folder
    shutil.rmtree(temp_folder)

def combine_videos_recursive(base_folder: str):
    base = Path(base_folder)
    if not base.exists():
        print(f"❌ Base folder not found: {base}")
        return

    # Walk all subfolders
    for folder in [d for d in base.rglob("*") if d.is_dir()]:
        combine_videos_in_folder(folder)

    # Also combine videos in the base folder itself
    combine_videos_in_folder(base)

if __name__ == "__main__":
    base_folder = input("Enter the base parent folder path: ").strip()
    combine_videos_recursive(base_folder)
