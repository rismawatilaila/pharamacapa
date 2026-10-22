#!/bin/bash
# PharmaCAPA AI - Local Server Launcher
PORT=3000

echo "=========================================================="
echo "  PharmaCAPA AI — Pharmaceutical Deviation & CAPA Copilot"
echo "  Standar CPOB 2018/2024 & ICH Q9/Q10"
echo "=========================================================="
echo "Starting local web server at http://localhost:$PORT ..."

# Check if port 3000 is occupied, if so increment
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    PORT=3001
fi

echo "Access the application in your browser at: http://localhost:$PORT"
python3 -m http.server $PORT
