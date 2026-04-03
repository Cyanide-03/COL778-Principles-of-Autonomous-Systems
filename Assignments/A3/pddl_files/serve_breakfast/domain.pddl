(define (domain serveBreakfast)
  (:requirements :strips :conditional-effects  :equality)

  ;; ───── Constants ────
  ;; Fixed objects in the scene
  (:constants bread egg fridge knife plate pan mug toaster stoveburner coffeemachine dining_table counter_1 counter_2 counter_1_l counter_2_l dining_table_l fridge_l default_l)

    ;; ───── Predicate Definitions ─────
    (:predicates
      (robotat ?l)
      (holding ?o)
      (open ?d)
      (switchedon ?d)
      (on ?d ?c)
      (in ?o ?c)
      (at ?o ?l)
      (handempty)
      (sliced ?o)
      (cooked ?o)
      (toasted ?o)
      (coffee_in ?m)
    )

    ;; ───── Action Definitions ─────
    ; #TODO
    (:action open
      :parameters (?d ?l)
      :precondition (and (robotat ?l) (not (open ?d)) (at ?d ?l))
      :effect (open ?d)
    )

    (:action move
      :parameters (?from ?to)
      :precondition (robotat ?from)
      :effect (and
        (not (robotat ?from))
        (robotat ?to)
      )
    )

    (:action turn_off
      :parameters (?d ?l)
      :precondition (and 
        (robotat ?l) 
        (at ?d ?l)
        (switchedon ?d)
      )
      :effect (not (switchedon ?d))
    )

    (:action turn_on
      :parameters (?d ?l)
      :precondition (and 
        (robotat ?l) 
        (at ?d ?l)
        (not (switchedon ?d))
      )
      :effect (and 
        (switchedon ?d)

        ;; this is when device=toaster, bread in toaster, bread=sliced then toast the bread
        (when (and (= ?d toaster) (in bread toaster) (sliced bread))
          (toasted bread)
        )

        ;; this is when device=coffeemachine, mug in coffeemachine then put coffee in mug
        (when (and (= ?d coffeemachine) (in mug coffeemachine))
          (coffee_in mug)
        )

        ;; this is when device=toaster, egg in pan, pan on stoveburner then cook the egg
        (when (and (= ?d stoveburner) (in egg pan) (on pan stoveburner))
          (cooked egg)
        )
      )
    )

    (:action slice
      :parameters (?o ?l)
      :precondition (and 
        (robotat ?l) 
        (holding knife)
        (not (handempty))
        (not (sliced ?o))
        (or 
          (and 
            (= ?o bread)
            (not (toasted ?o))
            (on ?o counter_1)
            (= ?l counter_1_l)
          )
          (and
            (= ?o egg)
            (not (cooked ?o))
            (on ?o counter_2)
            (= ?l counter_2_l)
          )
        )
      )
      :effect (sliced ?o)
    )

    (:action pick
      :parameters (?o ?c ?l)
      :precondition (and 
        (robotat ?l) 
        (not (holding ?o))
        (handempty)
        (or (on ?o ?c) (in ?o ?c))
        (at ?o ?l)
        (at ?c ?l)
        (or (not (= ?c fridge)) (open ?c))

      )
      :effect (and
        (holding ?o)
        (not (handempty))
        (not (on ?o ?c))
        (not (in ?o ?c))
        (not (at ?o ?l))
      )
    )

    (:action put
      :parameters (?o ?c ?l)
      :precondition (and 
        (robotat ?l) 
        (holding ?o)
        (not (handempty))
        (not (on ?o ?c))
        (not (in ?o ?c))
        (at ?c ?l)
        (not (or (= ?c bread) (= ?c egg) (= ?c knife)))
      )
      :effect (and
        (not (holding ?o))
        (handempty)
        (at ?o ?l)
        (when (or 
          (= ?c toaster) 
          (= ?c coffeemachine) 
          (= ?c mug) 
          (= ?c fridge)
          (= ?c pan)
        )
          (in ?o ?c)
        )
        (when (or 
          (= ?c plate) 
          (= ?c counter_1) 
          (= ?c counter_2) 
          (= ?c dining_table)
          (= ?c stoveburner)
        )
          (on ?o ?c)
        )
      )
    )
  )
