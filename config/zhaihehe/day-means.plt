infile=ARG1
set xdata time
set timefmt "%Y%m%d"
set xtics format "%m/%d" time
#set xrange ["201410":"201706"]
set xtics "20170101",3600*24*7
set xtics ("20170101", "20170201", "20170301", "20170401", "20170501", "20170601","20170701")
set mxtics 7
plot infile u 1:2 w lp pt 5 t "day mean"
