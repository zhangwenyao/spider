infile=ARG1
set xdata time
set timefmt "%Y%m%d-%H%M"
set xtics format "%m/%d" time
set xtics "20170616-0000",3600*24*7
#set mxtics 7
plot infile u 1:2 w lp pt 5 t "receiver week"
