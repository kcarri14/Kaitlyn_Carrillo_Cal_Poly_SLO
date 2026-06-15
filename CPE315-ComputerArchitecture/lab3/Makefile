JAVAC = /opt/jdk-16/bin/javac
JAVA  = /opt/jdk-16/bin/java

lab3:
	$(JAVAC) *.java

unixTestAll:
	$(JAVAC) *.java
	$(JAVA) lab3 testInput/input1.asm testScript/script1
	$(JAVA) lab3 testInput/input2.asm testScript/script2
	$(JAVA) lab3 testInput/input3.asm testScript/script3

unixTestDiff:
	$(JAVAC) *.java
	$(JAVA) lab3 testInput/input1.asm testScript/script1 | diff - -w -B testOutput/output1
	$(JAVA) lab3 testInput/input2.asm testScript/script2 | diff - -w -B testOutput/output2
	$(JAVA) lab3 testInput/input3.asm testScript/script3 | diff - -w -B testOutput/output3

testAll:
	javac *.java
	java lab3 testInput/input1.asm testScript/script1
	java lab3 testInput/input2.asm testScript/script2
	java lab3 testInput/input3.asm testScript/script3

test1:
	javac *.java
	java lab3 testInput/input1.asm testScript/script1

test2:
	javac *.java
	java lab3 testInput/input2.asm testScript/script2

test3:
	javac *.java
	java lab3 testInput/input3.asm testScript/script3

testDiff:
	javac *.java
	java lab3 testInput/input1.asm testScript/script1 | diff - -w -B testOutput/output1
	java lab3 testInput/input2.asm testScript/script2 | diff - -w -B testOutput/output2
	java lab3 testInput/input3.asm testScript/script3 | diff - -w -B testOutput/output3
