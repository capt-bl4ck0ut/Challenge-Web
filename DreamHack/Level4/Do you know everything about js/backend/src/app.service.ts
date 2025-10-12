import "urlpattern-polyfill";
import { Injectable, HttpException, HttpStatus } from "@nestjs/common";

type Link = { rel: string; href: string; hreflang?: string; title?: string };
type Manifest = {
  links?: Link[];
  schedule?: string;
  headers?: Record<string, string>;
  locale?: string;
};

type State = {
  ab: ArrayBuffer;
  view: Uint8Array;
  cursor: number;
  links: Link[];
  acceptLanguage: string;
  tokenRef?: WeakRef<object>;
  deadline?: number;
  signal?: AbortSignal;
  cached?: string;
};

@Injectable()
export class AppService {
  #flag: string = process.env.FLAG || "DH{redacted}";
  private allow = new RegExp("^app://driver/(echo|sum|time)$", "d");
  private pat: unknown = new (
    globalThis as { URLPattern?: new (init: object) => unknown }
  ).URLPattern!({
    protocol: "app",
    hostname: "driver",
    pathname: "/:name",
  });
  private gate = new WeakMap<object, true>();
  private vgate = new WeakMap<object, true>();
  private lastRef?: WeakRef<object>;

  private decodeB64(s: string): Uint8Array {
    const b = Buffer.from(s, "base64");
    const u = new Uint8Array(b.length);
    for (let i = 0; i < b.length; i++) u[i] = b[i];
    return u;
  }

  private buildState(manifest: Manifest): State {
    const cloned = structuredClone(manifest);

    if (!cloned || typeof cloned !== "object") {
      throw new HttpException({ status: "DENY" }, HttpStatus.FORBIDDEN);
    }

    const sch = typeof cloned.schedule === "string" ? cloned.schedule : "";

    if (!sch) {
      throw new HttpException({ status: "DENY" }, HttpStatus.FORBIDDEN);
    }

    const bytes = this.decodeB64(sch);

    const ab = new (ArrayBuffer as new (
      length: number,
      options?: { maxByteLength?: number },
    ) => ArrayBuffer)(bytes.length, {
      maxByteLength: Math.max(4096, bytes.length * 2),
    });

    const view = new Uint8Array(ab);
    view.set(bytes, 0);

    const links = Array.isArray(cloned.links)
      ? cloned.links.filter((x) => x && typeof x.href === "string")
      : [];

    const al = String(cloned.headers?.["accept-language"] || "");

    const result = { ab, view, cursor: 0, links, acceptLanguage: al };
    return result;
  }

  private readNextToken(st: State): string {
    let end = st.cursor;
    while (end < st.view.length && st.view[end] !== 0x7c) end++;

    const slice = st.view.slice(st.cursor, end);
    const dec = new TextDecoder("utf-8");
    const token = dec.decode(slice);

    const nextPos = Math.min(st.view.length, end + 1);

    const remain = st.view.length - nextPos;
    const abWithTransfer = st.ab as ArrayBuffer & {
      transfer?: (newLength: number) => ArrayBuffer;
    };

    if (abWithTransfer.transfer) {
      const rest =
        remain > 0
          ? new Uint8Array(st.view.subarray(nextPos))
          : new Uint8Array(0);
      st.ab = abWithTransfer.transfer(rest.length);
      st.view = new Uint8Array(st.ab);
      if (rest.length) st.view.set(rest, 0);
      st.cursor = 0;
    } else {
      st.cursor = nextPos;
    }

    return token;
  }

  private parseAcceptLanguage(h: string): { tag: string; q: number }[] {
    const out: { tag: string; q: number }[] = [];
    for (const part of String(h || "").split(",")) {
      const [lang, ...rest] = part.trim().split(";");
      if (!lang) continue;
      let q = 1.0;
      for (const r of rest) {
        const [k, v] = r.trim().split("=");
        if (k === "q") {
          const n = Number(v);
          if (!Number.isNaN(n)) q = Math.max(0, Math.min(1, n));
        }
      }
      out.push({ tag: lang.toLowerCase(), q });
    }
    return out.sort((a, b) => b.q - a.q);
  }

  private langMatchScore(
    hrefLang: string,
    prefs: { tag: string; q: number }[],
  ): number {
    const tag = String(hrefLang || "").toLowerCase();
    if (!tag) return 0;
    for (const p of prefs) {
      if (p.tag === "*" || p.tag === tag) return 1000 + p.q;
      const base = p.tag.split("-")[0];
      if (base && tag.startsWith(base)) return 500 + p.q;
    }
    return 0;
  }

