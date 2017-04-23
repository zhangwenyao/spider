#!/bin/bash

dates=(20160101 20160401 20160701 20161001)
lists=(0 1 2 3 4 5 6 7 8 9 \
  10 11 12 13 15 16 17 18 19 \
  20 21 22 23 24 25 26 27 28 29 \
  30 31 32 33 34 35 36 37 38 39 \
  40 41 42 43 \
  52 53 54 55 56 57 \
  64 65 66 67 68 69 \
  70 71 72 73 74 75 76 77 78 79 \
  80 81 82 83 84 85 86 87 88 89 \
  90 91 92 93 94 95 96 97 98 99 \
  100 101 102 103 104 105 106 107 108 109 \
  110 111 112 113 114 115 116 117 118 119 \
  120 121 122 123 124 125 126 127 128 129 \
  130 131 132 133 134 135 136 137 138 139 \
  140 141 142 143 144 145 146 147 148 149 \
  150 151 152 153 154 155 156 157 158 \
  201 202 203 204 205 206 207 208 209\
  210 211 212 213 214 215 216 217 218 219 \
  220 221 222 223 224 225 226 227 228 229)
for d in ${dates[@]}; do
  for l in ${lists[@]} ; do
    echo python3 live.py --web talkingdata --type apprank --list $l --dateType q --rankType a --date $d
    python3 live.py --web talkingdata --type apprank --list $l --dateType q --rankType a --date $d
    echo python3 live.py --web talkingdata --type apprank --list $l --dateType q --rankType g --date $d
    python3 live.py --web talkingdata --type apprank --list $l --dateType q --rankType g --date $d
    echo python3 live.py --web talkingdata --type apprank --list $l --dateType q --rankType r --date $d
    python3 live.py --web talkingdata --type apprank --list $l --dateType q --rankType r --date $d
  done
done
