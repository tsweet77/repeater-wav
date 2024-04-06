import wave
import numpy as np
from PIL import Image
import struct
import os
import math
import time
import re

def get_valid_filename(prompt):
    while True:
        filename = input(prompt)
        if not filename.endswith(".txt"):
            filename += ".txt"
        if os.path.exists(filename):
            return filename
        print("File not found. Please enter a valid filename.")

def main():
    channels = 0
    sampling_rate = 0
    amplitudewidth = 0
    text = None
    frequency_int = 0
    smoothing_factor = -1.0  # Adjust this value to control the smoothing effect
    smoothing_percent = "-1"

    input_file = get_valid_filename("Enter Input Text File: ")
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    while True:
        repeat_times_str = input("# Times to Repeat: ")
        if text != "":
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
            break

    try:
        if int(repeat_times_str) <= 0:
            repeat_times = 1
        else:
            repeat_times = int(repeat_times_str)
    except ValueError:
        repeat_times = 1

    # Find lowest and highest ASCII values
    min_ascii = min(ord(char) for char in text)
    max_ascii = max(ord(char) for char in text)
    # Find the range of ASCII values
    ascii_range = max_ascii - min_ascii

    while channels < 1 or channels > 8:
        channels_input = input("Enter Channels (1-8): ")
        try:
            channels = int(channels_input)
        except ValueError:
            channels = 1
    
    while amplitudewidth != 2 and amplitudewidth != 4:
        amplitudewidth_input = input("Enter Amplitude Width (2 or 4): ")
        try:
            amplitudewidth = int(amplitudewidth_input)
        except ValueError:
            amplitudewidth = 4
    
    while frequency_int < 20:
        frequency = input("Enter Frequency (Default 432Hz): ")
        try:
            #If lowercase right 2 characters are hz, then remove them
            if frequency[0:2].lower() == "hz":
                frequency = frequency[2:]
            
            frequency_int = int(frequency)
            if frequency_int < 1:
                frequency_int = 20
        except ValueError:
            frequency_int = 432

    while sampling_rate < frequency_int or sampling_rate > 767500:
        sampling_rate_input = input("Sampling Rate [Default 100X Frequency, Max 767500]: ")
        try:
            sampling_rate = int(sampling_rate_input)
        except ValueError:
            sampling_rate = 100 * frequency_int

    while smoothing_factor < 0.0 or smoothing_factor > 1.0:
        smoothing_percent = input("Smoothing Factor (0.0-100.0%, Default 50.0%): ")
        try:
            #If right most character of smoothing_percent == "%" then remove that last character
            if smoothing_percent[len(smoothing_percent) - 1:len(smoothing_percent)] == "%":
                smoothing_percent = smoothing_percent[0:len(smoothing_percent) - 1]

            smoothing_factor = float(smoothing_percent) / 100
            if smoothing_factor < 0.0:
                smoothing_factor = 0.0
                smoothing_percent = "0"
        except ValueError:
            smoothing_factor = 0.50
            smoothing_percent = "50"

    output_file = input_file + "_" + str(frequency_int) + "Hz_Smoothing_" + smoothing_percent + "_Percent_" + str(sampling_rate) + ".wav"

    # Open WAV file for writing
    sampleMax = (2147483647 if amplitudewidth == 4 else 32767)
    
    # Calculate the total number of samples
    total_samples = repeat_times * len(text) * sampling_rate // frequency_int
    last_progress_update = time.time()
    buffer = []

    with wave.open(output_file, "w") as wav_file:
        # Set parameters for the WAV file
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(amplitudewidth)  # 32-bit audio or 16 bit audio
        wav_file.setframerate(sampling_rate)

        # Generate the sine wave samples
        for i in range(total_samples):
            # Calculate the character index and sample index within the character
            char_index = (i // (sampling_rate // frequency_int)) % len(text)
            char = text[char_index]
            next_char = text[(char_index + 1) % len(text)]

            # Convert characters to amplitude values
            amplitude_current = (ord(char) - min_ascii) / ascii_range
            amplitude_next = (ord(next_char) - min_ascii) / ascii_range

            # Calculate the interpolation factor
            interpolation_factor = (i % (sampling_rate // frequency_int)) / (sampling_rate // frequency_int)

            # Interpolate the amplitude values
            amplitude = amplitude_current + (amplitude_next - amplitude_current) * interpolation_factor

            # Calculate the phase angle for the sine wave
            phase = 2 * math.pi * frequency_int * i / sampling_rate

            # Generate the trending sine wave sample
            if (smoothing_factor == 0.0):
                sample_value = int(amplitude * sampleMax * math.sin(phase))
            else:
                sample_value = int(sampleMax * (smoothing_factor * math.sin(phase) + (1 - smoothing_factor) * (2 * amplitude - 1)))

            for _ in range(channels):
                buffer.append(sample_value)

            if i % 100000 == 0:
                # Write the accumulated samples to the WAV file
                for sample in buffer:
                    wav_file.writeframes(struct.pack(('<i' if amplitudewidth == 4 else '<h'), sample))
                buffer = []

            if time.time() - last_progress_update >= 1:
                percentage = round((i / total_samples) * 100, 2)
                print(f"\rProgress: {percentage}%, Samples Written: {i}     \r", end='', flush=True)  # Use end='' to prevent newline character and flush to ensure immediate printing
                last_progress_update = time.time()  # Update the last progress update time

        # Write any remaining samples in the buffer
        for sample in buffer:
            wav_file.writeframes(struct.pack(('<i' if amplitudewidth == 4 else '<h'), sample))

    print(f"\rProgress: 100.00%, Samples Written: {total_samples}     ", flush=True)
    print("\nAudio file saved as " + output_file)

if __name__ == "__main__":
    main()