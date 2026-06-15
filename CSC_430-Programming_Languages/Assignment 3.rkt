#lang typed/racket
(require typed/rackunit)

(define-type ExprC (U binopC NumC AppC idC ifleq0))

(struct AppC ([func : Symbol] [arg : ExprC]) #:transparent)
(struct NumC ([n : Real]) #:transparent)
(struct binopC ([op : Symbol] [left : ExprC] [right : ExprC]) #:transparent)
(struct idC ([s : Symbol]) #:transparent)
(struct ifleq0 ([test : ExprC] [then : ExprC] [else : ExprC]) #:transparent)
;ask how to change arg to a list of symbols
(struct FunDefC [(def : Symbol) (name : Symbol) (params : (Listof Any)) (colon : Symbol) (body : ExprC)] #:transparent)
;(struct ProgC [program : (Listof FunDefC)])

(define op-hash-table
  (hash '+ +
        '- -
        '* *
        '/ (lambda ([a : Real] [b : Real]) (if (zero? b) (error 'interp "cant do division by 0") (/ a b)
                             ))))

;takes an s-expression and parses it
(define (parse [e : Sexp]) : ExprC
  (match e
    [(? real? n) (NumC n)]
    [(? symbol? s) (idC s)]
    [(list (? symbol? op) a b) (binopC op (parse a) (parse b))]
    [(list 'ifleq0? test then else) (ifleq0 (parse test) (parse then) (parse else))]
    [(list (? symbol? f) args) (AppC f (parse args))]
    [_ (error 'parse "Invalid s-expression")]))

;takes in an s-expression with a function definition and parses it
(define (parse-fundef [e : Sexp]) : FunDefC
  (match e
    [(list 'def (list (? symbol? f) (? symbol? params) ...) ': body) (FunDefC 'def f params ': (parse body))]
    [_ (error 'parse-fundef "bad function call")]))

;takes in an s-expression with multiple functions and parse it
(define (parse-prog [e : Sexp]) : (Listof FunDefC)
    (error 'parse-prog "TODO"))

;Tests
(check-equal? (parse '{+ 3 4}) (binopC '+ (NumC 3) (NumC 4)))
(check-equal? (parse '{ifleq0? 5 10 20}) (ifleq0 (NumC 5) (NumC 10) (NumC 20)))
(check-equal? (parse 'x) (idC 'x))
(check-equal? (parse '(f (+ x 4))) (AppC 'f (binopC '+ (idC 'x) (NumC 4))))
(check-exn (regexp (regexp-quote "Invalid s-expression"))
           (lambda () (parse '())))
(check-equal? (parse-fundef '(def (f x) : (double  x) )) (FunDefC 'def 'f '(x) ': (AppC 'double (idC 'x))))
(check-exn (regexp (regexp-quote "bad function call"))
           (lambda () (parse-fundef '())))