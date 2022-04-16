#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

evalsys_build() {  
   docker build -t evalsys_dev "$SCRIPT_DIR"
}

evalsys_run() {  
   docker run -d --name=evalsys_dev evalsys_dev tail -f /dev/null
 >/dev/null
}

evalsys_start() {  
    evalsys_run "$@"
}

evalsys_stop() {  
    docker stop evalsys_dev >/dev/null
    docker rm evalsys_dev >/dev/null
}

evalsys_restart() {
    evalsys_stop 2>/dev/null
    evalsys_run
}

evalsys_attach() {  
   docker exec -ti evalsys_dev bash
}

evalsys_init() {  
    evalsys_update "$@"
}

evalsys_update() {
    docker exec -ti evalsys_dev git clone https://github.com/evyli/evalsys.git || true
    docker exec -ti evalsys_dev bash -c "cd evalsys; git reset --hard"
    docker exec -ti evalsys_dev bash -c "cd evalsys; git pull"
    docker exec -ti evalsys_dev bash -c "cd evalsys; pip install -e ."
}

evalsys_test() {  
    docker exec -ti evalsys_dev bash -c "cd evalsys; python setup.py test"
}

CMD="$1"
shift 1
"evalsys_$CMD" "$@"