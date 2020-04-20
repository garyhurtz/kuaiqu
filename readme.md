# kuaiqu

Simple LRU cache

This more or less an OrderedDict that:

1. Stores items in the order they were most recently added, and
2. Removes as many of the least-recently updated (but not expired) items as necessary to reduce cache size to (maxsize - hysteresis)

Items in the cache expire when their age recahes the *expiration* limit, and also if they have not been accessed recently (i.e. "rolling" expiration).
 
# Use

Instantiate, then set and access values much like a python dict:

    >>> from kuaiqu import Kuaiqu
    
    >>> dut = Kuaiqu()

    >>> dut.set('hello', 'world')
    
    >>> dut.get('hello')
    'world' 
    
    >>> dut['hello']
    'world'

Configuration can be passed to the constructor:

* *maxsize* is the maximum number of items that can be stored in the cache.
* *hysteresis* is the number of items to remove when the cache gets trimmed. Items are removed according to their age (oldest items first).
* *rolling* is the maximum number of minutes that are allowed between object retrievals before the object expires.
* *expiration* is the maximum number of minutes that an object can exist in the cache, else None for no expiration.

Additional kwargs that are passed to the constructor will be passed to the cache as initial data.
 

# Methods

## keys()

Return the keys in the cache, as an OrderedDictKeysView.

## items()

Return (key, value) pairs for items in the cache, as an OrderedDictItemsView.

## set(key, value)

Add an object to the cache

## get(key)

Get an item from the cache, and update the *rolling* expiration. Also supports dictionary access.

## pop(key)

Pop an item from the cache and return the value.

## popitem()

Pop a random item from the cache and return it as a (key, value) pair.

## delete(key)

Delete an item from the cache

## prune(expired=True, length=True)

Remove items from the cache, using one or both of the *expired* and *length* strategies.

## clear

Clear all items from the cache.

# Operators and Functions

## len(instance)

Return the number of items in the cache. Note that this counts all (both expired and unexpired) items so may not provide the expected result in some cases.

## iter(instance)

Alternate call to *items()*.

## [key] in [instance]

Return True if the specified key is in the specified instance, else None. Does not consider where the object has expired.

## *arg and **kwargs expansion

Items in the cache can be passed to a function using either *arg or **kwarg notation.
