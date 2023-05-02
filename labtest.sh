#!/bin/bash

TIMEOUT="timeout 10" 
NCTIMEOUT="timeout 0.5" 
if [[ $OSTYPE != "linux-gnu" ]]; then
	TIMEOUT="" 
	NCTIMEOUT="" 
fi

sleep 0.1
rm -f a.out *.class nc.txt kk1.txt kk.txt res.txt
function RunSource {
	src=$1
	port=$2
	outfile=$3
	echo $src $port 
	if [[ "$src" =~ ".cpp" ]];
	then
		g++ $src
		sleep 0.01
		($TIMEOUT ./a.out $port  > $outfile & wait 2> /dev/null)  &
	elif [[ $src =~ ".c" ]];
	then
		gcc $src 
		sleep 0.01
		($TIMEOUT ./a.out $port  > $outfile & wait 2> /dev/null)  &
	elif [[ $src =~ ".java" ]];
	then
		javac $src 
		sleep 0.01
		cname=$(ls *.class | sed 's/.class//')
		($TIMEOUT java $cname $port  > $outfile & wait 2> /dev/null)    &
	elif [[ $src =~ ".py" ]];
	then
		($TIMEOUT python3 $src $port > $outfile   & wait 2> /dev/null)  &
	else
		echo "not supported" $src
		exit
	fi
	sleep 0.5
}

# input
src=$1;
port=$2;

succcnt=0

# Run the file server program
RunSource $src $port res.txt


# Test
# 1
tc=0
let "tc=tc+1"
echo $tc
echo "GET biga.html" | $NCTIMEOUT nc localhost $port > kk.txt
diff biga.html kk.txt
if [[ $? == 0 ]];
then
	let "succcnt=succcnt+1"
fi

# 2
let "tc=tc+1"
echo $tc
echo "GET palladio.jpg" | $NCTIMEOUT nc localhost $port > kk.txt
diff palladio.jpg kk.txt
if [[ $? == 0 ]];
then
	let "succcnt=succcnt+2"
fi

# 3
let "tc=tc+1"
echo $tc
echo "GET kkk.jpg" | $NCTIMEOUT nc localhost $port > kk.txt
grep -i "File Not Found" kk.txt &> /dev/null
if [[ $? == 0 ]];
then
	let "succcnt=succcnt+64"
fi

# 4
let "tc=tc+1"
echo $tc
echo "PUT kk.txt" | cat - biga.html | $NCTIMEOUT nc localhost $port 
diff biga.html kk.txt
if [[ $? == 0 ]];
then
	let "succcnt=succcnt+4"
fi

# 5
let "tc=tc+1"
echo $tc
#echo "PUT kk.txt" | cat - b.html | nc localhost $port 
#diff b.html kk.txt
echo "PUT kk.txt" | cat - palladio.jpg | $NCTIMEOUT nc localhost $port 
cmp palladio.jpg kk.txt 
if [[ $? == 0 ]];
then
	let "succcnt=succcnt+8"
fi

# 6
let "tc=tc+1"
echo $tc
echo "LS html" | $NCTIMEOUT nc localhost $port | sort  > kk.txt
ls *.html | sort > kk1.txt
diff kk1.txt kk.txt
if [[ $? == 0 ]];
then
	let "succcnt=succcnt+16"
fi


# 7
let "tc=tc+1"
echo $tc
echo "LS jpg" | $NCTIMEOUT nc localhost $port | sort  > kk.txt
ls *.jpg | sort > kk1.txt
diff kk1.txt kk.txt
if [[ $? == 0 ]];
then
	let "succcnt=succcnt+32"
fi

killall -q a.out python3 java 

echo "Result: " $succcnt $src

sleep 0.1

rm -f a.out *.class nc.txt kk1.txt kk.txt res.txt
