#!/usr/bin/env python3
import time, os

count = 0
print("Cache monitor starts...")
while(True):
  count += 5
  time.sleep(5)
  print(count, "seconds.")
  os.system("rndc dumpdb -cache && grep attacker /var/cache/bind/dump.db")
