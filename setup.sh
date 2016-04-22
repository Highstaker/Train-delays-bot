#!/bin/bash

INTERPRETER_NAME="train_delays_bot_python3"

# Go to script's folder
cd `dirname $0`

mkdir databases

mkdir tokens
touch tokens/token

#create environment
virtualenv env
# install dependencies
env/bin/python3 env/bin/pip3 install -r requirements.txt
# create a better-named python interpreter link
ln -s env/bin/python3 ${INTERPRETER_NAME}

#create a run file
echo "#!/bin/bash

_term() {
echo "Caught termination signal!"
kill -TERM \"\$child\" 2>/dev/null
}

trap _term SIGTERM SIGINT

./train_delays_bot_python3 train_delays_bot_main.py &

child=\$!
wait \"\$child\"

exit 0
" > run.sh

chmod +x run.sh

exit 0