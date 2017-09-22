infile=ARG1
set xdata time
set timefmt "%Y%m%d"
set xtics format "%m/%d" time
#set xrange ["201410":"201706"]
set xtics "20170102",3600*24*7
#set xtics ("201501", "201507", "201601", "201607", "201701", "201707")
#set mxtics 6
set logscale y
plot infile u 1:2 w lp pt 5 t "star day mean"
