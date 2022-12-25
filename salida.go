package main
import("fmt")

var HEAP[1000]float64
var STACK[1000]float64
var P, H float64
var t0,t1,t2,t3,t4,t5,t6 float64;


func print_true_proc() {
fmt.Printf("True")
}

func print_false_proc() {
fmt.Printf("False")
}

func main(){
	STACK[int(0)] = 5
	STACK[int(1)] = 1
	STACK[int(2)] = 2
	STACK[int(3)] = 3
	STACK[int(4)] = 4
	STACK[int(5)] = 5
	STACK[int(6)] = -1
	t0 = 0 + 1
	fmt.Printf("%c", int(91))
	L0:
	t1 = STACK[int(t0)]
	if(t1 == -1) {goto L1;}
	fmt.Printf("%d", int(t1))
	fmt.Printf("%c", int(32))
	t0 = t0 + 1
	goto L0;
	L1:
	fmt.Printf("%c", int(93))
	fmt.Printf("%c",int(10));
	t2 = 0 + 1
	t3 = 1  
	L2:
	t4 = STACK[int(t2)]
	if(t4 == -1) {goto L4;}
	if(t3 == 3) {goto L3;}
	t2 = t2 + 1
	t3 = t3 + 1
	goto L2;
	L3:
	STACK[int(t2)] = 45
	L4:
	fmt.Printf("%c", int(93))
	t5 = 0 + 1
	fmt.Printf("%c", int(91))
	L5:
	t6 = STACK[int(t5)]
	if(t6 == -1) {goto L6;}
	fmt.Printf("%d", int(t6))
	fmt.Printf("%c", int(32))
	t5 = t5 + 1
	goto L5;
	L6:
	fmt.Printf("%c", int(93))
	fmt.Printf("%c",int(10));
}
