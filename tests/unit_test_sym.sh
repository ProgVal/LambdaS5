#!/bin/bash
if [ $# -eq 1 ]; then
   ../bin/js ../tests/json_print.js $1 >> $1.ast
   ocamlrun ../obj/s5.d.byte -desugar ../tests/$1.ast -print es5 \
       -env ../envs/es5.env -json ../src/desugar.sh -sym-eval
   rm $1.ast
else
   echo "usage: unit_test_sym.sh <filepath>"
fi
