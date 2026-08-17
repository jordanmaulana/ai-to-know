# --- build stage: vite build -> /app/dist ---
FROM node:20-alpine AS build
WORKDIR /app
# pnpm@10.15.0 is pinned in package.json "packageManager"; corepack honours it.
RUN corepack enable
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY . .
# VITE_* are inlined into the bundle at build time (see src/lib/api.ts), so they belong here,
# not in the runtime stage. Declared after the install so changing a URL keeps the deps layer.
ARG VITE_API_URL
ARG VITE_GOOGLE_CLIENT_ID
ENV VITE_API_URL=$VITE_API_URL \
    VITE_GOOGLE_CLIENT_ID=$VITE_GOOGLE_CLIENT_ID
RUN pnpm run build

# --- serve stage: static files behind nginx ---
FROM nginx:alpine AS serve
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 3000
