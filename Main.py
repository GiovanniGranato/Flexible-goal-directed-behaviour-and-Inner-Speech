#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import copy
import datetime

#INHERITHED FILES AND FUNCTIONS

from geometricshapes import Triangle,Fovea,Square,Circle,Rectangle
import Environment
import Analysis_Tools_WCST # WCST ANALISYS TOOLS
import System_Components # COMPONENTS OF SYSTEM

def WCST_Execution(
                    System_parameters,
                    Graphics_on,
                    Extended_Graphics
                  ):

    '''

    This is a macro-function that allows to test a computational model with a neuropsychological task (Wisconsin Cards Sorting Test).

    args:
        - System_parameters: parameters of the computational model (Mu, Phi, Tau, Lambda)
        - Graphics_on: activation of graphics during the solution of WCST
        - Extended_Graphics: activation of an extended version of graphics, i.e. task enviroment, perception and WM activations
                            (in case of false value will be open a window with only the WM activations)

    return:

        - [uncorrect_responses_p, perseverative_errors_p, not_perseverative_errors_p, Fms_p, categories_completed]: Final list of WCST indices
        - WM_values_each_turn: values of working-memory for each turn of WCST
        - responses_list: WCST indices (raw data) for each turn

    '''

    Start_main = datetime.datetime.today()
    print('---------')
    print(' Test started at = ', Start_main)
    print('---------')

    inhibition_integrity = System_parameters[0]
    working_memory_forgetting = System_parameters[1]
    T_inhibition = System_parameters[2]
    Weight_Lang = System_parameters[3]


    # BEHAVIOURAL ERRORS - INITIALIZATION

    Perseverative_principle = [0]
    First_turn_Pers_Princ = copy.deepcopy(Perseverative_principle)
    perseverative_errors = 0
    not_perseverative_errors = 0
    distraibility_errors = 0
    total_errors = 0

    # PROPRIERTIES SELECTION - INITIALIZATION

    mental_actions = [1, 2, 3]
    correct_rules_order = [1, 2, 3, 1, 2, 3]  # 1 = color and 2 = form and 3 for size
    chosen_proprierty =  0 #1
    correct_rule = correct_rules_order[0]#copy.deepcopy(chosen_proprierty)

    Completed_Categories = 0
    matches = 0
    actions_made = 0

    responses_list = []
    qualitative_common_attributes = []

    # LIST OF ALL TURNS FOR SCORING - INITIALIZATION

    test_passed = False
    test_failed = False
    Error = False
    Ambiguity = False
    single_pers_response = False
    single_distraibility_error = False

    Scoring_list = [[actions_made, correct_rule, matches, qualitative_common_attributes, Error, Ambiguity, single_pers_response, single_distraibility_error, First_turn_Pers_Princ]]


    #INITIALIZE RBM AND VERBAL WM

    numbers_layers = 2
    load_choice = 1
    load_choice_second = 1

    Hidden_units = 150
    RBM_obj, RBM_obj_second = System_Components.RBM_initialization_first(numbers_layers, 1, Hidden_units, load_choice)
    RBM_obj_second = System_Components.RBM_initialization_second(load_choice_second)

    Verbal_WM = System_Components.Verbal_WM(3, 3)

    #INITIALIZE ABSTRACT WORKING-MEMORIES VALUES

    WM_values = np.array([0.5000, 0.5000, 0.5000], dtype=float)
    WM_values_each_turn = [[0.5000, 0.5000, 0.5000]]

    # SET CONSTANTS SYSTEM - INIT ENVIROMENT AND OLD FUNCTIONS

    accomplished_threshold = 0.001
    limits = np.array([[0.2, 0.8], [0.2, 0.8]])
    int = 1
    ext = 2


    # INITIALIZE ENVIRONMENT

    unit = 100  # SIZE OF SIDES OF ENVIRONMENT
    fovea_center = [0.5, 0.30]
    fovea_size = 0.2

    dim = 0.15 # 0.075       0.10606602  0.12990381  0.15
    dim_1 = 0.12990381
    dim_2 = 0.10606602
    dim_3 = 0.075

    # TABLET_CARDS / INTERNAL ENVIRONMENT

    table_cards_retina_focus = 1

    tab_first = [0.10, 0.75]  # [0.22, 0.82]
    tab_second = [0.35, 0.75]
    tab_third = [0.60, 0.75]
    tab_four = [0.85, 0.75]

    int_t1 = Triangle(tab_first, dim, [0, 0, 1], unit, 5)
    int_s1 = Square(tab_second, dim_1, [1, 0, 0], unit, 10)
    int_c1 = Circle(tab_third, dim_2, [0, 1, 0], unit, 3)
    int_b1 = Rectangle(tab_four, dim_3, [1, 1, 0], unit, 0, 10)

    table_cards = [int_t1, int_s1, int_c1, int_b1]
    int_env, int_fov, table_cards = Environment.initialize(unit, fovea_center, fovea_size, table_cards)

    # DECK_VARIABLES

    deck_pos = [0.5, 0.45] # DECK POSITION
    deck_card = 0 # COUNT SINGLE DECK CARD
    matches = 0 # COUNT CORRECTS MATCHES

    #Great, [sq,circ,bar,triang] [g,r,b,y]
    ext_s1 = Square(deck_pos, dim, [0, 1, 0], unit, 10)
    ext_s2 = Square(deck_pos, dim, [1, 0, 0], unit, 3)
    ext_s3 = Square(deck_pos, dim, [0, 0, 1], unit, 4)
    ext_s4 = Square(deck_pos, dim, [1, 1, 0], unit, 4)
    ext_c1 = Circle(deck_pos, dim, [0, 1, 0], unit, 3)
    ext_c2 = Circle(deck_pos, dim, [1, 0, 0], unit, 8)
    ext_c3 = Circle(deck_pos, dim, [0, 0, 1], unit, 5)
    ext_c4 = Circle(deck_pos, dim, [1, 1, 0], unit, 5)
    ext_b1 = Rectangle(deck_pos, dim, [0, 1, 0], unit, 0, 10)
    ext_b2 = Rectangle(deck_pos, dim, [1, 0, 0], unit, 0, 6)
    ext_b3 = Rectangle(deck_pos, dim, [0, 0, 1], unit, 0, 5)
    ext_b4 = Rectangle(deck_pos, dim, [1, 1, 0], unit, 0, 5)
    ext_t1 = Triangle(deck_pos, dim, [0, 1, 0], unit, 5)
    ext_t2 = Triangle(deck_pos, dim, [1, 0, 0], unit, 5)
    ext_t3 = Triangle(deck_pos, dim, [0, 0, 1], unit, 5)
    ext_t4 = Triangle(deck_pos, dim, [1, 1, 0], unit, 5)
    #Great - medium, [sq,circ,bar,triang] [g,r,b,y]
    ext_s5 = Square(deck_pos, dim_1, [0, 1, 0], unit, 10)
    ext_s6 = Square(deck_pos, dim_1, [1, 0, 0], unit, 3)
    ext_s7 = Square(deck_pos, dim_1, [0, 0, 1], unit, 4)
    ext_s8 = Square(deck_pos, dim_1, [1, 1, 0], unit, 4)
    ext_c5 = Circle(deck_pos, dim_1, [0, 1, 0], unit, 3)
    ext_c6 = Circle(deck_pos, dim_1, [1, 0, 0], unit, 8)
    ext_c7 = Circle(deck_pos, dim_1, [0, 0, 1], unit, 5)
    ext_c8 = Circle(deck_pos, dim_1, [1, 1, 0], unit, 5)
    ext_b5 = Rectangle(deck_pos, dim_1, [0, 1, 0], unit, 0, 10)
    ext_b6 = Rectangle(deck_pos, dim_1, [1, 0, 0], unit, 0, 6)
    ext_b7 = Rectangle(deck_pos, dim_1, [0, 0, 1], unit, 0, 5)
    ext_b8 = Rectangle(deck_pos, dim_1, [1, 1, 0], unit, 0, 5)
    ext_t5 = Triangle(deck_pos, dim_1, [0, 1, 0], unit, 5)
    ext_t6 = Triangle(deck_pos, dim_1, [1, 0, 0], unit, 5)
    ext_t7 = Triangle(deck_pos, dim_1, [0, 0, 1], unit, 5)
    ext_t8 = Triangle(deck_pos, dim_1, [1, 1, 0], unit, 5)
    # Medium - small, [sq,circ,bar,triang] [g,r,b,y]
    ext_s9 = Square(deck_pos, dim_2, [0, 1, 0], unit, 10)
    ext_s10 = Square(deck_pos, dim_2, [1, 0, 0], unit, 3)
    ext_s11 = Square(deck_pos, dim_2, [0, 0, 1], unit, 4)
    ext_s12 = Square(deck_pos, dim_2, [1, 1, 0], unit, 4)
    ext_c9 = Circle(deck_pos, dim_2, [0, 1, 0], unit, 3)
    ext_c10 = Circle(deck_pos, dim_2, [1, 0, 0], unit, 8)
    ext_c11= Circle(deck_pos, dim_2, [0, 0, 1], unit, 5)
    ext_c12= Circle(deck_pos, dim_2, [1, 1, 0], unit, 5)
    ext_b9 = Rectangle(deck_pos, dim_2, [0, 1, 0], unit, 0, 10)
    ext_b10 = Rectangle(deck_pos, dim_2, [1, 0, 0], unit, 0, 6)
    ext_b11= Rectangle(deck_pos, dim_2, [0, 0, 1], unit, 0, 5)
    ext_b12= Rectangle(deck_pos, dim_2, [1, 1, 0], unit, 0, 5)
    ext_t9 = Triangle(deck_pos, dim_2, [0, 1, 0], unit, 5)
    ext_t10 = Triangle(deck_pos, dim_2, [1, 0, 0], unit, 5)
    ext_t11= Triangle(deck_pos, dim_2, [0, 0, 1], unit, 5)
    ext_t12= Triangle(deck_pos, dim_2, [1, 1, 0], unit, 5)
    # Small, [sq,circ,bar,triang] [g,r,b,y]
    ext_s13 = Square(deck_pos, dim_3, [0, 1, 0], unit, 10)
    ext_s14 = Square(deck_pos, dim_3, [1, 0, 0], unit, 3)
    ext_s15 = Square(deck_pos, dim_3, [0, 0, 1], unit, 4)
    ext_s16 = Square(deck_pos, dim_3, [1, 1, 0], unit, 4)
    ext_c13 = Circle(deck_pos, dim_3, [0, 1, 0], unit, 3)
    ext_c14 = Circle(deck_pos, dim_3, [1, 0, 0], unit, 8)
    ext_c15 = Circle(deck_pos, dim_3, [0, 0, 1], unit, 5)
    ext_c16 = Circle(deck_pos, dim_3, [1, 1, 0], unit, 5)
    ext_b13 = Rectangle(deck_pos, dim_3, [0, 1, 0], unit, 0, 10)
    ext_b14 = Rectangle(deck_pos, dim_3, [1, 0, 0], unit, 0, 6)
    ext_b15 = Rectangle(deck_pos, dim_3, [0, 0, 1], unit, 0, 5)
    ext_b16 = Rectangle(deck_pos, dim_3, [1, 1, 0], unit, 0, 5)
    ext_t13 = Triangle(deck_pos, dim_3, [0, 1, 0], unit, 5)
    ext_t14 = Triangle(deck_pos, dim_3, [1, 0, 0], unit, 5)
    ext_t15 = Triangle(deck_pos, dim_3, [0, 0, 1], unit, 5)
    ext_t16 = Triangle(deck_pos, dim_3, [1, 1, 0], unit, 5)

    deck = [ext_s1, ext_s2, ext_s3, ext_s4, ext_c1, ext_c2, ext_c3, ext_c4, ext_b1, ext_b2, ext_b3, ext_b4, ext_t1, ext_t2,
            ext_t3, ext_t4, ext_s5, ext_s6, ext_s7, ext_s8, ext_c5, ext_c6, ext_c7, ext_c8, ext_b5, ext_b6, ext_b7, ext_b8,
            ext_t5, ext_t6, ext_t7, ext_t8, ext_s9, ext_s10, ext_s11, ext_s12, ext_c9, ext_c10, ext_c11, ext_c12, ext_b9,
           ext_b10, ext_b11, ext_b12, ext_t9, ext_t10, ext_t11, ext_t12, ext_s13, ext_s14, ext_s15, ext_s16, ext_c13, ext_c14,
            ext_c15, ext_c16, ext_b13, ext_b14, ext_b15, ext_b16, ext_t13, ext_t14, ext_t15, ext_t16] # DECK_CARDS

    np.random.shuffle(deck)
    ext_objects = [deck[0]] # TOP OF DECK
    ext_env, ext_fov, ext_objects = Environment.initialize(unit, fovea_center, fovea_size, ext_objects)



