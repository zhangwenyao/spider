infile=ARG1
set xdata time
set timefmt "%Y%m"
set xtics format "%Y/%m" time
#set xrange ["201410":"201706"]
set xtics "201501",3600*24*183,"201712"
#set xtics ("201501", "201507", "201601", "201607", "201701", "201707")
set mxtics 6
plot infile u 1:2 w lp pt 5 t "rank all"
