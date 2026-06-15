JAVAC = /opt/jdk-16/bin/javac
JAVA  = /opt/jdk-16/bin/java

lab2:
	$(JAVAC) *.java

unixTestAll:
	$(JAVAC) *.java
	$(JAVA) lab2 testFiles/test1.asm
	$(JAVA) lab2 testFiles/test2.asm
	$(JAVA) lab2 testFiles/test3.asm
	$(JAVA) lab2 testFiles/test4.asm

unixTestDiff:
	$(JAVAC) *.java
	$(JAVA) lab2 testFiles/test1.asm | diff - -w -B testOutputs/test1.output
	$(JAVA) lab2 testFiles/test2.asm | diff - -w -B testOutputs/test2.output
	$(JAVA) lab2 testFiles/test3.asm | diff - -w -B testOutputs/test3.output
	$(JAVA) lab2 testFiles/test4.asm | diff - -w -B testOutputs/test4.output


testAll:
	javac *.java
	java lab2 testFiles/test1.asm
	java lab2 testFiles/test2.asm
	java lab2 testFiles/test3.asm
	java lab2 testFiles/test4.asm

testDiff:
	javac *.java
	java lab2 testFiles/test1.asm | diff - -w -B testOutputs/test1.output
	java lab2 testFiles/test2.asm | diff - -w -B testOutputs/test2.output
	java lab2 testFiles/test3.asm | diff - -w -B testOutputs/test3.output
	java lab2 testFiles/test4.asm | diff - -w -B testOutputs/test4.output
