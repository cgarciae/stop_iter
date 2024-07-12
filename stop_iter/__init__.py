# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



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
      if interrupt:
          break

  finally:
    signal.signal(signal.SIGINT, current_handler)
    
  
__version__ = "0.2.4"

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

