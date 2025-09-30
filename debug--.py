import os
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

def combine_videos_in_folder(folder_path: str):
    folder = Path(folder_path)
    if not folder.exists():
        print(f"❌ Folder not found: {folder}")
        return

    video_files = sorted([f for f in folder.iterdir() if f.suffix.lower() == ".mp4"])
    if not video_files:
        print("❌ No MP4 files found in the folder.")
        return

    # Create temp folder on the same drive
    temp_folder = folder.parent / "temp_combiner"
    temp_folder.mkdir(exist_ok=True)

    clips = []
    for file in video_files:
        # Clean filename
        new_name = clean_filename(file.name)
        temp_file = temp_folder / new_name

        # Copy to temp folder
        shutil.copy(file, temp_file)
        print(f"📥 Copied: {file.name} -> {temp_file.name}")

        # Get short path for MoviePy
        short_file = safe_short_path(temp_file)
        clips.append(VideoFileClip(short_file))

    # Combine videos
    final_clip = concatenate_videoclips(clips)
    combined_video_name = "combined.mp4"
    combined_video_path = temp_folder / combined_video_name
    final_clip.write_videofile(str(combined_video_path))
    print(f"✅ Combined video created: {combined_video_path}")

    # Ensure output directory exists
    output_folder = Path(folder_path)
    output_folder.mkdir(parents=True, exist_ok=True)

    # Move combined video to the given directory
    final_destination = output_folder / combined_video_name
    shutil.move(str(combined_video_path), str(final_destination))
    print(f"📂 Combined video moved to: {final_destination}")

    # Remove temp folder
    shutil.rmtree(temp_folder)
    print(f"🗑 Temp folder removed: {temp_folder}")

if __name__ == "__main__":
    folder = input("Enter the path of the folder containing mp4 files: ").strip()
    combine_videos_in_folder(folder)
