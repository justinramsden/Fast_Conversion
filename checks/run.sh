#!/bin/sh
# Runs the engine tests and every browser check against this repo. Usage: sh checks/run.sh
# Needs: node, python3 with playwright, and Chrome at /usr/bin/google-chrome (edit executable_path in the scripts if elsewhere).
# Screenshots the checks take go to a temporary folder, printed at the end.
repo=$(cd "$(dirname "$0")/.." && pwd); here="$repo/checks"; work=$(mktemp -d); cd "$work" || exit 1
node "$repo/tests.js" | tail -1
python3 "$here/gzserve.py" "$repo" 8780 >/dev/null 2>&1 & server=$!
trap 'kill $server 2>/dev/null' EXIT; sleep 1
echo "== pad (keypad, 375x629 touch)"; python3 "$here/pad.py" | grep -v '^ok' | tail -8
echo "== keytime (budget: under 10 ms)"; python3 "$here/keytime.py"
for t in custom sug keys tips share qr ruler desk; do echo "== $t"; python3 "$here/$t.py" "$repo/index.html" 2>&1 | grep -v '^ok' | tail -3; done
echo "screenshots in $work"
