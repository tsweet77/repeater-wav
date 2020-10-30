#!/usr/bin/python
# -*- coding: utf-8 -*-

# Intention Repeater WAV File Writer created by Thomas Sweet
# Updated 10/24/2020 v2.2
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

PROCESS_STATEMENT = ": ONE INFINITE CREATOR. REQUESTING AID FROM ALL BEINGS WHO ARE WILLING TO ASSIST. METATRON'S CUBE. ALL AVAILABLE BENEFICIAL ENERGY GRIDS, ORGONE AETHER RESONATORS, & ORGONE BUBBLES. CREATE MANIFESTATION ZONE. ASCENSION PYRAMID. USE EVERY AVAILABLE RESOURCE. MANIFEST ASAP. CREATE STRUCTURE. CANCEL DESTRUCTIVE OR FEARFUL INTENTIONS, OR INTENTIONS THAT CONFLICT WITH THE HIGHEST AND GREATEST GOOD OF THE USER. REGULATE AND BALANCE THE ENERGY. USE THE MOST EFFECTIVE PATH IN THE MOST EFFICIENT WAY. OPTIMAL ENERGY. INTEGRATE THE ENERGY IN THE MOST EFFECTIVE AND PLEASANT WAY POSSIBLE. PROCESS THE CHANGES. GUIDED BY THE USER'S HIGHER SELF. CONNECTED TO SOURCE. ENABLE AND UTILIZE THE SACRED HEART, QUANTUM HEART, AND QUANTUM MIND. MANIFEST ALL SPECIFIED INTENTIONS AND/OR DESIRES, OR BETTER. IF IT WOULD AID IN THE MANIFESTATION PROCESS, PLEASE HELP USER TO SENSE AND EMOTIONALLY FEEL WHAT IT WOULD BE LIKE TO ALREADY BE EXPERIENCING THEIR SPECIFIED INTENTIONS AND/OR DESIRES NOW. PLEASE HELP USER TO RAISE THEIR VIBRATION TO THE LEVEL REQUIRED TO MAKE THEIR SPECIFIED INTENTIONS AND/OR DESIRES MANIFEST. ASSIST THE USER WITH ACHIEVING OPTIMAL GUT/HEART/MIND COHERENCE WITH THEIR SPECIFIED INTENTIONS AND/OR DESIRES. IF IT WOULD BENEFIT THE USER, ASSIST THEM WITH CLEARING & RELEASING ANY/ALL INTERNAL OR EXTERNAL INTERFERENCE OR BLOCKAGES TO THEIR SPECIFIED INTENTIONS AND/OR DESIRES. IT IS DONE. NOW RETURN A PORTION OF THE LOVE/LIGHT RECEIVED AND ACTIVATED BACK INTO THE HIGHER REALMS OF CREATION. I LOVE YOU. OM."

# Volume level should be from 0.000 to 1.000, and determines amplitude

volume_level = 1.000
sampling_rate = 96000.0
#sampling_rate = 111111.0

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


print("Intention Repeater WAV File Writer v2.2 software created by Thomas Sweet.\n")
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
peak_value_2 = peak_value * 2

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

benchmark = 0
start_time = float(time.time())

# See how many iterations the processor can run in one second.

minval = peak_value_2
maxval = -peak_value_2

for element in string_to_write_value:
    if ord(element) <= minval:
        minval = ord(element)

for element in string_to_write_value:
    if ord(element) >= maxval:
        maxval = ord(element)

widthval = maxval - minval

if widthval == 0:
    widthval = 0.00001

multiplier = peak_value_2 / widthval

obj = wave.open('benchmark.dat', 'wb')
obj.setnchannels(1)  # mono
obj.setsampwidth(2)
obj.setframerate(sampling_rate)

start_time = float(time.time())

while float(time.time()) - start_time < 1.00:
    benchmark += 1
    for element in string_to_write_value:
        if ord(element) < widthval / 2 + minval:
            value = ord(element) * multiplier + peak_value + peak_value - (ord(element) * multiplier + peak_value)
            value = int(value * volume_level)
        elif ord(element) > widthval / 2 + minval:
            value = ord(element) * multiplier - peak_value - peak_value - (ord(element) * multiplier - peak_value)
            value = int(value * volume_level)
        else:
            value = 0

        data = struct.pack('<h', value)
        obj.writeframesraw(data)

obj.close()

num_writes = 0

print("Press CTRL-C to stop running.\n")

obj = wave.open(filename, 'wb')
obj.setnchannels(1)  # mono
obj.setsampwidth(2)
obj.setframerate(sampling_rate)

# We write to the WAV file repeatedly until stopped or timer is reached.

try:
    while True:
        for d in range(benchmark):
            for element in string_to_write_value:
                if ord(element) < widthval / 2 + minval:
                    value = ord(element) * multiplier + peak_value + peak_value - (ord(element) * multiplier + peak_value)
                    value = int(value * volume_level)
                elif ord(element) > widthval / 2 + minval:
                    value = ord(element) * multiplier - peak_value - peak_value - (ord(element) * multiplier - peak_value)
                    value = int(value * volume_level)
                else:
                    value = 0

                data = struct.pack('<h', value)
                obj.writeframesraw(data)

            num_writes += 1
            if num_writes % benchmark == 0:
                sys.stdout.write('  ' + time.strftime('%H:%M:%S',
                                 time.gmtime(int(num_writes
                                 / benchmark))) + ' ['
                                 + human_format(num_writes) + '] '
                                 + string_to_write + '   \r')
                sys.stdout.flush()
                if run_time_param == time.strftime('%H:%M:%S',
                        time.gmtime(int(num_writes / benchmark))):
                    print("\nIntention written " \
                        + human_format(num_writes) \
                        + " times to " + filename + ".")
                    obj.close()
                    quit()
except KeyboardInterrupt:

    pass

print("\Intention written " \
    + human_format(num_writes) \
    + " times to " + filename + ".")

obj.close()
