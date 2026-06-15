#lang racket
   
  ;; this code defines the sim-SHEQ4 language as a module
  (module sim-SHEQ4 racket
    (provide
     [rename-out (#%lam-app #%app)
                 (#%lam-lam lambda)
                 (my-let let)
                 #;(my-if if)]
     else
     #%module-begin
     #%datum
     + - * / = equal? <= =>
     true false
     if)
    (require (for-syntax syntax/parse))
   
    (define-syntax (#%lam-lam stx)
      (syntax-case stx (:)
        [(_ (args ...) : body)
         #'(lambda (args ...) body)]
        [(_ z ...)
         (error 'zzz "ou44ch")]))
   
    (define-syntax (my-let stx)
      (syntax-parse stx
        [(_
          ((var:id (~literal =) rhs:expr) ...)
          (~literal in)
          body:expr
          (~literal end))
         #'(let ([var rhs] ...) body)]))
   
    ;; usually this is where lambda winds up, but not this year...
    ;; leaving this here for when we change to a non-first-position keyword again,
    ;; and lambdas get parsed as applications again:
    (define-syntax (#%lam-app stx)
      (syntax-case stx (:)
        [(_ e ...)
         #'(#%app e ...)])))
   
  ;; this module uses the sim-SHEQ4 language. That is, its
  ;; contents are written *in* the sim-SHEQ4 language.
  ;; the only edits you should make are inside this module:
  (module my-mod1 (submod ".." sim-SHEQ4)
   
    1234
   
    4567
   
    {+ 4 5}
   
    {if true 34 39}
    
    {{lambda  (x y) : {+ x y}} 4 3}
   
    {let ([z = {+ 9 14}]
          [y =  98])
      in
      {+ z y}
      end}
   
   
    ;; exercise 0: Using the binding form, give the name
    ;; `f` to the function that accepts an argument `x` and computes
    ;; x^2 + 4x + 4. Apply `f` to seven.

    {{lambda (x) : (+ (+ (* 4 x) (* x x)) 4)} 7}
   
    ;; exercise 1: Use the trick discussed in class to define
    ;; a `fact` function that computes the factorial of a given
    ;; number. Use it to compute the factorial of 12.
    {let{[fact = {lambda (self n) : {if {<= n 0}
                                        1
                                        {* n {self self {- n 1}}}}}]}
      in
      {fact fact 6}
      end}
    
   
    ;; exercise 2: Define a 'pow' function that accepts a base
    ;; and a (natural number) exponent, and computes the base to
    ;; the power of the exponent. Don't worry about non-natural
    ;; number exponents (6^1.5, 5^-4).
    {let {[pow = {lambda (self base exp) : {if {<= exp 0}
                                                 1
                                                 {* exp {self self base {- exp 1}}}}}]}
      in
      {pow pow 4 5}
      end}
   
    ;; exercise 3: use `fact` and `pow` to build a "sin" function
    ;; that accepts a number x and a number of terms `n`, and computes
    ;; (sin x) using `n` terms of the taylor expansion. (Note that
    ;; this is a little ambigious; do zero-coefficient terms count?
    ;; You can go either way on this.) Use this function to compute
    ;; the sine of 1 radian to an error of no more than ten to the minus
    ;; 30th.
    
   
    )
   
  ;; this code actually invokes the 'my-mod1 module, so that the
  ;; code runs.
  (require 'my-mod1)
