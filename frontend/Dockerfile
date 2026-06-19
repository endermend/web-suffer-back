FROM node:24-slim AS base
WORKDIR /app

FROM base AS deps
COPY package.json package-lock.json* ./
RUN --mount=type=cache,target=/root/.npm \
    npm install --only=production --legacy-peer-deps

FROM base AS build
COPY package.json package-lock.json* ./
RUN --mount=type=cache,target=/root/.npm \
    npm install --legacy-peer-deps
COPY . .
RUN npm run build-only

FROM nginx:alpine AS production
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# dev: Vite's own dev server, kept alive for `docker compose watch` —
# file changes are synced in by compose, Vite's HMR picks them up from there.
# Runs on port 80 so it lands on the same host port as the production nginx
# stage (no separate :5173 to remember).
FROM base AS dev
COPY package.json package-lock.json* ./
RUN --mount=type=cache,target=/root/.npm \
    npm install --legacy-peer-deps
COPY . .
EXPOSE 80
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "80"]