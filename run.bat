title "ArrowRoot (WSL 100) Server (DO NOT CLOSE)"
python --version
python -c "from qil_santec import WSL_TCP;WSL_server = WSL_TCP.cWSLServer(silent=False);WSL_server.run()"
pause