from celery.result import AsyncResult
from tasks import app
import sys
import os

def main(argv):
    if len(argv) == 2 and len(argv[1]) == 36:
        res = AsyncResult(argv[1], app=app)
        print(res.get())
    else:
        print('No id to get result!')


if __name__ == "__main__":
    main(sys.argv)