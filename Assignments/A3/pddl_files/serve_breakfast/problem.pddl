
(define (problem serveBreakfast-totable)
  (:domain servebreakfast)

  (:init
    ;; #TODO  

    ; Configurations
    (handempty)

    ; Objects location
    (robotat default_l)

    (in bread fridge)
    (in egg fridge)
    (on knife counter_1)
    (on toaster counter_1)
    (on mug counter_2)
    (on pan counter_2)
    (on plate dining_table)
    (on stoveburner counter_2)
    (on coffeemachine counter_1)
    
    (at fridge fridge_l)
    (at counter_1 counter_1_l)
    (at dining_table dining_table_l)
    (at counter_2 counter_2_l)

    (at bread fridge_l)
    (at egg fridge_l)
    (at knife counter_1_l)
    (at mug counter_2_l)
    (at pan counter_2_l)
    (at toaster counter_1_l)
    (at plate dining_table_l)
    (at stoveburner counter_2_l)
    (at coffeemachine counter_1_l)
  )

  (:goal 
    ;; #TODO
    (and
      ;; toast
      (sliced bread)
      (toasted bread)
      (on bread plate)
      (on plate dining_table)

      ;; egg
      (cooked egg)
      (in egg pan)
      (on pan dining_table)

      ;; coffee
      (coffee_in mug)
      (on mug dining_table)
    )
  )
)