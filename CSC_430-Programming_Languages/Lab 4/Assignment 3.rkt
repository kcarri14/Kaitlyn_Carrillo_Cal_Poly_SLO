#lang typed/racket
;Full project implemented and all tests passed when handed in 

(require typed/rackunit)

;<prog> ::= {<defn>*}
(define-type ProgC (Listof FunDefC))

;<defn> ::= { def <id> (<id>*) : <expr> }
;ask how to change arg to a list of symbols
(struct FunDefC [(name : Symbol) (params : (Listof Symbol)) (body : ExprC)] #:transparent)

;<expr> :: = <num>
;            {<op> <left> <right>}
;            {<id> <expr>...}
;            { ifleq0? ‹expr› ‹expr› ‹expr› }
;            {<id>
(define-type ExprC (U binopC NumC AppC idC ifleq0))
(struct NumC ([n : Real]) #:transparent)
(struct binopC ([op : Symbol] [left : ExprC] [right : ExprC]) #:transparent)
(struct AppC ([func : Symbol] [arg : (Listof ExprC)]) #:transparent)
(struct ifleq0 ([test : ExprC] [then : ExprC] [else : ExprC]) #:transparent)
(struct idC ([s : Symbol]) #:transparent)

;This is a look-up function for the binopC to get the arithmetic operation
(define op-hash-table
  (hash '+ +
        '- -
        '* *
        '/ (lambda ([a : Real] [b : Real]) (if (zero? b) (error 'interp "SHEQ: can't do division by zero") (/ a b)))
        ))

;this function defines what the binops are so that symbols can be compared by them and either error if there are used
;in the wrong place or be used to check that only binops are going through
(define (binops? a) (or (equal? a '+) (equal? a '-) (equal? a '*) (equal? a '/)))

;this function defines what symbols can not be
;cnbt = can not be this
(define (cnbt? s)
  (or (binops? s) (equal? s 'def) (equal? s 'ifleq0?) (equal? s ':)))


;This function takes an s-expression and parses it and outputs an ExprC
(define (parse [e : Sexp]) : ExprC
  (match e
    [(? real? n) (NumC n)]
    [(? cnbt? (? symbol? s))
     (error 'parse "SHEQ: cannot have +,-,/,*,def,:,ifleq0? as a identifier name")]
    [(? symbol? s) (idC s)]
    [(list 'ifleq0? test then else) (ifleq0 (parse test) (parse then) (parse else))]
    [(list (? binops? (? symbol? op)) (? cnbt? a)  b)
     (error 'parse "SHEQ: cannot have +,-,/,*,def,:,ifleq0? as a parameter name" )]
    [(list (? binops? (? symbol? op)) a (? cnbt? b))
     (error 'parse "SHEQ: cannot have +,-,/,*,def,:,ifleq0? as a parameter name" )]
    [(list (? binops? (? symbol? op)) a b) (binopC op (parse a) (parse b))]
    [(list (? cnbt? (? symbol? f)) args ...)
     (error 'parse "SHEQ: cannot have +,-,/,*,def,:,ifleq0? as a function name")]
    [(list (? symbol? f) args ...) (AppC f (for/list ([arg (in-list (cast args (Listof Sexp)))])(parse arg)))]
    [_ (error 'parse "SHEQ: Invalid s-expression")]))


;This function checks if there are duplicates in the function parameters
(define (checking-dups [params : (Listof Symbol)]) : (U Symbol #f)
  (check-duplicates params eq?))

;This function takes in an s-expression with a function definition and parses it and outputs a FunDefC

(define (parse-fundef [e : Sexp]) : FunDefC
  (match e
    [(list 'def (? cnbt? (? symbol? f)) (list (? symbol? params) ...) ': body)
     (error 'parse-fundef "SHEQ: can't have +,-,*,/, def,ifleq0?, or : as a function name ")]
    [(list 'def (? symbol? f) (list (? symbol? params) ...) ': body)
     (if (checking-dups (cast params (Listof Symbol)))
         (error 'parse-fundef "SHEQ: Cannot have duplicate identifiers in function call")
         (FunDefC  f ( cast params (Listof Symbol)) (parse body))) ]
    [_ (error 'parse-fundef "SHEQ: bad function call")]))


;This function takes in an s-expression with multiple functions and parse it and outputs a list of FunDefC
(define (parse-prog [e : Sexp]) : (Listof FunDefC)
  (match e
    [(list fundefs ...) (for/list : (Listof FunDefC)
                          ([func (in-list ( cast fundefs (Listof Sexp)))]) (parse-fundef func))]
    [_ (error 'parse_prog "SHEQ: Bad Syntax: program must be a list of def functions")]))


;; subst takes in an ExprC to replace a name with, the symbol of the name to be replaced, and the ExprC to do this in.
;; Returns an ExprC with the name replaced with an ExprC
;; The first argument is what to replace the name with. The second argument is the name to be replaced.
;; The third argument is the expression this will take place in.
(define (subst [sub : ExprC] [name : Symbol] [body : ExprC]) : ExprC
  (match body
    [(NumC n) body]
    [(idC s) (cond
               [(symbol=? s name) sub]
               [else body])]
    [(AppC f a) (AppC f (map (lambda ([x : ExprC]) (subst sub name x)) a))]
    [(binopC op l r) (binopC op (subst sub name l) (subst sub name r))]
    [(ifleq0 test then else) (ifleq0 (subst sub name test) (subst sub name then) (subst sub name else))]))

;this function makes the interp eager by evaluating the functions first instead of substituting first 
(define (evaluate [args : (Listof ExprC)] [funs : (Listof FunDefC)]) : (Listof ExprC)
  (for/list : (Listof ExprC) ([arg (in-list args)])
                        (NumC(interp arg funs))))

;; interp interprets the given expression, using the list of funs
;; Takes an ExprC and list of FunDefC as input
;; returns the evaluation of the expression as a Real
(define (interp [exp : ExprC] [funs : (Listof FunDefC)]) : Real
  (match exp
    [(NumC n) n]
    [(AppC f a) (define fun (get-fundef f funs))
                (if (= (length a) (length (FunDefC-params fun)))
                    (interp (subst-AppC (evaluate a funs)
                                    (FunDefC-params fun)    
                                    (FunDefC-body fun)) funs) (error 'interp "SHEQ: wrong number of arguments"))]
    [(binopC op left right) ((hash-ref op-hash-table op) (interp left funs) (interp right funs))]
    [(ifleq0 test then else) (if (<= (interp test funs) 0)
                                 (interp then funs)
                                 (interp else funs))]
    [(idC s) (error 'interp "SHEQ: unbound IdC ~e" s)]))


;; get-fundef takes a name and a list of FunDefC and returns the FunDefC with the same name
;; on failure, errors
;; takes a symbol and list of FunDefC as input
;; returns a FunDefC with the same name as the symbol
(define (get-fundef [n : Symbol] [fds : (Listof FunDefC)]) : FunDefC
  (cond
    [(empty? fds)
     (error 'get-fundef "SHEQ: reference to undefined function")]
    [(cons? fds)
     (cond
       [(equal? n (FunDefC-name (first fds))) (first fds)]
       [else (get-fundef n (rest fds))])]))


;; subst-AppC takes a list of args, list of params, a function body, and
;; returns the body with all parameters substituted with arguments.
;; Takes a list of ExprC, list of Symbol, and an ExprC as input
;; returns an ExprC with all parameters substituted
(define (subst-AppC [args : (Listof ExprC)] [fun-params : (Listof Symbol)] [fun-body : ExprC]) : ExprC
  (match args
    ['() fun-body]
    [(cons f r) (subst-AppC (rest args) (rest fun-params) (subst (first args) (first fun-params) fun-body))]))


;; interp-fns interprets the function 'main' from the fundefs
;; takes a list of FunDefC as input and
;; returns the evaluation of the function "main"
(define (interp-fns [funs : (Listof FunDefC)]) : Real
    (interp (FunDefC-body (get-fundef 'main funs)) funs))


;; top-interp parses and evaluates Sexps
;; takes an Sexp representing a program as input and
;; returns the evaluation of the program 
(define (top-interp [fun-sexps : Sexp]) : Real
    (interp-fns (parse-prog fun-sexps)))


;Tests

;parse tests
(check-equal? (parse '{+ 3 4}) (binopC '+ (NumC 3) (NumC 4)))
(check-equal? (parse '{ifleq0? 5 10 20}) (ifleq0 (NumC 5) (NumC 10) (NumC 20)))
(check-equal? (parse 'x) (idC 'x))
(check-equal? (parse '{f {+ x 4}}) (AppC 'f (list (binopC '+ (idC 'x) (NumC 4)))))
(check-equal? (parse '{f { g {+ x 4}}}) (AppC 'f (list (AppC 'g (list (binopC '+ (idC 'x) (NumC 4)))))))
(check-equal? (parse '{f x y}) (AppC 'f (list (idC 'x) (idC 'y))))
(check-equal? (parse '{+ x y})
              (binopC '+ (idC 'x) (idC 'y)))
(check-equal? (parse '{* 2 3})
              (binopC '* (NumC 2) (NumC 3)))
(check-equal? (parse '{foo 1 2})
              (AppC 'foo (list (NumC 1) (NumC 2))))

(check-equal? (parse 'foo) (idC 'foo))

(check-exn (regexp (regexp-quote "SHEQ: Invalid s-expression"))
           (lambda () (parse '())))
(check-exn (regexp (regexp-quote "SHEQ: cannot have +,-,/,*,def,:,ifleq0? as a function name"))
           (lambda () (parse '{/ 3 4 5})))

(check-exn (regexp (regexp-quote "SHEQ: cannot have +,-,/,*,def,:,ifleq0? as a parameter name"))
           (lambda () (parse '{/ / 4 })))

(check-exn (regexp (regexp-quote "SHEQ: cannot have +,-,/,*,def,:,ifleq0? as a parameter name"))
           (lambda () (parse '{/ 5 + })))

(check-exn (regexp (regexp-quote "SHEQ: cannot have +,-,/,*,def,:,ifleq0? as a identifier name"))
           (lambda () (parse '/)))

;parse-fundef tests
(check-equal? (parse-fundef '{def f (x) : {double  x}}) (FunDefC 'f '(x) (AppC 'double (list (idC 'x)))))
(check-equal? (parse-fundef '{def f (x) : {+ x 2}}) (FunDefC 'f '(x) (binopC '+ (idC 'x) (NumC 2))))

(check-exn (regexp (regexp-quote "SHEQ: bad function call"))
           (lambda () (parse-fundef '{})))
(check-exn (regexp (regexp-quote "SHEQ: can't have +,-,*,/, def,ifleq0?, or : as a function name "))
           (lambda () (parse-fundef '(def * (x) : (* x 2)))))
(check-exn (regexp (regexp-quote "SHEQ: Cannot have duplicate identifiers in function call"))
           (lambda () (parse-fundef '{def f (x x y x) : (+ x x)})))

(check-equal? (parse-fundef '{def f () : {double  5}}) (FunDefC 'f '() (AppC 'double (list (NumC 5)))))
(check-equal? (parse-fundef '{def five () : 5})
              (FunDefC 'five '() (NumC 5)))

;parse-prog tests
(check-equal? (parse-prog '{{def f () : 5}
                            {def main () : {+ 2 3}}})(list (FunDefC 'f '() (NumC 5))
                                                           (FunDefC 'main '() (binopC '+ (NumC 2) (NumC 3)))))
(check-equal?
 (parse-prog '{{def five () : 5}
               {def area (w h) : {* w h}}})
 (list (FunDefC 'five '() (NumC 5))
       (FunDefC 'area '(w h) (binopC '* (idC 'w) (idC 'h)))))

(check-exn (regexp (regexp-quote "SHEQ: Bad Syntax: program must be a list of def functions"))
           (lambda () (parse-prog 'x)))


;; Interp Tests
(check-= (interp (NumC 17) '()) 17 0.1)
(check-= (interp (binopC '+ (NumC 3) (NumC 4)) '()) 7 0.1)
(check-= (interp (binopC '- (NumC 10) (NumC 7)) '()) 3 0.1)
(check-= (interp (binopC '* (NumC 4) (NumC 8)) '()) 32 0.1)
(check-= (interp (binopC '/ (NumC 30) (NumC 5)) '()) 6 0.1)
(check-= (interp (ifleq0 (NumC 5) (NumC 10) (NumC 0)) '()) 0 0.1)
(check-= (interp (ifleq0 (NumC -1) (NumC 10) (NumC 0)) '()) 10 0.1)
(check-exn (regexp (regexp-quote "SHEQ: unbound IdC 'x"))
           (lambda () (interp (idC 'x) '())))
(check-exn (regexp (regexp-quote "SHEQ: can't do division by zero"))
           (lambda () (interp (binopC '/ (NumC 2) (NumC 0)) '())))
(check-exn (regexp (regexp-quote "SHEQ: wrong number of arguments"))
           (lambda () (interp (AppC 'a (list (NumC 1) (NumC 2)))
                              (list (FunDefC 'a '(b) (binopC '+ (idC 'b) (NumC 5)))))))
(check-= (interp (AppC 'f (list (NumC 8)))
                 (list (FunDefC 'f '(x) (binopC '+ (NumC 10) (idC 'x))))) 18 0.1)
(check-= (interp (AppC 'f (list (NumC 50) (NumC 25) (NumC 20) (NumC 33)))
                 (list (FunDefC 'g '(a b c d) (binopC '+
                                                      (binopC '- (idC 'a) (idC 'b))
                                                      (binopC '* (idC 'c) (idC 'd))))
                       (FunDefC 'f '(a b c d) (binopC '+
                                                      (binopC '* (idC 'a) (idC 'b))
                                                      (binopC '- (idC 'c) (idC 'd)))))) 1237 0.1)

;; subst tests
(check-equal? (subst (NumC 5) 'x (idC 'y)) (idC 'y))
(check-equal? (subst (NumC 5) 'x (AppC 'y (list (binopC '* (idC 'x) (NumC 10)))))
              (AppC 'y (list (binopC '* (NumC 5) (NumC 10)))))
(check-equal? (subst (NumC 10) 'z (ifleq0 (idC 'z) (idC 'z) (binopC '- (idC 'z) (NumC 1))))
              (ifleq0 (NumC 10) (NumC 10) (binopC '- (NumC 10) (NumC 1))))

;; get-fundef tests
(check-equal? (get-fundef 'y (list (FunDefC 'x '(z) (NumC 5))
                                   (FunDefC 'y '(b) (binopC '+ (NumC 1) (idC 'b)))
                                   (FunDefC 'j '(u i) (NumC 5))))
              (FunDefC 'y '(b) (binopC '+ (NumC 1) (idC 'b))))
(check-exn (regexp (regexp-quote "SHEQ: reference to undefined function"))
           (lambda () (get-fundef 'a (list (FunDefC 'x '(z) (NumC 5))
                                           (FunDefC 'y '(b) (binopC '+ (NumC 1) (idC 'b)))
                                           (FunDefC 'j '(u i) (NumC 5))))))

;; subst-AppC tests
(check-equal? (subst-AppC (list (NumC 7) (NumC 2)) '(x y)
                          (binopC '+ (idC 'x) (idC 'y)))
              (binopC '+ (NumC 7) (NumC 2)))
(check-= (interp (subst-AppC (list (NumC 7) (NumC 2)) '(x y)
                             (binopC '+ (idC 'x) (idC 'y))) '()) 9 0.1)

;; interp-fns tests
(check-= (interp-fns (list (FunDefC 'f '() (NumC 5))
                           (FunDefC 'main '() (binopC '+ (NumC 2) (NumC 3))))) 5 0.1)
(check-= (interp-fns (list (FunDefC 'f '() (NumC 5))
                           (FunDefC 'main '() (binopC '+ (AppC 'f '()) (NumC 3))))) 8 0.1)

;; top-interp tests
(check-= (top-interp '{{def f () : 5}
                       {def main () : {+ 2 3}}}) 5 0.1)
(check-= (top-interp '{{def f () : 5}
                            {def main () : {+ {f} 3}}}) 8 0.1)
(check-= (top-interp '{{def f (x y) : {+ x y}}
                             {def main () : {f 1 2}}}) 3 0.1)
(check-= (top-interp '{{def f () : 5}
                             {def main () : {+ {f} {f}}}}) 10 0.1)



