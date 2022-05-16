from io import StringIO
import sys


s = StringIO()

for i in range(0, 5):
    print("BONJOUR", file=s)
    result_string = s.getvalue()
    s = StringIO()
    print(result_string)