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



import functools
import signal
from typing import Any, Callable, Iterable, TypeVar, overload

A = TypeVar('A')
F = TypeVar('F', bound=Callable[..., Any])

class Missing: ...
MISSING = Missing()

class InterruptHandler:
  def __init__(self):
    self.interrupt = False
    self.current_handler = None

  def _interrupt_handler(self, sig, frame):
    self.interrupt = True
  
  def __enter__(self):
    self.interrupt = False
    self.current_handler = signal.signal(signal.SIGINT, self._interrupt_handler)
    return self
  
  def __exit__(self, *args):
    signal.signal(signal.SIGINT, self.current_handler)
    self.current_handler = None
    self.interrupt = False

  def __del__(self):
    if self.current_handler:
      signal.signal(signal.SIGINT, self.current_handler)

  def __call__(self, f: F) -> F:
    @functools.wraps(f)
    def stop_iter_wrapper(*args, **kwargs):
      with self:
        return f(*args, **kwargs)
    return stop_iter_wrapper # type: ignore
  
  def stop_iter(self, iterable: Iterable[A], /):
    with self:
      for elem in iterable:
        if self.interrupt:
            break
        yield elem
        if self.interrupt:
            break

@overload
def stop_iter() -> InterruptHandler: ...
@overload
def stop_iter(iterable: Iterable[A], /) -> Iterable[A]: ...
def stop_iter(iterable: Iterable[A] | Missing = MISSING, /) -> Iterable[A] | InterruptHandler:
  interrupt_handler = InterruptHandler()

  if isinstance(iterable, Missing):
    return interrupt_handler
  else:
    return interrupt_handler.stop_iter(iterable)
    
  
__version__ = "0.2.5"

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

  with stop_iter() as it:
    for n in slow_integers():
      if it.interrupt:
        break
      print(n)
    
  print("\ninfinity")

  @(it := stop_iter())
  def print_slow_integers():
    for n in slow_integers():
      if it.interrupt:
        break
      print(n)

  print_slow_integers()
  print("\ninfinity")