### START MAIN FUNCTIONING ######################################################################################

    selected_proprierty, chosen_proprierty = System_Components.rule_selection(mental_actions, WM_values,
                                                                              T_inhibition)

    # LANGUAGE CONTRIBUTE TO STRATEGY SELECTION

    WM_values, verbal_prod = Verbal_WM.fin_activation(chosen_proprierty, WM_values, Weight_Lang)

    if Graphics_on:

        plt.ion()
        # plt.figure()
        # plt.axis('off')

        System_Components.foveate_deck_tablet(int_fov, int_env, table_cards[table_cards_retina_focus])  # SACCADE DIRECTED TO FIRST GOAL
        System_Components.foveate_deck_tablet(ext_fov, ext_env, deck[deck_card])  # SACCADE DIRECTED TO DECK

        if Extended_Graphics:

            int_fov_im, ext_fov_im = Analysis_Tools_WCST.Graphics(int_env, table_cards, int_fov, ext_env, ext_objects, ext_fov,
                 unit, actions_made, perseverative_errors, not_perseverative_errors, Completed_Categories, matches, correct_rule, chosen_proprierty, RBM_obj, RBM_obj_second,WM_values_each_turn, responses_list, True, System_parameters)

        else:

            WM_Activations_plot = Analysis_Tools_WCST.Plot_WM_values(WM_values_each_turn, responses_list, True, System_parameters)

    while (test_failed == False) and (test_passed == False):


        System_Components.foveate_deck_tablet(int_fov, int_env, table_cards[table_cards_retina_focus]) # SACCADE DIRECTED TO FIRST CARD
        System_Components.foveate_deck_tablet(ext_fov, ext_env, deck[deck_card]) # SACCADE DIRECTED TO DECK
        System_Components.check_target_position(ext_env, deck_pos, ext_fov) # FOCUS ON THE DECK AND EXTRACT THE RETINA IMAGE
        add_card = System_Components.check_free_space(ext_env, deck_pos, ext_fov) # CHECK IF THE POSITION OF DECK IS FREE

        # print("  STEP - DECK CHECK: IF FREE ADD CARD ")

        if add_card == True: # ...IF IS FREE:

            deck_card += 1

            if deck_card == 64:
                deck_card = 0
                ext_objects = [deck[0]]  # TOP OF DECK
                ext_objects[0].center = np.array(deck_pos)
                ext_env = Environment.redraw(ext_env, unit, ext_objects)

            elif deck_card < 64:
                ext_objects[0] = copy.deepcopy(deck)[deck_card]
                ext_env = Environment.redraw(ext_env, unit, ext_objects)



            if Graphics_on:

                if Extended_Graphics:

                    int_fov_im, ext_fov_im = Analysis_Tools_WCST.Graphics(int_env, table_cards, int_fov, ext_env, ext_objects, ext_fov,
                 unit, actions_made, perseverative_errors, not_perseverative_errors, Completed_Categories, matches, correct_rule, chosen_proprierty, RBM_obj, RBM_obj_second,WM_values_each_turn, responses_list, True, System_parameters)

                else:

                    WM_Activations_plot =  Analysis_Tools_WCST.Plot_WM_values(WM_values_each_turn, responses_list, True,
                                                                                        System_parameters)


        Table_Env_eye, Table_Env_brain = System_Components.RBM_processing(int_fov.get_focus_image(int_env),
                                                                          numbers_layers, False,
                                                                          chosen_proprierty, False,
                                                                          RBM_obj, int, RBM_obj_second)
        table_card_attributes = RBM_obj_second.object_attributes

        Deck_Env_eye, Deck_Env_brain = System_Components.RBM_processing(ext_fov.get_focus_image(ext_env), numbers_layers,
                                                                        False,
                                                                        chosen_proprierty, False,
                                                                        RBM_obj, ext, RBM_obj_second)

        deck_card_attributes = RBM_obj_second.object_attributes


        #print(" STEP  - CHECK IF THE THE DECK CARD  AND TABLE CARD CORRESPOND... ")

        same_image = System_Components.Visual_comparator(Table_Env_brain, Deck_Env_brain, accomplished_threshold)


        if not same_image:

            #print(" STEP  - ...IF THE TABLE CARD AND THE DECK_CARD DO NOT CORRESPOND: SEARCH ANOTHER TABLE CARD ")


            table_cards_retina_focus += 1  # SEQUENTIAL SACCADES

            if table_cards_retina_focus == (len(table_cards)):

                table_cards_retina_focus = 0

            System_Components.foveate_deck_tablet(int_fov, int_env, table_cards[table_cards_retina_focus])

        elif same_image:

            #print(" STEP - IF THE TABLE CARD AND THE DECK_CARD CORRESPOND... ")


            if Graphics_on:

                if Extended_Graphics:

                    int_fov_im, ext_fov_im = Analysis_Tools_WCST.Graphics(int_env, table_cards, int_fov, ext_env, ext_objects, ext_fov,
                                                          unit, actions_made, perseverative_errors,
                                                          not_perseverative_errors, Completed_Categories, matches,
                                                          correct_rule, chosen_proprierty, RBM_obj, RBM_obj_second,
                                                          WM_values_each_turn, responses_list,
                                                          True, System_parameters)

                else:

                    WM_Activations_plot = Analysis_Tools_WCST.Plot_WM_values(WM_values_each_turn, responses_list, True,
                                                                                       System_parameters)



            #print(" STEP - ...WATCH THE DECK ")

            System_Components.foveate_deck_tablet(ext_fov, ext_env, deck[deck_card])

            #print(" STEP -  MOVE! ")

            action = System_Components.parameterised_skill
            action_input = (int_fov.center, limits)
            action(ext_objects[0], *action_input)
            ext_env = Environment.redraw(ext_env, unit, ext_objects)
            ext_fov.move(int_fov.center - ext_fov.center)

            actions_made += 1

            external_feedback, Common_Atributes = Analysis_Tools_WCST.External_operator_feedback(correct_rule, deck_card_attributes, table_card_attributes)

            match, WM_values = System_Components.Abstract_Working_Memory_External_Feedback_Processing(external_feedback, chosen_proprierty, WM_values,
                                                                                                                inhibition_integrity)

            WM_values = System_Components.Abstract_Working_Memory_Decay(chosen_proprierty, mental_actions,
                                                                                  working_memory_forgetting,
                                                                                  WM_values)

            # INSERT HERE THE LANGUAGE CONTRIBUTE - CONTRIBUTE TO REINFORCE PROCESSING

            WM_values, verbal_prod = Verbal_WM.fin_activation(chosen_proprierty, WM_values, Weight_Lang, external_feedback)


            WM_values_each_turn = Analysis_Tools_WCST.Update_WM_values_list(WM_values_each_turn, WM_values)


            actual_turn, matches, perseverative_errors, not_perseverative_errors, distraibility_errors, total_errors, Perseverative_principle, responses_list = Analysis_Tools_WCST.WCST_online_errors_computation(actions_made, correct_rule, matches, perseverative_errors,
                                                                                                                                                                                                              not_perseverative_errors, distraibility_errors, total_errors, Perseverative_principle, table_card_attributes, deck_card_attributes, responses_list)

            Scoring_list, Perseverative_principle, perseverative_errors = Analysis_Tools_WCST.Update_scoring_list(copy.copy((Scoring_list)), actual_turn, Perseverative_principle, perseverative_errors)

            selected_proprierty, chosen_proprierty = System_Components.rule_selection(mental_actions, WM_values, T_inhibition)

            # INSERT HERE THE LANGUAGE CONTRIBUTE - CONTRIBUTE TO STRATEGY SELECTION

            WM_values, verbal_prod = Verbal_WM.fin_activation(chosen_proprierty, WM_values, Weight_Lang)

            if Graphics_on:

                if Extended_Graphics:

                    int_fov_im, ext_fov_im = Analysis_Tools_WCST.Graphics(int_env, table_cards, int_fov, ext_env, ext_objects, ext_fov,
                 unit, actions_made, perseverative_errors, not_perseverative_errors, Completed_Categories, matches, correct_rule, chosen_proprierty, RBM_obj, RBM_obj_second,WM_values_each_turn, responses_list, True, System_parameters)

                else:

                    WM_Activations_plot = Analysis_Tools_WCST.Plot_WM_values(WM_values_each_turn, responses_list, True,
                                                                                       System_parameters)



        if Graphics_on:

            if Extended_Graphics:

                int_fov_im, ext_fov_im = Analysis_Tools_WCST.Graphics(int_env, table_cards, int_fov, ext_env, ext_objects, ext_fov,
                                                      unit, actions_made, perseverative_errors,
                                                      not_perseverative_errors, Completed_Categories, matches,
                                                      correct_rule, chosen_proprierty, RBM_obj, RBM_obj_second,
                                                      WM_values_each_turn, responses_list, True,
                                                      System_parameters)

            else:

                WM_Activations_plot = Analysis_Tools_WCST.Plot_WM_values(WM_values_each_turn, responses_list, True,
                                                                                   System_parameters)

        #BREAK IF TEST IS PASSED OR IS FAILED FOR WSCT


        test_failed, test_passed, matches, Completed_Categories, correct_rule, Perseverative_principle = Analysis_Tools_WCST.WSCT_check_task_passing_conditions(actions_made, matches, Completed_Categories, correct_rules_order, Perseverative_principle, chosen_proprierty)

        if test_passed or test_failed:

            Stop_main = datetime.datetime.today()

            print(' Test stop at = ', Stop_main, ', WCST execution time = ', Stop_main - Start_main)
            print('---------')

            categories_completed, correct_responses_p, uncorrect_responses_p, perseverative_responses_p, perseverative_errors_p, not_perseverative_errors_p, Fms_p, Total_errors_percentual_p, Perseverative_responses_percentual_p, Perseverative_errors_percentual_p, Not_perseverative_errors_percentual_p, responses_list = Analysis_Tools_WCST.Post_processing_scoring_list(copy.deepcopy(Scoring_list))

            plt.close()

            if test_failed:

                global_result = 'FAILED'

            elif test_passed:

                global_result = 'PASSED'

            print("SUBJECT FINAL RESULT:" + str(global_result) + str(" (Parameter profile =  ") + str(
                System_parameters) + str(")"))
            print("")
            print("Total turns = " + str(actions_made))
            print('Completed Categories = ', Completed_Categories)
            print(
                "Total errors = " + str(total_errors) + str(" (") + str(np.around((total_errors / actions_made) * 100, decimals = 2)) + str(
                    " % )"))
            print("")
            print("Errors analisys: ")
            print("")
            print(str("- Perseverative errors = ") + str(perseverative_errors) + str(" (") + str(np.around(
                (perseverative_errors / total_errors) * 100, decimals = 2)) + str(" % )"))
            print(str("- Non_Perseverative errors = ") + str(not_perseverative_errors) + str(" (") + str(
                np.around((not_perseverative_errors / total_errors) * 100, decimals = 2)) + str(" % )"))
            print(str("- Failure to Maintain Set (FMS) = ") + str(distraibility_errors) + str(" (") + str(
                np.around((distraibility_errors / total_errors) * 100, decimals = 2)) + str(" % )"))

    return [uncorrect_responses_p, perseverative_errors_p, not_perseverative_errors_p, Fms_p, categories_completed], WM_values_each_turn, responses_list

    ###END MAIN FUNCTIONING ######################################################################################

