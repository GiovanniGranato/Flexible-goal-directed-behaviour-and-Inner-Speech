
import System_Components
import Environment
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
import copy
import uuid
import os
style.use('ggplot')




# ERRORS COMPUTATIONS AND OTHER FUNCTIONS ------------------

def External_operator_feedback(external_rule,
                               deck_card_attributes,
                               table_card_attributes):

    ### EXTERNAL OPERATOR ACTION #############################

    common_attributes = 0
    qualitative_common_attributes = []

    for i in range(0, table_card_attributes.shape[1]):
        if table_card_attributes[0, i] > 0:
            if table_card_attributes[0, i] == deck_card_attributes[0, i]:
                common_attributes += 1
                if i in range(0, 4):
                    qualitative_common_attributes.append(1)
                elif i in range(4, 8):
                    qualitative_common_attributes.append(2)
                elif i in range(8, 12):
                    qualitative_common_attributes.append(3)

    if external_rule in qualitative_common_attributes:
        feedback = 1
    else:
        feedback = 0

    return feedback, len(qualitative_common_attributes)


def WCST_online_errors_computation(actions_made, correct_rule, matches, perseverative_errors,
                              not_perseverative_errors, distraibility_errors, total_errors, Perseverative_principle,
                              table_card_attributes, deck_card_attributes, responses_list):

    # CHECK COMMON ATTRIBUTES BETWEEN TABLET CARD AND DECK CARD
    common_attributes = 0
    qualitative_common_attributes = []
    responses_list.append([])

    for i in range(0, table_card_attributes.shape[1]):
        if table_card_attributes[0, i] > 0:
            if table_card_attributes[0, i] == deck_card_attributes[0, i]:
                common_attributes += 1
                if i in range(0, 4):
                    qualitative_common_attributes.append(1)
                elif i in range(4, 8):
                    qualitative_common_attributes.append(2)
                elif i in range(8, 12):
                    qualitative_common_attributes.append(3)

    qualitative_common_attributes = list(qualitative_common_attributes)

    if correct_rule not in qualitative_common_attributes:

        Error = True
        single_pers_response = False
        Ambiguity = False
        single_distraibility_error = False

        if common_attributes == 1:

            if Perseverative_principle == [0]:
                Perseverative_principle[0] = qualitative_common_attributes[0]


            elif qualitative_common_attributes[0] == Perseverative_principle[0]:  # PERSEVERATIVE ERROR

                single_pers_response = True



        elif common_attributes > 1:

            Ambiguity = True

        if matches > 5:
            single_distraibility_error = True

        matches = 0

    elif correct_rule in qualitative_common_attributes:

        matches += 1
        responses_list[actions_made - 1].append([1])
        Error = False
        Ambiguity = False
        single_distraibility_error = False
        single_pers_response = False

        # if Perseverative_principle[0] in qualitative_common_attributes:
        #     single_pers_response = True
        # elif Perseverative_principle[0] not in qualitative_common_attributes:

    if Error == True:
        total_errors += 1

    if (Error == True) and (single_pers_response == True):
        perseverative_errors += 1  # PERSEVERATIVE ERRORS
        responses_list[actions_made - 1].append([2])

    if (Error == True) and (single_pers_response == False):
        not_perseverative_errors += 1  # NOT - PERSEVERATIVE ERRORS
        responses_list[actions_made - 1].append([3])

    if single_distraibility_error == True:
        distraibility_errors += 1  # FAILURE TO MAINTAIN SET (FMS)
        responses_list[actions_made - 1].append([4])

    actual_turn = [actions_made, correct_rule, matches, list(qualitative_common_attributes), Error,
                   Ambiguity, single_pers_response, single_distraibility_error, copy.deepcopy(Perseverative_principle)]

    return actual_turn, matches, perseverative_errors, not_perseverative_errors, distraibility_errors, total_errors, Perseverative_principle, responses_list


