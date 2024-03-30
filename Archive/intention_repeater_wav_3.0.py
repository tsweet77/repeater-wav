#!/usr/bin/python
# -*- coding: utf-8 -*-

# Intention Repeater WAV File Writer created by Thomas Sweet
# Updated 3/8/2024 v3.0
# Requires Python v3.5.3 or greater
# Run using Windows/Linux/MacOS: python3 intention_repeater_wav.py
# Automated Example Linux/MacOS: python3 intention_repeater_wav.py "HH:MM:SS" "WAV Filename" "Intentions/Filename with Intentions"
# Automated Example Windows: intention_repeater_wav.py "HH:MM:SS" "WAV Filename" "Intentions/Filename with Intentions"
# Intention Repeater is powered by a Servitor (20 Years / 2000+ hours in the making)
# Servitor Info: https://enlightenedstates.com/2017/04/07/servitor-just-powerful-spiritual-tool/
# Website: https://www.intentionrepeater.com/
# Forum: https://forums.intentionrepeater.com/
# Licensed under GNU General Public License v3.0
# This means you can modify, redistribute and even sell your own modified software, as long as it's open source too and released under this same license.
# https://choosealicense.com/licenses/gpl-3.0/
# Note, 1 minute of running can produce an approx. 55 MB file that is approx. 5m long on an i3 with 4GB RAM and a SSD.

import time
import sys
import wave
import struct

PROCESS_STATEMENT = ": ONE INFINITE CREATOR. REQUESTING AID FROM BEINGS OF LIGHT. OM."

# Volume level should be from 0.000 to 1.000, and determines amplitude

volume_level = 0.95
sampling_rate = 96000.0

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), [
        '',
        'K',
        'M',
        'B',
        'T',
        'Q',
        ][magnitude])


print("Intention Repeater WAV File Writer v3.0 software created by Thomas Sweet.\n")
print("This software comes with no guarantees or warranty of any kind.\n")

args = list(sys.argv)

try:
    run_time_param = str(args[1])
    filename_param = str(args[2])
    string_to_write_param = str(args[3])
except:
    run_time_param = ''
    string_to_write_param = ''
    filename_param = ''

string_to_write = ''
string_to_write_value = ''
filename = ''

peak_value = 32767

if filename_param == '':
    while filename == '':
        filename = input('Filename to Write (.wav): ')
else:
    filename = filename_param

if str.lower(filename[-4:]) != '.wav':
    if str.lower(filename[-1:]) == '.':
        filename += 'wav'
    else:
        filename += '.wav'

if string_to_write_param == '':
    while string_to_write == '':
        string_to_write = input('Intention to Write: ')
else:
    string_to_write = string_to_write_param

string_to_write_value += ' ' + PROCESS_STATEMENT

minval = peak_value
maxval = -peak_value

for element in string_to_write_value:
    if ord(element) < minval:
        minval = ord(element)
    if ord(element) > maxval:
        maxval = ord(element)

widthval = maxval - minval
range_factor = 0.95
scaled_peak_value = int(peak_value * range_factor)

num_writes = 0
start_time = time.time()
last_update_time = start_time

print("Press CTRL-C to stop running.\n")

obj = wave.open(filename, 'wb')
obj.setnchannels(1)  # mono
obj.setsampwidth(2)
obj.setframerate(sampling_rate)

# We write to the WAV file repeatedly until stopped or timer is reached.

try:
    while True:
        for element in string_to_write_value:
            ascii_val = ord(element)
            scaled_val = int((ascii_val - minval) / widthval * scaled_peak_value * 2 - scaled_peak_value)
            if num_writes % 2 == 0:
                value = scaled_val
            else:
                value = -scaled_val

            data = struct.pack('<h', value)
            obj.writeframesraw(data)

            num_writes += 1

            current_time = time.time()
            if current_time - last_update_time >= 1:
                elapsed_time = int(current_time - start_time)
                sys.stdout.write('  ' + time.strftime('%H:%M:%S', time.gmtime(elapsed_time)) +
                                 ' [' + human_format(num_writes) + '] ' + string_to_write + '   \r')
                sys.stdout.flush()
                last_update_time = current_time

            if run_time_param and time.strftime('%H:%M:%S', time.gmtime(elapsed_time)) >= run_time_param:
                print("\nIntention written " + human_format(num_writes) + " times to " + filename + ".")
                obj.close()
                quit()
except KeyboardInterrupt:
    pass

print("\nIntention written " + human_format(num_writes) + " times to " + filename + ".")
obj.close()