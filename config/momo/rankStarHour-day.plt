infile=ARG1
set xdata time
set timefmt "%Y%m%d"
set xtics format "%m/%d" time
#set xrange ["201410":"201706"]
set xtics "20170609",3600*24*14
#set xtics ("201501", "201507", "201601", "201607", "201701", "201707")
set mxtics 14
#set yrange [0:2e7]
set yrange [4e6:1e7]
set ytics 0,5e6,2e7
set mytics 5
plot infile u 1:2 w lp pt 5 t "rankStar/user/day"