def WSCT_check_task_passing_conditions(actions_made,
                                       matches,
                                       Completed_Categories,
                                       correct_rules_order,
                                       Perseverative_principle,
                                       chosen_proprierty):

        test_failed = False
        test_passed = False
        correct_rule = correct_rules_order[Completed_Categories]

        if actions_made == 128:
            test_failed = True


        elif actions_made < 128:

            if matches == 10:
                Completed_Categories += 1
                if Completed_Categories == 6:
                    test_passed = True
                    correct_rule = correct_rules_order[0]
                else:
                    correct_rule = correct_rules_order[Completed_Categories]
                    matches = 0
                    Perseverative_principle[0] = correct_rules_order[Completed_Categories - 1]






        return test_failed, test_passed, matches, Completed_Categories, correct_rule, Perseverative_principle



def Update_scoring_list(Scoring_list,
                        actual_turn,
                        Perseverative_principle,
                        perseverative_errors):

        Scoring_list.append(actual_turn)

        if actual_turn[0] > 2:

            last_three_turn = Scoring_list[-3]
            last_two_turn = Scoring_list[-2]
            last_turn = Scoring_list[-1]

            if ((last_three_turn[3] == last_two_turn[3])) and ((last_two_turn[3] == last_turn[3])) and\
                    (last_turn[4]  == True) and (last_turn[5]  == False) and (last_turn[6]  == False):

                Perseverative_principle[0] = last_turn[3][0]
                perseverative_errors += 2

        return Scoring_list, Perseverative_principle, perseverative_errors


