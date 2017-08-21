infile=ARG1
set xdata time
set timefmt "%Y%m%d-%H%M"
set xtics format "%m%d" time
#set xrange ["201410":"201706"]
set xtics "20170609-0000",3600*24*7
#set xtics ("201501", "201507", "201601", "201607", "201701", "201707")
set mxtics 7
set yrange [3e6:1e7]
#set logscale y
plot infile u 1:2 w lp pt 5 t "rankStar/user/hour"
