from time import sleep
from sys import platform
from random import randint
import signal

from client.comm import Comm
from module.cli_controller import CLIController

should_stop = False

def main():
    module = CLIController(Comm(), ["modules/swarm_ui/module/commands.json"])

    while not should_stop and not module.stopped:
        module.process()
        sleep(0.05)

    module.stop()


def stop(signal, frame):
    global should_stop
    should_stop = True


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

if platform != "win32":
    signal.signal(signal.SIGQUIT, stop)

if __name__ == "__main__":
    main()
