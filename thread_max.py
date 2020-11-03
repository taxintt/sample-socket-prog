#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading

def loop():
    while True:
        time.sleep(1)

def main():
    for _ in range(10000):
        t = threading.Thread(target=loop)
        t.daemon = True
        t.start()

        print(threading.active_count())

if __name__ == "__main__":
    main()