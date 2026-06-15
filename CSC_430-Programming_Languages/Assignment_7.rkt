#lang typed/racket
;Project is fully implemented and all tests passed

(require typed/rackunit)
	
;‹expr› ::= ‹num›
;       |‹id›
;       |‹string›
;       |{ ‹id› := ‹expr› }
;       |{ if ‹expr› ‹expr› ‹expr› }
;       |{ let { [<ty> ‹id›=‹expr›]* } in ‹expr› end }
;       |{ lambda ( [<ty>‹id›]* ) : ‹expr› }
;       |{ ‹expr› ‹expr›* }
;       |{ rlet { [ ‹ty› ‹id› = ‹expr› ] } in ‹expr› end }

(define-type ExprC (U NumC strC idC ifC lambdaC AppC MutC SeqC RecC))

(struct NumC ([n : Real]) #:transparent)
(struct idC ([s : Symbol]) #:transparent)
(struct strC ([str : String]) #:transparent)
(struct MutC ([id : Symbol] [exp : ExprC]) #:transparent)
(struct ifC ([test : ExprC] [then : ExprC] [else : ExprC]) #:transparent)
(struct lambdaC ([types : (Listof Types)] [args : (Listof Symbol)] [body : ExprC]) #:transparent)
(struct AppC ([func : ExprC] [args : (Listof ExprC)]) #:transparent)
(struct SeqC ([func : (Listof ExprC)]) #:transparent)
(struct RecC ([type : Types] [arg : Symbol] [func : ExprC] [body : ExprC]) #:transparent)


;; this function defines what symbols can not be
;; cnbt = can not be this
(define (cnbt? [s : Sexp]) : Boolean
  (or (equal? s 'if) (equal? s ':) (equal? s 'let)
      (equal? s '=) (equal? s 'in) (equal? s 'end) (equal? s ':=)
      (equal? s 'rlet) (equal? s 'lambda) (equal? s '->)))


;Values
(define-type Value (U BoolV StrV NumV CloV PrimV NullV ArrayV))
(struct NumV ([n : Real]) #:transparent)
(struct BoolV ([b : Boolean]) #:transparent)
(struct StrV ([s : String]) #:transparent)
(struct CloV ([params : (Listof Symbol)] [body : ExprC] [env : Environment]) #:transparent)
(struct PrimV ([name : Symbol]) #:transparent)
(struct NullV () #:transparent)
(struct ArrayV ([name : Location] [len : Natural]) #:transparent)

;Environments
(define-type Location Natural)
(define-type Store (Vectorof Value))
(struct Binding ([name : Symbol] [val : Location]) #:transparent)
(define-type Environment (Listof Binding))

;<ty> ::= num
;       | bool
;       | str
;       | intarray
;       | {<ty>* -> <ty>
(define-type Types (U NumT StrT BoolT IntarrayT FunT NullT))
(struct NumT () #:transparent)
(struct StrT () #:transparent)
(struct BoolT () #:transparent)
(struct IntarrayT () #:transparent)
(struct FunT ([args : (Listof Types)] [return : Types]) #:transparent)
(struct NullT () #:transparent)

;Typed Environment
(struct type-bind ([name : Symbol] [ty : Types]) #:transparent)
(define-type TEnv (Listof type-bind))

(define base-tenv : TEnv
  (list (type-bind 'true (BoolT))
        (type-bind 'false (BoolT))
        (type-bind '+ (FunT (list (NumT) (NumT)) (NumT)))
        (type-bind '- (FunT (list (NumT) (NumT)) (NumT)))
        (type-bind '* (FunT (list (NumT) (NumT)) (NumT)))
        (type-bind '/ (FunT (list (NumT) (NumT)) (NumT)))
        (type-bind '<= (FunT (list (NumT) (NumT)) (BoolT)))
        (type-bind 'num-eq? (FunT (list (NumT) (NumT)) (BoolT)))
        (type-bind 'str-eq? (FunT (list (StrT) (StrT)) (BoolT)))
        (type-bind 'substring (FunT (list (StrT) (NumT) (NumT)) (StrT)))
        (type-bind 'strlen (FunT (list (StrT)) (NumT)))
        (type-bind 'make-array (FunT (list (NumT) (NumT)) (IntarrayT)))
        (type-bind 'aref (FunT (list (IntarrayT) (NumT)) (NumT)))
        (type-bind 'aset! (FunT (list (IntarrayT) (NumT) (NumT)) (NullT)))
        (type-bind 'alen (FunT (list (IntarrayT)) (NumT)))))


;the top environment that contains the 16 pre-exisiting bindings
(define top-env : Environment
  (list (Binding 'true 1)
        (Binding 'false 2)
        (Binding '+ 3)
        (Binding '- 4)
        (Binding '* 5)
        (Binding '/ 6)
        (Binding 'strlen 7)
        (Binding '<= 8)
        (Binding 'substring 9)
        (Binding 'num-eq? 10)
        (Binding 'str-eq? 11)
        (Binding 'alen 12)
        (Binding 'make-array 13)
        (Binding 'aset! 14)
        (Binding 'aref 15)))

;makes the initial store with the initial bindings
(define (make-initial-store [memsize : Natural]) : Store
  (define store : Store (make-vector memsize (BoolV #f)))
  (vector-set! store (ann 0 Natural) (NumV 16))
  (vector-set! store (ann 1 Natural) (BoolV #t))
  (vector-set! store (ann 2 Natural) (BoolV #f))
  (vector-set! store (ann 3 Natural) (PrimV '+))
  (vector-set! store (ann 4 Natural) (PrimV '-))
  (vector-set! store (ann 5 Natural) (PrimV '*))
  (vector-set! store (ann 6 Natural) (PrimV '/))
  (vector-set! store (ann 7 Natural) (PrimV 'strlen))
  (vector-set! store (ann 8 Natural) (PrimV '<=))
  (vector-set! store (ann 9 Natural) (PrimV 'substring))
  (vector-set! store (ann 10 Natural) (PrimV 'num-eq?))
  (vector-set! store (ann 11 Natural) (PrimV 'str-eq?))
  (vector-set! store (ann 12 Natural) (PrimV 'alen))
  (vector-set! store (ann 13 Natural) (PrimV 'make-array))
  (vector-set! store (ann 14 Natural) (PrimV 'aset!))
  (vector-set! store (ann 15 Natural) (PrimV 'aref)) store)

;returns the next free memeory store in the first cell 
(define (next-free [store : Store]) : Natural
  (match (vector-ref store (ann 0 Natural))
    [(NumV n) (cast n Natural)]))

;puts the new next free memory after allocation and returns n
(define (new-free [store : Store] [n : Natural]) : Natural
  (vector-set! store (ann 0 Natural) (NumV n)) n)

;takes in a store and a number and allocates that amount of space and returns the base location
(define (allocate [store : Store] [length : Natural]) : Natural
  (define base (next-free store))
  (define new (+ base length))
  (if (= length 0)
      (error 'allocate "SHEQ: cannot allocate 0 cells")
      (if (> new (vector-length store))
          (error 'allocate "SHEQ: out of memory ~e" new)
          (new-free store new))) base)

;accepts any SHEQ4 value and returns a string (double-quoted wrapped)
(define (serialize [v : Value]) : String
  (match v
    [(NumV n) (~v n)]
    [(BoolV bool) (if bool "true" "false")]
    [(StrV str) (~v str)]
    [(PrimV op) "#<primop>"]
    [(CloV arg body env) "#<procedure>"]
    [(NullV) "null"]
    [(ArrayV loc len) "#<array>"]))

;this function takes in a symbol and an environment to find the symbol's value in the environment
(define (lookup [for : Symbol] [env : Environment] [store : Store]) : Value
  (cond
    [(empty? env) (error 'lookup "SHEQ: id not found ~e" for)]
    [else (cond
            [(symbol=? for (Binding-name (first env)))
             (vector-ref store (Binding-val (first env)))]
            [else (lookup for (rest env) store)])]))

;this function takes in a symbol and a type environement to find the symbols type
(define (type-lookup [for : Symbol] [env : TEnv]) : Types
  (cond
    [(empty? env) (error 'type-lookup "SHEQ: id not found ~e" for)]
    [else (cond
            [(symbol=? for (type-bind-name (first env)))
             (type-bind-ty (first env))]
            [else (type-lookup for (rest env))])]))

; this function takes in a symbol, a value, environment, and store,
; and mutates the original value of the symbol in the store to the new value
; returns a NullV
(define (mutate [for : Symbol] [new : Value] [env : Environment] [store : Store]) : Value
  (cond
    [(empty? env) (error 'lookup "SHEQ: cannot mutate unbound id ~e" for)]
    [else (cond
            [(symbol=? for (Binding-name (first env)))
             (vector-set! store (Binding-val (first env)) new)
             (NullV)]
            [else (mutate for new (rest env) store)])]))

;This function takes an s-expression and parses it and outputs an ExprC
(define (parse [e : Sexp]) : ExprC
  (match e
    [(list 'seq args ...) (SeqC (map parse (cast args (Listof Sexp))))]
    [(list 'rlet (list arg) 'in body 'end) (parse-rec arg body)]
    [(? real? n) (NumC n)]
    [(? string? str) (strC str)]
    [(list (? symbol? id) ':= exp) (MutC id (parse exp))] 
    [(? cnbt? (? symbol? s))
     (error 'parse "SHEQ: cannot have ~e as an identifier name" s)]
    [(? symbol? s) (idC s)]
    [(list 'if test then else) (ifC (parse test) (parse then) (parse else))]
    
    [(list 'lambda (list args ...) ': body)
     (define names 
       (for/list : (Listof Symbol) ([a (in-list (cast args (Listof Sexp)))])
         (match a
           [(list _ (? symbol? x)) x]
           [_ (error 'parse "SHEQ: expected [<ty> <id>]; got ~e" a)])))

     (define types
       (for/list : (Listof Types) ([a (in-list (cast args (Listof Sexp)))])
         (match a
           [(list ty (? symbol? _)) (parse-type ty)])))
     
     (if (check-duplicates (cast names (Listof Symbol))) ; cast must succeed by definition of pattern above
         (error 'parse "SHEQ: functions cannot have multiple paramaters with the same identifier ~e" names)
         ; cast must succeed by definition of pattern above
         (lambdaC (cast types (Listof Types)) (cast names (Listof Symbol)) (parse body)))]
    [(list 'let args 'in body 'end) (desugar args body)]
    
    [(cons op args) (AppC (parse op) (map parse (cast args (Listof Sexp))))] ; cast must succeed by definition of Sexp
    [x (error 'parse "SHEQ: Invalid s-expression ~e" x)]))


; parse-rec takes in an argument defintion and a body and returns a RecC
(define (parse-rec [arg : Sexp] [body : Sexp]) : ExprC
  (match arg
    [(list type (? symbol? id) '= func)
     (if (cnbt? id)
         (error 'parse-rec "SHEQ: cannot have if, :, let, in, end, = as identifiers, ~e" id)
         (RecC (parse-type type) id (parse func) (parse body)))] ; cast must succeed by definition of pattern above
    [_ (error 'parse-rec "SHEQ: invalid syntax for rlet statement ~e" arg)]))


;; desugar takes in the arguments and the body of a let statement and desugars it into an AppC
(define (desugar [args : Sexp] [body : Sexp]) : ExprC
  (match args
    [(list (list ty (? symbol? var) '= rst) ...)
     (define names : (Listof Symbol)
       (cast var (Listof Symbol)))
     (define (reserved? [lst : (Listof Symbol)]) : Boolean
       (match lst
         ['() #f]
         [(cons (? cnbt? _) _) #t]
         [(cons _ rest) (reserved? rest)]))
     
     (define types (for/list : (Listof Types)([t (in-list (cast ty (Listof Sexp)))]) (parse-type t)))
     (define chedup (check-duplicates names))
     (if (reserved? names)
         (error 'desugar "SHEQ: cannot have if, :, let, in, end, = as params ~e" names)
         (if (not (false? chedup))
             (error 'desugar "SHEQ: duplicate parameters")
             (AppC (lambdaC types names (parse body)) (map parse (cast rst (Listof Sexp))))))]                                    
    [_ (error 'parse "SHEQ: invalid syntax for let statement ~e" args)]))


;parses the types in the parser
(define (parse-type [s : Sexp]) : Types
  (match s
    ['num (NumT)]
    ['str (StrT)]
    ['bool (BoolT)]
    ['intarray (IntarrayT)]
    [(list args ... '-> return)
     (FunT (map parse-type (cast args (Listof Sexp))) (parse-type return))]
    [_ (error 'parse_type "SHEQ: not a type, ~e" s)]))


;makes sure that the types of the two inputs are the same
(define (equal-types? [t1 : Types] [t2 : Types]) : Boolean
  (match (list t1 t2)
    [(list (NumT) (NumT)) #t]
    [(list (StrT) (StrT)) #t]
    [(list (BoolT) (BoolT)) #t]
    [(list (IntarrayT) (IntarrayT)) #t]
    [(list (FunT args1 ret1) (FunT args2 ret2)) (and (= (length args1) (length args2))
                                                     (for ([a1 args1] [a2 args2])
                                                       (equal-types? a1 a2)) (equal-types? ret1 ret2))]
    [_ #f]))


;takes in a exprC and makes sure the types are correct
(define (type-check [expr : ExprC] [tenv : TEnv]) : Types
  (match expr
    [(NumC n) (NumT)]
    [(strC s) (StrT)]
    [(idC i) (type-lookup i tenv)]
    [(ifC t th el) (define t-type (type-check t tenv))
                   (if (BoolT? t-type)
                       (let () (type-check th tenv) (type-check el tenv))
                       (error 'type-checker "SHEQ: the condition must be a Boolean, got ~e" t-type))]
    ;ask if the type of the id can change with the type of the expression
    [(SeqC a) (define arg-vals : (Listof Types) (map (lambda ([arg : ExprC])
                                                       (type-check arg tenv)) a)) (last arg-vals)]
    [(MutC i e) (type-lookup i tenv) (type-check e tenv)]
    [(lambdaC t n b) (if (= (length t) (length n))
                         (let ()
                           (define extension : (Listof type-bind)
                             (for/list : (Listof type-bind)
                               ([types_list (in-list t)]
                                [arg_list (in-list n)])
                               (type-bind arg_list types_list)))
                           (define call-env (append extension tenv))
                           (FunT t (type-check b call-env)))
                         (error 'type-check "SHEQ: wrong number of arguments, got ~e, needed ~e"
                                (length t) (length n)))]
    [(AppC f args) (define type-func (type-check f tenv))
                   (match type-func
                     [(FunT arg ret) (if (= (length args) (length arg))
                                         (for ([a (in-list args)]
                                               [ar (in-list arg)])
                                           (define type-args (type-check a tenv))
                                           (if (equal-types? type-args ar)
                                               (NullT)
                                               (error 'type-check "SHEQ: type mismatch. expected ~e, got ~e"
                                                      type-args ar)))
                                         (error 'type-check "SHEQ: wrong number of arguments, got ~e, needed ~e"
                                                (length args) (length arg))) ret]
                     [_ (error 'type-checker "SHEQ: attempt to call non-function, ~e" expr)])]
    [(RecC type arg func body) (define extension (list (type-bind arg type)))
                               (define rec-env  (append extension tenv))
                               (define type-func (type-check func rec-env))
                               (if (equal-types? type type-func)
                                   (type-check body rec-env)
                                   (error 'type-check "SHEQ: type mismatch. expected ~e got ~e" type type-func))]))

;this is a helper function for the interp function that will do all the interps for the PrimV operators
;takes in a sumbol and the operands and uses a matching pattern to find the correct primop to use
(define (primv-interp [sym : Symbol] [operands : (Listof Value)] [store : Store]) : Value
  (match (list sym operands)
    [(list '+ (list (NumV a) (NumV b))) (NumV (+ a b))]
    [(list '- (list (NumV a) (NumV b))) (NumV (- a b))]
    [(list '* (list (NumV a) (NumV b))) (NumV (* a b))]
    [(list '/ (list (NumV a) (NumV b))) (if (zero? b)
                                            (error 'primv-interp
                                                   "SHEQ: can't do division by ~e" b) (NumV (/ a b)))]
    [(list '<= (list (NumV a) (NumV b))) (if (<= a b)
                                             (BoolV #t)
                                             (BoolV #f))]
    [(list 'strlen (list (StrV s))) (NumV (string-length s))]
    [(list 'num-eq? (list (NumV a) (NumV b))) (if (equal? a b)
                                                  (BoolV #t)
                                                  (BoolV #f))]
    [(list 'str-eq? (list (StrV a) (StrV b))) (if (equal? a b)
                                                  (BoolV #t)
                                                  (BoolV #f))]
    [(list 'substring (list (StrV s) (NumV start) (NumV stop)))
     (if (and (>= stop start)
              (and (exact-integer? start) (>= start 0))
              (and (exact-integer? stop) (>= stop 0))
              (<= start (string-length s))
              (<= stop (string-length s)))
         (StrV (substring s start stop))
         (error 'primv-interp "SHEQ: invalid start and stop indices ~e ~e" start stop))]
    [(list 'make-array (list (NumV s) fill))
     (if (exact-integer? s)
         (if (>= s 1)
             (let ([base (allocate store s)])
               (for ([i (in-range base (+ base s))])
                 (vector-set! store i fill))
               (ArrayV base s))
             (error 'primv-interp "SHEQ: array must have a length that is positive: ~e"s))
         (error 'primv-interp "SHEQ: array length must be a whole number: ~e" s))
     ]
    [(list 'alen arr) (NumV (length arr))]
    [(list 'aref (list (ArrayV location length) (NumV num)))
     (if (and (>= num 0) (< num length))
         (vector-ref store (+ location (cast num Natural)))
         (error 'primv-interp "SHEQ: index out of bounds ~e" num))]
    [(list 'aset! (list (ArrayV location length) (NumV n) fill))
     (if (exact-integer? n)
         (if (and (>= n 0) (< n length))
             (vector-set! store (+ location n) fill)
             (error 'primv-interp "SHEQ: index out of bounds ~e" n))
         (error 'primv-interp "SHEQ: index must be a whole number ~e" n))
     
     (NullV)]
    [(list '+ (list _ _)) (error 'primv-interp "SHEQ: need numbers for + ~e" operands)]
    [(list '- (list _ _)) (error 'primv-interp "SHEQ: need numbers for - ~e" operands)]
    [(list '* (list _ _)) (error 'primv-interp "SHEQ: need numbers for * ~e" operands)]
    [(list '/ (list _ _)) (error 'primv-interp "SHEQ: need numbers for / ~e" operands)]
    [(list '<= (list _ _)) (error 'primv-interp "SHEQ: need numbers for <= ~e" operands)]
    [(list 'strlen (list _ )) (error 'primv-interp "SHEQ: need a string to get the length")]
    [(list '+ args) (error 'primv-interp "SHEQ: need two arguments for + ~e" operands)]
    [(list '- args) (error 'primv-interp "SHEQ: need two arguments for - ~e" operands)]
    [(list '* args) (error 'primv-interp "SHEQ: need two arguments for * ~e" operands)]
    [(list '/ args) (error 'primv-interp "SHEQ: need two arguments for / ~e" operands)]
    [(list '<= args) (error 'primv-interp "SHEQ: need two arguments for <= ~e" operands)]
    [(list 'strlen args) (error 'primv-interp "SHEQ: need 1 string to get the length")]
    [(list 'substring args) (error 'primv-interp "SHEQ: need a string, a start, and a stop variable to subst")]
    [(list 'num-eq? args) (error 'primv-interp "SHEQ: need two arguments to see if they are equal")]
    [(list 'str-eq? args) (error 'primv-interp "SHEQ: need two arguments to see if they are equal")]))

;(struct RecC ([type : Types] [arg : Symbol] [func : ExprC] [body : ExprC]) #:transparent)
;takes in an ExprC that was outputted by the parser and an environment and interprets the ExprC to
;give the output as a value which can be a real, boolean, string, closure, or prim op
(define (interp [exp : ExprC] [env : Environment] [store : Store]) : Value
  (match exp
    [(NumC n) (NumV n)]
    [(strC s) (StrV s)]
    [(idC i) (lookup i env store)]
    [(lambdaC types args body) (CloV args body env)]
    [(SeqC a) (define arg-vals : (Listof Value) (map (lambda ([arg : ExprC])
                                                       (interp arg env store)) a)) (last arg-vals)]
    [(MutC id expr)
     (mutate id (interp expr env store) env store)
     (NullV)]
    [(AppC f a)
     (define fun (interp f env store))
     (define arg-vals : (Listof Value) (map (lambda ([arg : ExprC]) (interp arg env store)) a))
     (match fun
       [(CloV p b e)
        (if (= (length p) (length arg-vals))
            (let ()
              (define extension : (Listof Binding)
                (for/list : (Listof Binding)
                  ([params_list : Symbol (in-list p)]
                   [arg_list : Value (in-list arg-vals)])
                  
                  (let ()
                    (define new-loc (allocate store 1))
                    (vector-set! store new-loc arg_list)
                    (Binding params_list new-loc))))
              (define call-env (append extension e))
              (interp b call-env store))
            (error 'interp "SHEQ: wrong number of arguments: need ~e, got ~e"
                   (length p) (length arg-vals)))]
       [(PrimV op) (primv-interp op arg-vals store)]
       [_  (error 'interp "SHEQ: attempted to call a non-function")])]
    [(ifC test then else)
     (define interp_test (interp test env store))
     (match interp_test
       [(BoolV b) (if b
                      (interp then env store)
                      (interp else env store))]
       [_ (error 'interp "SHEQ: if expression must be a boolean value")])]
    [(RecC type arg func body) (let ()
                                 (define new-loc (allocate store 1))
                                 (vector-set! store new-loc (NullV))
                                 (define extension (list (Binding arg new-loc)))
                                 (define call-env (append extension env))
                                 (mutate arg (interp func call-env store) call-env store)
                                 (interp body call-env store))]))

;top-interp combines all of the functions into one function that will interpret what the user gives it
(define (top-interp [s : Sexp]) : String
  (define expr : Types (type-check (parse s) base-tenv))
  (serialize (interp (parse s) top-env (make-initial-store 2000))))


;accepts a guard fucntion and a body function and keeps running the body until guard returns false
(define while '{let {[while = "temp"]}
                 in
                 {seq
                  {while := {lambda ([guard] [body]) : {if {guard}
                                                           {seq {body} {while guard body}}
                                                           false}}}
                  while}
                 end})

;accepts an array of numbers and its size and returns true if the array is in strictly increasing order
(define in-order '{lambda ([intarray arr] [num size]) :
                    {let {[num i = 0]
                          [str ok = true]}
                      in
                      {seq
                       {while
                        {lambda () : (if ok {<= i {- size 2}} false)}
                        {lambda () :
                          {seq
                           {if {<= {aref arr {+ i 1}} {aref arr i}}
                               {ok := false}
                               true}
                           {i := {+ i 1}}}}}
                       ok}
                      end}})



;TESTS
;lookup
(check-exn (regexp (regexp-quote "SHEQ: id not found 'no-such"))
           (lambda () (lookup  'no-such top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: id not found 'no-such"))
           (lambda () (type-lookup  'no-such base-tenv)))

; allocate
(check-exn (regexp (regexp-quote "SHEQ: out of memory 3"))
           (lambda () (allocate (vector (NumV 1) (BoolV #f)) 2)))


;array-primvs
(define store1 (make-initial-store 30))
(define arr (primv-interp 'make-array (list (NumV 2) (NumV 1)) store1 ))
(check-equal? (primv-interp 'aref (list arr (NumV 0)) store1) (NumV 1))
(check-equal? (primv-interp 'aref (list arr (NumV 1)) store1) (NumV 1))
(primv-interp 'aset! (list arr (NumV 0) (NumV 4)) store1)
(check-equal? (primv-interp 'aref (list arr (NumV 0)) store1) (NumV 4))


(check-exn (regexp (regexp-quote "SHEQ: array must have a length that is positive: -2"))
           (lambda () (primv-interp  'make-array (list (NumV -2) (NumV 1)) store1 )))

(check-exn (regexp (regexp-quote "SHEQ: array length must be a whole number: 2.1"))
           (lambda () (primv-interp  'make-array (list (NumV 2.1) (NumV 1)) store1 )))

(check-exn (regexp (regexp-quote "SHEQ: index out of bounds 9"))
           (lambda () (primv-interp  'aset! (list arr (NumV 9) (NumV 4)) store1 )))

(check-exn (regexp (regexp-quote "SHEQ: index must be a whole number 2.3" ))
           (lambda () (primv-interp  'aset! (list arr (NumV 2.3) (NumV 4)) store1 )))

(check-exn (regexp (regexp-quote "SHEQ: index out of bounds 4" ))
           (lambda () (primv-interp  'aref (list arr (NumV 4)) store1 )))

(check-equal? (serialize (primv-interp 'make-array (list (NumV 3) (NumV 7)) (make-initial-store 100))) "#<array>")
(check-equal? (primv-interp 'alen (list arr) store1) (NumV 1))

(check-exn (regexp (regexp-quote "SHEQ: cannot allocate 0 cells"))
           (lambda () (allocate store1 0)))

#;(check-equal? (top-interp
                 (list 'let (list (list 'while '= while))                       
                       'in
                       (list 'let (list (list 'in-order '= in-order))            
                             'in '(in-order (array 1 3 7 10) 4) 'end)
                       'end)) "true")



;interp
(check-equal? (interp (parse '{let {[num x = 5]}
                                in
                                {let {[{num -> num} func = {lambda () : {x := 10}}]}
                                  in
                                  {func}
                                  end}
                                end}) top-env (make-initial-store 20))
              (NullV))
(check-exn (regexp (regexp-quote "SHEQ: cannot mutate unbound id 'x"))
           (lambda () (interp (parse '{x := 10}) top-env (make-initial-store 20))))
(check-equal? (interp (NumC 17) top-env (make-initial-store 100)) (NumV 17))
(check-equal? (interp (strC "Hello there") top-env (make-initial-store 100)) (StrV "Hello there"))
(check-equal? (interp (idC 'true) top-env (make-initial-store 100)) (BoolV #t))
(check-equal? (interp (idC 'false) top-env (make-initial-store 100)) (BoolV #f))
(check-equal? (interp (AppC (lambdaC (list (NumT)) '(x)  (idC 'x)) (list (NumC 42)))
                      top-env (make-initial-store 100)) (NumV 42))
(check-equal? (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y) (AppC (idC '+) (list (idC 'x) (idC 'y))))
                            (list (NumC 5) (NumC 6))) top-env (make-initial-store 100)) (NumV 11))
(check-equal? (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y) (AppC (idC '-) (list (idC 'x) (idC 'y))))
                            (list (NumC 5) (NumC 6))) top-env (make-initial-store 100)) (NumV -1))
(check-equal? (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y) (AppC (idC '*) (list (idC 'x) (idC 'y))))
                            (list (NumC 5) (NumC 6))) top-env (make-initial-store 100)) (NumV 30))
(check-equal? (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y) (AppC (idC '/) (list (idC 'x) (idC 'y))))
                            (list (NumC 6) (NumC 6))) top-env  (make-initial-store 100)) (NumV 1))
(check-equal? (interp (AppC (lambdaC  (list (NumT) (NumT)) '(x y) (AppC (idC '<=) (list (idC 'x) (idC 'y))))
                            (list (NumC 5) (NumC 6))) top-env (make-initial-store 100)) (BoolV #t))
(check-equal? (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y) (AppC (idC '<=) (list (idC 'x) (idC 'y))))
                            (list (NumC 6) (NumC 5))) top-env (make-initial-store 100)) (BoolV #f))
(check-equal? (interp (AppC (lambdaC (list (StrT)) '(x) (AppC (idC 'strlen) (list (idC 'x))))
                            (list (strC "hello") )) top-env (make-initial-store 100)) (NumV 5))
(check-equal? (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y) (AppC (idC 'num-eq?) (list (idC 'x) (idC 'y))))
                            (list (NumC 5) (NumC 6))) top-env (make-initial-store 100)) (BoolV #f))
(check-equal? (interp (AppC (lambdaC (list (StrT) (StrT)) '(x y) (AppC (idC 'str-eq?) (list (idC 'x) (idC 'y))))
                            (list (strC "hi") (strC "hi"))) top-env (make-initial-store 100)) (BoolV #t))
(check-equal? (interp (AppC (lambdaC (list (StrT) (StrT)) '(x y) (AppC (idC 'str-eq?) (list (idC 'x) (idC 'y))))
                            (list (strC "hi") (strC "hie"))) top-env (make-initial-store 100)) (BoolV #f))
(check-equal? (interp {AppC {lambdaC (list (NumT) (NumT)) '(z y) {AppC {idC '+} {list {idC 'z} {idC 'y}}}}
                            {list {AppC {idC '+} {list {NumC 9} {NumC 14}}} {NumC 98}}}
                      top-env (make-initial-store 100)) {NumV 121})
(check-equal? (interp (ifC (idC 'true) (NumC 1) (NumC 0)) top-env (make-initial-store 100)) (NumV 1))
(check-equal? (interp (ifC (idC 'false) (NumC 1) (NumC 0)) top-env (make-initial-store 100)) (NumV 0))
(check-equal? (primv-interp 'substring (list (StrV "apple") (NumV 2) (NumV 4))
                            (make-initial-store 100)) (StrV "pl"))
(check-equal? (primv-interp 'substring (list (StrV "apple") (NumV 2) (NumV 2))
                            (make-initial-store 100)) (StrV ""))
(check-equal? (primv-interp 'substring (list (StrV "apple") (NumV 0) (NumV 4))
                            (make-initial-store 100)) (StrV "appl"))
(check-equal? (primv-interp 'substring (list (StrV "apple") (NumV 0) (NumV 5))
                            (make-initial-store 100)) (StrV "apple"))
(check-equal? (interp (parse '{rlet {[{num -> num}
                              square-helper =
                              {lambda {[num n]} : {if {<= n 0} 0 {+ n {square-helper {- n 2}}}}}]}
                            in {let {[{num -> num}
                                      square =
                                      {lambda {[num n]} : {square-helper {- {* 2 n} 1}}}]}
                                 in {square 13}
                                 end}
                            end})
                      top-env
                      (make-initial-store 2000))
              (NumV 169))

(check-exn (regexp (regexp-quote "SHEQ: invalid start and stop indices 6 4"))
           (lambda () (primv-interp 'substring (list (StrV "apple") (NumV 6) (NumV 4)) (make-initial-store 100))))
(check-exn (regexp (regexp-quote "SHEQ: invalid start and stop indices 3.0 5.0"))
           (lambda () (primv-interp 'substring (list (StrV "apple") (NumV 3.0) (NumV 5.0)) (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: if expression must be a boolean value"))
           (lambda () (interp (ifC (idC '+) (NumC 1) (NumC 0)) top-env (make-initial-store 100))))
(check-exn (regexp (regexp-quote "SHEQ: can't do division by 0"))
           (lambda () (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y) (AppC (idC '/) (list (idC 'x) (idC 'y))))
                                    (list (NumC 6) (NumC 0))) top-env (make-initial-store 100))))
(check-exn (regexp (regexp-quote "SHEQ: wrong number of arguments"))
           (lambda () (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y) (idC 'x)) (list (NumC 1)))
                              top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: attempted to call a non-function"))
           (lambda () (interp (AppC (NumC 0) (list)) top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need two arguments for /"))
           (lambda () (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y)
                                             (AppC (idC '/) (list (idC 'x) (idC 'y) (NumC 5))))
                                    (list (NumC 6) (NumC 0))) top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need two arguments for +"))
           (lambda () (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y)
                                             (AppC (idC '+) (list (idC 'x) (idC 'y) (NumC 5))))
                                    (list (NumC 6) (NumC 0))) top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need two arguments for -"))
           (lambda () (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y)
                                             (AppC (idC '-) (list (idC 'x) (idC 'y) (NumC 5))))
                                    (list (NumC 6) (NumC 0))) top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need two arguments for *"))
           (lambda () (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y)
                                             (AppC (idC '*) (list (idC 'x) (idC 'y) (NumC 5))))
                                    (list (NumC 6) (NumC 0))) top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need two arguments for <="))
           (lambda () (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y)
                                             (AppC (idC '<=) (list  (NumC 5))))
                                    (list (NumC 6) (NumC 0))) top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need 1 string to get the length"))
           (lambda () (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y)
                                             (AppC (idC 'strlen)
                                                   (list (idC 'x) (idC 'y) (NumC 5))))
                                    (list (NumC 6) (NumC 0))) top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need a string, a start, and a stop variable to subst"))
           (lambda () (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y) (AppC (idC 'substring)
                                                                               (list (idC 'x) (idC 'y) (NumC 5))))
                                    (list (NumC 6) (NumC 0))) top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need two arguments to see if they are equal"))
           (lambda () (interp (AppC (lambdaC (list (NumT) (NumT)) '(x y) (AppC (idC 'num-eq?)
                                                                               (list (idC 'x) (idC 'y) (NumC 5))))
                                    (list (NumC 6) (NumC 0))) top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need two arguments to see if they are equal"))
           (lambda () (interp (AppC (lambdaC (list (StrT) (StrT)) '(x y) (AppC (idC 'str-eq?)
                                                                               (list (idC 'x) (idC 'y) (NumC 5))))
                                    (list (strC "6") (strC "0"))) top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need numbers for +"))
           (lambda () (interp (AppC (lambdaC (list (StrT) (NumT)) '() (AppC (idC '+) (list (strC "hi") (NumC 5)))) '())
                              top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need numbers for -"))
           (lambda () (interp (AppC (lambdaC (list (StrT) (NumT)) '() (AppC (idC '-) (list (strC "hi") (NumC 5)))) '())
                              top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need numbers for *"))
           (lambda () (interp (AppC (lambdaC (list (StrT) (NumT)) '() (AppC (idC '*) (list (strC "hi") (NumC 5)))) '())
                              top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need numbers for /"))
           (lambda () (interp (AppC (lambdaC (list (StrT) (NumT)) '() (AppC (idC '/) (list (strC "hi") (NumC 5)))) '())
                              top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need numbers for <="))
           (lambda () (interp (AppC (lambdaC (list (StrT) (NumT)) '() (AppC (idC '<=) (list (strC "hi") (NumC 5)))) '())
                              top-env (make-initial-store 100))))

(check-exn (regexp (regexp-quote "SHEQ: need a string to get the length"))
           (lambda () (interp (AppC (lambdaC (list (NumT)) '() (AppC (idC 'strlen) (list (NumC 5)))) '())
                              top-env (make-initial-store 100))))
(check-equal? (type-check (parse '{let {[num x = 0]} in {seq {x := 42} x}  end}) base-tenv) (NumT))
(check-equal? (interp (parse '{let {[num x = 0]} in {seq {x := 42} x}  end}) top-env (make-initial-store 50)) (NumV 42))
;serialize
(check-equal? (serialize (BoolV #t)) "true")
(check-equal? (serialize (BoolV #f)) "false")
(check-equal? (serialize (NumV 5)) "5")
(check-equal? (serialize (StrV "hello")) "\"hello\"")
(check-equal? (serialize (PrimV '+)) "#<primop>")
(check-equal? (serialize (CloV (list '+) (NumC 5) top-env)) "#<procedure>")
(check-equal? (serialize (NullV)) "null")

;; parse tests
(check-equal? (parse 17) (NumC 17))
(check-equal? (parse "hello") (strC "hello"))
(check-equal? (parse 'true) (idC 'true))
(check-equal? (parse 'false) (idC 'false))
(check-equal? (parse '{+ 1 2}) (AppC (idC '+)
                                     (list (NumC 1) (NumC 2))))
(check-equal? (parse '{- 10 4}) (AppC (idC '-)
                                      (list (NumC 10) (NumC 4))))
(check-equal? (parse '{* 37 2}) (AppC (idC '*)
                                      (list (NumC 37) (NumC 2))))
(check-equal? (parse '{/ 4 0}) (AppC (idC '/)
                                     (list (NumC 4) (NumC 0))))
(check-equal? (parse '{<= 10 20}) (AppC (idC '<=)
                                        (list (NumC 10) (NumC 20))))
(check-equal? (parse '{substring "hello" 0 2}) (AppC (idC 'substring)
                                                     (list (strC "hello") (NumC 0) (NumC 2))))
(check-equal? (parse '{strlen "word"}) (AppC (idC 'strlen)
                                             (list (strC "word"))))
(check-equal? (parse '{equal? 0 "zero"}) (AppC (idC 'equal?)
                                               (list (NumC 0) (strC "zero"))))

(check-equal? (parse 'x) (idC 'x))
(check-equal? (parse '{if true {+ 1 1} {- 1 1}})
              (ifC (idC 'true)
                   (AppC (idC '+) (list (NumC 1) (NumC 1))) (AppC (idC '-) (list (NumC 1) (NumC 1)))))
(check-equal? (parse '{let {[num x = 2]} in {+ x 2} end})
              (AppC (lambdaC (list (NumT)) '(x) (AppC (idC '+)
                                                      (list (idC 'x) (NumC 2))))
                    (list (NumC 2))))
(check-equal? (parse '{let {[str x = "hello"] [num y = 1] [num z = 3]} in {substring x y z} end})
              (AppC (lambdaC (list (StrT) (NumT) (NumT)) '(x y z) (AppC
                                                                   (idC 'substring)
                                                                   (list (idC 'x) (idC 'y) (idC' z))))
                    (list (strC "hello") (NumC 1) (NumC 3))))
(check-equal? (parse '{rlet {[{num -> num}
                              square-helper =
                              {lambda {[num n]} : {if {<= n 0} 0 {+ n {square-helper {- n 2}}}}}]}
                            in {let {[{num -> num}
                                      square =
                                      {lambda {[num n]} : {square-helper {- {* 2 n} 1}}}]}
                                 in {square 13}
                                 end}
                            end})
              (RecC (FunT (list (NumT)) (NumT))
                    'square-helper
                    (lambdaC (list (NumT)) (list 'n)
                             (ifC
                              (AppC (idC '<=) (list (idC 'n) (NumC 0)))
                              (NumC 0)
                              (AppC (idC '+)
                                    (list (idC 'n)
                                          (AppC (idC 'square-helper)
                                                (list (AppC (idC '-) (list (idC 'n) (NumC 2)))))))))
                    (AppC
                     (lambdaC
                      (list (FunT (list (NumT)) (NumT)))
                      '(square)
                      (AppC (idC 'square)
                            (list (NumC 13))))
                     (list (lambdaC (list (NumT)) '(n)
                                    (AppC (idC 'square-helper)
                                          (list (AppC (idC '-)
                                                      (list (AppC (idC '*)
                                                                  (list (NumC 2) (idC 'n)))
                                                            (NumC 1))))))))))

(check-equal? (parse '{let {} in {+ 1 2} end})
              (AppC (lambdaC '() '() (AppC (idC '+) (list (NumC 1) (NumC 2)))) '()))
(check-equal? (parse '{lambda ([num x] [num y]) : {+ x y}})
              (lambdaC (list (NumT) (NumT)) '(x y) (AppC (idC '+) (list (idC 'x) (idC 'y)))))
(check-equal? (parse '{lambda ([num z]) : {* z 500}})
              (lambdaC (list (NumT)) '(z) (AppC (idC '*) (list (idC 'z) (NumC 500)))))
(check-equal? (parse '{lambda ([num s]) : {strlen s}})
              (lambdaC (list (NumT)) '(s) (AppC (idC 'strlen) (list (idC 's)))))
(check-exn (regexp (regexp-quote "SHEQ: Invalid s-expression '()"))
           (lambda () (parse '())))
(check-exn (regexp (regexp-quote "SHEQ: cannot have 'if as an identifier name"))
           (lambda () (parse 'if)))
(check-exn (regexp (regexp-quote "SHEQ: cannot have ': as an identifier name"))
           (lambda () (parse ':)))
(check-exn (regexp (regexp-quote "SHEQ: cannot have 'let as an identifier name"))
           (lambda () (parse 'let)))
(check-exn (regexp (regexp-quote "SHEQ: cannot have '= as an identifier name"))
           (lambda () (parse '=)))
(check-exn (regexp (regexp-quote "SHEQ: cannot have 'in as an identifier name"))
           (lambda () (parse 'in)))
(check-exn (regexp (regexp-quote "SHEQ: cannot have 'end as an identifier name"))
           (lambda () (parse 'end)))
(check-exn (regexp (regexp-quote "SHEQ: functions cannot have multiple paramaters with the same identifier"))
           (lambda () (parse '{lambda ([num x] [num x]) : (+ x x)})))

(check-exn (regexp (regexp-quote "SHEQ: duplicate parameter"))
           (lambda () (parse '(let ((num z = (lambda () : 3)) (num z = 9)) in (z) end))))

(check-exn (regexp (regexp-quote "SHEQ: cannot have if, :, let, in, end, = as params"))
           (lambda () (parse '(let ((str let = "")) in "World" end))))
(check-equal? (parse '{x := 20}) (MutC 'x (NumC 20)))
(check-equal? (parse '{x := "hello"}) (MutC 'x (strC "hello")))

(check-exn (regexp (regexp-quote "SHEQ: expected [<ty> <id>]; got '(num)"))
           (lambda () (parse '{lambda ([num]) : 0})))

(check-exn (regexp (regexp-quote "SHEQ: expected [<ty> <id>]; got '(num x y)"))
           (lambda () (parse '{lambda ([num x y]) : 0})))

(check-exn (regexp (regexp-quote "SHEQ: the condition must be a Boolean, got (NumT)" ))
           (lambda () (type-check (ifC (NumC 1) (NumC 1) (NumC 0)) base-tenv)))

(check-exn (regexp (regexp-quote "SHEQ: wrong number of arguments, got 1, needed 2" ))
           (lambda () (type-check (lambdaC (list (NumT)) '(x y) (idC 'x)) base-tenv)))

(check-exn (regexp (regexp-quote "SHEQ: type mismatch. expected (NumT), got (BoolT)" ))
           (lambda () (type-check (parse '{let {[bool x = 0]} in {seq {x := 42} x}  end}) base-tenv)))

(check-exn (regexp (regexp-quote "SHEQ: wrong number of arguments, got 1, needed 2"))
           (lambda () (type-check (parse '{+ 1}) base-tenv)))

(check-exn (regexp (regexp-quote "SHEQ: attempt to call non-function, (AppC (NumC 5) (list (NumC 1)))"))
           (lambda () (type-check (parse '{5 1}) base-tenv)))

(check-exn (regexp (regexp-quote "SHEQ: wrong number of arguments, got 2, needed 1"))
           (lambda () (type-check (parse '{{lambda ([intarray x]) : x} 1 2}) base-tenv)))

(check-exn (regexp (regexp-quote "not a type, 'blah"))
           (lambda () (parse '{let {[blah x = 2]} in {+ x 2} end})))

; parse-rec tests
(check-exn (regexp (regexp-quote "SHEQ: invalid syntax for rlet statement '(num let 7)"))
           (lambda () (parse-rec '[num let 7] '{if {<= let 0} "yes" "no"})))
(check-exn (regexp (regexp-quote "SHEQ: cannot have if, :, let, in, end, = as identifiers, 'let"))
           (lambda () (parse-rec '[num let = 7] '{if {<= let 0} "yes" "no"})))

(check-equal? (parse-rec
               '[{num -> num} square-helper = {lambda {[num n]} : {if {<= n 0} 0 {+ n {square-helper {- n 2}}}}}]
               '{let {[{num -> num}
                       square =
                       {lambda {[num n]} : {square-helper {- {* 2 n} 1}}}]}
                  in {square 13}
                  end})
              (RecC (FunT (list (NumT)) (NumT)) 'square-helper
                    (parse '{lambda {[num n]} : {if {<= n 0} 0 {+ n {square-helper {- n 2}}}}})
                    (parse '{let {[{num -> num}
                                   square =
                                   {lambda {[num n]} : {square-helper {- {* 2 n} 1}}}]}
                              in {square 13}
                              end})))

;; desugar tests
(check-equal? (desugar '{[num x = 1] [str y = true]} '{if y x 0})
              (AppC (lambdaC (list (NumT) (StrT)) '(x y) (ifC (idC 'y) (idC 'x) (NumC 0)))
                    (list (NumC 1) (idC 'true))))
(check-equal? (desugar '{} '{+ 50 100})
              (AppC (lambdaC '() '() (AppC (idC '+) (list (NumC 50) (NumC 100)))) '()))
(check-exn (regexp (regexp-quote "SHEQ: invalid syntax for let statement"))
           (lambda () (desugar 'what 'there)))
(check-exn (regexp (regexp-quote "SHEQ: cannot have if, :, let, in, end, = as params"))
           (lambda () (desugar '{[str let = 12]} '{+ 1 2})))
(check-exn (regexp (regexp-quote "SHEQ: duplicate parameter"))
           (lambda () (desugar '{[num x = 12] [num x = 3]} '{+ x x})))

;; mutate tests
(define test-store : Store (vector (NumV 3) (NumV 20) (NumV 55)))
(define test-env : Environment (list (Binding 'x 1) (Binding 'y 2)))
(check-equal? (let ()
                (mutate 'x (NumV 11) test-env test-store)
                (vector-ref test-store (ann 1 Natural))) (NumV 11))
(check-equal? (mutate 'y (NumV 11) test-env test-store) (NullV))
(check-exn (regexp (regexp-quote "SHEQ: cannot mutate unbound id 'z"))
           (lambda () (mutate 'z (NumV 1) test-env test-store)))

;; type-check tests
(check-equal? (type-check (RecC (FunT (list (NumT)) (NumT)) 'square-helper
                    (parse '{lambda {[num n]} : {if {<= n 0} 0 {+ n {square-helper {- n 2}}}}})
                    (parse '{let {[{num -> num}
                                 square =
                                 {lambda {[num n]} : {square-helper {- {* 2 n} 1}}}]}
                            in {square 13}
                            end}))
                          base-tenv)
              (NumT))
(check-exn (regexp (regexp-quote "SHEQ: type mismatch. expected (NumT) got (BoolT)"))
           (lambda () (type-check (RecC
                                   (NumT)
                                   'test
                                   (AppC (idC '<=)
                                         (list (NumC 0) (NumC 5)))
                                   (NumC 5))
                                  base-tenv)))

;; checking-dups tests
(check-equal? (check-duplicates '(x y z)) #f)
(check-equal? (check-duplicates '(x y x)) 'x)

(check-equal? (equal-types? (BoolT) (BoolT))#t)
(check-equal? (equal-types? (IntarrayT) (IntarrayT))#t)
(check-equal? (equal-types? (FunT (list (NumT) (NumT)) (NumT)) (FunT (list (NumT) (NumT)) (NumT))) #t)
(check-equal? (equal-types? (BoolT) (NumT)) #f)

;top-interp tests

(check-equal? (top-interp '{let {[str x = "hello"] [num y = 1] [num z = 3]} in {substring x y z} end}) "\"el\"")

(check-equal? (top-interp '{let {[{num -> num} f = {lambda ([num n]) : {+ n 1}}]}
                             in
                             {f 10}
                             end}) "11")
(check-equal? (top-interp '{if {num-eq? 4 {+ 2 2}} true false}) "true")

(top-interp '{let {[{num -> num} f = {lambda ([num n]) : {+ n 1}}]}
                             in
                             {f 10}
                             end})
;(top-interp '{{lambda ([num x] [num y]) : (+ x z)} 5 6})

(top-interp '{rlet {[{num -> num}
                              square-helper =
                              {lambda {[num n]} : {if {<= n 0} 0 {+ n {square-helper {- n 2}}}}}]}
                            in {let {[{num -> num}
                                      square =
                                      {lambda {[num n]} : {square-helper {- {* 2 n} 1}}}]}
                                 in {square 13}
                                 end}
                            end})

(top-interp '{rlet {[{num -> num} fact = {lambda {[num n]} : 
                                           {if (<= n 0) 
                                               1
                                               {* n {fact {- n 1}}}}}]}
                    in {fact 6}
                    end})

