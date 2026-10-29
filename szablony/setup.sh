#!/usr/bin/env bash
# Pobiera fonty (Inter, Roboto) do szablony/fonts – raz na sesję.
set -e
cd "$(dirname "$0")"
mkdir -p fonts && cd fonts
for p in inter@5.0.18 roboto@5.0.13; do
  n=${p%@*}
  [ -d "$n" ] && continue
  npm pack "@fontsource/$p" >/dev/null 2>&1
  mkdir -p tmp && tar xzf fontsource-${n}-*.tgz -C tmp && mv tmp/package "$n" && rm -rf tmp fontsource-${n}-*.tgz
done
echo "fonty gotowe: $(ls)"
