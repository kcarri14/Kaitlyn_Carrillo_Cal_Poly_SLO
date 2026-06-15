#lang racket
(require rackunit)
;warmup
;accepts a function and an argument and applies the function to the argument
(define one (lambda (f) (lambda (x) (f x))))

(check-equal? ((one (lambda (x) (+ x 1))) 5) 6)

;Problem 1
;accepts a fucntion and an arugment and applies the function to trhe result of applying the function

(define two (lambda (f) (lambda (x) (f (f x)))))

(check-equal? ((two (lambda (x) (+ x 1))) 5) 7)

;Problem 2
;accepts a finction and an arugment and returns the argument
(define zero (lambda (f) (lambda (x) x)))

(check-equal? ((zero (lambda (x) (+ x 1))) 4) 4)

;Problem 3
;accepts a number-like function and returns a new-number like function that does the function one more time

(define add1
  (lambda (n)
    (lambda (f)
      (lambda (x)
        (f ((n f) x))))))

(check-equal? (((add1 two) (lambda (x) (+ x 1))) 4) 7)

;Problem 4
;accepts two functions like zero and one and returns a fucntion that applies its first
;argument and its second argument the number of times that corresponds with te sum fo the two numbers

(define add (lambda (f1)
              (lambda (f2)
                (lambda (x1)
                  (lambda (x2)
                    ((f1 x1) ((f2 x1) x2)))))))

(check-equal? ((((add two) zero) (lambda (x) (+ x 1))) 4) 6)

;Problem 5
;accepts two arguments and returns the first one

(define tru (lambda (x1) (lambda (x2) x1)))

(check-equal? ((tru 4) (lambda (x) x) )4)

;Problem 6
;accepts two arguments and returns the second one
(define fals (lambda (x1) (lambda (x2) x2)))

(check-equal? ((fals (lambda (x) x)) 4)4)

;Problem 7
;accepts three arguments and if the first is true return result of second argument
;and if its false return the result of the third argument
(define if (lambda (x1) (lambda (x2) (lambda (x3) ((x1 x2) x3)))))

(check-equal? (((if tru) 4) 3) 4)
(check-equal? (((if fals) 4) 3)3)



