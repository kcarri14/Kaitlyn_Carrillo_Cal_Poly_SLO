#lang typed/racket

(require typed/rackunit)

(define-type ExprC (U NumC strC idC ifC lambdaC AppC ))

(struct NumC ([n : Real]) #:transparent)
(struct idC ([s : Symbol]) #:transparent)
(struct strC ([str : String]) #:transparent)
(struct ifC ([test : ExprC] [then : ExprC] [else : ExprC]) #:transparent)
(struct lambdaC ([args : (Listof Symbol)] [body : ExprC]) #:transparent)
(struct AppC ([func : ExprC] [args : (Listof ExprC)]) #:transparent)

(define set_symbols '(+ - * = ? / ! $))
(define set_exprc '(ifC lambdaC AppC))
(define alpha-bet '(a b c d e f g h i))

;Problem 1
;produces a random symbol froma fixed set of size 8

(define (random-symbol [set : (Listof Symbol)]) : Symbol
  (define index (random (length set)))
  (list-ref set index))

;Problem 2
;produces a random expression that does nto conatin any other expressions
(define (random-base-term)
  (match (random 3)
    [0 (NumC (random 100))]
    [1 (idC (random-symbol set_symbols))]
    [2 (strC "a")]))

;Problem 3
; accepts a max depth and produces an expression tree whose depth does not exceed the given one
(define (random-term [max-depth : Real] [set : (Listof Symbol)]) : ExprC
  (if (= max-depth 0)
      (random-base-term)
      (let ()
        (define expr (random-symbol set_exprc))
        (match expr
          ['ifC (ifC (random-term (- max-depth 1) set) (random-term (- max-depth 1) set) (random-term (- max-depth 1) set))]
          ['lambdaC (let ()
                      
                      (define na : Integer (random 4))
                      (define name-func (for/list : (Listof Symbol) ([n : Natural (in-range na)])
                                                       (random-symbol alpha-bet)))
                      (define body (random-term (- max-depth 1) (append name-func set)))
                      (lambdaC name-func body))]
          ['AppC (let ()
                   (define na : Integer (random 4))
                   (define func (random-term (- max-depth 1) set))
                   (define args (for/list : (Listof ExprC) ([n : Natural (in-range na)])
                                                       (idC (random-symbol alpha-bet))))
                   (AppC func args))]))))

;Problem 4
;takes a parsed expression and produces concrete syntax that corresponds to this, represented as an s-expression
(define (unparsed [exp : ExprC]) : Sexp
  (match exp
    [(NumC n) n]
    [(strC s) s]
    [(idC i) i]
    [(ifC t th el) (list 'if (unparsed t) (unparsed th) (unparsed el))]
    [(AppC f a) (cons (unparsed f) (for/list : (Listof Sexp)
                                ([arg : ExprC (in-list a)])
                                (unparsed arg)))]
    [(lambdaC args body) (list 'lambda args ': (unparsed body))]))

;Problem 5
;generates a random term and prints its concrete syntax and returns the term
(define (quiz)
  (define test (random-term 5 set_symbols))
  (println test)
  (unparsed test))

(define secret (quiz))

(check-equal? (unparsed (AppC (idC '-)
                                      (list (NumC 10) (NumC 4)))) '{- 10 4})


