import wbetools
import tkinter
from .lab1 import URL

def lex(body):
    print(f"[LEX] Starting lexical analysis, body length: {len(body)}")
    text = ""
    in_tag = False
    tag_count = 0
    for c in body:
        if c == "<":
            in_tag = True
            tag_count += 1
        elif c == ">":
            in_tag = False
        elif not in_tag:
            text += c
        wbetools.record("lex", text)
    print(f"[LEX] Completed: {len(text)} characters, {tag_count} tags removed")
    return text

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18

SCROLL_STEP = 100

def layout(text):
    print(f"[LAYOUT] Starting layout, text length: {len(text)}")
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    line_count = 1
    for c in text:
        display_list.append((cursor_x, cursor_y, c))
        cursor_x += HSTEP
        if cursor_x >= WIDTH - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
            line_count += 1
        wbetools.record("layout", display_list)
    print(f"[LAYOUT] Completed: {len(display_list)} characters laid out, {line_count} lines")
    return display_list

class Browser:
    def __init__(self):
        print(f"[BROWSER] Initializing browser window {WIDTH}x{HEIGHT}")
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )

        self.canvas.pack()

        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        print(f"[BROWSER] Browser initialized, scroll position: {self.scroll}")

    def load(self, url):
        print(f"[BROWSER] Loading URL...")
        body = url.request()
        text = lex(body)
        self.display_list = layout(text)
        print(f"[BROWSER] Display list created with {len(self.display_list)} elements")
        self.draw()

    def draw(self):
        print(f"[BROWSER] Drawing at scroll position: {self.scroll}")
        self.canvas.delete("all")
        drawn = 0
        for x, y, c in self.display_list:
            wbetools.record("draw")
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c)
            drawn += 1
        print(f"[BROWSER] Drew {drawn} characters on canvas")

    def scrolldown(self, e):
        print(f"[BROWSER] Scrolling down from {self.scroll} to {self.scroll + SCROLL_STEP}")
        self.scroll += SCROLL_STEP
        self.draw()

if __name__ == "__main__":
    import sys

    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()

# 실행 방법: python lab2.py http://info.cern.ch
# GUI 창이 뜨며, Down 키로 스크롤 가능
