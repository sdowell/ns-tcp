if {$argc != 2} {
  puts "Expected args: -TCP proto- -Queue proto-"
  exit 1
}
set tcp [lindex $argv 0]
set queue [lindex $argv 1]
puts "TCP: $tcp"
puts "Queue: $queue"

#Create a simulator object
set ns [new Simulator]

#Open the nam trace file
set nf [open $tcp.$queue.out w]
$ns namtrace-all $nf

#Define a 'finish' procedure
proc finish {} {
        global ns nf tcp queue
        $ns flush-trace
	#Close the trace file
        close $nf
	#Execute nam on the trace file
        exec nam $tcp.$queue.out &
        exit 0
}

#Create two nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

#Create a duplex link between the nodes
$ns duplex-link $n1 $n2 10Mb 1ms $queue
$ns duplex-link $n5 $n2 10Mb 1ms $queue
$ns duplex-link $n2 $n3 1.5Mb 1ms $queue
$ns duplex-link $n3 $n4 10Mb 1ms $queue
$ns duplex-link $n3 $n6 10Mb 1ms $queue

#Re-Orient nodes
$ns duplex-link-op $n1 $n2 orient right-down      
$ns duplex-link-op $n5 $n2 orient right-up 
$ns duplex-link-op $n2 $n3 orient right 
$ns duplex-link-op $n3 $n4 orient right-up 
$ns duplex-link-op $n3 $n6 orient right-down

#Create a UDP agent and attach it to node n5
set udp0 [new Agent/UDP]
$ns attach-agent $n5 $udp0

#Create a TCP agent and attach it to node n1
set tcp1 [new Agent/TCP/$tcp]
$tcp1 set fid_ 1
if {$tcp == "Sack1"} {
  puts "TCP/Sack1, using Sack1 sink"
  set sink1 [new Agent/TCPSink/Sack1]
} else {
  set sink1 [new Agent/TCPSink]
}
$ns attach-agent $n1 $tcp1
$ns attach-agent $n4 $sink1
$ns connect $tcp1 $sink1
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ns at 0.5 "$ftp1 start"
$ns at 5.5 "$ftp1 stop"


# Create a CBR traffic source and attach it to udp0
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 500
$cbr0 set interval_ 0.004
$cbr0 attach-agent $udp0

#Create a Null agent (a traffic sink) and attach it to node n6
set null0 [new Agent/Null]
$ns attach-agent $n6 $null0

#Connect the traffic source with the traffic sink
$ns connect $udp0 $null0 

#Schedule events for the CBR agent
$ns at 1.5 "$cbr0 start"
$ns at 5.5 "$cbr0 stop"
#Call the finish procedure after 5 seconds of simulation time
$ns at 6.0 "finish"

#Run the simulation
$ns run
