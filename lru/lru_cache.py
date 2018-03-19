from collections import namedtuple
from collections import OrderedDict
import time


class simple_lru_cache(object):  # pylint: disable=invalid-name
  """Decorator for cache similar to LRU. Works only on global functions.

  LRU stands for Least Recently Used. This is a cache which remembers
  the arguments a function was called with and the result it returned.
  It assumes that given the same arguments the function will always
  return the same result.
  For the time being this decorator can only be applied to static functions
  and class functions, but not on instance functions.

  Important: The cache key is generated from the function arguments,
  the arguments are first turned to their str representations and then
  concatinated. For this reason you should again be mindful when decorating
  functions with this cache. When creating the key the value and the type
  of arguments is considered.

  """

  _CachedResult = namedtuple('CachedResult', ['result', 'time'])

  def __init__(self, maxsize=255, timeout=60):
    self._maxsize = maxsize
    self._timeout = timeout
    self._cached_results = OrderedDict()

  @staticmethod
  def _calculate_cache_key(args, kwargs):
    args_hash = u' '.join(
      [str(arg) + str(type(arg)) for arg in args]
    )
    kwargs_hash = u' '.join(
      [str(kwargs[key]) + str(type(kwargs[key])) for key in kwargs]
    )
    return args_hash + kwargs_hash

  def __getitem__(self, key):
    result, valid_until = self._cached_results.get(key, (None, None))
    if result is None:
      return None
    if valid_until < time.time():
      # print("timed-out")
      return None
    return result

  def __setitem__(self, key, value):
    cached_result = self._CachedResult(value, time.time() + self._timeout)
    self._cached_results[key] = cached_result
    if len(self._cached_results) > self._maxsize:
      # print("popitem")
      self._cached_results.popitem(False)

  def __call__(self, func, *args, **kwargs):
    def run_func_and_remember_result(*args, **kwargs):
      key = self._calculate_cache_key(args, kwargs)
      cached_result = self[key]
      if cached_result:
        # print("found :)")
        return cached_result

      result = func(*args)
      self[key] = result
      return result
    return run_func_and_remember_result
