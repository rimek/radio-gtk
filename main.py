#!/bin/env python3

import logging
import os
import shlex
import subprocess

from gi.repository import GObject, Gtk

cwd = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger()

STATUS_STOP = 0
STATUS_PLAY = 1
ICONS = [
    "icons/stop.png",
    "icons/play.png",
]

streams = {
    # TODO find a high quality stream
    'PR3 works, lq': 'http://stream3.polskieradio.pl:8904',  # poor quality but works
    'PR3 (old1)': 'http://www.polskieradio.pl/st/program3M.asx',
    'PR3 (old2)': 'mms://stream.polskieradio.pl/program3_wma10',
    'PR3 (old3)': 'http://ic.dktr.pl:8000/trojka3.ogg'
}


class Radio:
    process = None
    player = 'mpv %s'

    def __init__(self):
        self.status = STATUS_STOP
        self.stream = list(streams.values())[0]

        self.init_tray_icon()

        self.mainloop = GObject.MainLoop()
        try:
            self.mainloop.run()
        except KeyboardInterrupt:
            logger.info('Ctrl+C hit, quitting')
            self.quit()

    def init_trayicon(self):
        self.status_icon = Gtk.StatusIcon()
        self.status_icon.set_from_file(ICONS[self.status])

        self.status_icon.connect("activate", self.activated)
        self.status_icon.connect("popup-menu", self.make_menu)
        self.status_icon.set_visible(True)

    def player_cmd(self):
        return shlex.split(self.player % self.stream)

    def activated(self, widget):
        self.status += 1
        self.status %= 2

        if self.status == STATUS_STOP:
            self.stop()
        elif self.status == STATUS_PLAY:
            self.play()

    def play(self):
        self.process = subprocess.Popen(self.player_cmd(), shell=False)
        self.status_icon.set_from_file(ICONS[STATUS_PLAY])

    def stop(self):
        self.process_stop()
        self.status_icon.set_from_file(ICONS[STATUS_STOP])

    def restart(self):
        self.stop()
        self.play()

    def change_stream(self, stream_name):
        self.stream = streams[stream_name]
        self.restart()

    def make_menu(self, data, event_btn, event_time):
        menu = Gtk.Menu()
        for k, v in streams.items():
            stream_item = Gtk.MenuItem(k)
            menu.append(stream_item)
            stream_item.connect_object("activate", self.change_stream, k)
            stream_item.show()

        quit_item = Gtk.MenuItem("quit")
        menu.append(quit_item)
        quit_item.connect_object("activate", self.quit, "quit app")
        quit_item.show()

        menu.popup(None, None, None, None, event_btn, event_time)

    def quit(self, *args):
        try:
            self.process.terminate()
        except Exception as e:
            logger.warn(e)

        self.mainloop.quit()

if __name__ == "__main__":
    radio = Radio()
