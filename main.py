#! /usr/bin/python2

import pygtk,os
pygtk.require("2.0")
import gtk
import shlex
import subprocess
import pexpect

START = 0
STOP = 1
LOADING = 2
ICONS = dict({START: "play.png", STOP: "stop.png", LOADING: "loading.png"})

play_command = 'mplayer mms://stream.polskieradio.pl/program3 -cache 150'

os.chdir('/add/projekty/radio/')

class Radio:
    process = ""

    def __init__(self):
        self.status = STOP

        self.statusIcon = gtk.StatusIcon()
        self.load_icon(ICONS[STOP])

        self.statusIcon.connect("activate", self.activated)
        self.statusIcon.connect("popup-menu", gtk.main_quit)
        self.statusIcon.set_visible(True)

        self.play_args = shlex.split(play_command)

        gtk.main()

    def load_icon(self, name):
        self.statusIcon.set_from_file("%s" % name)

    def activated(self, widget):
        self.status = (self.status + 1) % 2

        self.load_icon(ICONS[LOADING])
        self.play(self.status)

    def play(self, action):
        if action == START:
            self.process = subprocess.Popen(self.play_args)
            #self.process = pexpect.spawn(play_command)
            #print self.process.expect('AUDIO\:.*')
            self.load_icon(ICONS[START])
        else:
            self.process.terminate()
            self.load_icon(ICONS[STOP])



if __name__ == "__main__":
    radio = Radio()

