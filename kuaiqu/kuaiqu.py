# -*- coding: UTF-8 -*-
import itertools
from collections import OrderedDict
from datetime import datetime, timedelta


class Kuaiqu(object):

    def __init__(self, maxsize=50, hysteresis=10, rolling=None, expiration=None, **kwargs):
        """

        :param maxsize: the maximum number of items in the cache
        :param hysteresis: the number of oldest items to remove when cache overflows
        :param rolling: the number of minutes to wait between accesses before expiring, or None
        :param expiration: the maximum number of minutes an obj can exist in the cache, else no expiration if None
        :param kwargs:
        """

        self.cache = OrderedDict(**kwargs)

        # set length bounds
        self.upper_bound = maxsize
        self.lower_bound = maxsize - hysteresis

        # set object expiration
        self.rolling = timedelta(minutes=rolling) if rolling else None
        self.expiration = timedelta(minutes=expiration) if expiration else None

    def __len__(self):
        """
        Return the number of items in the cache.

        May include expired items

        :return:
        """
        return len(self.cache)

    def __contains__(self, key):
        """
        Return True if key in cache.

        Key may have expired.

        :param key:
        :return:
        """
        return key in self.cache

    def __iter__(self):
        """
        Return an iterator over (key, value) pairs stored in the cache.

        May include expired items
        :return:
        """
        return self.items()

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, key):
        return self.get(key)

    def __delitem__(self, key):
        self.delete(key)

    def keys(self):
        """
        Return keys in the cache

        :return:
        """
        return self.cache.keys()

    def items(self):
        """
        Return an iterator over (key, val) pairs in the cache

        :return:
        """
        return (
            (key, obj)
            for key, (rolling, expiration, obj) in self.cache.items()
        )

    def pop(self, key):
        """
        Remove and return key from cache

        :param key:
        :return: Value stored under key, else None if key doesnt exist
        """

        (_, _, obj) = self.cache.pop(key, (None, None, None))

        return obj

    def popitem(self, last=True):
        """
        Pop an item and return it directly

        Item may have expired.

        :param last: Return the first or last item. Default last.
        :return:
        """

        key, (rolling, expiration, obj) = self.cache.popitem(last=last)

        return key, obj

    def set(self, key, obj):
        """
        Store obj under key, with optional expiration.

        :param key:
        :param obj:
        :return:
        """

        rolling = datetime.utcnow() + self.rolling if self.rolling else None

        # if this key is already in the dict remove it
        if key in self.cache:

            _, expiration, _ = self.cache[key]

            self.delete(key)

            # assign the packed value
            self.cache[key] = (rolling, expiration, obj)

        else:

            expiration = datetime.utcnow() + self.expiration if self.expiration else None

            # assign the packed value
            self.cache[key] = (rolling, expiration, obj)

            if len(self.cache) > self.upper_bound:
                # want to keep unexpired items in the cache as long as possible
                # if cache to big first remove expired items
                # if still too big, then trim back to lower_bound
                self.prune(expired=True, length=True)

    def get(self, key):
        """
        Retrieve an item from the cache

        :param key: the key to retrieve
        :return: the value stored under key, else None if it doesnt exist or has expired
        """

        # retrieve the packed value
        rolling, expiration, obj = self.cache.get(key) or (None, None, None)

        # print(rolling, expiration, obj)

        if any(limit is not None and limit <= datetime.utcnow() for limit in (rolling, expiration)):

            # key expired, so remove it
            self.delete(key)

            # clear out all expired items whenever I find a single expired item
            self.prune(expired=True, length=False)

            return None

        return obj

    def _prune_length(self):
        """
        Prune cache size down to lower bound

        :return: None
        """

        deletes = {
            key
            for key, (_, _, _) in itertools.islice(self.cache.items(), self.lower_bound)
        }

        for key in deletes:
            self.delete(key)

    def _prune_expired(self):
        """
        Remove any expired items from the cache

        :return: None
        """

        # execute in two passes so I dont alter the cache as I iterate it

        # first get a set of expired keys
        deletes = {
            key
            for key, (rolling, expiration, obj) in self.cache.items()
            if any(limit is not None and limit <= datetime.utcnow() for limit in (rolling, expiration))
        }

        # now delete them
        for key in deletes:
            self.delete(key)

    def prune(self, expired=True, length=True):
        """
        Remove items from the cache.

        Remove expired items first, then only remove unexpired items if there are too many of them.

        :param expired:
        :param length:
        :return:
        """
        if expired:
            self._prune_expired()

        if length:
            self._prune_length()

    def delete(self, key):
        """
        Delete key from cache

        :param key:
        :return: None
        """
        self.cache.pop(key, None)

    def clear(self):
        """
        Remove all items from the cache
        :return:
        """
        self.cache.clear()