# VARIOUS PARAMETERS PROFILES

Optimal = [1, 0.1, 0, 1]

Baldo_Control = [0.49, 0.97, 0.10, 0.81]
Baldo_Non_verbal_shad = [0.17, 0.09, 0.12, 0.23]
Baldo_verbal_shad = [0.14, 0.14, 0.13, 0.14]

Extreme_Perseverative_model = [0.001, 0.97, 0.10, 0.81]
Distracted_model = [0.49, 0.97, 0.4, 0.81]
Irrational_model = [0.49, 1.00, 0.10, 0.81]

# SETTING OF SYSTEM PARAMETERS PROFILE

print('\n Setting of system parameters...\n')

parameters_setting_choice = input('Do you want to set the system parameters? (Yes or No, N.B. '
                                  'in case of "No" they will generate random values) =   ')

while (parameters_setting_choice.upper() != 'YES') and (parameters_setting_choice.upper() != 'NO'):

    print(' Ops, wrong insertion: this question only accepts "Yes" or "No" answers ')

    parameters_setting_choice = input(' Do you want to set the system parameters? (Yes or No, N.B. '
                                      'in case of "No" they will generate random values) =   ')

if parameters_setting_choice.upper() == 'YES':


    # MU---

    Mu_Error_Sensitivity = input('Please insert a value of the parameter "Error Sensitivity" (Range 0-1, Healthy/Control condition = 0.49) =   ')

    Mu_Error_Sensitivity = float(Mu_Error_Sensitivity)

    while (Mu_Error_Sensitivity < 0) or (Mu_Error_Sensitivity > 1):

        print(' Ops, wrong insertion: this parameter (Error sensitivity) only accepts "int" or "float" values in range [0, 1] ')

        Mu_Error_Sensitivity = input('Please insert a value of the parameter "Error Sensitivity" (Range 0-1, Healthy/Control condition = 0.49) =   ')

        Mu_Error_Sensitivity = float(Mu_Error_Sensitivity)

    # PHI---

    Phi_Forgetting_Speed = input('Please insert a value of the parameter "Forgetting Speed" (Range 0-1, Healthy/Control condition = 0.97) =   ')

    Phi_Forgetting_Speed = float(Phi_Forgetting_Speed)

    while (Phi_Forgetting_Speed < 0) or (Phi_Forgetting_Speed > 1):

        print(' Ops, wrong insertion: this parameter (Forgetting_Speed) only accepts "int" or "float" values in range [0, 1] ')

        Phi_Forgetting_Speed = input('Please insert a value of the parameter "Forgetting Speed" (Range 0-1, Healthy/Control condition = 0.97) =   ')

        Phi_Forgetting_Speed = float(Phi_Forgetting_Speed)

    # TAU---

    Tau_Distractibility = input('Please insert a value of the parameter "Distractibility" (Range 0-0.3, Healthy/Control condition = 0.10) =   ')

    Tau_Distractibility = float(Tau_Distractibility)

    while (Tau_Distractibility < 0) or (Tau_Distractibility > 0.3):

        print(' Ops, wrong insertion: this parameter (Distractibility) only accepts "int" or "float" values in range [0, 0.3] ')

        Tau_Distractibility = input('Please insert a value of the parameter "Distractibility" (Range 0-1, Healthy/Control condition = 0.10) =   ')

        Tau_Distractibility = float(Tau_Distractibility)

    # Lambda---

    Lambda_Language_Contribution = input('Please insert a value of the parameter "Language Contribution" (Range 0-1, Healthy/Control condition = 0.81) =   ')

    Lambda_Language_Contribution = float(Lambda_Language_Contribution)

    while (Lambda_Language_Contribution < 0) or (Lambda_Language_Contribution > 1):

        print(' Ops, wrong insertion: this parameter (Language Contribution) only accepts "int" or "float" values in range [0, 1] ')

        Lambda_Language_Contribution = input('Please insert a value of the parameter "Language Contribution" (Range 0-1, Healthy/Control condition = 0.81) =   ')

        Lambda_Language_Contribution = float(Lambda_Language_Contribution)

