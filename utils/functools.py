import logging

try:
    from functools import cached_property
except ImportError:
    from threading import RLock
    from typing import Any, Optional

    _NOT_FOUND = object()

    class cached_property:  # noqa: E303
        def __init__(self, func: Any):
            self.func = func
            self.attrname: Optional[str] = None
            self.__doc__ = func.__doc__
            self.lock = RLock()

        def __set_name__(self, owner: Any, name: str) -> None:
            if self.attrname is None:
                self.attrname = name
            elif name != self.attrname:
                raise TypeError(
                    f"Cannot assign the same cached_property to two different names ({self.attrname!r} and {name!r})."
                )

        def __get__(self, instance: Any, owner: Any = None) -> Any:
            if instance is None:
                return self
            if self.attrname is None:
                raise TypeError("Cannot use cached_property instance without calling __set_name__ on it.")
            try:
                cache = instance.__dict__
            except AttributeError:
                msg = f"No '__dict__' attribute on {type(instance).__name__!r} instance to cache {self.attrname!r} property."
                logging.error(msg)  # 记录错误日志
                raise TypeError(msg) from None
            val = cache.get(self.attrname, _NOT_FOUND)
            if val is _NOT_FOUND:
                with self.lock:
                    # check if another thread filled cache while we awaited lock
                    val = cache.get(self.attrname, _NOT_FOUND)
                    if val is _NOT_FOUND:
                        val = self.func(instance)
                        try:
                            cache[self.attrname] = val
                        except TypeError:
                            msg = (
                                f"The '__dict__' attribute on {type(instance).__name__!r} instance "
                                f"does not support item assignment for caching {self.attrname!r} property."
                            )
                            logging.error(msg)  # 记录错误日志
                            raise TypeError(msg) from None
            return val

# 新增的日志设置
logging.basicConfig(
    filename='app.log',  # 日志文件名称
    filemode='a',  # 'a'表示追加模式写入
    level=logging.INFO,  # 记录INFO级别及以上的信息
    format='%(asctime)s - %(levelname)s - %(message)s'  # 日志格式
)

# 示例日志记录调用
logging.info("functools.py 模块已加载")