def Post_processing_scoring_list(Scoring_list):
    # WITHOUT SANDIWICH RULE......

    correct_responses = 0
    uncorrect_responses = 0
    perseverative_responses = 0
    perseverative_errors = 0
    not_perseverative_errors = 0
    Fms = 0
    Single_subject_scoring = copy.deepcopy(list(Scoring_list))
    del Single_subject_scoring[0]
    total_turns = len(Single_subject_scoring)
    turns_to_change = []

    for i in range(0, len(Single_subject_scoring)):
        single_turn = Single_subject_scoring[i]
        if single_turn[4] == False:
            correct_responses += 1
        elif single_turn[4] == True:
            uncorrect_responses += 1

            if single_turn[6] == True:
                perseverative_errors += 1
            elif single_turn[6] == False:
                not_perseverative_errors += 1
        if single_turn[6] == True:
            perseverative_responses += 1
        if single_turn[7] == True:
            Fms += 1

    # PERCENTUALS

    Total_errors_percentual = np.around((uncorrect_responses / total_turns) * 100)
    Perseverative_responses_percentual = np.around((perseverative_responses / total_turns) * 100)
    Perseverative_errors_percentual = np.around((perseverative_errors / total_turns) * 100)
    Not_perseverative_errors_percentual = np.around((not_perseverative_errors / total_turns) * 100)

    # print("--------------WITHOUT SANDWICE-------------------")
    # print("Total responses = " + str(total_turns))
    # print("Correct responses = " + str(correct_responses))
    # print("Not Correct responses = " + str(uncorrect_responses) + str(" (") + str(
    #     Total_errors_percentual) + str("% )"))
    # print("Perseverative responses = " + str(perseverative_responses) + str(" (") + str(
    #     Perseverative_responses_percentual) + str("% )"))
    # print("Perseverative errors = " + str(perseverative_errors) + str(" (") + str(
    #     Perseverative_errors_percentual) + str("% )"))
    # print(" Not perseverative errors = " + str(not_perseverative_errors) + str(" (") + str(
    #     Not_perseverative_errors_percentual) + str("% )"))
    # print("Failure to Maintain Set (FMS) = " + str(Fms))
    # print("--------------WITHOUT SANDWICE-------------------")

    # WITH SANDIWICH RULE......
    correct_responses = 0
    uncorrect_responses = 0
    perseverative_responses = 0
    perseverative_errors = 0
    not_perseverative_errors = 0
    categories_completed = 0
    Fms = 0
    Single_subject_scoring = copy.deepcopy(list(Scoring_list))
    del Single_subject_scoring[0]
    total_turns = len(Single_subject_scoring)
    Single_subject_scoring = np.array(Single_subject_scoring, dtype=object)
    turns_to_change = []

    for i in range(0, Single_subject_scoring.shape[0]):
        single_turn = Single_subject_scoring[i]

        if single_turn[2] == 10:
            categories_completed += 1

        if (single_turn[4] == True) and (single_turn[6] == True):
            turns_to_change.append(single_turn[0])

        if len(turns_to_change) == 2:
            if (turns_to_change[1] - turns_to_change[0]) > 1:
                Perseverative_princ = Single_subject_scoring[turns_to_change[0] - 1, 8][0]
                first_serie_element = turns_to_change[0] - 1
                last_serie_element = turns_to_change[1] - 1
                cards_serie = Single_subject_scoring[first_serie_element:last_serie_element + 1, 3]
                Pers_serie = True
                for single_card in cards_serie:
                    if Perseverative_princ not in single_card:
                        Pers_serie = False

                # if Pers_serie == False:
                #     print(" In this serie not all cards have also prseverative principle ")
                if Pers_serie == True:
                    Single_subject_scoring[first_serie_element:last_serie_element, 6] = True
                    # print(" In this serie all cards have prseverative principle ")
                del turns_to_change[0]

            elif (turns_to_change[1] - turns_to_change[0]) == 1:
                del turns_to_change[0]

    Single_subject_scoring = list(Single_subject_scoring)
    responses_list = []
    for i in range(0, len(Single_subject_scoring)):
        single_turn = Single_subject_scoring[i]
        responses_list.append([])
        if single_turn[4] == False:
            correct_responses += 1
            responses_list[i].append([1])
        elif single_turn[4] == True:
            uncorrect_responses += 1

            if single_turn[6] == True:
                perseverative_errors += 1
                responses_list[i].append([2])
            elif single_turn[6] == False:
                not_perseverative_errors += 1
                responses_list[i].append([3])
        if single_turn[6] == True:
            perseverative_responses += 1
        if single_turn[7] == True:
            Fms += 1
            responses_list[i].append([4])

    # PERCENTUALS

    Total_errors_percentual = np.around((uncorrect_responses / total_turns) * 100)
    Perseverative_responses_percentual = np.around((perseverative_responses / total_turns) * 100)
    Perseverative_errors_percentual = np.around((perseverative_errors / total_turns) * 100)
    Not_perseverative_errors_percentual = np.around((not_perseverative_errors / total_turns) * 100)

    return categories_completed, correct_responses, uncorrect_responses, perseverative_responses, perseverative_errors, \
           not_perseverative_errors, Fms, Total_errors_percentual, Perseverative_responses_percentual, \
           Perseverative_errors_percentual, Not_perseverative_errors_percentual, responses_list


def Update_WM_values_list(WM_values_each_turn, WM_values):

    WM_values_each_turn.append(WM_values)

    return WM_values_each_turn

# GRAPHICS AND PLOTS ------------------

