#lang racket
   
  ;; this code defines the sim-SHEQ4 language as a module
  (module sim-SHEQ4 racket
    (provide
     [rename-out (#%lam-app #%app)
                 (#%lam-lam lambda)
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
   
    ;; usually this is where lambda winds up, but not this year...
    ;; leaving this here for when we change to a different keyword again,
    ;; and lambdas get parsed as applications again:
    (define-syntax (#%lam-app stx)
      (syntax-case stx (:)
        [(_ e ...)
         #'(#%app e ...)]))
   
    #;(define-syntax (my-if stx)
      (syntax-case stx ()
        [(_ e1 e2 e3)
         #'(if e1 e2 e3)])))
   
  ;; this module uses the sim-SHEQ4 language. That is, its
  ;; contents are written *in* the sim-SHEQ4 language.
  ;; the only edits you should make are inside this module:
  (module my-mod1 (submod ".." sim-SHEQ4)
   
    1234
   
    4567
   
    {+ 4 5}
   
    {if true 34 39}
   
    {{lambda (x y) : {+ x y}} 4 3}
   
    ;; exercise 0: write a function that adds one to a number.
    {lambda (x) : {+ x 1}}
   
    ;; exercise 1: combining the definition and application forms,
    ;; apply the function that adds one to a number to the number 17.
    {{lambda (x) : {+ x 1}}
     17}
    ;; thought exercise: does running this program "give a name to a value" anywhere?
    ;; if so, what name and what value?
    "gave a name to 1 and it was x"
    ;; exercise 2: write a function that accepts a function 'h' and applies
    ;; it to 8.
    {lambda (h) : {h 8}}
    ;; exercise 3: combining the definition and application forms,
    ;; apply the function that applies its argument to 8 to the function
    ;; that adds one to a number.
    {{lambda (h) : {h 8}}
      {lambda (x) : {+ x 1}}}
    ;; thought exercise: does running this program "give a name to a value"
    ;; anywhere? if so, what name(s) and what value(s)?
    "gave the add one function the name h and gave x the value of 8"
    
    ;; exercise 4 (a bit harder): write a function that performs function composition:
    ;; that is, it accepts functions named 'f' and 'g' and returns a new
    ;; function of one argument that applies first 'g' and then 'f' to its
    ;; argument
    {{lambda (f g) : {lambda (f g) : {g f}}} {lambda (f) : {+ x 1}} {lambda (g) : {* x 2}}}
   
    ;; exercise 5 (harder): Write a program that gives the name "compose" to
    ;; the function defined in the previous exercise, gives the name "add1" to
    ;; the function that adds one, and then gives the name "add2" to the composition
    ;; of add1 and add1, and finally applies this add2 function to 99.
   
    )
   
  ;; this code actually invokes the 'my-mod1 module, so that the
  ;; code runs.
  (require 'my-mod1)
