import os
import subprocess

def get_custom_pathname(file_path: str) -> str:
    """
    Get the base name of a file without its extension with custom logic to extract the requrired part of the name.
    """
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    # custom logic to extract the required part of the name
    tutorial_number = base_name.split('｜')[1].split('-')[1].split('#')[1].split('[')[0].strip()
    topic = base_name.split('｜')[0].strip().replace(" ", "_")
    custom_pathname = f"{tutorial_number if len(tutorial_number) > 1 else f'0{tutorial_number}'}_{topic}"

    return custom_pathname


def create_output_file_path(output_dir: str, base_name: str) -> str:
    """
    Create the output file path for the mp3 file based on the output directory and base name.
    """
    return os.path.join(output_dir, f"{base_name}.mp3")


def convert_videos_to_mp3(video_files: list[str], output_dir: str) -> None:
    """
    convert a list of video files to mp3 format and save them in the specified output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for video_file in video_files:
        # get the base name of the video file without extension
        custom_pathname = get_custom_pathname(video_file)

        # create output file path for the mp3 file
        output_file = create_output_file_path(output_dir, custom_pathname)

        # use ffmpeg to convert the video file to mp3 format
        command = ['ffmpeg', '-i', f"videos/{video_file}", output_file]

        try:
            subprocess.run(command, check=True)
            print(f"Successfully converted {video_file} to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {video_file}: {e}")


video_files = os.listdir('videos')
output_dir = 'audios'
convert_videos_to_mp3(video_files, output_dir)