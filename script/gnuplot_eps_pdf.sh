#!/bin/bash
#./gnuplot_eps_pdf.sh graph.plt outfile [\"data.txt\" ...]


if [ $# -lt 2 ];then
  echo "$0 'plt' 'name' [...]"
  exit 1
fi


#gnuplot
plt="$1"
outfile="$2"
shift
shift
gnuplot << EOF
set terminal push
set terminal pdfcairo color solid enh lw 2 font "Helvetica, 18"
set out "$outfile.pdf"
call "$plt" $@
set output
set terminal postscript eps color solid enh lw 1 font "Helvetica, 24"
set out "$outfile.eps"
call "$plt" $@
set output
set terminal pop
EOF

