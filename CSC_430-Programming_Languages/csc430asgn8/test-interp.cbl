       IDENTIFICATION DIVISION.
       PROGRAM-ID. test-interp.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  INPUT-AST PIC X(50).
       01  INPUT-NUMC REDEFINES INPUT-AST.
           05 FILLER PIC X(40).
           05 INPUT-VAL PIC S9(5)V99999.
       01  INPUT-IDC REDEFINES INPUT-AST.
      *    Essentially the same as input-str
           05 FILLER PIC X(40).
           05 INPUT-SYM PIC X(10).
       01  INPUT-STR REDEFINES INPUT-AST.
           05 FILLER PIC X(40).
           05 INPUT-STRING PIC X(10).
       01  INPUT-APPC REDEFINES INPUT-AST.
           05 INPUT-FUNC-TYPE PIC X(10).
           05 INPUT-FUNC PIC X(10).
           05 INPUT-ARGS PIC X(10) OCCURS 3 TIMES.
       01  INPUT-LAMC REDEFINES INPUT-AST.
           05 INPUT-PARAMS PIC X(40).
           05 INPUT-BODY PIC X(10).
           

       01  INPUT-TYPE PIC X(2).

       01  WS-ACTUAL-RES PIC X(50).
       01  ERROR-MSG REDEFINES WS-ACTUAL-RES.
           05 SHEQ-LABEL PIC X(10).
               88 IS-SHEQ-ERROR VALUE "SHEQ ERROR".
           05 REST PIC X(40).

       01  WS-EXPECTED-RES PIC X(50).
       01  WS-EXPECTED-RES-NUM REDEFINES WS-EXPECTED-RES.
           05 FILLER PIC X(40).
           05 EXPECTED-NUM PIC S9(5)V99999.
       01  WS-EXPECTED-RES-CLOV REDEFINES WS-EXPECTED-RES.
           05 EXPECTED-PARAMS PIC X(40).
           05 EXPECTED-BODY PIC X(10).
           *> how do we put environment, no more memory

       01  WS-TEST-COUNT PIC 9(2) VALUE ZEROS.
       01  WS-PASS-COUNT PIC 9(2) VALUE ZEROS.
       01  WS-FAIL-COUNT PIC 9(2) VALUE ZEROS.

       01  CURR-ENVR.
           05 BINDING OCCURS 30 TIMES INDEXED BY ENVR-IDX.
               10 SYMBOLS PIC X(10) VALUE SPACE.
               10 BOUND-VALS.
                   15 VAL-TYPES PIC X(1).
                   15 VALS PIC X(10).

       PROCEDURE DIVISION.
           PERFORM SET-TOP-ENV.
           PERFORM TEST-INTERP-NUMC-1.
           PERFORM TEST-INTERP-IDC-1.
           PERFORM TEST-INTERP-IDC-2.
           PERFORM TEST-INTERP-STRC-1.
           PERFORM TEST-INTERP-PRIM-ADD.
           PERFORM SHOW-TEST-RESULTS.
           STOP RUN.

       SHOW-TEST-RESULTS.
           DISPLAY "# of Tests Ran: ".
           DISPLAY WS-TEST-COUNT.
           DISPLAY "# Passed: ".
           DISPLAY WS-PASS-COUNT.
           DISPLAY "# Failed: ".
           DISPLAY WS-FAIL-COUNT.

       TEST-INTERP-NUMC-1.
           PERFORM CLEAR-IO.
           MOVE -3.14159 TO EXPECTED-NUM.
           ADD 1 TO WS-TEST-COUNT.
           MOVE -3.14159
               TO INPUT-VAL.
           MOVE "N" TO INPUT-TYPE.
           CALL 'SHEQ4' USING
               INPUT-AST,
               INPUT-TYPE,
               CURR-ENVR,
               WS-ACTUAL-RES.
           IF WS-ACTUAL-RES = WS-EXPECTED-RES THEN
               ADD 1 TO WS-PASS-COUNT
            ELSE
               DISPLAY "FAILED TEST-INTERP-NUMC-1"
               ADD 1 TO WS-FAIL-COUNT
           END-IF.

       TEST-INTERP-IDC-1.
           PERFORM CLEAR-IO.
           MOVE "TEST" TO WS-EXPECTED-RES.
           ADD 1 TO WS-TEST-COUNT.
           MOVE "TEST"
               TO INPUT-SYM.
           MOVE "I" TO INPUT-TYPE.
           CALL "SHEQ4" USING
               INPUT-AST,
               INPUT-TYPE,
               CURR-ENVR,
               WS-ACTUAL-RES.
           IF IS-SHEQ-ERROR THEN
               ADD 1 TO WS-PASS-COUNT
            ELSE 
                DISPLAY "FAILED TEST-INTERP-IDC-1"
                ADD 1 TO WS-FAIL-COUNT
           END-IF.

       TEST-INTERP-IDC-2.
           PERFORM CLEAR-IO.
           MOVE "World!" TO WS-EXPECTED-RES.
           ADD 1 TO WS-TEST-COUNT.
           MOVE "Hello" TO SYMBOLS(1).
           MOVE "S" TO VAL-TYPES(1).
           MOVE "World!" TO VALS(1).
           MOVE "Hello" TO INPUT-SYM.
           MOVE "I" TO INPUT-TYPE.
           CALL "SHEQ4" USING
               INPUT-AST,
               INPUT-TYPE,
               CURR-ENVR,
               WS-ACTUAL-RES.
           IF WS-ACTUAL-RES = WS-EXPECTED-RES THEN
               ADD 1 TO WS-PASS-COUNT
            ELSE
                DISPLAY "FAILED TEST-INTERP-IDC-2"
                ADD 1 TO WS-FAIL-COUNT
           END-IF.

       TEST-INTERP-STRC-1.
           PERFORM CLEAR-IO.
      *    Check for unbound identifier
           MOVE "DEFNOTSYM" TO WS-EXPECTED-RES.
           ADD 1 TO WS-TEST-COUNT.
           MOVE "DEFNOTSYM"
               TO INPUT-STR.
           MOVE "S" TO INPUT-TYPE.
           CALL 'SHEQ4' USING
               INPUT-AST,
               INPUT-TYPE,
               CURR-ENVR,
               WS-ACTUAL-RES.
           IF WS-ACTUAL-RES = WS-EXPECTED-RES THEN
               ADD 1 TO WS-PASS-COUNT
            ELSE
                DISPLAY "FAILED TEST-INTERP-STRC-1"
               ADD 1 TO WS-FAIL-COUNT
           END-IF.
           
       TEST-INTERP-LAMC-1.
           PERFORM CLEAR-IO.
           MOVE "body" TO EXPECTED-BODY.
           MOVE "x" TO EXPECTED-PARAMS.
           MOVE "body" TO INPUT-BODY.
           MOVE "x" TO INPUT-PARAMS.
           MOVE "L" TO INPUT-TYPE.
           CALL 'SHEQ4' USING
               INPUT-AST,
               INPUT-TYPE,
               CURR-ENVR,
               WS-ACTUAL-RES.
           IF WS-ACTUAL-RES = WS-EXPECTED-RES THEN
               ADD 1 TO WS-PASS-COUNT
            ELSE
                DISPLAY "FAILED TEST-INTERP-STRC-1"
               ADD 1 TO WS-FAIL-COUNT
           END-IF.

       TEST-INTERP-PRIM-ADD.
           PERFORM CLEAR-IO.
           MOVE 3 TO EXPECTED-NUM.
           ADD 1 TO WS-TEST-COUNT.
           MOVE "P" TO INPUT-FUNC-TYPE.
           MOVE "+" TO INPUT-FUNC.
           MOVE "A" TO INPUT-TYPE.
           MOVE "0000100000" TO  INPUT-ARGS(1).
           MOVE "0000200000" TO  INPUT-ARGS(2).
           CALL 'SHEQ4' USING
               INPUT-AST,
               INPUT-TYPE,
               CURR-ENVR,
               WS-ACTUAL-RES.
           IF WS-ACTUAL-RES = WS-EXPECTED-RES THEN
               ADD 1 TO WS-PASS-COUNT
            ELSE
                DISPLAY "FAILED TEST-INTERP-PRIM-ADD"
               ADD 1 TO WS-FAIL-COUNT
           END-IF.
       
       

       SET-TOP-ENV.
           DISPLAY "Setting up top environment...".
           MOVE "+" TO SYMBOLS(1).
           MOVE "P" TO VAL-TYPES(1).
           MOVE "+" TO VALS(1).

           MOVE "-" TO SYMBOLS(2).
           MOVE "P" TO VAL-TYPES(2).
           MOVE "-" TO VALS(2).

           MOVE "*" TO SYMBOLS(3).
           MOVE "P" TO VAL-TYPES(3).
           MOVE "*" TO VALS(3).

           MOVE "/" TO SYMBOLS(4).
           MOVE "P" TO VAL-TYPES(4).
           MOVE "/" TO VALS(4).

           MOVE "<=" TO SYMBOLS(5).
           MOVE "P" TO VAL-TYPES(5).
           MOVE "<=" TO VALS(5).

           MOVE "substring" TO SYMBOLS(6).
           MOVE "P" TO VAL-TYPES(6).
           MOVE "substring" TO VALS(6).

           MOVE "strlen" TO SYMBOLS(7).
           MOVE "P" TO VAL-TYPES(7).
           MOVE "strlen" TO VALS(7).

           MOVE "equal?" TO SYMBOLS(8).
           MOVE "P" TO VAL-TYPES(8).
           MOVE "equal?" TO VALS(8).

           MOVE "true" TO SYMBOLS(9).
           MOVE "B" TO VAL-TYPES(9).
           MOVE "true" TO VALS(9).

           MOVE "false" TO SYMBOLS(10).
           MOVE "B" TO VAL-TYPES(10).
           MOVE "false" TO VALS(10).

           MOVE "error" TO SYMBOLS(11).
           MOVE "P" TO VAL-TYPES(11).
           MOVE "error" TO VALS(11).

       CLEAR-IO.
           MOVE SPACES TO WS-EXPECTED-RES.
           MOVE SPACES TO WS-ACTUAL-RES.
           
           


       END PROGRAM test-interp.
       