else:

    Mu_Error_Sensitivity = np.around(np.random.uniform(0, 1), decimals = 3)
    Phi_Forgetting_Speed = np.around(np.random.uniform(0, 1), decimals = 3)
    Tau_Distractibility = np.around(np.random.uniform(0, 0.3), decimals = 3)
    Lambda_Language_Contribution = np.around(np.random.uniform(0, 1), decimals = 3)

# GRAPHICS SETTING

Graphics_on_decision = input('Do you want to check a graphic visualization of system inner processes during the WCST execution? (Yes or No) =   ')


while (Graphics_on_decision.upper() != 'YES') and (Graphics_on_decision.upper() != 'NO'):

    print(' Ops, wrong insertion: this question only accepts "Yes" or "No" answers ')

    Graphics_on_decision = input('Do you want to check a graphic visualization of system inner processes during the WCST execution? (Yes or No) =   ')

if Graphics_on_decision.upper() == 'YES':

    Graphics_on = True

    Graphics_on_Advance_decision = input('Do you want a "complete version" of graphics (a window with all elements, i.e. enviroment, perception and working-memory)\n'
                                         ' or a "compact version" of graphics (a window with just the working-memory values)? (Yes for "complete version" or No for "compact version", '
                                         '\nN.B. th complete version extends the execution time) =   ')

    while (Graphics_on_Advance_decision.upper() != 'YES') and (Graphics_on_Advance_decision.upper() != 'NO'):

        print(' Ops, wrong insertion: this question only accepts "Yes" or "No" answers ')

        Graphics_on_Advance_decision = input(
            'Do you want a "complete version" of graphics (a window with all elements, i.e. enviroment, perception and working-memory)\n'
            ' or a "compact version" of graphics (a window with just the working-memory values)? (Yes for "complete version" or No for "compact version", '
            '\nN.B. the complete version extends the execution time) =   ')

    if Graphics_on_Advance_decision.upper() == 'YES':

        Graphic_Extended_on = True

    else:

        Graphic_Extended_on = False

