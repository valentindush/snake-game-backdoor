from cx_Freeze import setup, Executable

setup(
    name="SNAKE GAME",
    version="1.0",
    description="Snake game made with pygame",
    executables=[Executable("main.py")]
)