def Graphics(int_env,
                 table_cards,
                 int_fov,
                 ext_env,
                 ext_objects,
                 ext_fov,
                 unit,
                 actions_made,
                 perseverative_errors,
                 not_perseverative_errors,
                 Completed_Categories,
                 matches,
                 correct_rule,
                 chosen_proprierty,
                 RBM_obj,
                 RBM_obj_second,
                 WM_values_each_turn,
                 responses_list,
                 GRaphic_on_WM,
                 sys_params):

    plt.figure(1)
    plt.clf()

    plt.suptitle(' Behavior and internal functioning of the system ', fontsize=18, weight='bold')


    if correct_rule == 1:
        correct_rule_name = str(" COLOR ")

    elif correct_rule == 2:
        correct_rule_name = str(" FORM ")

    elif correct_rule == 3:
        correct_rule_name = str(" SIZE ")

    if chosen_proprierty == 1:
        chosen_rule_name = str(" COLOR ")

    elif chosen_proprierty == 2:
        chosen_rule_name = str(" FORM ")

    elif chosen_proprierty == 3:
        chosen_rule_name = str(" SIZE ")

    # BOX COLOR

    if matches > 0:
        if correct_rule == chosen_proprierty:
            match = 'green'
        elif correct_rule != chosen_proprierty:
            match = 'grey'
    if matches == 0:
        match = 'red'


    text = plt.figtext(0.02, 0.03, " Cards used = " + str(actions_made) + str("   ") + str(" Completed Categories = ")
                    + str(Completed_Categories), bbox = {'facecolor':'cornflowerblue'}, fontsize= 12)

    text = plt.figtext(0.3, 0.03, "Correct rule = " + correct_rule_name  + str("   ") + str(" Chosen rule = ")
                    + chosen_rule_name + str("   ") + str(" matches = ") + str(matches), bbox = {'facecolor':match},fontsize= 12)

    text = plt.figtext(0.7, 0.03, " Perseverative errors = "  + str(perseverative_errors) + str("   ") + str(" Non - perseverative errors = ") + str(not_perseverative_errors)
                        , bbox = {'facecolor':'red'}, fontsize= 12)


    int_env = Environment.redraw(int_env, unit, table_cards)
    int_fov_im = int_fov.get_focus_image(int_env)

    ext_env = Environment.redraw(ext_env, unit, ext_objects)
    ext_fov_im = ext_fov.get_focus_image(ext_env)


    Table_Env_eye, Table_Env_brain = System_Components.RBM_processing(int_fov_im, 2, False,
                                                                      chosen_proprierty, False,
                                                                      RBM_obj, 1, RBM_obj_second)

    Deck_Env_eye, Deck_Env_brain = System_Components.RBM_processing(ext_fov_im, 2, False,
                                                                    chosen_proprierty, False,
                                                                    RBM_obj, 2, RBM_obj_second)

    plt.subplot2grid((3, 3), (0, 0), colspan = 1, rowspan = 1)
    #plt.subplot(331)
    plt.title('Table cards', fontweight = 'bold')
    plt.xlim(0, unit)
    plt.ylim(0, unit)
    plt.imshow(int_env)

    # PLOT DESK EDGES
    plt.plot([0.0*unit, 0.00*unit, 1.1*unit, 1.1*unit, 0.00*unit], [0.6*unit, 0.9*unit, 0.9*unit, 0.6*unit, 0.6*unit], 'w-')

    # PLOT FOVEA EDGES
    fov_indices = int_fov.get_index_values()
    plt.plot([fov_indices[0][0], fov_indices[0][0], fov_indices[0][1],
              fov_indices[0][1], fov_indices[0][0]],
             [fov_indices[1][0], fov_indices[1][1], fov_indices[1][1],
              fov_indices[1][0], fov_indices[1][0]], 'w-'
             )
    plt.axis('off')

    plt.subplot2grid((3, 3), (0, 1), colspan = 1, rowspan = 1)
    plt.title('Table focus of Fovea', fontweight = 'bold')
    plt.imshow(Table_Env_eye)
    plt.axis('off')

    plt.subplot2grid((3, 3), (0, 2), colspan=1, rowspan=1)
    plt.title('Perceived table card', fontweight = 'bold')
    plt.imshow(Table_Env_brain)
    plt.axis('off')



    plt.subplot2grid((3, 3), (1, 0), colspan=1, rowspan=1)
    plt.title('Deck', fontweight = 'bold')
    plt.xlim(0, unit)
    plt.ylim(0, unit)
    plt.imshow(ext_env)
    # PLOT DECK EDGES
    plt.plot([0.0*unit, 0.00*unit, 1.1*unit, 1.1*unit, 0.00*unit],
              [0.6*unit, 0.9*unit, 0.9*unit, 0.6*unit, 0.6*unit], 'w-')
    # # PLOT FOVEA EDGES
    fov_indices = ext_fov.get_index_values()
    plt.plot([fov_indices[0][0], fov_indices[0][0], fov_indices[0][1],
              fov_indices[0][1], fov_indices[0][0]],
             [fov_indices[1][0], fov_indices[1][1], fov_indices[1][1],
              fov_indices[1][0], fov_indices[1][0]], 'w-'
             )
    # plt.tick_params(axis='x', labelbottom='off')
    # plt.tick_params(axis='y', labelbottom='off')
    plt.axis('off')

    plt.subplot2grid((3, 3), (1, 1), colspan=1, rowspan=1)
    plt.title('Deck Focus of Fovea', fontweight = 'bold')
    plt.imshow(Deck_Env_eye)
    plt.axis('off')



    plt.subplot2grid((3, 3), (1, 2), colspan=1, rowspan=1)
    plt.title('Perceived deck card', fontweight = 'bold')
    plt.imshow(Deck_Env_brain)
    plt.axis('off')

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% WM VALUES PLOT

    plt.subplot2grid((3, 3), (2, 0), colspan=3, rowspan=1)
    #plt.margins(0)

    # values graphic
    X_values = len(WM_values_each_turn)

    three_values_matrix = np.vstack(WM_values_each_turn)

    color_line = three_values_matrix[:, 0]
    form_line = three_values_matrix[:, 1]
    size_line = three_values_matrix[:, 2]

    # errors graphic

    correct_responses = []
    perseverative_errors = []
    non_perseverative_errors = []
    fms_errors = []

    for z in range(0, len(responses_list)):

        single_turn = responses_list[z][0]
        if 1 in single_turn:
            correct_responses.append([z, 1.03])
        if 2 in single_turn:
            perseverative_errors.append([z, 1.09])
        if 3 in single_turn:
            non_perseverative_errors.append([z, 1.15])
        if len(responses_list[z]) > 1:
            fms_errors.append([z, 1.21])

    correct_responses = np.array([correct_responses])
    perseverative_errors = np.array([perseverative_errors])
    non_perseverative_errors = np.array([non_perseverative_errors])
    fms_errors = np.array([fms_errors])

    # ax1 = plt.subplot(211)

    Labels = ['CR', 'PE', 'NPE', 'FMS']

    #plt.clf()
    plt.plot(range(0, X_values), color_line, linestyle=':', linewidth=3, color='cornflowerblue', label='color rule')
    plt.plot(range(0, X_values), form_line, linewidth=3, color='darkred', label='form rule')
    plt.plot(range(0, X_values), size_line, 'k', color='y', label='size rule')
    plt.xticks(np.arange(0, X_values, 10), fontsize=18)
    plt.ylim((0., 1.30))
    if GRaphic_on_WM == True:
        plt.xlim((0, 130))

    plt.xlabel('Choices', weight='bold', labelpad= 1)
    plt.ylabel('WM units activation', weight='bold', labelpad= 7)
    plt.title(' Internal functioning of executive working-memory ', weight='bold')

    plt.legend()

    if correct_responses != []:
        x, y = correct_responses.T
        plt.scatter(x, y, marker='o', color='k')
    if perseverative_errors != []:
        x, y = perseverative_errors.T
        plt.scatter(x, y, marker='o', color='grey')
    if non_perseverative_errors != []:
        x, y = non_perseverative_errors.T
        plt.scatter(x, y, marker='o', color='k')

    if fms_errors != []:
        x, y = fms_errors.T
        plt.scatter(x, y, marker='o', color='grey')
    plt.yticks(np.arange(1.03, 1.27, 0.06), Labels, fontsize=9)





    plt.draw()
    plt.pause(0.2)

    return int_fov_im, ext_fov_im

