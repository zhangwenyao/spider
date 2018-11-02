infile=ARG1
set xdata time
set timefmt "%Y%m%d"
set xtics format "%Y-%m" time
set xrange ["20170601":"20181201"]
set xtics "20170701",60*60*24*91
#set xtics ("201704", "201707", "2017010", "201801", "201804", "201807")
#set mxtics 31
set yrange [8e6:4.5e7]
#set ytics (5e6,1e7,2e7,3e7)
#set mytics 5
plot infile u 1:2 w l lt 3 lw 3 t "rankStar/user/day"
