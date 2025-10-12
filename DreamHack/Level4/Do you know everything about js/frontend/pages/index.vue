<template>
  <div class="wrap">
    <h1>Manifest Console</h1>

    <section class="card">
      <h2>Links</h2>
      <div class="row">
        <label>rel</label>
        <select v-model="linkRel">
          <option value="driver">driver</option>
          <option value="variant">variant</option>
          <option value="alternate">alternate</option>
          <option value="driver-variant">driver-variant</option>
        </select>
        <label>href</label>
        <input v-model="linkHref" placeholder="app://driver/echo" />
      </div>
      <div class="row">
        <label>hreflang</label>
        <input v-model="linkLang" placeholder="en-US" />
        <label>title</label>
        <input v-model="linkTitle" placeholder="alpha" />
        <button @click="addLink">Add</button>
      </div>
      <ul>
        <li v-for="(l, i) in links" :key="i">
          <code>{{ l.rel }}</code>
          <span>→</span>
          <code>{{ l.href }}</code>
          <span v-if="l.hreflang">|</span>
          <code v-if="l.hreflang">{{ l.hreflang }}</code>
          <span v-if="l.title">|</span>
          <code v-if="l.title">{{ l.title }}</code>
          <button @click="removeLink(i)">Remove</button>
        </li>
      </ul>
    </section>

    <section class="card">
      <h2>Schedule</h2>
      <div class="row">
        <label>tokens</label>
        <input v-model="scheduleText" placeholder="echo|echo|time" />
        <button @click="setSafe">Set Safe</button>
      </div>
      <div class="row">
        <label>base64</label>
        <input v-model="scheduleB64" />
        <button @click="syncFromText">Encode</button>
        <button @click="syncToText">Decode</button>
      </div>
      <p class="hint">ASCII 토큰만 사용하십시오. 구분자는 | 입니다.</p>
    </section>

    <section class="card">
      <h2>Headers</h2>
      <div class="row">
        <label>name</label>
        <input v-model="hName" placeholder="accept-language" />
        <label>value</label>
        <input v-model="hValue" placeholder="en-US,en;q=0.9" />
        <button @click="addHeader">Add</button>
      </div>
      <ul>
        <li v-for="(kv, i) in headerEntries" :key="i">
          <code>{{ kv[0] }}</code>
          <span>:</span>
          <code>{{ kv[1] }}</code>
          <button @click="removeHeader(i)">Remove</button>
        </li>
      </ul>
    </section>

    <section class="card">
      <h2>Locale</h2>
      <div class="row">
        <label>locale</label>
        <input v-model="locale" placeholder="en-US" />
      </div>
    </section>

    <section class="card">
      <h2>Manifest JSON</h2>
      <textarea :value="manifestJson" readonly></textarea>
      <div class="row">
        <button @click="send" :disabled="sending">Send</button>
        <span v-if="sending">Sending...</span>
      </div>
    </section>

    <section class="card">
      <h2>Response</h2>
      <textarea :value="respText" readonly></textarea>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useRuntimeConfig } from "#imports"

const { public: { apiBase } } = useRuntimeConfig()
const api = apiBase as string
const links = ref<{ rel: string; href: string; hreflang?: string; title?: string }[]>([
  { rel: "driver", href: "app://driver/echo", hreflang: "en" }
])
const linkRel = ref("driver")
const linkHref = ref("app://driver/echo")
const linkLang = ref("")
const linkTitle = ref("")
function addLink() {
  const item: { rel: string; href: string; hreflang?: string; title?: string } = {
    rel: linkRel.value,
    href: linkHref.value
  }
  if (linkLang.value) item.hreflang = linkLang.value
  if (linkTitle.value) item.title = linkTitle.value
  links.value.push(item)
  linkRel.value = "driver"
  linkHref.value = "app://driver/echo"
  linkLang.value = ""
  linkTitle.value = ""
}
function removeLink(i: number) {
  links.value.splice(i, 1)
}
const scheduleText = ref("echo|echo|time")
const scheduleB64 = ref("ZWNob3xlY2hvfHRpbWU=")
function toBase64Ascii(s: string) {
  if (typeof window !== "undefined" && typeof (window as any).btoa === "function") return (window as any).btoa(s)
  return Buffer.from(s, "binary").toString("base64")
}
function fromBase64Ascii(b: string) {
  if (typeof window !== "undefined" && typeof (window as any).atob === "function") return (window as any).atob(b)
  return Buffer.from(b, "base64").toString("binary")
}
function syncFromText() {
  scheduleB64.value = toBase64Ascii(scheduleText.value)
}
function syncToText() {
  try {
    scheduleText.value = fromBase64Ascii(scheduleB64.value)
  } catch {
    scheduleText.value = ""
  }
}
function setSafe() {
  scheduleText.value = "echo|echo|time"
  syncFromText()
}
watchEffect(() => {
  if (!scheduleB64.value) syncFromText()
})
const headers = ref<Record<string, string>>({
  "accept-language": "en-US,en;q=0.9"
})
const hName = ref("")
const hValue = ref("")
function addHeader() {
  if (!hName.value) return
  headers.value = { ...headers.value, [hName.value]: hValue.value }
  hName.value = ""
  hValue.value = ""
}
const headerEntries = computed(() => Object.entries(headers.value))
function removeHeader(i: number) {
  const arr = Object.entries(headers.value)
  arr.splice(i, 1)
  headers.value = Object.fromEntries(arr)
}
const locale = ref("en-US")
const manifest = computed(() => {
  return {
    links: links.value,
    schedule: scheduleB64.value,
    headers: headers.value,
    locale: locale.value
  }
})
const manifestJson = computed(() => JSON.stringify({ manifest: manifest.value }, null, 2))
const respText = ref("")
const sending = ref(false)
async function send() {
  sending.value = true
  respText.value = ""
  try {
    const res = await $fetch<any>("/dispatch", {
      baseURL: api,
      method: "POST",
      body: { manifest: manifest.value }
    })
    respText.value = JSON.stringify(res, null, 2)
  } catch (e: any) {
    const msg = typeof e?.data === "string" ? e.data : (e?.message ? String(e.message) : "error")
    respText.value = msg
  } finally {
    sending.value = false
  }
}
</script>

<style scoped>
.wrap { max-width: 920px; margin: 24px auto; padding: 8px 12px; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; }
h1 { font-size: 24px; margin: 0 0 8px 0; }
h2 { font-size: 18px; margin: 0 0 8px 0; }
.card { border: 1px solid #ddd; border-radius: 8px; padding: 12px; margin-bottom: 12px; }
.row { display: flex; gap: 8px; align-items: center; margin-bottom: 8px; flex-wrap: wrap; }
label { min-width: 90px; }
input, select { padding: 6px 8px; border: 1px solid #ccc; border-radius: 6px; min-width: 200px; }
button { padding: 6px 10px; border: 1px solid #888; border-radius: 6px; background: #f7f7f7; cursor: pointer; }
button:disabled { opacity: 0.6; cursor: not-allowed; }
ul { padding-left: 18px; }
li { margin: 4px 0; display: flex; gap: 8px; align-items: center; }
textarea { width: 100%; min-height: 180px; padding: 8px; border: 1px solid #ccc; border-radius: 6px; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 13px; }
code { background: #f2f2f2; padding: 2px 6px; border-radius: 4px; }
span { opacity: 0.75; }
.hint { opacity: 0.7; font-size: 12px; }
</style>
