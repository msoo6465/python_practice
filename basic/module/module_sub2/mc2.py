# mc2.py
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.abspath('../module_sub1'))
try:
    import mb1
except Exception as e:
    print(e)
try:
    import mb2
except Exception as e:
    print(e)
try:
    import mc1
except Exception as e:
    print(e)
try:
    import ma1
except Exception as e:
    print(e)
try:
    import ma2
except Exception as e:
    print(e)

print('Here is mc2')