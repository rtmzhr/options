def simulate(option_consultant):
    future_strike_question = "What is the future strike you wish to simulate?\n" \
                          "Please Write a number\n"
    simulation_question = "Do you want to run simulation?\n" \
                          "Press 1 for Simulate    2 for Quit\n"
    if input(simulation_question) == "1":
        simulation = True
    else:
        simulation = False
    while simulation:
        user_future_strike = int(input(future_strike_question))
        print(option_consultant)
        print("The simulation indicated that you will gain {}$ in total\n"
              .format(option_consultant.simulate_profit(user_future_strike)))
        if input(simulation_question) == "1":
            simulation = True
        else:
            simulation = False
