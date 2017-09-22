infile=ARG1
set xdata time
set timefmt "%Y%m%d"
set xtics format "%m/%d" time
#set xrange ["201410":"201706"]
set xtics "20170102",3600*24*14
#set xtics ("201501", "201507", "201601", "201607", "201701", "201707")
set mxtics 14
set logscale y
set yrange [4e6:1e7]
set ytics (3e6,"" 4e6, 5e6,"" 6e6,"" 7e6,"" 8e6,"" 9e6,1e7,2e7)
#set mytics 2
plot infile u 1:2 w lp pt 5 t "rankStar/user/day"
