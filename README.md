# Browser Engineering

밑바닥부터 시작하는 웹 브라우저 구현 프로젝트

이 프로젝트는 "밑바닥부터 시작하는 웹 브라우저" 책을 기반으로, Python을 사용하여 웹 브라우저를 처음부터 구현합니다. curl이나 requests 같은 라이브러리 없이, 소켓 프로그래밍으로 HTTP 통신부터 화면 렌더링까지 직접 구현합니다.

**참고 도서**: [밑바닥부터 시작하는 웹 브라우저](https://product.kyobobook.co.kr/detail/S000217503808)

## 프로젝트 구조

```
browser-engineering/
├── src/
│   ├── __init__.py
│   ├── lab1.py          # Lab 1: HTTP 클라이언트 (CLI)
│   ├── lab2.py          # Lab 2: 간단한 GUI 브라우저 (문자 단위)
│   ├── lab3.py          # Lab 3: 텍스트 포맷팅 (단어 단위)
│   └── wbetools.py      # 유틸리티 함수
├── pyproject.toml
└── README.md
```

## 설치 및 실행

이 프로젝트는 Python 표준 라이브러리만 사용하므로 별도의 패키지 설치가 필요 없습니다.

### 요구사항

- Python 3.8 이상
- Tkinter (대부분의 Python 설치에 포함되어 있음)