else:

    Graphics_on = False
    Graphic_Extended_on = False
    Graphics_on_Advance_decision = 'NO'


System_params = [Mu_Error_Sensitivity, Phi_Forgetting_Speed, Tau_Distractibility, Lambda_Language_Contribution]

print('\n ...system parameters set.\n')

print('\n ---Settings overview--- \n\n')
print(' *System Parameters:\n')
print(' - Error_Sensitivity (Mu): ', Mu_Error_Sensitivity, '(Range 0-1, Healthy/Control condition = 0.49)')
print(' - Forgetting_Speed (Phi): ', Phi_Forgetting_Speed, '(Range 0-1, Healthy/Control condition = 0.97)')
print(' - Distractibility (Tau): ', Tau_Distractibility, '(Range 0-0.3, Healthy/Control condition = 0.10)')
print(' - Language_Contribution (Lambda): ', Lambda_Language_Contribution, '(Range 0-1, Healthy/Control condition = 0.81)')

print('\n *Graphics:', Graphics_on_decision.upper(), ', extended graphics:', Graphics_on_Advance_decision.upper())


Errors_list, WM_values_each_turn, responses_list = WCST_Execution(
                                                             System_params,
                                                             Graphics_on,
                                                             Graphic_Extended_on
                                                            )
WM_Activations_plot = Analysis_Tools_WCST.Plot_WM_values(
                                    WM_values_each_turn,
                                    responses_list,
                                    False,
                                    System_params
                                    )

Errors_Plot = Analysis_Tools_WCST.Plot_WSCT_single_subject(System_params,
                                                           len(responses_list),
                                                           Errors_list
                                                           )

plt.show(WM_Activations_plot)
plt.show(Errors_Plot)


print('Stop computations')



