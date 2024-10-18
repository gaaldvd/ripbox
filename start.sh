if [ "$#" -eq 0 ]
  then
    echo "> Usage: $0 [-c/-g]"
    exit 1
fi

while getopts "cg" flag; do
  case $flag in
    c) mode="cli";;
    g) mode="gui";;
    *)
      echo "> Usage: $0 [-c/-g] [-a author] [-t title]"
      exit 1;;
  esac
done

echo "> Setting up application..."
echo "  Mode: $mode"
pipenv run python ripbox_$mode.py
