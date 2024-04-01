import subprocess
import sys

def convert_to_mp4(audio_file):
    # Create the background image
    #create_background_image(audio_file)
    
    # Prepare output filename
    output_file = audio_file.rsplit('.', 1)[0] + '.mp4'
    
    # Use FFmpeg to combine the image and audio into an MP4
    command = [
        'ffmpeg',
        '-loop', '1',
        '-i', 'background.png',
        '-i', audio_file,
        '-c:v', 'libx264',
        '-tune', 'stillimage',
        '-c:a', 'aac',
        '-b:a', '192k',
        #'-ar', '96000',  # Set the audio sampling rate to 43,200 Hz
        '-pix_fmt', 'yuv420p',
        '-shortest',
        output_file
    ]
    subprocess.run(command)

if __name__ == "__main__":
    # Take the audio file name from the command line argument
    audio_file = sys.argv[1]
    convert_to_mp4(audio_file)
