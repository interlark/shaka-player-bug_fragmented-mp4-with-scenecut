#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
from shutil import rmtree

import requests
from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DEMO_DIR = os.path.join(SCRIPT_DIR, 'demo')
VIDEO_DIR = os.path.join(DEMO_DIR, 'videos')
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, 'html_templates')
DATA_JSON = os.path.join(SCRIPT_DIR, 'demo_data.json')

def download_file(url, dest):
    r = requests.get(url)
    with open(dest, 'wb') as f_dl:
        f_dl.write(r.content)

def create_dirs():
    if os.path.isdir(DEMO_DIR):
        rmtree(DEMO_DIR)
    os.mkdir(DEMO_DIR)
    os.mkdir(VIDEO_DIR)

def encode_video(filename, fps, fragment_duration=6):
    """Encode video for HLS stream with and without no-scenecut option
    Args:
        filename (str): filename of input video file.
        fps (float): input video file's FPS (frames per second).
        fragment_duration (int): output stream's segment duration (in seconds), could be 2, 4, 6, etc...
    """
    for no_scenecut in (False, True):
        # command for 1st pass
        cmd_first_pass = [
            'ffmpeg',
            '-y', '-i', filename,
            '-an', '-sn', '-dn',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-b:v', '2000k', '-maxrate', '2200k', '-bufsize', '4000k',
            '-g', str(round(fps)*2), '-keyint_min', str(round(fps)*2),
            '-force_key_frames', f'expr:gte(t,n_forced*2)',
            '-profile:v', 'main',
            '-preset', 'slow',
            '-pass', '1',
            '-f', 'mp4',
        ] + \
        (['-x264opts', 'no-scenecut'] if no_scenecut else []) + ['/dev/null']

        # command for 2nd pass
        cmd_second_pass = [
            'ffmpeg',
            '-y', '-i', filename,
            '-sn', '-dn',
            '-c:a', 'aac', '-ar', '48000', '-b:a', '128k', '-ac', '2',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-b:v', '2000k', '-maxrate', '2200k', '-bufsize', '4000k',
            '-g', str(round(fps)*2), '-keyint_min', str(round(fps)*2),
            '-force_key_frames', f'expr:gte(t,n_forced*2)',
            '-profile:v', 'main',
            '-preset', 'slow',
            '-movflags', '+faststart',
            '-pass', '2',
            '-f', 'mp4',
        ] + \
        (['-x264opts', 'no-scenecut', 'encoded-no-scenecut.mp4'] if no_scenecut else ['encoded.mp4'])

        # command for creating hls stream
        cmd_fragments = [
            'ffmpeg',
            '-i', 'encoded-no-scenecut.mp4' if no_scenecut else 'encoded.mp4',
            '-vcodec', 'copy',
            '-acodec', 'copy',
            '-f', 'hls',
        '-hls_time', str(fragment_duration),
        '-start_number', '0', 
        '-hls_list_size', '0',
        '-hls_playlist_type', 'vod',
        ]
        if no_scenecut:
            cmd_fragments += [
                '-hls_segment_filename', 'fragment-no-scenecut-%03d.ts',
                '-master_pl_name', 'master-no-scenecut.m3u8',
                'fragments-no-scenecut.m3u8'
            ]
        else:
            cmd_fragments += [
                '-hls_segment_filename', 'fragment-%03d.ts',
                '-master_pl_name', 'master.m3u8',
                'fragments.m3u8'
            ]

        subprocess.call(cmd_first_pass)
        subprocess.call(cmd_second_pass)
        subprocess.call(cmd_fragments)


def build_video_html(entry, player_name, no_scenecut):
    jinja2_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    page_path = os.path.join(DEMO_DIR, f'video_{player_name}_{entry["id"]}{"_without_scenecut" if no_scenecut else ""}.html')
    content = jinja2_env.get_template(f'video_{player_name}.j2').render(entry=entry, title=f'{entry["name"]} ({player_name})', no_scenecut=no_scenecut)
    with open(page_path, 'w') as f_html:
        f_html.write(content)

def build_index_html(data):
    jinja2_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    page_path = os.path.join(DEMO_DIR, 'index.html')
    content = jinja2_env.get_template('index.j2').render(data=data, title=None)
    with open(page_path, 'w') as f_html:
        f_html.write(content)

if __name__ == '__main__':
    # create_dirs()
    with open(DATA_JSON, 'r') as f_data:
        data = json.load(f_data)
        build_index_html(data)
        for entry in data:
            print(f'Workin on', entry['name'], file=sys.stderr)
            entry_dir = os.path.join(VIDEO_DIR, entry['dir'])
            # os.mkdir(entry_dir)
            # os.chdir(entry_dir)
            # download_file(entry['url'], entry['filename'])
            # encode_video(entry['filename'], entry['fps'])
            for player in ('shaka', 'hlsjs'):
                build_video_html(entry, player, no_scenecut=False)
                build_video_html(entry, player, no_scenecut=True)