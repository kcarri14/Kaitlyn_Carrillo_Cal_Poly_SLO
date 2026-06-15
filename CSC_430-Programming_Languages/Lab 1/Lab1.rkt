#lang racket
(require rackunit)

; Exercise 15
; consumes two boolean values and uses the implication boolean (not p or q) 

(define (==> sunny friday)
  (or (not sunny) friday))

(==> true true)

(check-equal? (==> true false) false)
(check-equal? (==> true true) true)
(check-equal? (==> false false) true)
(check-equal? (==> false true) true)

;Exer



