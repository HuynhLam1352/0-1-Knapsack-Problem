mkdir Build
cd Build
pyinstaller --onefile --windowed --clean --name GUI ../main.py
rm -r ./build
rm ./GUI.spec