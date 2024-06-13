@echo off
REM Guarda la ruta actual
set "CURRENT_DIR=%~dp0"

REM Activa el entorno virtual
call "%CURRENT_DIR%venv\Scripts\activate.bat"

REM Ejecuta el script main.py
python "%CURRENT_DIR%main.py"

pause