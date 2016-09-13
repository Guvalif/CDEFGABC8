# -*- coding: utf-8 -*-

'''
@file  CDEFGABC8.py
@brief Application entry point.
'''

__author__    = 'Kazuyuki TAKASE'
__copyright__ = 'PLEN Project Company Inc, and all authors.'
__license__   = 'The MIT License'


import os
import sys
import json
import time
from argparse import ArgumentParser
from drivers.usb.core import USBDriver


# Create module level instances.
# =============================================================================
TEMPO = 0.25


def set_base_position(driver):
    base = {
        'left_shoulder_pitch': 770,
        'right_shoulder_pitch': -735
    }

    for joint, value in base.items():
        driver.applyDiff(joint, value)


def attack_left_arm(driver):
    attack_l = {
        'left_shoulder_pitch': 675
    }

    for joint, value in attack_l.items():
        driver.applyDiff(joint, value)

    time.sleep(TEMPO)

    set_base_position(driver)


def attack_right_arm(driver):
    attack_r = {
        'right_shoulder_pitch': -659
    }

    for joint, value in attack_r.items():
        driver.applyDiff(joint, value)

    time.sleep(TEMPO)

    set_base_position(driver)


def play_sound(driver, sound):
    cdefgabc8 = {
        'c': {
            'left_shoulder_roll': -82,
            'left_elbow_roll': 0
        },
        'd': {
            'left_shoulder_roll': -2,
            'left_elbow_roll': 0
        },
        'e': {
            'left_shoulder_roll': 108,
            'left_elbow_roll': 0
        },
        'f': {
            'left_shoulder_roll': 108,
            'left_elbow_roll': -138
        },
        'g': {
            'right_shoulder_roll': -75,
            'right_elbow_roll': 135
        },
        'a': {
            'right_shoulder_roll': -75,
            'right_elbow_roll': 0
        },
        'b': {
            'right_shoulder_roll': 30,
            'right_elbow_roll': 0
        },
        'c8': {
            'right_shoulder_roll': 125,
            'right_elbow_roll': 0
        },
        '-': {},
        '<': {},
        '>': {}
    }

    def _tempo_down(_):
        global TEMPO; TEMPO *= 2

    def _tempo_up(_):
        global TEMPO; TEMPO /= 2

    commands = {
        'c': attack_left_arm,
        'd': attack_left_arm,
        'e': attack_left_arm,
        'f': attack_left_arm,
        'g': attack_right_arm,
        'a': attack_right_arm,
        'b': attack_right_arm,
        'c8': attack_right_arm,
        '-': lambda d: time.sleep(TEMPO),
        '<': _tempo_down,
        '>': _tempo_up
    }

    for joint, value in cdefgabc8[sound].items():
        driver.applyDiff(joint, value)

    time.sleep(TEMPO)

    commands[sound](driver)


def main(args):
    # Get device mapping.
    # -------------------------------------------------------------------------
    if os.path.isfile('device_map.json'):
        with open('device_map.json', 'r') as fin:
            DEVICE_MAP = json.load(fin)
    else:
        print('"device_map.json" is not found!')

        sys.exit()


    # Create USB driver instance and connect a PLEN.
    # -------------------------------------------------------------------------
    driver = USBDriver(DEVICE_MAP, None)
    
    if not driver.connect():
        print('PLEN is not found!')

        sys.exit()


    # Set default position and read music.
    #
    # Default music is "Twinkle Twinkle Little Star" :)
    # -------------------------------------------------------------------------
    music = args.file.read() if args.file else 'c c g g a a g - f f e e d d c'

    set_base_position(driver)

    raw_input()

    map(lambda s: play_sound(driver, s), music.split())


# Application entry point.
# =============================================================================
if __name__ == '__main__':
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        '-f', '--file',
        dest     = 'file',
        type     = file,
        metavar  = '<FILE>',
        help     = 'Please set any score file you would like to play.'
    )

    args = arg_parser.parse_args()
    main(args)
