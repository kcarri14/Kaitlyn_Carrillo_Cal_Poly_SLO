       IDENTIFICATION DIVISION.
       PROGRAM-ID. SHEQ4 RECURSIVE.
       
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  ERROR-DESC PIC X(40).
       01  ERROR-MSG PIC X(50).
       01  TEMP-NUM-1 PIC S9(5)V99999.
       01  TEMP-NUM-2 PIC S9(5)V99999.

       LOCAL-STORAGE SECTION.
       01  LS-APPC.
           05 LS-APPC-FUNC PIC X(10).
           05 LS-APPC-FUNC-TYPE PIC X(10).
           05 LS-APPC-ARGS PIC X(10) OCCURS 3 TIMES
               INDEXED BY LS-ARG-IDX.
       01  LS-ENVR.
           05 LS-BINDING OCCURS 30 TIMES INDEXED BY LS-ENVR-IDX.
               10 LS-SYMBOLS PIC X(10).
               10 LS-BOUND-VALS.
                   15 LS-VAL-TYPES PIC X(1).
                   15 LS-VALS PIC X(10).   
       
       LINKAGE SECTION.
       01  ABS-SYN-TREE PIC X(50).
       01  NUMC REDEFINES ABS-SYN-TREE.
           05 FILLER PIC X(40).
           05 VAL PIC S9(5)V99999.
       01  STRC REDEFINES ABS-SYN-TREE.
           05 FILLER PIC X(40).
           05 STR PIC X(10).
       01  IDC REDEFINES ABS-SYN-TREE.
           05 FILLER PIC X(40).
           05 SYM PIC X(10).
       01  APPC REDEFINES ABS-SYN-TREE.
           05 APPC-TYPE PIC X(10).
           05 APPC-FUNC PIC X(10).
               88 IS-ADD          VALUE "+".
               88 IS-SUB          VALUE "-".
               88 IS-MUL          VALUE "*".
               88 IS-DIV          VALUE "/".
               88 IS-LEQ          VALUE "<=".
               88 IS-SUBSTRING    VALUE "substring".
               88 IS-STRLEN       VALUE "strlen".
               88 IS-EQUAL        VALUE "equal?".
               88 IS-ERROR        VALUE "error".
           05 APPC-ARGS.
               10 APPC-CHARS PIC X(10) OCCURS 3 TIMES.
           05 APPC-ARGS-NUM REDEFINES APPC-ARGS.
               10 APPC-NUMS PIC S9(5)V99999 OCCURS 3 TIMES.
       
       01  LAMC REDEFINES ABS-SYN-TREE.
           05 LAMC-PARAMS PIC X(40).
           05 LAMC-BODY PIC X(10).
       *> Definitions for APPC recursion
      *01  INTERP-FUNC PIC X(50).
      *01  INTERP-FUNC-TYPE PIC X(50).
       
       01  AST-TYPE PIC X(2).
       01  INTERP-RESULT PIC X(50).
       01  INTERP-RESULT-NUM REDEFINES INTERP-RESULT.
           05 FILLER PIC X(40).
           05 RESULT-NUM-VAL PIC S9(5)V99999.
       01  INTERP-RESULT-STR REDEFINES INTERP-RESULT.
           05 RESULT-STR PIC X(50).
       01  INTERP-RESULT-CLOV REDEFINES INTERP-RESULT.
           05 RESULT-PARAMS PIC X(40).
           05 RESULT-BODY PIC X(10).
           *> how do we put environment, no more memory
       01  ENVR.
           05 BINDING OCCURS 30 TIMES INDEXED BY ENVR-IDX.
               10 SYMBOLS PIC X(10).
               10 BOUND-VALS.
                   15 VAL-TYPES PIC X(1).
                   15 VALS PIC X(10).    

       
       PROCEDURE DIVISION USING
               ABS-SYN-TREE,
               AST-TYPE,
               ENVR,
               INTERP-RESULT.
           EVALUATE AST-TYPE
            WHEN "N" *> NUMC case
                MOVE VAL TO RESULT-NUM-VAL
            WHEN "I" *> IDC case
                SET ENVR-IDX TO 1
                    SEARCH BINDING
                    AT END
                        STRING
                            "Unbound identifier, received "
                                DELIMITED BY SIZE
                            SYM
                                DELIMITED BY SIZE 
                            INTO ERROR-DESC
                       PERFORM RAISE-ERROR
                    WHEN SYMBOLS(ENVR-IDX) = SYM
                    MOVE VALS(ENVR-IDX) TO INTERP-RESULT
                END-SEARCH
            WHEN "S" *> STRC case
                MOVE ABS-SYN-TREE TO INTERP-RESULT
            WHEN "If" *> IFC case
                CONTINUE
            WHEN "L" *> LAMC case
      *         PERFORM HANDLE-LAMC
                CONTINUE
            WHEN "A" *> APPC case
                PERFORM INTERP-APPC
                CONTINUE
            WHEN OTHER
                CONTINUE
           END-EVALUATE.
           
           GOBACK.
        
       RAISE-ERROR.
           STRING "SHEQ ERROR: " DELIMITED BY SIZE
                    ERROR-DESC DELIMITED BY SIZE
                    INTO ERROR-MSG
           MOVE ERROR-MSG TO INTERP-RESULT.
           GOBACK.
    
      *HANDLE-LAMC.
      *    MOVE LAMC-PARAMS TO RESULT-PARAMS
      *    MOVE LAMC-BODY TO RESULT-BODY
      *     *> environment?
      *    GOBACK.



    
       INTERP-APPC.
           EVALUATE APPC-TYPE
            WHEN "P" *> Primitive case
            PERFORM INTERP-PRIM.
           GOBACK.
       
       *> function for PRIMVs
       INTERP-PRIM.
           EVALUATE TRUE
               WHEN IS-ADD
                   COMPUTE RESULT-NUM-VAL
                       = APPC-NUMS(1) + APPC-NUMS(2)
                    ON SIZE ERROR
                        MOVE "Sum is too large!"
                            TO ERROR-DESC
                        PERFORM RAISE-ERROR
                   END-COMPUTE
               WHEN IS-SUB
                   CONTINUE
               WHEN IS-MUL
                   CONTINUE
               WHEN IS-DIV
                   CONTINUE
               WHEN IS-LEQ
                   CONTINUE
               WHEN IS-SUBSTRING
                   CONTINUE
               WHEN IS-STRLEN
                   CONTINUE
               WHEN IS-EQUAL
                   CONTINUE
               WHEN IS-ERROR
                   CONTINUE
               WHEN OTHER
                   MOVE "Unknown primitive operation." TO ERROR-DESC
                   PERFORM RAISE-ERROR
               END-EVALUATE.
           GOBACK.


       END PROGRAM SHEQ4.
           