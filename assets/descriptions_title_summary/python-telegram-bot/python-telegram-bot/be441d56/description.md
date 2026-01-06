# Remove `__dict__` from `__slots__` and drop Python 3.6

Major refactoring to improve memory efficiency and enforce stricter attribute management by removing `__dict__` from `__slots__` across all PTB classes. Also drops Python 3.6 support, setting minimum version to **3.7+**.