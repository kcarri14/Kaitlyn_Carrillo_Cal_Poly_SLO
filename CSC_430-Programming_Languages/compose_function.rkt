#lang racket

(define (compose f g)
  (lambda (x) (f(g x))))

(define (add_five x)
  (+ x 5))

(define (double x)
   (*  2 x))

((compose add_five double) 7)