def Plot_WSCT_single_subject(params,
                             Errors_list):
    # Data_to plot..

    labels = ['CC', 'TE', 'PE', 'NPE', 'FMS']



    categories_completed = Errors_list[4]
    total_errors = Errors_list[0]
    perseverative_errors = Errors_list[1]
    not_perseverative_errors = Errors_list[2]
    distraibility_errors = Errors_list[3]

    Y_data_to_plot = np.around(np.transpose(
        np.array([categories_completed, total_errors, 0, perseverative_errors, not_perseverative_errors, 0,
                  distraibility_errors, 0])), decimals=3)

    STDs = np.zeros(len(Y_data_to_plot))

    # removing spaces

    Y_data_to_plot = np.delete(Y_data_to_plot, [2, 5, 7])
    STDs = np.delete(STDs, [2, 5, 7])

    Result_Plot = plt.figure()
    Result_Plot.suptitle(
        ' WCST Errors scoring  (Single Subject)\n\n' + str(' [ Mu = ') + str(
            np.around(params[0], decimals=3)) + str(', Phi = ') + str(
            np.around(params[1], decimals=3)) + str(', Tau = ') + str(
            np.around(params[2], decimals=3))  + str(', Lambda = ') + str(
            np.around(params[3], decimals=3)) + str(' ] '), fontsize=20, fontweight='bold')

    vertical_limit_graphic = 7
    oriz_limit_graphic = 10
    plt.rc('font', weight='bold')

    # PLOT
    Result_Plot = plt.subplot2grid((vertical_limit_graphic, oriz_limit_graphic), (0, 0), colspan=9, rowspan=4)

    plt.bar(range(0, len(Y_data_to_plot)), Y_data_to_plot, color='cornflowerblue')
    plt.errorbar(range(0, len(Y_data_to_plot)), Y_data_to_plot, STDs, fmt='.k')
    #plt.ylim(0, 40)
    plt.xticks(range(0, len(Y_data_to_plot)), labels)

    if perseverative_errors > not_perseverative_errors:
        color_perseverative = {'facecolor': 'white'}
        color_non_perseverative = {'facecolor': 'white'}

    elif perseverative_errors < not_perseverative_errors:
        color_perseverative = {'facecolor': 'white'}
        color_non_perseverative = {'facecolor': 'white'}

    elif perseverative_errors == not_perseverative_errors:
        color_perseverative = {'facecolor': 'white'}
        color_non_perseverative = {'facecolor': 'white'}

    Tables_errors_systems = plt.subplot2grid((vertical_limit_graphic, oriz_limit_graphic), (4, 0), colspan=9,
                                             rowspan=3)

    Subjects_measures_all_matrices = copy.deepcopy(Y_data_to_plot)
    Subjects_measures_all_matrices = Subjects_measures_all_matrices

    # Table_Errors = np.array(Table_Errors, dtype='str')
    #
    # for column in range(0, Subjects_measures_all_matrices.shape[0]):
    #
    #         val = np.around(Subjects_measures_all_matrices, decimals=2)[column]
    #
    #         Table_Errors[column] = copy.deepcopy(val)

    Table_Errors = np.array(Subjects_measures_all_matrices, dtype='str')
    Table_comparison = Tables_errors_systems.table(cellText= [Table_Errors],
                                                   rowColours=['g'],
                                                   colColours=['#6495ED', '#6495ED', '#6495ED', '#6495ED', '#6495ED'],
                                                   loc='center', colLabels=['CC', 'TE', 'PE', 'NPE', 'FMS'], rowLabels=['Errors'],
                                                   cellLoc='center')

    Tables_errors_systems.axis("off")
    Table_comparison.auto_set_font_size(False)
    Table_comparison.set_fontsize(12)

    text = plt.figtext(0.1, 0.10,
                       'CC = Completed Categories, TE = Total Errors, PE = Perseverative Errors, NPE = Non Perseverative Errors, FME = Failures-to-maintains Sets',
                       fontsize=12)

    print('---------')
    return Result_Plot


