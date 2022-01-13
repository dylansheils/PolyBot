from subprocess import call
import time
import sched, time
s = sched.scheduler(time.time, time.sleep)
def do_something(sc):
    print("Running...")
    call(["python", "main.py"])
    s.enter(10, 1, do_something, (sc,))

s.enter(10, 1, do_something, (s,))
s.run()