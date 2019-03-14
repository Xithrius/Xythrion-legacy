if [ "$(uname)" == 'Darwin' ]; then
          echo "Your platform ($(uname -a)) is not supported."
          exit 1
fi

python bot.py
