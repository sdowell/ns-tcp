if {$argc != 1} {
  puts "Expected args: -Queue proto-"
  exit 1
}
set queue [lindex $argv 0]
puts "Queue: $queue"

#Create a simulator object
set ns [new Simulator]

#Open the nam trace file
set nf [open $queue.out w]
$ns namtrace-all $nf

#Define a 'finish' procedure
proc finish {} {
        global ns nf queue
        $ns flush-trace
	#Close the trace file
        close $nf
	#Execute nam on the trace file
        exec nam $queue.out &
        exit 0
}

#Create two nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]
set n7 [$ns node]
set n8 [$ns node]

#Create a duplex link between the nodes
$ns duplex-link $n1 $n2 10Mb 1ms $queue
$ns duplex-link $n5 $n2 10Mb 1ms $queue
$ns duplex-link $n2 $n3 1.5Mb 1ms $queue
$ns duplex-link $n3 $n4 10Mb 1ms $queue
$ns duplex-link $n3 $n6 10Mb 1ms $queue
$ns duplex-link $n7 $n2 10Mb 1ms $queue
$ns duplex-link $n3 $n8 10Mb 1ms $queue

#Re-Orient nodes
$ns duplex-link-op $n1 $n2 orient right-down      
$ns duplex-link-op $n5 $n2 orient right-up 
$ns duplex-link-op $n2 $n3 orient right 
$ns duplex-link-op $n3 $n4 orient right-up 
$ns duplex-link-op $n3 $n6 orient right-down
$ns duplex-link-op $n2 $n7 orient left
$ns duplex-link-op $n3 $n8 orient right

#Create a UDP agent and attach it to node n1
set udp0 [new Agent/UDP]
$ns attach-agent $n1 $udp0
# Create a CBR traffic source and attach it to udp0
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 1000
$cbr0 set interval_ 0.008
$cbr0 attach-agent $udp0
#Create a Null agent (a traffic sink) and attach it to node n6
set null0 [new Agent/Null]
$ns attach-agent $n4 $null0
#Connect the traffic source with the traffic sink
$ns connect $udp0 $null0
#Schedule events for the CBR agent
$ns at 0.5 "$cbr0 start"
$ns at 5.5 "$cbr0 stop"

#Create a UDP agent and attach it to node n5
set udp1 [new Agent/UDP]
$ns attach-agent $n5 $udp1
# Create a CBR traffic source and attach it to udp0
set cbr1 [new Application/Traffic/CBR]
$cbr1 set packetSize_ 1000
$cbr1 set interval_ 0.008
$cbr1 attach-agent $udp1
#Create a Null agent (a traffic sink) and attach it to node n6
set null1 [new Agent/Null]
$ns attach-agent $n6 $null1
#Connect the traffic source with the traffic sink
$ns connect $udp1 $null1
#Schedule events for the CBR agent
$ns at 0.6 "$cbr1 start"
$ns at 5.6 "$cbr1 stop"

#Create a UDP agent and attach it to node n7
set udp2 [new Agent/UDP]
$ns attach-agent $n7 $udp2
# Create a CBR traffic source and attach it to udp0
set cbr2 [new Application/Traffic/CBR]
$cbr2 set packetSize_ 500
$cbr2 set interval_ 0.00667
$cbr2 attach-agent $udp2
#Create a Null agent (a traffic sink) and attach it to node n6
set null2 [new Agent/Null]
$ns attach-agent $n8 $null2
#Connect the traffic source with the traffic sink
$ns connect $udp2 $null2
#Schedule events for the CBR agent
$ns at 0.7 "$cbr2 start"
$ns at 5.7 "$cbr2 stop"


#Call the finish procedure after 5 seconds of simulation time
$ns at 6.0 "finish"

#Run the simulation
$ns run
