#!/usr/bin/env python3
"""
Browser Engineering 프로젝트 실행 스크립트

사용법:
    python run.py [lab번호] [URL]

예시:
    python run.py 1 http://example.org
    python run.py 2 http://example.org
    python run.py 3 http://browser.engineering/examples/example1-formatting.html
    python run.py 4 https://browser.engineering/layout.html
    python run.py 5 https://browser.engineering/layout.html
    python run.py 6 https://browser.engineering/layout.html
    python run.py 7 https://browser.engineering/
"""

import sys
import os

# src 디렉토리를 Python path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n사용 가능한 Lab:")
        print("  1: HTTP 클라이언트 (CLI) - URL의 HTML 소스를 터미널에 출력")
        print("  2: 간단한 GUI 브라우저 (문자 단위 렌더링)")
        print("  3: 텍스트 포맷팅 브라우저 (단어 단위 + 볼드/이탤릭)")
        print("  4: HTML 파싱 트리 구조 브라우저 (DOM tree)")
        print("  5: 블록 레이아웃 브라우저 (Block layout + Document layout)")
        print("  6: CSS 스타일링 브라우저 (CSS parsing + styling)")
        print("  7: 탭 브라우저 (Tabs + Chrome UI)")
        return

    lab_num = sys.argv[1]

    default_urls = {
        "1": "http://example.org",
        "2": "http://example.org",
        "3": "http://browser.engineering/examples/example1-formatting.html",
        "4": "http://browser.engineering/examples/example1-formatting.html",
        "5": "http://browser.engineering/examples/example1-formatting.html",
        "6": "http://browser.engineering/examples/example1-formatting.html",
        "7": "https://browser.engineering/",
    }

    url = (
        sys.argv[2]
        if len(sys.argv) > 2
        else default_urls.get(lab_num, "http://example.org")
    )

    if lab_num == "1":
        print(f"=== Lab 1: HTTP 클라이언트 실행 ===")
        print(f"URL: {url}\n")
        from lab1 import URL

        parsed_url = URL(url)
        body = parsed_url.request()
        print(body)

    elif lab_num == "2":
        print(f"=== Lab 2: GUI 브라우저 (문자 단위) 실행 ===")
        print(f"URL: {url}")
        from lab2 import Browser

        browser = Browser()
        browser.load(url)
        browser.window.mainloop()

    elif lab_num == "3":
        print(f"=== Lab 3: 텍스트 포맷팅 브라우저 실행 ===")
        print(f"URL: {url}")
        from lab1 import URL
        from lab3 import Browser

        browser = Browser()
        browser.load(URL(url))
        browser.window.mainloop()

    elif lab_num == "4":
        print(f"=== Lab 4: HTML 파싱 트리 브라우저 실행 ===")
        print(f"URL: {url}")
        import tkinter
        from lab1 import URL
        from lab4 import Browser

        browser = Browser()
        browser.load(URL(url))
        tkinter.mainloop()

    elif lab_num == "5":
        print(f"=== Lab 5: 블록 레이아웃 브라우저 실행 ===")
        print(f"URL: {url}")
        import tkinter
        from lab1 import URL
        from lab5 import Browser

        browser = Browser()
        browser.load(URL(url))
        tkinter.mainloop()

    elif lab_num == "6":
        print(f"=== Lab 6: CSS 스타일링 브라우저 실행 ===")
        print(f"URL: {url}")
        import tkinter
        from lab1 import URL
        from lab6 import Browser

        browser = Browser()
        browser.load(URL(url))
        tkinter.mainloop()

    elif lab_num == "7":
        print(f"=== Lab 7: 탭 브라우저 실행 ===")
        print(f"URL: {url}")
        import tkinter
        from lab7 import URL, Browser

        browser = Browser()
        browser.new_tab(URL(url))
        tkinter.mainloop()

    else:
        print(f"오류: 알 수 없는 Lab 번호 '{lab_num}'")
        print("사용 가능한 Lab: 1, 2, 3, 4, 5, 6, 7")
        sys.exit(1)


if __name__ == "__main__":
    main()


# https://browser.engineering/layout.html
