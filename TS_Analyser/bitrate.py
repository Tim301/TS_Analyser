#!/usr/bin/env python3
#
# FFProbe Bitrate Graph
#
# Copyright (c) 2013-2019, Eric Work
# All rights reserved.
#

import sys
import shutil
import argparse
import subprocess

# prefer C-based ElementTree
def getBitrate(path, max):
    try:
        import xml.etree.cElementTree as etree
    except ImportError:
        import xml.etree.ElementTree as etree

    # check for ffprobe in path
    if not shutil.which("ffprobe"):
        sys.stderr.write("Error: Missing ffprobe from package 'ffmpeg'\n")
        sys.exit(1)

    # parse command line arguments
    parser = argparse.ArgumentParser(
        description="Graph bitrate for audio/video stream")
    #parser.add_argument('input', help="input file/stream", metavar="INPUT")
    parser.add_argument('-s', '--stream', help="stream type",
                        choices=["audio", "video"], default="video")
    parser.add_argument('-o', '--output', help="output file")
    parser.add_argument('-p', '--progress', help="show progress",
                        action='store_true')
    parser.add_argument('--min', help="set plot minimum (kbps)", type=int)
    parser.add_argument('--max', help="set plot maximum (kbps)", type=int)
    args = parser.parse_args()

    bitrate_data = {}
    bitrate_frame = []
    frame_count = 0
    frame_rate = None
    frame_time = 0.0
    total_time = None

    # get stream duration from the container
    if args.progress:
        with subprocess.Popen(
                ["ffprobe",
                 "-show_entries", "format",
                 "-print_format", "xml",
                 path
                 ],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL) as proc_format:

            # parse format header xml
            format_data = etree.parse(proc_format.stdout)
            format_elem = format_data.find('.//format')

            # save the total time for later
            try:
                total_time = float(format_elem.get('duration'))
            except:
                sys.stderr.write("Error: Failed to determine stream duration\n")
                sys.exit(1)

    # set ffprobe stream specifier
    if args.stream == 'audio':
        stream_spec = 'a'
    elif args.stream == 'video':
        stream_spec = 'V'
    else:
        raise RuntimeError("Invalid stream type")

    # get frame data for the selected stream
    with subprocess.Popen(
            ["ffprobe",
             "-show_entries", "frame",
             "-select_streams", stream_spec,
             "-print_format", "xml",
             path
             ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL) as proc_frame:

        # process xml elements as they close
        for event in etree.iterparse(proc_frame.stdout):

            # skip non-frame elements
            node = event[1]
            if node.tag != 'frame':
                continue

            # count number of frames
            frame_count += 1

            # get frame rate only once (assumes non-variable framerate)
            # TODO: use 'pkt_duration_time' each time instead
            if frame_rate is None:
                # audio frame rate, 1 / frame duration
                if args.stream == 'audio':
                    frame_rate = 1.0 / float(node.get('pkt_duration_time'))

                # video frame rate, read stream header
                else:
                    with subprocess.Popen(
                            ["ffprobe",
                             "-show_entries", "stream",
                             "-select_streams", "V",
                             "-print_format", "xml",
                             path
                             ],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL) as proc_stream:

                        # parse stream header xml
                        stream_data = etree.parse(proc_stream.stdout)
                        stream_elem = stream_data.find('.//stream')

                        # compute frame rate from ratio
                        frame_rate_ratio = stream_elem.get('avg_frame_rate')
                        (dividend, divisor) = frame_rate_ratio.split('/')
                        frame_rate = float(dividend) / float(divisor)

            # collect frame data
            try:
                frame_time = float(node.get('best_effort_timestamp_time'))
            except:
                try:
                    frame_time = float(node.get('pkt_pts_time'))
                except:
                    if frame_count > 1:
                        frame_time += float(node.get('pkt_duration_time'))

            frame_bitrate = (float(node.get('pkt_size')) * 8 / 1000) * frame_rate
            frame = (frame_time, frame_bitrate)
            bitrate_frame.append(frame_bitrate)  # Save in the table

            if frame_count == max:
                break

        # check if ffprobe was successful
        if frame_count == 0:
            sys.stderr.write("Error: No frame data, failed to execute ffprobe\n")
            sys.exit(1)

    return bitrate_frame

# end frame subprocess
