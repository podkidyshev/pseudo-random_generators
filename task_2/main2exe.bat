pyinstaller main.spec --onefile
move .\dist\distribs.exe .\
rd /S /Q .\build
rd /S /Q .\dist