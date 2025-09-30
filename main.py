import os

import Path

file = Path(r"D:\Videos\ShortPathTest\02_general-implementation-of-forward-propagation.mp4")
short_path = win32api.GetShortPathName(str(file))
print(short_path)  # Should now return something like D:\Videos\SHORTP~1\...
