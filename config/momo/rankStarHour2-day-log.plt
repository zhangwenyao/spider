infile=ARG1
set xdata time
set timefmt "%Y%m%d"
set xtics format "%Y-%d" time
set xrange ["20170601":"20181201"]
set xtics "20170701",60*60*24*91
#set xtics ("201501", "201507", "201601", "201607", "201701", "201707")
#set mxtics 31
set logscale y
set yrange [9e6:1e8]
#set ytics (1e7,2e7, 3e7, "" 5e7, 1e8)
#set mytics 2
plot infile u 1:2 w l lt 3 lw 3 t "rankStar/user/day"
