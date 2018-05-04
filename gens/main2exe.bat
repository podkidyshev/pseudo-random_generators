pyinstaller main.spec --onefile
move .\dist\generators.exe .\
rd /S /Q .\build
rd /S /Q .\dist