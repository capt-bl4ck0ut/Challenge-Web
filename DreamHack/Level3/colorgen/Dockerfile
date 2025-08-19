FROM node:20-alpine
LABEL author=winky

WORKDIR /app

COPY app .
COPY flag.txt /

RUN apk add --no-cache gcc musl-dev shadow \
    && npm i \
    && useradd -m winky \
    && printf '#include <unistd.h>\n#include <stdlib.h>\nint main(){setreuid(0, 0); system("cat /flag.txt"); return 0;}\n' > /tmp/a.c \
    && gcc /tmp/a.c -o /readflag \
    && chown root:root /readflag \
    && chmod 4755 /readflag \
    && chmod 400 /flag.txt \
    && chown root:root /flag.txt

USER winky
CMD ["node", "app.js"]
