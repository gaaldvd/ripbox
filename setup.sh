echo "> Setting up pipenv..."
pipenv sync
echo "> Configuring privileges..."
chmod +x ripbox.sh
chmod +x update.sh

echo "> Done. Goodbye!"
