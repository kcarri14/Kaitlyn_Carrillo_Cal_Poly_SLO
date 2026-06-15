#lang typed/racket
(require typed/rackunit)
;Problem 1
;accepts an s-expression ans uses a single match pattern to return true for
;s-expressions that are a list containing a number, the symbol 'chris, and a symbol
(define (parse000 [lst : Sexp]): Boolean
  (match lst
    [(list (? real? n) 'chris (? symbol? s)) #t]
    [_ #f]))

(check-equal? (parse000 '(10 chris humbug)) #t)
(check-equal? (parse000 '(1 chris 10))#f)
(check-equal? (parse000 '(10 chris)) #f)

;Problem 2
;accepts a s-expression and uses the same match pattern but returns the symbol in cases of sucess

(define (parse001 [lst2 : Sexp]) : (U Symbol Boolean)
  (match lst2
    [(list (? real? n) 'chris (? symbol? s)) s]
    [_ #f]))

(check-equal? (parse001 '(12 chris bruh)) 'bruh)
(check-equal? (parse001 '(1 chris 10)) #f)
(check-equal? (parse001 '(chris 10)) #f)

;Problem 3
;accepts an s-expression and succeds if that list is length 3 and the second element is a list of real number
(define (parse002 [lst3 : Sexp]) : (U (Listof Real) Boolean)
  (match lst3
    [(list _ (list (? real? r) ...) _) (cast r (Listof Real)) ]
    [_ #f]))

(check-equal? (parse002 '(10 (10 30 20) 10))'(10 30 20))
(check-equal? (parse002 '(chris (10 20 30) 'bruh)) '(10 20 30))
(check-equal? (parse002 '(chris is crazy))#f)


;Problem 4
;accepts an s-expression and succedds for alist of lists of exactly three numbers each and
;returns the sum of the first numbers in the list minus the sum of the third number sin the lists
(define (parse003 [lst4 : Sexp]) : (U Real Boolean)
  (match lst4
    [(list (list (? real? firsts) (? real?) (? real? thirds)) ...)
     (- (foldl + 0 (cast firsts (Listof Real))) (foldl + 0 (cast thirds (Listof Real))))]
    [_ #f]))

(check-equal? (parse003 '((0 1 2) (1 2 3) (2 3 4))) -6)
(check-equal? (parse003 '(chris is crazy)) #f)
(check-equal? (parse003 '()) 0)

;Problem 5
;accpets a value and returns the sumbol 'okay if the input is a number and otherwise uses error to signal
;an error
(define (ohno [value : Any]) : Symbol
  (match value
    [(? real? value) 'okay]
    [_ (error 'ohno "expected a number, got ~e" value)]))

(check-equal? (ohno 5) 'okay)

(check-exn (regexp (regexp-quote "expected a number"))
           (lambda () (ohno 'chris)))
;Problem 6
;Describe the Arith language in chaper 3
(define-type ArithC (U numC plusC multC expC))
(struct numC  ([n : Real]) #:transparent)
(struct plusC ([l : ArithC] [r : ArithC]) #:transparent)
(struct multC ([l : ArithC] [r : ArithC]) #:transparent)
(struct expC ([n : ArithC]) #:transparent)


;Problem 7
;Develop the evaluation method from the textbook
(define (interp [arith : ArithC]) : Real
  (match arith
    [(numC n) n]
    [(plusC left right) (+ (interp left) (interp right))]
    [(multC left right) (* (interp left) (interp right))]
    [(expC num) (define val (interp num))
                (* val val)]))


(check-equal? (interp (numC 5))5)
(check-equal? (interp (plusC (numC 2)(multC (numC 5) (numC 6)))) 32)
(check-equal? (interp (expC (numC 3))) 9)

;Problem 8
;accepts an ArithC and returns a new ArithC where the left and right terms of every addition are swapped
(define (swap-adds [tree : ArithC]) : ArithC
  (printf "Entering swap-adds with tree: ~e\n" tree)
  (match tree
    [(numC tree) (numC tree)]
    [(plusC left right) (plusC (swap-adds right) (swap-adds left))]
    [(multC left right) (multC (swap-adds right) (swap-adds left))]))

(check-equal? (swap-adds (numC 5)) (numC 5))
(check-equal? (swap-adds (plusC (numC 2)(multC (numC 5) (numC 6)))) (plusC (multC (numC 6) (numC 5)) (numC 2)))

;add a print f to your swapadds function that pronts each tree on entry 

;Problem 9
;develop a parser for the arith language
(define (parse [e : Sexp]) : ArithC
  (match e
    [(? real? n) (numC n)]
    [(list '+ left right) (plusC (parse left) (parse right))]
    [(list '* left right) (multC (parse left) (parse right))]
    [(list '^2 num) (expC (parse num))]
    [other (error 'parse "Syntax error, got ~e" other)]))

(check-equal? (parse '10) (numC 10))
(check-equal? (parse '{+ 2 {* 5 6}}) (plusC (numC 2)(multC (numC 5) (numC 6))))
(check-equal? (parse '(^2 3)) (expC(numC 3)))

(check-exn (regexp (regexp-quote "Syntax error"))
           (lambda () (parse '{})))

;Problem 10
;accepts an s-expression and calls that parser and the interp function
(define (top-interp [value : Sexp]) : Any
  (interp (parse value)))

(check-equal? (top-interp '{+ 2 {* 5 6}}) 32)

;Problem 11
; consumes two list of number of the same length and returns a new list of lists
;where each element of the new list is a list containing both of the corresponding elements from the og list
(define (zip [lst1 : (Listof Real)] [lst2 : (Listof Real)]) : Any
    (match* (lst1 lst2)
    [('() '()) '()]
    [((cons f1 r1) (cons f2 r2)) (cons (list f1 f2) (zip r1 r2))]
    [(_ _) (error 'zip "Lists must be the same length")]))

(check-equal? (zip '(10 20 30) '(40 50 60)) '((10 40) (20 50) (30 60)))
(check-equal? (zip '() '()) '())
(check-exn (regexp (regexp-quote "Lists must be the same length"))
           (lambda () (zip '(10) '(20 30))))