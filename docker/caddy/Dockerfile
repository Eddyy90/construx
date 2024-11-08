FROM caddy:builder AS builder

RUN xcaddy build --with github.com/caddy-dns/route53

FROM caddy:latest

COPY Caddyfile /etc/caddy/Caddyfile

COPY --from=builder /usr/bin/caddy /usr/bin/caddy