# -*- coding: utf-8 -*-

'''
@file  CDEFGABCn.py
@brief Application entry point.
'''

__author__    = 'Kazuyuki TAKASE'
__copyright__ = 'PLEN Project Company Inc, and all authors.'
__license__   = 'The MIT License'


import os
import sys
import json
from time import sleep
from argparse import ArgumentParser
from drivers.usb.core import USBDriver


# Create module level instances.
# =============================================================================
THIRD_TEMPO = 0.10


def play_sound(driver, sound):
    def _attack(move0, move1, attack, base):
        driver.apply(move0[0], move0[1])
        driver.apply(move1[0], move1[1])
        sleep(THIRD_TEMPO)

        driver.apply(attack[0], attack[1])
        sleep(THIRD_TEMPO)

        driver.apply(base[0], base[1])
        sleep(THIRD_TEMPO)

    def _sleep():
        sleep(THIRD_TEMPO * 3)

    def _tempo_down():
        global THIRD_TEMPO; THIRD_TEMPO *= 2

    def _tempo_up():
        global THIRD_TEMPO; THIRD_TEMPO /= 2

    commands = {
        'c': [
            _attack,
            ('left_shoulder_roll', 375),
            ('left_elbow_roll', 60),
            ('left_shoulder_pitch', 430),
            ('left_shoulder_pitch', 475)
        ],
        'd': [
            _attack,
            ('left_shoulder_roll', 495),
            ('left_elbow_roll', 60),
            ('left_shoulder_pitch', 440),
            ('left_shoulder_pitch', 475)
        ],
        'e': [
            _attack,
            ('left_shoulder_roll', 590),
            ('left_elbow_roll', 60),
            ('left_shoulder_pitch', 435),
            ('left_shoulder_pitch', 475)
        ],
        'f': [
            _attack,
            ('left_shoulder_roll', 590),
            ('left_elbow_roll', -85),
            ('left_shoulder_pitch', 415),
            ('left_shoulder_pitch', 475)
        ],
        'g': [
            _attack,
            ('right_shoulder_roll', -350),
            ('right_elbow_roll', 180),
            ('right_shoulder_pitch', -510),
            ('right_shoulder_pitch', -570)
        ],
        'a': [
            _attack,
            ('right_shoulder_roll', -350),
            ('right_elbow_roll', 11),
            ('right_shoulder_pitch', -525),
            ('right_shoulder_pitch', -570)
        ],
        'b': [
            _attack,
            ('right_shoulder_roll', -240),
            ('right_elbow_roll', 11),
            ('right_shoulder_pitch', -535),
            ('right_shoulder_pitch', -570)
        ],
        'cn': [
            _attack,
            ('right_shoulder_roll', -140),
            ('right_elbow_roll', 11),
            ('right_shoulder_pitch', -525),
            ('right_shoulder_pitch', -570)
        ],
        '-': [_sleep],
        '<': [_tempo_down],
        '>': [_tempo_up]
    }

    commands[sound][0](*commands[sound][1:])


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

    driver.homePosition()

    while True:
        map(lambda s: play_sound(driver, s), music.split())

        if (not args.loop): break


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

    arg_parser.add_argument(
        '-l', '--loop',
        dest     = 'loop',
        action   = 'store_true',
        help     = 'Please set boolean that decides doing loop.'
    )

    args = arg_parser.parse_args()
    main(args)
