(deftemplate person
     (slot name)
     (slot parent)
     (slot gender))



   (deffacts initial-facts
     (person (name john) (parent none) (gender male))
     (person (name mary) (parent john) (gender female))
     (person (name susan) (parent mary) (gender female))
     (person (name tom) (parent susan) (gender male))
     (person (name alice) (parent tom) (gender female))
     (person (name kelly) (parent alice) (gender female))
     (person (name dominic) (parent kelly) (gender male)))

   (defrule find-ancestor
     (person (name ?x) (parent ?y))
     (person (name ?y) (parent ?z))
     =>
     (assert (person (name ?x) (parent ?z))))

   (defrule print-ancestor
     (person (name ?x) (parent ?z))
     =>
     (printout t ?x " is an ancestor of " ?z crlf))

   (defrule find-mother
     (person (name ?x) (parent ?y) (gender female))
     =>
     (assert (mother ?x ?y)))

   (defrule find-father
     (person (name ?x) (parent ?y) (gender male))
     =>
     (assert (father ?x ?y)))

   (defrule find-brother
     (person (name ?x) (parent ?z) (gender male))
     (person (name ?y) (parent ?z))
     (test (neq ?x ?y))
     =>
     (assert (brother ?x ?y)))

   (defrule find-sister
     (person (name ?x) (parent ?z) (gender female))
     (person (name ?y) (parent ?z))
     (test (neq ?x ?y))
     =>
     (assert (sister ?x ?y)))
  
   (defrule infer-grandparent
    (person (name ?gc) (parent ?p))
    (person (name ?p)  (parent ?gp))
    (not (grandparent ?gp ?gc))
    =>
    (assert (grandparent ?gp ?gc))
    (assert (grandchild  ?gc ?gp)))

    
  (defrule infer-uncle
    (brother ?u ?p)
    (person (name ?n) (parent ?p))
    (not (uncle ?u ?n))
    =>
    (assert (uncle ?u ?n)))

  (defrule infer-aunt
    (sister ?a ?p)
    (person (name ?n) (parent ?p))
    (not (aunt ?a ?n))
    =>
    (assert (aunt ?a ?n)))


  (defrule infer-cousins
  (person (name ?x) (parent ?px&~none))
  (person (name ?y) (parent ?py&~none))
  (or (brother ?px ?py) (sister ?px ?py)
      (brother ?py ?px) (sister ?py ?px))
  (test (neq ?x ?y))
  (not (cousin ?x ?y))
  =>
  (assert (cousin ?x ?y)))

  (defrule infer-second-cousins
    (person (name ?x) (parent ?px))
    (person (name ?y) (parent ?py))
    (cousin ?px ?py)
    (test (neq ?x ?y))
    (not (second_cousin ?x ?y))
    =>
    (assert (second_cousin ?x ?y)))
