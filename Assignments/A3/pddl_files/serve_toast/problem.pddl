
(define (problem serveToast-totable)
  (:domain serveToast)

  (:init
    ;; #TODO

    ; Configurations
    (handempty)

    ; Objects location
    (robotat default_l)

    (in bread fridge)
    (on knife counter_1)
    (on toaster counter_1)
    (on plate dining_table)
    
    (at fridge fridge_l)
    (at counter_1 counter_1_l)
    (at dining_table dining_table_l)
    (at counter_2 counter_2_l)

    (at bread fridge_l)
    (at knife counter_1_l)
    (at toaster counter_1_l)
    (at plate dining_table_l)
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