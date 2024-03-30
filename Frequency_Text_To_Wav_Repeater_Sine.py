<<<<<<< HEAD
import wave
import numpy as np
from PIL import Image
import struct
import os
import math

def main():
    channels = 0
    sampling_rate = 0
    amplitudewidth = 0
    samplesPerCharacter = 0
    text = None
    frequency_int = 0
    numsteps = 0

    while True:
        text = input("Enter Intention: ")
        if text != "":
            break

    repeat_times = int(input("# Times to Repeat: "))
    try:
        if repeat_times <= 0:
            repeat_times = 1
    except ValueError:
        repeat_times = 1

    # Find lowest and highest ASCII values
    min_ascii = min(ord(char) for char in text)
    max_ascii = max(ord(char) for char in text)
    # Find the range of ASCII values
    ascii_range = max_ascii - min_ascii

    while sampling_rate < 48000 or sampling_rate > 767500:
        sampling_rate_input = input("Enter Sampling Rate [Default 48000, Max 767500]: ")
        try:
            sampling_rate = int(sampling_rate_input)
        except ValueError:
            sampling_rate = 0
    print(f"Valid input received: {sampling_rate}")

    while channels < 1 or channels > 8:
        channels_input = input("Enter Channels (1-8): ")
        try:
            channels = int(channels_input)
        except ValueError:
            channels = 0
    print(f"Valid input received: {channels}")

    while amplitudewidth != 2 and amplitudewidth != 4:
        amplitudewidth_input = input("Enter Amplitude Width (2 or 4): ")
        try:
            amplitudewidth = int(amplitudewidth_input)
        except ValueError:
            amplitudewidth = 0
    print(f"Valid input received: {amplitudewidth}")

    while frequency_int < 1:
        frequency = input("Enter Frequency (Default 432Hz): ")
        try:
            #If lowercase right 2 characters are hz, then remove them
            if frequency[0:2].lower() == "hz":
                frequency = frequency[2:]
            
            frequency_int = int(frequency)
            if frequency_int < 1:
                frequency_int = 1
        except ValueError:
            frequency_int = 432

    output_file = "Output_Sine_" + str(frequency_int) + "Hz_" + str(sampling_rate) + ".wav"

    # Open WAV file for writing
    sampleMax = (2147483647 if amplitudewidth == 4 else 32767)
    
    # Calculate the scaling factor
    scaling_factor = sampleMax / ascii_range

    stepsize = int(sampling_rate / frequency_int / 2)
    #numsteps = int(sampling_rate / stepsize)

    print(f"Stepsize: {stepsize}, Numsteps: {numsteps}, ascii_range: {ascii_range}")

    sign = 1

    with wave.open(output_file, "w") as wav_file:
        # Set parameters for the WAV file
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(amplitudewidth)  # 32-bit audio or 16 bit audio
        wav_file.setframerate(sampling_rate)

        # Calculate the total number of samples
        total_samples = repeat_times * len(text) * sampling_rate // frequency_int

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

            # Generate the sine wave sample
            sample_value = int(amplitude * sampleMax * math.sin(phase))

            for _ in range(channels):
                wav_file.writeframes(struct.pack(('<i' if amplitudewidth == 4 else '<h'), sample_value))

    print("Audio file saved as " + output_file)

if __name__ == "__main__":
=======
import wave
import numpy as np
from PIL import Image
import struct
import os
import math

def main():
    channels = 0
    sampling_rate = 0
    amplitudewidth = 0
    samplesPerCharacter = 0
    text = None
    frequency_int = 0
    numsteps = 0

    while True:
        text = input("Enter Intention: ")
        if text != "":
            break

    repeat_times = int(input("# Times to Repeat: "))
    try:
        if repeat_times <= 0:
            repeat_times = 1
    except ValueError:
        repeat_times = 1

    # Find lowest and highest ASCII values
    min_ascii = min(ord(char) for char in text)
    max_ascii = max(ord(char) for char in text)
    # Find the range of ASCII values
    ascii_range = max_ascii - min_ascii

    while sampling_rate < 48000 or sampling_rate > 767500:
        sampling_rate_input = input("Enter Sampling Rate [Default 48000, Max 767500]: ")
        try:
            sampling_rate = int(sampling_rate_input)
        except ValueError:
            sampling_rate = 0
    print(f"Valid input received: {sampling_rate}")

    while channels < 1 or channels > 8:
        channels_input = input("Enter Channels (1-8): ")
        try:
            channels = int(channels_input)
        except ValueError:
            channels = 0
    print(f"Valid input received: {channels}")

    while amplitudewidth != 2 and amplitudewidth != 4:
        amplitudewidth_input = input("Enter Amplitude Width (2 or 4): ")
        try:
            amplitudewidth = int(amplitudewidth_input)
        except ValueError:
            amplitudewidth = 0
    print(f"Valid input received: {amplitudewidth}")

    while frequency_int < 1:
        frequency = input("Enter Frequency (Default 432Hz): ")
        try:
            #If lowercase right 2 characters are hz, then remove them
            if frequency[0:2].lower() == "hz":
                frequency = frequency[2:]
            
            frequency_int = int(frequency)
            if frequency_int < 1:
                frequency_int = 1
        except ValueError:
            frequency_int = 432

    output_file = "Output_Sine_" + str(frequency_int) + "Hz_" + str(sampling_rate) + ".wav"

    # Open WAV file for writing
    sampleMax = (2147483647 if amplitudewidth == 4 else 32767)
    
    # Calculate the scaling factor
    scaling_factor = sampleMax / ascii_range

    stepsize = int(sampling_rate / frequency_int / 2)
    #numsteps = int(sampling_rate / stepsize)

    print(f"Stepsize: {stepsize}, Numsteps: {numsteps}, ascii_range: {ascii_range}")

    sign = 1

    with wave.open(output_file, "w") as wav_file:
        # Set parameters for the WAV file
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(amplitudewidth)  # 32-bit audio or 16 bit audio
        wav_file.setframerate(sampling_rate)

        # Iterate over pixels and write audio samples
        frames_to_write = []
        for r in range(repeat_times):
            for i in range(len(text) - 1):
                char = text[i]
                next_char = text[i + 1]

                # Convert pixel data to audio samples
                sample_current = int((ord(char) - min_ascii) * scaling_factor) * sign
                sign = -sign  # Alternate between positive and negative for each character
                next_sample = int((ord(next_char) - min_ascii) * scaling_factor) * sign

                # Create samplesPerCharacter steps from first pixel to the second
                for j in range(stepsize):
                    # Calculate the phase angle for the sine wave
                    phase = 2 * math.pi * j / stepsize

                    # Generate the sine wave sample
                    sample_new = int((sample_current + (next_sample - sample_current) * j / stepsize) * math.sin(phase))
                    
                    for _ in range(channels):
                        frames_to_write.append(struct.pack(('<i' if amplitudewidth == 4 else '<h'), sample_new))

                if len(frames_to_write) >= 1000:
                    wav_file.writeframes(b"".join(frames_to_write))
                    frames_to_write = []

            if frames_to_write:
                wav_file.writeframes(b"".join(frames_to_write))

    print("Audio file saved as " + output_file)

if __name__ == "__main__":
>>>>>>> c2780fcfa4edd21fdfc5cdad401d962b034cf237
    main()