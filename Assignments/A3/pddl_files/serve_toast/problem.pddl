
(define (problem serveToast-totable)
  (:domain serveToast)

  (:init
    ;; #TODO

    ; Configurations
    (handempty)
    (not (open fridge))
    (not (switchedon toaster))

    ; Objects location
    (robotat default_l)
    (on plate dining_table)
    (on knife counter_1)
    (in bread fridge)
    (at toaster counter_1_l)
    (at fridge fridge_l)
    (at dining_table dining_table_l)
    (at counter_1 counter_1_l)
    (at counter_2 counter_2_l)
  )

  (:goal
    ;; #TODO
    (and 
      (sliced bread)
      (toasted bread)
      (on bread plate)
      (on plate dining_table)
    )
  )
)