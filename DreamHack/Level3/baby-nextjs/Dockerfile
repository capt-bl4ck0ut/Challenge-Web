FROM node:20-alpine@sha256:1a526b97cace6b4006256570efa1a29cd1fe4b96a5301f8d48e87c5139438a45 AS base


FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY ./src/package.json ./src/package-lock.json ./
RUN npm ci


FROM base AS builder
ENV NEXT_TELEMETRY_DISABLED=1

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY ./src ./
RUN npm run build


FROM base AS runner
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

WORKDIR /app

RUN mkdir .next
RUN chown nextjs:nodejs .next

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

COPY ./flag.txt /

USER nextjs

EXPOSE 8000

ENV PORT=8000
ENV HOSTNAME="0.0.0.0"
CMD ["node", "server.js"]
