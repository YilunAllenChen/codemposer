from sys import argv
from psonic import *
from threading import Thread, Event
from rich import print
import re
import random


BEAT_MULT = 0.8
memory = {}

# C1+, E1+, G1+
BASE_ADJ = 2 * 12
TOP = 80
note_list = (
    list(range(12 + BASE_ADJ, TOP, 12))        # C1+
    # + list(range(26, TOP, 12))      # D1+
    + list(range(16 + BASE_ADJ, TOP, 12))      # E1+
    # + list(range(29, TOP, 12))      # F1+
    + list(range(19 + BASE_ADJ, TOP, 12))      # G1+
    + list(range(21 + BASE_ADJ, TOP, 12))      # A1+
    + list(range(23 + BASE_ADJ, TOP, 12))      # B1+
)


splitters = r"[, | . | \( | \) | ' ' | \[ | \] | = | \{ | \} | \" | \' ]"

# set_server_parameter('10.0.0.78',4560)
set_server_parameter('127.0.0.1',4560)

def drumming_thread(done_composing: Event, sleepTime=[0.25, 0.125, 0.125, 0.25, 0.25, 1]):
    while not done_composing.is_set():
        for i in sleepTime:
            sample(DRUM_BASS_HARD, amp=1.5, rate=0.5)
            sleep(i * BEAT_MULT)

def play_piano(note):
    use_synth(PIANO)
    play(note, release=0.5, amp=1.5)

def play_bell(note):
    use_synth(PRETTY_BELL)
    play(note, release=0.5, amp=1.5)

def play_pluck(note):
    use_synth(PLUCK)
    play(note, release=0.5, amp=1.5)

def compose_from_file_thread(filepath: str, done_composing: Event):
    with open(file=filepath) as f:
        while True:
            l = f.readline()
            if len(l) == 0:
                break
            if len(l.strip()) == 0:
                sleep(0.25)
            print(l.rstrip())
            for word in re.split(splitters, l):
                if word.strip() == "":
                    continue
                # print(word)
                if word not in memory:
                    chorus_size = int(random.random() * 3) + 1
                    notes = random.choices(note_list, k=chorus_size)
                    sleep_time = random.choice([0.125] * 5 + [0.25])
                    memory[word] = [notes, sleep_time]
                notes, sleep_time = memory[word]
                for note in notes:
                    play_fn = random.choice([
                        # play_pluck,
                        play_piano,
                        play_bell
                    ])
                    play_fn(note)
                sleep(sleep_time * BEAT_MULT)
            sleep(0.125)
    done_composing.set()



if __name__ == "__main__":
    
    filepath = argv[1]
    random.seed(filepath)
    
    done_composing = Event()

    all_threads = [
            # Thread(target=drumming_thread, args=[done_composing]),
            Thread(target=compose_from_file_thread, args=[filepath, done_composing])
    ]
    for t in all_threads:
        t.start()


    for t in all_threads:
        t.join()

    print("Thanks for listening!")
