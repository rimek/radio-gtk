#!/bin/env python3
import os
from gi.repository import Gtk as gtk
import shlex
import subprocess

ICONS = ["icons/stop.png", "icons/play.png", "icons/loading.png"]

# play_command = 'mplayer mms://stream.polskieradio.pl/program3 -cache 150'
play_command = 'mplayer http://ic.dktr.pl:8000/trojka3.ogg -nolirc -cache 150'

os.path.dirname(os.path.realpath(__file__))

class Radio:
    process = None

    def __init__(self):
        self.status = 0

        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_from_file(ICONS[self.status])

        self.status_icon.connect("activate", self.activated)
        self.status_icon.connect("popup-menu", self.quit)
        self.status_icon.set_visible(True)

        self.play_args = shlex.split(play_command)

        gtk.main()

    def activated(self, widget):
        self.status = (self.status + 1) % 2
        self.play(self.status)

    def play(self, action):
        if action:
            self.process = subprocess.Popen(self.play_args, shell=False)
        else:
            self.process_stop()
        self.status_icon.set_from_file(ICONS[self.status])

    def process_stop(self):
        if self.process:
            self.process.terminate()

    def quit(self, arg1, arg2, arg3):
        self.process_stop()
        gtk.main_quit() 

if __name__ == "__main__":
    radio = Radio()
