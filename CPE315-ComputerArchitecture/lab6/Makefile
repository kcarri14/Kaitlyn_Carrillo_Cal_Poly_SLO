JAVAC = /opt/jdk-16/bin/javac
JAVA  = /opt/jdk-16/bin/java

lab6:
	$(JAVAC) *.java

unixTestAll:
	$(JAVAC) *.java
	$(JAVA) lab6 mem_stream.1
	$(JAVA) lab6 mem_stream.2

unixTestDiff:
	$(JAVAC) *.java
	$(JAVA) lab6 mem_stream.1 | diff - -w -B mem_stream1.out
	$(JAVA) lab6 mem_stream.2 | diff - -w -B mem_stream2.out
	

testAll:
	javac *.java
	java lab6 mem_stream.1
	java lab6 mem_stream.2

test1:
	javac *.java
	java lab6 mem_stream.1

test2:
	javac *.java
	java lab6 mem_stream.1

testDiff:
	javac *.java
	java lab6 mem_stream.1 | diff - -w -B mem_stream1.out
	java lab6 mem_stream.2 | diff - -w -B mem_stream2.out
