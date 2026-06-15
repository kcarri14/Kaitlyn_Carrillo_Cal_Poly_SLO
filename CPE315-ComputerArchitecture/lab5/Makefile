JAVAC = /opt/jdk-16/bin/javac
JAVA  = /opt/jdk-16/bin/java

lab5:
	$(JAVAC) *.java

unixTestAll:
	$(JAVAC) *.java
	$(JAVA) lab5 lab4_fib20.asm lab5.script 2
	$(JAVA) lab5 lab4_fib20.asm lab5.script 4
	$(JAVA) lab5 lab4_fib20.asm lab5.script 8

unixTestDiff:
	$(JAVAC) *.java
	$(JAVA) lab5 lab4_fib20.asm lab5.script 2 | diff - -w -B lab5_ghr2.output
	$(JAVA) lab5 lab4_fib20.asm lab5.script 4 | diff - -w -B lab5_ghr4.output
	$(JAVA) lab5 lab4_fib20.asm lab5.script 8 | diff - -w -B lab5_ghr8.output

testAll:
	javac *.java
	java lab5 lab4_fib20.asm lab5.script 2
	java lab5 lab4_fib20.asm lab5.script 4
	java lab5 lab4_fib20.asm lab5.script 8

test2:
	javac *.java
	java lab5 lab4_fib20.asm lab5.script 2

test4:
	javac *.java
	java lab5 lab4_fib20.asm lab5.script 4

test8:
	javac *.java
	java lab5 lab4_fib20.asm lab5.script 8

testDiff:
	javac *.java
	java lab5 lab4_fib20.asm lab5.script 2 | diff - -w -B lab5_ghr2.output
	java lab5 lab4_fib20.asm lab5.script 4 | diff - -w -B lab5_ghr4.output
	java lab5 lab4_fib20.asm lab5.script 8 | diff - -w -B lab5_ghr8.output
