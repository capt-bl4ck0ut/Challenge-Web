export default defineNuxtConfig({
  ssr: true,
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      apiBase: "/api",
    },
    apiBaseServer: "http://localhost:3000",
  },
  routeRules: {
    "/api/**": { proxy: "http://localhost:3000/**" },
  },
})
