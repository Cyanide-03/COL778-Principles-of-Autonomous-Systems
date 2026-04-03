(define (domain serveToast)
  (:requirements :strips :conditional-effects  :equality)

  ;; ───── Constants ────
  ;; Fixed objects in the scene
  (:constants bread egg fridge knife plate pan mug toaster stoveburner coffeemachine dining_table counter_1 counter_2 counter_1_l counter_2_l dining_table_l fridge_l default_l)

    ;; ───── Predicate Definitions ─────
    (:predicates
    ; #TODO
      (robotat ?l)
      (holding ?o)
      (open ?d)
      (switchedon ?d)
      (sliced ?o)
      (toasted ?o)
      (on ?d ?c)
      (in ?o ?c)
      (at ?o ?l)
      (handempty)
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
        ;; this is when device is toaster and bread is in 
        ;; toaster then toast the bread
        (when (and (= ?d toaster) (in bread toaster) (sliced bread))
            (toasted bread)
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
        (not (toasted ?o))
        (on ?o counter_1)
        (= ?l counter_1_l)
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
        (or (= ?c counter_1) (= ?c counter_2) (= ?c dining_table) (= ?c toaster) (= ?c plate))
      )
      :effect (and
        (not (holding ?o))
        (handempty)
        (at ?o ?l)
        (when (= ?c toaster)
          (in ?o ?c)
        )
        (when (not (= ?c toaster))
          (on ?o ?c)
        )
      )
    )
  )