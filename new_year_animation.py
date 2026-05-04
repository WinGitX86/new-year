# Copyright (C) 2026 WinGitX86
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Author: WinGitX86

import curses
import random
import time
import sys
import os

class TermAnimation:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        self.stdscr.timeout(30)

        self.height, self.width = stdscr.getmaxyx()
        if self.height < 24 or self.width < 80:
            self.resize_warning()

        self.running = True
        self.start_time = time.time()
        self.fallings = []
        self.blessings = ["福", "禄", "寿", "喜", "财", "马", "吉", "祥", "顺", "安", "康"]
        self.scroll_text = "祝您新春快乐，阖家幸福，马到成功，财源广进！"
        self.scroll_x = self.width - 1

        self.init_colors()
        self.draw_static()

    def resize_warning(self):
        self.stdscr.clear()
        try:
            self.stdscr.addstr(0, 0, "请将终端窗口放大到至少 80x24 以获得最佳体验", curses.A_BOLD)
            self.stdscr.addstr(2, 0, "按任意键继续...")
            self.stdscr.getch()
        except curses.error:
            pass
        self.height, self.width = self.stdscr.getmaxyx()

    def init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        curses.init_pair(4, curses.COLOR_MAGENTA, -1)
        curses.init_pair(5, curses.COLOR_CYAN, -1)

    def draw_static(self):
        self.stdscr.clear()
        border_color = curses.color_pair(2) | curses.A_BOLD

        for x in range(self.width):
            try:
                self.stdscr.addch(0, x, '=', border_color)
                self.stdscr.addch(self.height - 1, x, '=', border_color)
            except curses.error:
                pass

        for y in range(1, self.height - 1):
            try:
                self.stdscr.addch(y, 0, '|', border_color)
                self.stdscr.addch(y, self.width - 1, '|', border_color)
            except curses.error:
                pass

        title = "2026 马年大吉"
        subtitle = "新年快乐 · 万事如意"
        try:
            self.stdscr.addstr(2, (self.width - len(title)) // 2, title,
                               curses.color_pair(2) | curses.A_BOLD)
            self.stdscr.addstr(4, (self.width - len(subtitle)) // 2, subtitle,
                               curses.color_pair(1) | curses.A_BOLD)
        except curses.error:
            pass

        self.draw_lantern(6, 2, "left")
        self.draw_lantern(6, self.width - 12, "right")
        self.draw_horse(18, 3)
        self.draw_firecrackers(20, self.width - 15)

    def draw_lantern(self, y, x, side):
        try:
            for i, line in enumerate([
                "   .   ", " .###. ", " # # # ", "  ###  ", "   |   "
            ]):
                if y + i < self.height - 1 and x + len(line) < self.width:
                    self.stdscr.addstr(y + i, x, line, curses.color_pair(1))

            if side == "left" and y - 1 >= 0 and x + 4 < self.width:
                self.stdscr.addstr(y - 1, x + 4, "\\", curses.color_pair(2))
            elif side == "right" and y - 1 >= 0 and x + 4 < self.width:
                self.stdscr.addstr(y - 1, x + 4, "/", curses.color_pair(2))
        except curses.error:
            pass

    def draw_horse(self, y, x):
        horse = [
            "  /\\___/\\  ",
            " (  o o  ) ",
            "  \\  ^  /  ",
            "   \\---/   ",
            "   |   |   ",
            "   |马 |   "
        ]
        for i, line in enumerate(horse):
            try:
                if y + i < self.height - 1 and x + len(line) < self.width:
                    self.stdscr.addstr(y + i, x, line, curses.color_pair(3))
            except curses.error:
                pass

    def draw_firecrackers(self, y, x):
        for i in range(5):
            try:
                if y - i < self.height - 1 and x + 3 < self.width:
                    self.stdscr.addstr(y - i, x, "[!!]", curses.color_pair(1))
                    self.stdscr.addstr(y - i, x + 4, "  |", curses.color_pair(2))
            except curses.error:
                pass

    def add_falling(self):
        ch = random.choice(self.blessings)
        x = random.randint(2, self.width - 3)
        speed = random.uniform(0.3, 0.8)
        color = random.choice([1, 2, 4, 5])
        self.fallings.append({
            "ch": ch,
            "x": x,
            "y": 8,
            "speed": speed,
            "color": color
        })

    def update_falling(self):
        new_list = []
        for f in self.fallings:
            f["y"] += f["speed"]
            if f["y"] < self.height - 2:
                try:
                    self.stdscr.addch(int(f["y"]), f["x"], f["ch"],
                                      curses.color_pair(f["color"]) | curses.A_BOLD)
                except curses.error:
                    pass
                new_list.append(f)
        self.fallings = new_list

    def draw_scroll(self):
        try:
            if self.scroll_x < -len(self.scroll_text):
                self.scroll_x = self.width - 1
            for i, ch in enumerate(self.scroll_text):
                x = self.scroll_x + i
                if 0 <= x < self.width:
                    self.stdscr.addch(12, x, ch, curses.color_pair(2))
            self.scroll_x -= 1
        except curses.error:
            pass

    def run(self):
        last_drop = time.time()
        while self.running:
            self.stdscr.clear()
            self.draw_static()

            if time.time() - last_drop > 0.3:
                self.add_falling()
                last_drop = time.time()

            self.update_falling()
            self.draw_scroll()

            try:
                self.stdscr.addstr(self.height - 2, 2, "拜年动画播放中... 30秒后自动退出",
                                   curses.color_pair(4))
                elapsed = time.time() - self.start_time
                remaining = max(0, 30 - elapsed)
                self.stdscr.addstr(self.height - 2, self.width - 20, f"剩余 {int(remaining)} 秒",
                                   curses.color_pair(4))
            except curses.error:
                pass

            self.stdscr.refresh()

            if elapsed >= 30:
                break

            curses.napms(100)

        self.cleanup()

    def cleanup(self):
        self.stdscr.clear()
        try:
            self.stdscr.addstr(self.height // 2, (self.width - 30) // 2, "拜年动画结束，祝您马年大吉！",
                               curses.color_pair(2) | curses.A_BOLD)
        except curses.error:
            pass
        self.stdscr.refresh()
        curses.napms(2000)

        # 自毁：删除自身脚本文件
        try:
            os.remove(sys.argv[0])
        except OSError:
            pass

        self.running = False

def main(stdscr):
    anim = TermAnimation(stdscr)
    anim.run()

if __name__ == "__main__":
    curses.wrapper(main)