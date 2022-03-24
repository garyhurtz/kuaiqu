# -*- coding: UTF-8 -*-
import itertools
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Any, Iterator, Optional, Set, Tuple


class Kuaiqu(object):
    """
    Simple cache.
    """

    def __init__(
        self,
        maxsize: int = 50,
        hysteresis: int = 10,
        rolling: Optional[int] = None,
        expiration: Optional[int] = None,
        **kwargs
    ) -> None:
        """

        Parameters:

        **maxsize**: int
            the maximum number of items in the cache

        **hysteresis**: int
            the number of oldest items to remove when cache overflows

        **rolling**: int, optional
            the number of minutes to wait between accesses before expiring, or None

        **expiration**: int, optional
            the maximum number of minutes an obj can exist in the cache, else no expiration if None

        **kwargs**:
            optional keyword args
        """

        self.cache: OrderedDict[
            str, Tuple[Optional[datetime], Optional[datetime], Any]
        ] = OrderedDict(**kwargs)
        """
        The actual cache.

        Values are stored in the cache as a 3-tuple of the form: (rolling, expiration, obj)
        """

        self.upper_bound: int = maxsize
        """
        The maximum number of items that can exist in the queue.
        """

        self.lower_bound: int = maxsize - hysteresis
        """
        The maximum number of items that will remain in the queue after trimming.
        """

        self.rolling: timedelta = timedelta(minutes=rolling) if rolling else None
        """
        The amount of time and object can exists between accesses.
        """

        self.expiration: timedelta = (
            timedelta(minutes=expiration) if expiration else None
        )
        """
        The maximum amount of time an object can exist within the cache
        """

    def __len__(self) -> int:
        """
        Returns:

            The number of items in the cache.

        *Note*: This is a raw count and may include expired items.
        """
        return len(self.cache)

    def __contains__(self, key: str) -> bool:
        """

        Parameters:

        **key**: str
            the key to check

        Returns:

            True if the specified key exists in the cache.

        *Note*: Although a key may exist, the object may have expired.
        """
        return key in self.cache

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        """
        Returns:

            An iterator over (key, value) pairs stored in the cache.

        *Note*: The resulting iterator may include expired items.
        """
        return self.items()

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Add an item to the cache.

        Parameters:

        **key**: str
            the key for referencing the value in the cache

        **value**: Any
            the object to store in the cache
        """
        self.set(key, value)

    def __getitem__(self, key: str) -> Any:
        """
        Get an item from the cache.

        Parameters:

        **key**: str
            the key for referencing the value in the cache

        Returns:

        The object stored in the cache.
        """
        return self.get(key)

    def __delitem__(self, key: str) -> None:
        """
        Delete an item from the cache.

        **key**: str
            the key for referencing the value in the cache
        """
        self.delete(key)

    def keys(self) -> Set[str]:
        """
        Returns:
            The set of keys in the cache
        """
        return self.cache.keys()

    def items(self) -> Iterator[tuple[str, Any]]:
        """
        Returns:

        An iterator over (key, val) pairs in the cache
        """
        return ((key, obj) for key, (rolling, expiration, obj) in self.cache.items())

    def pop(self, key: str) -> Any:
        """
        Remove and return key from cache

        Parameters:

        **key**: str
            the key for referencing the value in the cache

        Returns:

        The object stored under the specified key, else None if the key does
        not exist
        """

        (_, _, obj) = self.cache.pop(key, (None, None, None))

        return obj

    def popitem(self, last: bool = True) -> tuple[str, Any]:
        """
        Pop an item and return it directly

        Item may have expired.

        Returns:

        The first or last item. Default last.
        """

        key, (_, _, obj) = self.cache.popitem(last=last)

        return key, obj

    def set(self, key: str, obj: Any) -> None:
        """
        Store obj under key, with optional expiration.

        Parameters:

        **key**: str
            the key for referencing the value in the cache

        **obj**: str

        Returns:

        None.
        """

        # if this key is already in the cache get the existing expiration
        if key in self.cache:

            _, expiration, _ = self.cache[key]

        else:

            expiration = (
                datetime.utcnow() + self.expiration if self.expiration else None
            )

        rolling = datetime.utcnow() + self.rolling if self.rolling else None

        # assign the packed value
        self.cache[key] = (rolling, expiration, obj)

        if len(self.cache) > self.upper_bound:
            # want to keep unexpired items in the cache as long as possible
            # if cache too big first remove expired items
            # if still too big, then trim back to lower_bound
            self.prune(expired=True, length=True)

    def get(self, key: str) -> Any:
        """
        Retrieve an item from the cache

        Parameters:

        **key**: str
            the key for referencing the value in the cache

        Returns:

        The value stored under key, else None if it does not exist or has expired
        """

        # retrieve the packed value
        rolling, expiration, obj = self.cache.get(key) or (None, None, None)

        # print(rolling, expiration, obj)

        if any(
            limit is not None and limit <= datetime.utcnow()
            for limit in (rolling, expiration)
        ):

            # key expired, so remove it
            self.delete(key)

            # clear out all expired items whenever I find a single expired item
            self.prune(expired=True, length=False)

            return None

        return obj

    def _prune_length(self) -> None:
        """
        Prune cache size down to lower bound

        Returns:

        None
        """

        deletes = {
            key
            for key, (_, _, _) in itertools.islice(self.cache.items(), self.lower_bound)
        }

        for key in deletes:
            self.delete(key)

    def _prune_expired(self) -> None:
        """
        Remove any expired items from the cache

        Returns:

        None
        """

        # execute in two passes so I dont alter the cache as I iterate it

        # first get a set of expired keys
        deletes = {
            key
            for key, (rolling, expiration, obj) in self.cache.items()
            if any(
                limit is not None and limit <= datetime.utcnow()
                for limit in (rolling, expiration)
            )
        }

        # now delete them
        for key in deletes:
            self.delete(key)

    def prune(self, expired: bool = True, length: bool = True) -> None:
        """
        Remove items from the cache.

        Parameters:

        **expired**: bool
        If True remove all expired items from the cache.

        **length**: bool
        If True remove (possibly unexpired) items to ensure that no more than
        *lower_bound* items remain in the cache.

        Returns:

        None

        When both *expired* and *length* are true, expired items are removed
        first, then unexpired items are removed if needed to satisfy
        *lower_bound*.
        """
        if expired:
            self._prune_expired()

        if length:
            self._prune_length()

    def delete(self, key: str) -> None:
        """
        Delete key from cache

        Parameters:

        **key**: str
            the key that references the value in the cache

        Returns:

        None
        """
        self.cache.pop(key, None)

    def clear(self) -> None:
        """
        Remove all items from the cache

        Returns:

        None
        """
        self.cache.clear()