  private resolveVariant(st: State, label: string): string {
    const prefs = this.parseAcceptLanguage(st.acceptLanguage);
    let best: Link | null = null;
    let bestScore = -1;
    for (const lnk of st.links) {
      const rel = String(lnk.rel || "").toLowerCase();
      if (rel !== "variant" && rel !== "alternate" && rel !== "driver-variant")
        continue;
      const ttl = String(lnk.title || "");
      if (ttl !== label) continue;
      const score = this.langMatchScore(lnk.hreflang || "", prefs);
      if (score > bestScore) {
        bestScore = score;
        best = lnk;
      }
    }
    if (!best || typeof best.href !== "string") return "";
    try {
      const u = new URL(best.href);
      const seg = u.pathname.split("/").filter(Boolean);
      const name = seg[0] || "";
      const tk =
        st.tokenRef && typeof st.tokenRef.deref === "function"
          ? st.tokenRef.deref()
          : undefined;
      if (tk) this.vgate.set(tk, true);
      return name;
    } catch {
      return "";
    }
  }

  private finalizeName(st: State, raw: string): string {
    if (st.cached) return st.cached;
    let name = raw;
    if (raw.startsWith("v:")) {
      const label = raw.slice(2);
      const resolved = this.resolveVariant(st, label);
      name = resolved || raw;
    }
    st.cached = name;
    return name;
  }

  private makeDriver(st: State): unknown {
    const base = {};
    let primitiveFn: (() => string) | null = null;
    return new Proxy(base, {
      get: (t, p: any, r) => {
        if (p === Symbol.toPrimitive) {
          if (!primitiveFn) {
            primitiveFn = () => {
              if (!st.tokenRef) {
                const tok = Object.freeze({ t: Date.now() });
                st.tokenRef = new WeakRef(tok);
                this.gate.set(tok, true);
                st.deadline = Date.now() + 1200;
                st.signal = AbortSignal.timeout(1200);
                this.lastRef = st.tokenRef;
              }
              if (!st.cached) {
                const raw = this.readNextToken(st);
                const next = this.readNextToken(st);
                if (raw !== "echo" && raw !== "sum" && raw !== "time") {
                  st.cached = raw;
                } else {
                  st.cached = this.finalizeName(st, next);
                }
              }
              const result = "app://driver/" + st.cached;
              return result;
            };
          }
          return primitiveFn;
        }
        if (p === "toString") {
          return () => (primitiveFn ? primitiveFn() : "");
        }
        return Reflect.get(t, p, r) as unknown;
      },
    });
  }

  private adapters(): Record<string, () => string> {
    return {
      echo: () => "ok",
      sum: () => "0",
      time: () => String(Date.now()),
      getFlag: () => this.getFlag(this.lastRef),
    };
  }

  private getFlag(ref?: WeakRef<object>): string {
    if (!ref || typeof ref.deref !== "function") return "";
    const k = ref.deref();
    if (k && this.gate.get(k) === true && this.vgate.get(k) === true)
      return this.#flag;
    return "";
  }

  dispatch(manifest: Manifest): { out: string; pass: boolean } {
    if (!manifest || typeof manifest !== "object") {
      throw new HttpException({ status: "DENY" }, HttpStatus.FORBIDDEN);
    }

    const st = this.buildState(manifest);
    const driver: unknown = this.makeDriver(st);

    const first = "app://driver/" + this.readNextToken(st);
    const m = this.allow[Symbol.match](first);

    const hasValidIndices =
      m &&
      "indices" in m &&
      Array.isArray(m.indices) &&
      m.indices[0]?.[0] === 0;

    if (!m || !hasValidIndices) {
      throw new HttpException({ status: "DENY" }, HttpStatus.FORBIDDEN);
    }

    const second = String(driver);

    const patResult = (
      this.pat as {
        test?: (input: string) => boolean;
      }
    )?.test?.(second);

    if (!patResult) {
      throw new HttpException({ status: "DENY" }, HttpStatus.FORBIDDEN);
    }

    if (st.signal && st.signal.aborted) {
      throw new HttpException({ status: "DENY" }, HttpStatus.FORBIDDEN);
    }

    const ex = (
      this.pat as {
        exec?: (
          input: string,
        ) => { pathname?: { groups?: { name?: string } } } | null;
      }
    )?.exec?.(second);

    const name: string = ex?.pathname?.groups?.name || "";
    const fn = this.adapters()[name];

    if (typeof fn !== "function") {
      throw new HttpException({ status: "DENY" }, HttpStatus.FORBIDDEN);
    }

    const out = String(fn());
    const pass = out === this.#flag;

    return { out, pass };
  }
}
