import wbetools
import tkinter
import tkinter.font
from lab1 import URL
from lab2 import WIDTH, HEIGHT, HSTEP, VSTEP, SCROLL_STEP, Browser

class Text:
    def __init__(self, text):
        self.text = text

    @wbetools.js_hide
    def __repr__(self):
        return "Text('{}')".format(self.text)

class Tag:
    def __init__(self, tag):
        self.tag = tag

    @wbetools.js_hide
    def __repr__(self):
        return "Tag('{}')".format(self.tag)

def lex(body):
    print(f"[LEX] Starting tokenization, body length: {len(body)}")
    out = []
    buffer = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if buffer: out.append(Text(buffer))
            buffer = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(buffer))
            buffer = ""
        else:
            buffer += c
    if not in_tag and buffer:
        out.append(Text(buffer))
    text_count = len([t for t in out if isinstance(t, Text)])
    tag_count = len([t for t in out if isinstance(t, Tag)])
    print(f"[LEX] Completed: {text_count} text tokens, {tag_count} tag tokens")
    return out

FONTS = {}

def get_font(size, weight, style):
    key = (size, weight, style)
    if key not in FONTS:
        font = tkinter.font.Font(size=size, weight=weight,
            slant=style)
        label = tkinter.Label(font=font)
        FONTS[key] = (font, label)
    return FONTS[key][0]

class Layout:
    def __init__(self, tokens):
        print(f"[LAYOUT] Starting layout with {len(tokens)} tokens")
        self.tokens = tokens
        self.display_list = []

        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.size = 12

        self.line = []
        for tok in tokens:
            self.token(tok)
        self.flush()
        print(f"[LAYOUT] Completed: {len(self.display_list)} words in display list")

    def token(self, tok):
        if isinstance(tok, Text):
            for word in tok.text.split():
                self.word(word)
        elif tok.tag == "i":
            print(f"[LAYOUT] Style changed to italic")
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            print(f"[LAYOUT] Weight changed to bold")
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"
        elif tok.tag == "small":
            self.size -= 2
            print(f"[LAYOUT] Font size decreased to {self.size}")
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
            print(f"[LAYOUT] Font size increased to {self.size}")
        elif tok.tag == "/big":
            self.size -= 4
        elif tok.tag == "br":
            print(f"[LAYOUT] Line break")
            self.flush()
        elif tok.tag == "/p":
            print(f"[LAYOUT] Paragraph end")
            self.flush()
            self.cursor_y += VSTEP
        
    def word(self, word):
        font = get_font(self.size, self.weight, self.style)
        w = font.measure(word)
        if self.cursor_x + w > WIDTH - HSTEP:
            self.flush()
        self.line.append((self.cursor_x, word, font))
        self.cursor_x += w + font.measure(" ")

    def flush(self):
        if not self.line: return
        print(f"[LAYOUT] Flushing line with {len(self.line)} words")
        wbetools.record("initial_y", self.cursor_y, self.line);
        metrics = [font.metrics() for x, word, font in self.line]
        wbetools.record("metrics", metrics)
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        wbetools.record("max_ascent", max_ascent);
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
            wbetools.record("aligned", self.display_list);
        max_descent = max([metric["descent"] for metric in metrics])
        wbetools.record("max_descent", max_descent);
        self.cursor_y = baseline + 1.25 * max_descent
        print(f"[LAYOUT] Line flushed, new cursor_y: {self.cursor_y:.2f}")
        self.cursor_x = HSTEP
        self.line = []
        wbetools.record("final_y", self.cursor_y);

@wbetools.patch(Browser)
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
        self.display_list = []
        print(f"[BROWSER] Browser initialized")

    def load(self, url):
        print(f"[BROWSER] Loading URL...")
        body = url.request()
        tokens = lex(body)
        self.display_list = Layout(tokens).display_list
        print(f"[BROWSER] Display list created with {len(self.display_list)} words")
        self.draw()

    def draw(self):
        print(f"[BROWSER] Drawing at scroll position: {self.scroll}")
        self.canvas.delete("all")
        drawn = 0
        for x, y, word, font in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + font.metrics("linespace") < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=word, font=font, anchor="nw")
            drawn += 1
        print(f"[BROWSER] Drew {drawn} words on canvas")

if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()

# 실행 방법: python src/lab3.py http://info.cern.ch
# GUI 창이 뜨며, 폰트 포맷팅(bold, italic 등) 적용됨