#lang racket
(require typed/rackunit)
;Problem 3
;takes a number 'a' and return a function that takes number 'b' and returns a + b
(define (curried-add a)
  (define (curried-bdd b)
    (+ a b))
  curried-bdd)

(check-equal? ((curried-add 5)7) 12)

;Problem 4
;takes a function of two arguments f, and produces a function that we'll call M
;function M takes one argument and produces a function N
;N takes one argument and produces the result of calling the input function f
(define (curry2 f)
  (lambda (a)
    (lambda (b)
      (f a b))))

(check-equal? (((curry2 +) 2)4) 6)

;Problem 5
;takes a fucntion of three arguments, and produces a function that takes one argument
;produces a function that tajes one argument and produces a fucntion that takes one argument
;and produces the result of calling the input function
(define (curry3 f)
  (lambda (a)
    (lambda (b)
      (lambda (c)
        (f a b c)))))

(check-equal? ((((curry3 +) 2)4)5) 11)


;Problem 6
;consumes a list and symbol and returns true exactly when the symbol occurs in the list
(define (contains? lst sym)
  (match lst
    ['() #f]
    [(cons f r) (if (equal? f sym) #t (contains? r sym))]))

(check-equal? (contains? '(kaitlyn carrillo) 'carrillo) #t)
(check-equal? (contains? '() 'carrillo) #f)

;Problem 6.1
;consumes a source list of symbols and list of query symbols and returns a list of booleans
;indicating for the corresponding element of the query list whether it occurs in the source list
(define (in-list-many? source-lst query-lst)
  (map ((curry2 contains?) source-lst) query-lst))

(check-equal? (in-list-many? '(kaveh grace) '(kaitlyn kaveh carrillo grace) ) '(#f #t #f #t))
