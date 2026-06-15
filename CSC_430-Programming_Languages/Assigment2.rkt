#lang typed/racket
(require typed/rackunit)

;I finished the whole assignment :)

;Problem 2.3.3
;consumes the number of attendees (of a show) and produces how much income the attendees produce
(define customer-ticket 5)
(define performance-cost 20)
(define customer-cost 0.5)

(define (total-profit [num-peep : Real]) : Real
  (- (- (* customer-ticket num-peep) performance-cost) (* customer-cost num-peep)))


;Problem 3.3.3
;consumes the radius of the cylinder's base disk and its height and returns its surface area

(define (area-cylinder [r : Natural] [h : Natural]) : Real
  (+(*(*(* 2 pi )r)h)(*(* 2 pi)(expt r 2))))


;Problem 2.2
;given a writing utensil, it returns the distance in meters how long itll write for
;before it runs out

; represents a writing implement
(define-type Writer (U Pen Pencil))
; ink volume in ml, how-full a number in the range 0.0 to 1.0
(struct Pen ([ink-volume : Real] [how-full : Real]) #:transparent)
; length in cm
(struct Pencil ([length : Real]) #:transparent)

(define pen-meters 150)
(define pencil-meters 56)

(define pen1 (Pen 12 1.0))

(define (how-far-to-write [writing-utensil : Writer]) : Real
  (match writing-utensil
    [(Pen ink full) (*(* ink full) pen-meters)]
    [(Pencil len) (* pencil-meters len)]))


;Problem 2.3
;data defintions
(define-type Polynomial (U Linear Quadratic))
(struct Linear ([A : Real] [B : Real] ) #:transparent)
(struct Quadratic ([A : Real] [B : Real] [C : Real]) #:transparent)

;accepts a polynomial and a value for x and returns the correct result when plugging x in
(define (interp [Equation : Polynomial] [x : Real]) : Real
  (match Equation
    [(Linear slope intercept) (+(* slope x) intercept)]
    [(Quadratic a b c) (+(+(*(expt x 2) a) (* b x))c)]))



;Problem 2.4

; accepts a polynomial and returns another polynomial that is the derative of it
(define (derivative [Equation : Polynomial]) : Polynomial
  (match Equation
    [(Quadratic a b c) (Linear (* a 2) b)]
    [(Linear slope intercept) (Linear 0 slope)]))



;Problem 2.5
(define-type BTree (U Leaf Node))
(struct Leaf ([sym : Symbol]) #:transparent)
(struct Node ([left : BTree] [right : BTree]) #:transparent)
; Finish the examples
(define bt1 (Node (Node (Node (Leaf 'hello) (Leaf 'world)) (Node (Leaf 'whats) (Leaf 'up))) (Leaf 'huh)))
(define bt2 (Node (Leaf 'kaitlyn) (Leaf 'carrillo)))
(define bt3 (Leaf 'bruh))


;Problem 2.6
;takes in a binary tree and produces a binary tree of the same shape just the leaves have symbols 'zz
(define (zz-tree [binary-tree : BTree]) : BTree
  (match binary-tree
    [(Leaf s) (Leaf 'zz)]
    [(Node a b) (Node (zz-tree a) (zz-tree b))]))



;Problem 2.7
;takes in a binary tree and produces a left-right mirror of the bianry tree
(define (mirror [binary-tree : BTree]) : BTree
  (match binary-tree
    [(Leaf s) (Leaf s)]
    [(Node a b) (Node (mirror b) (mirror a))]))



;Problem 2.8
; accepts a binary tree and produces the shortest path to a leaf
(define (min-depth [binary-tree : BTree]) : Natural
  (match binary-tree
    [(Leaf s) 0]
    [(Node a b) (add1 (min (min-depth a) (min-depth b)))  ]))



;Problem 2.9
;takes in a binary tree and a symbol and returns if the symbol is in that tree
(define (contains? [binary-tree : BTree] [sym : Symbol]) : Boolean
  (match binary-tree
    [(Leaf s) (if (equal? s sym) #t #f)]
    [(Node a b) (or (contains? a sym) (contains? b sym))]))


;Problem 2.10
;takes in a source binary tree and a symbol and replacement binary tree
;returns a new tree where every node of the source tree containing the symbol is replaced by the replacement tree
(define (subst [binary-tree : BTree] [sym : Symbol] [replacement-tree : BTree]) : BTree
  (match binary-tree
    [(Leaf s) (if (equal? s sym) replacement-tree binary-tree)]
    [(Node a b) (Node (subst a sym replacement-tree) (subst b sym replacement-tree))]))


;2.3.3 tests
(check-equal? (total-profit 50) 205.0)
(check-equal? (total-profit 0) -20)

;3.3.3 tests
(check-= (area-cylinder 2 4) 75.4 0.1)
(check-= (area-cylinder 3 60) 1187.52 0.1)

;2.2 tests
(check-equal? (how-far-to-write pen1) 1800.0)
(check-equal? (how-far-to-write (Pen 2 0.8)) 240.0)
(check-equal? (how-far-to-write (Pencil 24)) 1344)

;2.3 tests
(check-equal? (interp (Linear 3 4) 2) 10)
(check-equal? (interp (Quadratic 5 6 10) 2) 42)

;2.4 tests
(check-equal? (derivative (Quadratic 3 4 5)) (Linear 6 4))
(check-equal? (derivative (Linear 98 3)) (Linear 0 98))

;2.6 tests
(check-equal? (zz-tree bt2) (Node (Leaf 'zz) (Leaf 'zz)))
(check-equal? (zz-tree bt1) (Node (Node (Node (Leaf 'zz) (Leaf 'zz)) (Node (Leaf 'zz) (Leaf 'zz))) (Leaf 'zz)))
(check-equal? (zz-tree bt3) (Leaf 'zz))

;2.7 tests
(check-equal? (mirror bt2) (Node (Leaf 'carrillo) (Leaf 'kaitlyn)))
(check-equal? (mirror bt3) (Leaf 'bruh))

;2.8 tests
(check-equal? (min-depth bt1) 1)
(check-equal? (min-depth bt3) 0)

;2.9 tests
(check-equal? (contains? bt1 'hello) #t)
(check-equal? (contains? bt1 'hi) #f)

;2.10 tests 
(check-equal? (subst bt3 'bruh bt2) (Node (Leaf 'kaitlyn) (Leaf 'carrillo)))
(check-equal? (subst bt2 'kaitlyn bt3) (Node (Leaf 'bruh) (Leaf 'carrillo)))