def Plot_WM_values(WM_values_each_turn,
                             responses_list,
                             GRaphic_on_WM,
                             sys_params):


    inhibition_integrity = sys_params[0]
    working_memory_forgetting = sys_params[1]
    T_inhibition = sys_params[2]
    if len(sys_params) > 3:
        Lang_Weight = sys_params[3]

    #values graphic
    X_values = len(WM_values_each_turn)

    three_values_matrix = np.vstack(WM_values_each_turn)

    color_line = three_values_matrix[:,0]
    form_line = three_values_matrix[:,1]
    size_line = three_values_matrix[:,2]

    #errors graphic

    correct_responses = []
    perseverative_errors = []
    non_perseverative_errors = []
    fms_errors = []

    for z in range(0, len(responses_list)):

        single_turn = responses_list[z][0]
        if 1 in single_turn:
            correct_responses.append([z, 1.03])
        if 2 in single_turn:
            perseverative_errors.append([z,  1.09])
        if 3 in single_turn:
            non_perseverative_errors.append([z,  1.15])
        if len(responses_list[z]) > 1:
            fms_errors.append([z,  1.21])


    correct_responses = np.array([correct_responses])
    perseverative_errors = np.array([perseverative_errors])
    non_perseverative_errors = np.array([non_perseverative_errors])
    fms_errors = np.array([fms_errors])

    if GRaphic_on_WM:

        fig_motiv = plt.figure(50)

    else:

        fig_motiv = plt.figure()


    # ax1 = plt.subplot(211)

    Labels = ['CR', 'PE', 'NPE', 'FMS']

    plt.clf()
    plt.plot(range(0,X_values), color_line, linestyle= ':', linewidth=3, color = 'cornflowerblue', label = 'color rule')
    plt.plot(range(0, X_values), form_line, linewidth= 3, color = 'darkred', label = 'form rule')
    plt.plot(range(0, X_values), size_line, 'k', color = 'y', label = 'size rule')
    plt.xticks(np.arange(0, X_values, 10), fontsize = 18)
    plt.ylim((0., 1.30))
    if GRaphic_on_WM == True:
        plt.xlim((0, 130))

    plt.xlabel('Choices', fontsize = 23)
    plt.ylabel('WM units activation', fontsize= 22)

    if len(sys_params) > 3:

        plt.title(' Internal functioning of executive working-memory ' + str('\n\n [ Mu = ') + str(
            np.around(inhibition_integrity, decimals= 3)) + str(', Phi = ') + str(np.around(working_memory_forgetting, decimals = 3)) + str(', Tau = ') + str(
            np.around(T_inhibition, decimals=3)) + str(', Lambda = ') + str(
            np.around(Lang_Weight, decimals=3)) + str(' ]'), fontsize=20, weight='bold')
    else:

        plt.title(' Internal functioning of executive working-memory ' + str('\n\n [ I = ') + str(
            np.around(inhibition_integrity, decimals=3)) + str(', F = ') + str(
            np.around(working_memory_forgetting, decimals=3)) + str(', T = ') + str(
            np.around(T_inhibition, decimals=3)) + str(' ]'), fontsize=20, weight='bold')



    plt.legend()

    if correct_responses != []:
        x, y = correct_responses.T
        plt.scatter(x, y, marker='o', color = 'k')
    if perseverative_errors != []:
        x, y = perseverative_errors.T
        plt.scatter(x, y, marker='o', color = 'grey')
    if non_perseverative_errors != []:
        x, y = non_perseverative_errors.T
        plt.scatter(x, y, marker='o', color = 'k')

    if fms_errors != []:
        x, y = fms_errors.T
        plt.scatter(x, y, marker='o', color = 'grey')
    plt.yticks(np.arange(1.03, 1.27, 0.06), Labels, fontsize=17)

    if GRaphic_on_WM == True:

        plt.pause(0.0001)

    # else:
    #     plt.show()

    return fig_motiv
