#!/bin/bash

python test262/test262/tools/test262.py \
  --command ./s5-test262 \
  --tests test262/test262/ \
  --full-summary \
  --threads 6
  
