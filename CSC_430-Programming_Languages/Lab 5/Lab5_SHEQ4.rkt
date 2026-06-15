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
   
   
    
   
    ;takes a number and adds it to itseld 3 times and then doubles it
    {let ([one = {lambda (f) : (lambda (x) : (f x))}]
          [two = {lambda (f) : (lambda (x) : (f(f x)))}]
          [add = (lambda (f1) : (lambda (f2) : (lambda (x1) : (lambda (x2) : ((f1 x1) ((f2 x1) x2))))))])
      in
      {let ([three = ((add two) one)]
            [double = (lambda (n) : (* n 2))])
        in
        (= ((three double) 2) 16)
        end}
      end}
    
    )
   
  ;; this code actually invokes the 'my-mod1 module, so that the
  ;; code runs.
  (require 'my-mod1)
   
