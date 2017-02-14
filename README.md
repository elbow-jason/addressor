## Usage

```python

>>> from addressor import (generate_pipe, predict)
>>> pipe = generate_pipe()
>>> stuff = [
...     "123 Maple Street San Francisco, California 85555",
...     "Mary Check it out",
...     "1000 dollar bills for 10 people",
...     "First Name Ryan, Last Name BirkishBurstBleck",
...     "17333 N Scottsdale Rd. Scottsdale, AZ 85053",
...     "FIZZ BUZZ THE OUTTA THE WORK",
...     "!23112123123123132",
...     "'asjdfkhasdf9asdfasd|||||||",
...     "123 Maple Rd.",
...     "12 Buckle Your Shoe, 34 Lock the door, 56 pick up sticks"
... ]

>>> predict(pipe, stuff)
['address',
 'not_address',
 'not_address',
 'not_address',
 'address',
 'not_address',
 'not_address',
 'not_address',
 'address',
 'not_address']

```
