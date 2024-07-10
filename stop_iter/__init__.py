

import signal
from typing import Iterable, TypeVar

A = TypeVar('A')

def stop_iter(iterable: Iterable[A], /):

  interrupt = False
  def _interrupt_handler(sig, frame):
    nonlocal interrupt
    interrupt = True
  current_handler = signal.signal(signal.SIGINT, _interrupt_handler)

  try:
    for elem in iterable:
      if interrupt:
          break
      yield elem

  finally:
    signal.signal(signal.SIGINT, current_handler)
    
  
__version__ = "0.0.0"

if __name__ == "__main__":
  import time

  def slow_integers():
    count = 0
    while True:
      yield (count := count + 1)
      time.sleep(1)

  for n in stop_iter(slow_integers()):
    print(n)
  print("\ninfinity")

