(define (domain serveToast)
  (:requirements :strips :conditional-effects :equality)

  (:constants bread egg fridge knife plate pan mug toaster stoveburner coffeemachine dining_table counter_1 counter_2 counter_1_l counter_2_l dining_table_l fridge_l default_l)

  (:predicates
    (robotat ?l)
    (holding ?o)
    (open ?d)
    (switchedon ?d)
    (sliced ?o)
    (toasted ?o)
    (on ?o ?c)     ; Object ?o is on surface ?c
    (in ?o ?c)     ; Object ?o is in container ?c
    (handempty)
  )

  (:action move
    :parameters (?from ?to)
    :precondition (robotat ?from)
    :effect (and (not (robotat ?from)) (robotat ?to))
  )

  (:action open
    :parameters (?d ?l)
    :precondition (and (robotat ?l) (not (open ?d)))
    :effect (open ?d)
  )

  (:action pick
    :parameters (?o ?c ?l)
    ;; Added checks for both 'on' and 'in' to match the initial state
    :precondition (and 
      (robotat ?l) 
      (handempty)
      (or (on ?o ?c) (in ?o ?c)) 
      (at ?o ?c)
      (or (not (= ?c fridge)) (open ?c))
    )
    :effect (and
      (holding ?o)
      (not (handempty))
      (not (on ?o ?c))
      (not (in ?o ?c))
    )
  )

  (:action put
    :parameters (?o ?c ?l)
    :precondition (and (robotat ?l) (holding ?o))
    :effect (and
      (not (holding ?o))
      (handempty)
      (when (= ?c toaster) (in ?o ?c))
      (when (not (= ?c toaster)) (on ?o ?c))
    )
  )

  (:action slice
    :parameters (?o ?l)
    :precondition (and 
      (robotat ?l) 
      (holding knife)
      (not (sliced ?o))
      (on ?o counter_1)
    )
    :effect (sliced ?o)
  )

  (:action turn_on
    :parameters (?d ?l)
    :precondition (and (robotat ?l) (not (switchedon ?d)))
    :effect (and 
      (switchedon ?d)
      (when (and (= ?d toaster) (in bread toaster)) (toasted bread))
    )
  )
)