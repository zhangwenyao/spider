infile=ARG1
set xdata time
set timefmt "%Y%m%d"
set xtics format "%y/%m" time
#set xrange ["201410":"201706"]
#set xtics "20170101",3600*24*7
set xtics ("20161001","20161101","20161201","20170101","20170201","20170301","20170401","20170501","20170601","20170701")
#set mxtics 7
set ylabel "top20 / 10^4"
set yrange [0:350]
set ytics nomirror
set y2label "top10000 / 10^8"
set y2tics
set y2range [0:4.5]
plot	infile u 1:($2/100/10000) w lp pt 5 axis x1y1 t "top20", \
		infile u 1:($5) w lp pt 5 axis x1y2 t "top10000"
