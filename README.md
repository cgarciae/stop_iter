# stop_iter

``stop_iter`` takes an iterable and returns a new iterable that can be safely stopped using ``SIGINT``. This is useful when you have a long-running computation, such as machine learning training loops, that you want to be able to stop without losing all of the work that has been done so far.

## Installation

```bash
pip install stop_iter
```

## Usage
The following code will print the integers until you press ``Ctrl+C`` and then print "infinity".

```python
from stop_iter import stop_iter

def integers():
  count = 0
  while True:
    yield (count := count + 1)

for n in stop_iter(integers()):
  print(n)

print("\ninfinity")
```
Also works as a context manager:
```python
with stop_iter() as it:
  for n in integers():
    print(n)
    if it.interrupt:
      break
```
And as a decorator:
```python
@(it := stop_iter())
def print_integers():
  for n in integers():
    print(n)
    if it.interrupt:
      break

print_integers()
```
