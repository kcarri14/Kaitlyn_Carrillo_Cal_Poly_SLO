JAVAC = /opt/jdk-16/bin/javac
JAVA  = /opt/jdk-16/bin/java

lab4:
	$(JAVAC) *.java

unixTestAll:
	$(JAVAC) *.java
	$(JAVA) lab4 testInput/input1.asm testScript/script1
	$(JAVA) lab4 testInput/input2.asm testScript/script2
	$(JAVA) lab4 testInput/input3.asm testScript/script3
	$(JAVA) lab4 testInput/input4.asm testScript/script4

unixTestDiff:
	$(JAVAC) *.java
	$(JAVA) lab4 testInput/input1.asm testScript/script1 | diff - -w -B testOutput/output1
	$(JAVA) lab4 testInput/input2.asm testScript/script2 | diff - -w -B testOutput/output2
	$(JAVA) lab4 testInput/input3.asm testScript/script3 | diff - -w -B testOutput/output3
	$(JAVA) lab4 testInput/input4.asm testScript/script4 | diff - -w -B testOutput/output4

testAll:
	javac *.java
	java lab4 testInput/input1.asm testScript/script1
	java lab4 testInput/input2.asm testScript/script2
	java lab4 testInput/input3.asm testScript/script3
	java lab4 testInput/input4.asm testScript/script4

test1:
	javac *.java
	java lab4 testInput/input1.asm testScript/script1

test2:
	javac *.java
	java lab4 testInput/input2.asm testScript/script2

test3:
	javac *.java
	java lab4 testInput/input3.asm testScript/script3


test4:
	javac *.java
	java lab4 testInput/input4.asm testScript/script4

testDiff:
	javac *.java
	java lab4 testInput/input1.asm testScript/script1 | diff - -w -B testOutput/output1
	java lab4 testInput/input2.asm testScript/script2 | diff - -w -B testOutput/output2
	java lab4 testInput/input3.asm testScript/script3 | diff - -w -B testOutput/output3
	java lab4 testInput/input4.asm testScript/script4 | diff - -w -B testOutput/output4
