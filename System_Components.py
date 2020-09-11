import numpy as np
import copy
import scipy.ndimage as ndimage
from geometricshapes import Fovea
import matplotlib.style as style
style.use('ggplot')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.ndimage
from scipy.interpolate import interp1d
import csv



### WORKING-MEMORY ################################

def Abstract_Working_Memory_External_Feedback_Processing(external_feedback, selected_proprierty, action_reward_value, inhibition_integrity=1):

    Total_mental_actions = [1, 2, 3]
    selected_proprierty = Total_mental_actions.index(selected_proprierty)


    ### INTERNAL PROCESSING OF FEEDBACK #############################

    if external_feedback == 1:
        inhibition_integrity = 0.7

    action_reward_value[selected_proprierty] += inhibition_integrity * (external_feedback - action_reward_value[selected_proprierty])

    return external_feedback, np.around(action_reward_value, decimals=2)

def Abstract_Working_Memory_Decay(selected_mental_action, total_actions, working_memory_forgetting, action_reward_value):


    remained_proprierties = copy.deepcopy(total_actions)

    #remained_proprierties.remove(selected_mental_action)

    for i in range(0, len(remained_proprierties)):

        action_reward_value[total_actions.index(remained_proprierties[i])] += working_memory_forgetting * (0.5 - action_reward_value[total_actions.index(remained_proprierties[i])])

    return action_reward_value


### VISUAL COMPARATOR ################################

def Visual_comparator(image_array_1, image_array_2, threshold=0.1):

    vector_1 = image_array_1.flatten('F')
    vector_2 = image_array_2.flatten('F')
    diff = vector_1 - vector_2
    norm = np.linalg.norm(diff)
    if norm/len(vector_1) <= threshold:
        return True
    else:
        return False


### TOP-DOWN SELECTOR/MANIPULATOR ################################

def lateral_inhibition(competitive_activations, T = 0.01):


    competitive_activations = copy.deepcopy(competitive_activations)
    selected_attribute = np.argmax(competitive_activations)


    competitive_activations = np.exp(competitive_activations / T)
    competitive_activations = competitive_activations / sum(competitive_activations)
    competitive_activations = np.cumsum(competitive_activations)

    noise_treshold = np.random.random_sample()



    for i in range(0, len(competitive_activations)):
        if (competitive_activations[i] - noise_treshold) >= 0:
            selected_attribute = i
            break



    return selected_attribute

def Hard_lateral_inhibition(competitive_activations):

        competitive_activations = copy.deepcopy(competitive_activations)
        selected_attribute = np.argmax(competitive_activations)

        competitive_activations[competitive_activations != 0.0] = 0.0
        competitive_activations[selected_attribute] = 1

        return competitive_activations

def rule_selection(mental_actions, action_reward_value, T_inhibition):

    selected_proprierty = lateral_inhibition(action_reward_value, T_inhibition)
    selected_mental_action = mental_actions[selected_proprierty]

    return selected_proprierty, selected_mental_action

def Top_down_Manipulator(proprierty, RBM_obj_second):


        RBM_obj_second.real_activation_second_hidden = copy.deepcopy(RBM_obj_second.hidden_output)  # to save variable for reconstruction of second RF
        RBM_obj_second.object_attributes = np.reshape(
                (np.concatenate((Hard_lateral_inhibition(copy.deepcopy(RBM_obj_second.hidden_output[0, 0:4])),
                                 Hard_lateral_inhibition(copy.deepcopy(RBM_obj_second.hidden_output[0, 4:8])),
                                 (Hard_lateral_inhibition(copy.deepcopy(RBM_obj_second.hidden_output[0, 8:12])))))),(1, 12)) # TO SAVE VARIABLE FOR EXTERNAL OPERATOR

        # FIXED WEIGHTS/VALUES OF MANIPULATOR (DISINHIBITION)
        weights_first_layer = np.array([-1, -1, -1])
        weights_inibitor_layer =  10 * np.array([[-1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, -1, -1, -1, -1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1]])
        inibitor_layer = np.array([1, 1, 1])

        # ATTRIBUTES MANIPULATION
        RBM_obj_second.hidden_output[0:12] = np.reshape(
            (np.concatenate((Hard_lateral_inhibition(copy.deepcopy(RBM_obj_second.hidden_output[0, 0:4])),
                             Hard_lateral_inhibition(copy.deepcopy(RBM_obj_second.hidden_output[0, 4:8])),
                             (Hard_lateral_inhibition(copy.deepcopy(RBM_obj_second.hidden_output[0, 8:12])))))),(1, 12))

        #TRASFORMATION FROM SELECTED PROPERTY TO INPUT VECTOR FOR MANIPULATION
        if proprierty == 0:
            input_ = np.array([1, 1, 1])

        elif proprierty == 1:
            input_ = np.array([1, 0, 0])
        elif proprierty == 2:
            input_ = np.array([0, 1, 0])
        elif proprierty == 3:
            input_ = np.array([0, 0, 1])
        elif proprierty > 3:
            input_ = np.array([0, 0, 0])

        # CATEGORIES MANIPULATION
        inibitor_layer += input_ * weights_first_layer
        selection_bias = np.dot(inibitor_layer, weights_inibitor_layer)
        RBM_obj_second.hidden_output += selection_bias # APPLICATION OF BIAS ON THE LAST LAYER OF RBM

        # SIMULATION OF NEURAL POPULATION INTO THIS TASK: IN OUR SYS ACTIVATIONS UNDER 0 HAVE NO SENSE SO WE ASSIGNED A 0 VALUE TO THEM (DO NOT PARTECIPATE TO RECONSTRUCTION)

        RBM_obj_second.hidden_output[RBM_obj_second.hidden_output < 0] = 0

        RBM_obj_second.real_activation_second_hidden = copy.deepcopy(RBM_obj_second.hidden_output)

        # random_treshold = np.random.random_sample()  # noise, case
        #
        #
        # RBM_obj_second.hidden_output[RBM_obj_second.hidden_output > random_treshold] = 1

        return proprierty, RBM_obj_second.hidden_output, RBM_obj_second

### INNER SPEECH SYSTEM ################################

class Verbal_WM():

    def __init__(self, size_inp, size_out, temp=1.):

        self.temp = temp
        self.learn_weights = np.load('.\\System_files\\weights_save_2.npy')
        self.final_weights = np.load('.\\System_files\\weights_save_1.npy')

    def fin_activation(self, selected_category, wm_values, language_weight, feedback=1):

        # if feedback == 0:
        #     language_weight = 0.001

        if selected_category == 1:
            self.inputs = np.array([1., 0., 0.])

        elif selected_category == 2:
            self.inputs = np.array([0., 1., 0.])

        else:
            self.inputs = np.array([0., 0., 1.])

        self.inputs = np.hstack((self.inputs, feedback))
        out_final_hidd = np.dot(self.inputs, self.learn_weights.T)
        out_final_hidd_transformed = 1 / (1 + np.exp(-out_final_hidd / self.temp))
        out_final_hidd_transformed = np.around(out_final_hidd_transformed)
        out_final_overt = np.dot(out_final_hidd_transformed, self.final_weights.T)
        wm_values += out_final_overt * language_weight
        wm_values[wm_values > 1] = 1
        wm_values[wm_values < 0] = 0
        return wm_values, out_final_overt
        # wm_values

### HIERARCHICAL PERCEPTUAL SYSTEM ################################



class RBM(object):

    def __init__(self, single_layer, size_hidden, learning_rate = 0.1, alfa = 0.0, sparsety = 0.0, K = 1):

        # other variables
        self.size_hidden = size_hidden
        self.K = K
        self.sparsety = sparsety
        self.learning_rate = learning_rate
        self.alfa = alfa
        self.n = 0
        self.single_layer = single_layer
        self.input_units = 0
        self.reconstructed_matrices = []
        self.reconstructed_all_output = []
        self.single_input_errors = x = [[] for i in range(64)]
        self.single_input_errors_2 = x = [[] for i in range(64)]
        self.Std_epoc = []
        self.rec_cards = []
        self.Max_performance = []
        self.FirstSecondErrors = []
        self.FirstErrors = []
        self.SecondErrors = []
        self.action_reward_value = np.zeros((1,2))
        self.inhibition_integrity = 1.0
        self.test_RF = 0
        self.All_Polygons = 0

        #VARIABLES FOR MULTI RESONANCES RBM
        self.noise_level = 0
        self.resonances_count = 0
        self.distractor = 0
        self.distractors = 0
        self.Weight_distractor = 0

        #INPUT VARIABLES

        self.cumulated_bias_hidden_weights = np.zeros((1,size_hidden))
        self.input = np.zeros((self.input_units))
        self.input_update_weights = np.zeros((self.input_units, size_hidden))
        self.input_update_weights_prev = np.zeros((self.input_units, size_hidden))
        self.cumulated_input_hidden_weights = np.zeros((self.input_units, size_hidden))
        self.input_weights = np.zeros((self.input_units, size_hidden))
        self.rec_input = np.zeros((self.input_units))
        self.image_side = 28
        #inputs_biases
        self.cumulated_bias_input_weights = np.zeros((1,size_hidden))
        self.bias_inputs_update_weights_prev = np.zeros((1, size_hidden))
        self.bias_inputs_weights = np.zeros((1, size_hidden))



        #HIDDENS VARIABLES

        self.selected_max_hiddens_activation = []
        self.reconstructed_all_hidden = []

        #hidden_biases
        self.cumulated_bias_hidden_weights = np.zeros((1, self.input_units))
        self.bias_hidden_update_weights_prev = np.zeros((1,self.input_units))
        self.bias_hidden_weights = np.zeros((1, self.input_units))
        self.reconstructed_hidden_bias = [0]


#   FUNCTIONS FOR LOADING IMAGES, GETTING INPUTS, INITIALIZATING WEIGHTS

    def get_images (self, resize_choice, MNIST = 0):

        self.MNIST_value = MNIST

        if MNIST == 0:

            if resize_choice == 1:

                originals_matrices = np.load(".\\System_files\\RBM_ALL_MEASURE_polygons.npz")

                inputs_test_learn = np.load(".\\System_files\\RBM_ALL_MEASURE_polygons.npz")

                originals_matrices = [originals_matrices[key] for key in originals_matrices]
                originals_matrices = originals_matrices[0]

                inputs_test_learn = [inputs_test_learn[key] for key in inputs_test_learn]
                inputs_test_learn = inputs_test_learn[0]


                #print("resize of polygons = from 66 x 66 to 28 x 28 " '\n')

                self.originals_matrices = inputs_test_learn #np.array(inputs_test_learn)

                self.inputs_test_learn = inputs_test_learn #np.array(inputs_test_learn)

                self.number_input_units = len(inputs_test_learn[0])

                self.image_side = np.sqrt(self.number_input_units / 3)

    def variables_changes_for_images(self, single_layer, hidden_output_first = 0, input_units = 0):


        #dynamical initialization of RBM class depending on images..


        if single_layer == 1:

            self.input_units = self.inputs_test_learn[0].shape[0]

        elif single_layer == 2:

            self.input_units = hidden_output_first



        self.input = np.zeros((self.input_units))
        self.input_update_weights = np.zeros((self.input_units, self.size_hidden))
        self.input_update_weights_prev = np.zeros((self.input_units, self.size_hidden))
        self.cumulated_input_hidden_weights = np.zeros((self.input_units, self.size_hidden))
        self.input_weights = np.zeros((self.input_units, self.size_hidden))
        self.rec_input = np.zeros((self.input_units))

        #hidden_biases
        self.cumulated_bias_hidden_weights = np.zeros((1, self.input_units))
        self.bias_hidden_update_weights_prev = np.zeros((1,self.input_units))
        self.bias_hidden_weights = np.zeros((1, self.input_units))

    def get_input(self, single_layer, batch_single, Batch_size_first, hiddens_second_input = 0):



        # CHOICE OF INPUT (FIRST RBM TAKES THE DATABASE WHILE SECOND RBM TAKES OUTPUT OF FIRST RBM)
        if single_layer == 1:
            self.input = self.inputs_test_learn

        # BATCH MODE ON/OFF
        elif single_layer == 2:
            if Batch_size_first == hiddens_second_input.shape[0]:
                self.input = hiddens_second_input
            elif Batch_size_first == 1:
                self.input = hiddens_second_input[batch_single]

        self.input_first = copy.deepcopy(self.input)

        return self.input


    def initialization_weights(self, size_input, size_hidden):

        self.input_weights = np.random.uniform(-0.1, 0.1, (size_input, size_hidden))

        self.bias_inputs_weights = np.random.uniform(-0.1, 0.1,(1, size_hidden))

        self.bias_hidden_weights = np.random.uniform(-0.1, 0.1,(1, size_input))


#    SPREAD, RECONSTRUCTION FUNCTIONS

    def get_output_first_layer(self, stochasticity = False):


        self.hidden_pot = np.dot(self.input, self.input_weights)

        self.hidden_pot = self.hidden_pot + self.bias_inputs_weights

        self.hidden_output = 1 / (1 + np.exp(-(self.hidden_pot)))


        # STOCHASTIC TRANSFORMATION (BINARY VALUES OF 0 OR 1) + IMPLEMENTATION OF SPARSETY (IF NECESSARY)
        if stochasticity == True:

            random_treshold = np.random.random_sample()  # noise, case


            self.hidden_output[self.hidden_output > random_treshold] = 1

            self.hidden_output[self.hidden_output < random_treshold] = 0


            current_sparsety = (np.sum(((np.sum((self.hidden_output), axis = 0)) / self.input.shape[0]))) / self.hidden_output.shape[1]

            current_target = (current_sparsety - self.sparsety)

            self.penalty = self.learning_rate * current_target * self.K

            if current_sparsety <= self.sparsety:

                self.penalty = 0 * self.penalty # if current sparsety is lower then target sparsety: penalty = 0



            self.hidde_output_first = self.hidden_output


        return self.hidden_output

    def input_reconstruction(self, test=0, print_error = 1):

        rec_pot = np.dot(self.hidden_output, self.input_weights.T)

        rec_pot = rec_pot + self.bias_hidden_weights

        self.rec_input = 1 / (1 + np.exp(-(rec_pot)))

        self.rec_input_with_distractor = (1 - self.Weight_distractor) * self.rec_input + self.Weight_distractor * self.distractor


        self.before_subst_input = np.copy(self.input)

        self.input = self.rec_input_with_distractor

        #EPOC ERROR CALCULATION

        self.error_1 = np.abs(self.input_first - self.rec_input)

        self.errors_for_input = self.error_1.sum(axis=1) / self.error_1.shape[1]

        self.avg_errors_1 = np.mean(self.errors_for_input * 100)

        self.St_dev_errors_1 = np.std(self.errors_for_input * 100)

        self.percent_error_1 = self.avg_errors_1

        return  self.rec_input, self.errors_for_input

    # LOAD WEIGHTS OF RBM

    def load_weights(self, load_choice, single_layer):

        if load_choice == 1:

            self.input_weights = np.load(
                '.\\System_files\\RBM_layer_weights_' + str(
                    single_layer) + str('.npy'))
            self.bias_inputs_weights = np.load(
                '.\\System_files\\RBM_layer_Bias_inputs_weights_' + str(
                    single_layer) + str('.npy'))
            self.bias_hidden_weights = np.load(
                '.\\System_files\\RBM_layer_Bias_hidden_weights_' + str(
                    single_layer) + str('.npy'))
            self.hidden_output = np.load(
                '.\\System_files\\hidden_output_layer_' + str(
                    single_layer) + str('.npy'))



    #   BIOLOGICAL / NEUROPSYCHOLOGICAL INSPIRED FUNCTIONS

    def cortical_magnification(self, fovea_image):

        not_magnificated_fovea = fovea_image
        if (np.isscalar(not_magnificated_fovea) == True) or (np.sum(not_magnificated_fovea) == 0):
            not_magnificated_fovea = np.zeros((20, 20, 3))

        magnificated_fovea = scipy.ndimage.zoom(not_magnificated_fovea, (1.4, 1.4, 1))

        magnificated_fovea = magnificated_fovea.flatten('F')
        # magnificated_fovea = magnificated_fovea.reshape(1, magnificated_fovea.shape[0])

        if np.sum(magnificated_fovea) > 1:
            max = np.max(magnificated_fovea)
            min = np.min(magnificated_fovea)
            m = interp1d([min, max], [0, 1])
            magnificated_fovea = m(magnificated_fovea)

        return magnificated_fovea

    def Hard_lateral_inhibition(self, competitive_activations):

        competitive_activations = copy.deepcopy(competitive_activations)
        selected_attribute = np.argmax(competitive_activations)

        competitive_activations[competitive_activations != 0.0] = 0.0
        competitive_activations[selected_attribute] = 1

        return competitive_activations# RBM FUNCTIONS (INITIALIZATION, LEARNING, ACTIVATION)

    # FUNCTION THAT RETURNS GRAPHS AND RECEPTIVE FIELDS

    def Graphical_reconstruction_inputs_hiddens_outputs(self, RBM_obj, Total_inputs, plot_choice, Hidden_units_second, hiddens_plotted, numbers_layers, int_ext, Graphic_on, RBM_obj_second =0):


        for inp in range(0,Total_inputs):

            RBM_obj.Polygons_recostructions(inp)


            if Graphic_on == True:

                # GRAPHICAL RECONSTRUCTION OF INPUT
                RBM_obj.Graphical_poly_rec(inp, plot_choice, hiddens_plotted, numbers_layers, int_ext)

                if RBM_obj.test_RF == 1:

                    # GRAPHICAL RECONSTRUCTION OF HIDDEN RECEPTIVE FIELDS

                    RBM_obj.Polygons_hidden_recostruction(inp, plot_choice, hiddens_plotted)
                    RBM_obj.Graphical_hidden_rec(1, inp, numbers_layers)

                    if numbers_layers == 2:
                         RBM_obj.Polygons_hidden_second_recostruction(RBM_obj, RBM_obj_second, Hidden_units_second)
                         RBM_obj.Graphical_hidden_rec(2, inp, numbers_layers, RBM_obj_second)






            #RBM_obj.reconstructed_all_hidden = []


    # MATRICIAL RECONSTRUCTIONS (INPUTS, HIDDENS, OUTPUTS)

    def Polygons_recostructions(self, single_input):

        if self.MNIST_value == 0:
            self.image_side = np.sqrt(((self.rec_input.shape[1]) / 3))

        elif self.MNIST_value == 1:
            self.image_side = np.sqrt(((self.rec_input.shape[1]) / 1))


        reconstructed_single_input = self.rec_input
        reconstructed_single_original = self.before_subst_input.reshape(1, self.input_first.shape[0])


        self.n += 1



        if self.MNIST_value == 0:
            self.original = reconstructed_single_original[single_input].reshape([int(self.image_side), int(self.image_side), 3], order='F')

        elif self.MNIST_value == 1:
            self.original = reconstructed_single_original[single_input].reshape([int(self.image_side), int(self.image_side)])


        # change of values ina 0-1 range
        max = np.max(self.original)
        min = np.min(self.original)
        m = interp1d([min, max], [0, 1])
        self.original = m(self.original)

        if self.MNIST_value == 0:
            self.rec_matrix = reconstructed_single_input[single_input].reshape([int(self.image_side), int(self.image_side), 3], order='F')

        elif self.MNIST_value == 1:
            self.rec_matrix = reconstructed_single_input[single_input].reshape([int(self.image_side), int(self.image_side)])


        #change of values ina 0-1 range
        max = np.max(self.rec_matrix)
        min = np.min(self.rec_matrix)
        m = interp1d([min, max], [0, 1])
        self.rec_matrix = m(self.rec_matrix)

        self.reconstructed_matrices.append(self.rec_matrix)

    def Polygons_hidden_recostruction(self, single_inp, personal_plotting_choice, hiddens_plotted):

        self.hiddens_activation_for_inp = self.hidden_output[single_inp,:]

        if self.single_layer == 2:

            self.hiddens_activation_for_inp = self.input


        #loop for reconstruction of each Hidden receptors field...

        for i in range(0, len(self.hiddens_activation_for_inp)):

            if self.hiddens_activation_for_inp[i] > 0.1:

                self.selected_max_hiddens_activation.append(i)

        if personal_plotting_choice == 1:

            self.selected_max_hiddens_activation = self.hiddens_activation_for_inp.argsort()[::-1][:hiddens_plotted]


        for i in range(0, len(self.selected_max_hiddens_activation)):

                self.rec_single_hidden = self.input_weights[:, self.selected_max_hiddens_activation[i]] #take single hidden receptor field

                # change of values ina 0-1 range

                max = np.max(self.rec_single_hidden)
                min = np.min(self.rec_single_hidden)
                m = interp1d([min, max],[0,1])
                self.rec_single_hidden = m(self.rec_single_hidden)


                #reconstruction of hiddens matrices

                if self.MNIST_value == 0:
                    self.recostructed_single_hidden = self.rec_single_hidden.reshape([int(self.image_side), int(self.image_side), 3], order='F')

                elif self.MNIST_value == 1:
                    self.recostructed_single_hidden = self.rec_single_hidden.reshape([int(self.image_side), int(self.image_side)])

                self.reconstructed_all_hidden.append(self.recostructed_single_hidden)



        # bias receptor field reconstruction
        if self.MNIST_value == 0:

            self.reconstructed_hidden_bias[0] = (self.bias_hidden_weights.reshape([int(self.image_side), int(self.image_side), 3], order='F'))

        elif self.MNIST_value == 1:

            self.reconstructed_hidden_bias[0] = (self.bias_hidden_weights.reshape([int(self.image_side), int(self.image_side)]))

        max = np.max(self.reconstructed_hidden_bias)
        min = np.min(self.reconstructed_hidden_bias)
        m = interp1d([min, max], [0, 1])
        self.reconstructed_hidden_bias = m(self.reconstructed_hidden_bias)

    def Polygons_hidden_second_recostruction(self, RBM_obj_first, RBM_obj_second, Hidden_units_second):

        output_second_RBM_initital = copy.deepcopy(RBM_obj_second.real_activation_second_hidden)
        if output_second_RBM_initital.shape[0] != 1:
            bias = np.ones((output_second_RBM_initital.shape[0], 1))
            output_second_RBM_initital = np.concatenate((output_second_RBM_initital, bias), axis=1)
        else:
            bias = 1
            output_second_RBM_initital = np.insert(output_second_RBM_initital, output_second_RBM_initital.shape[1], bias)




        # simulated reconstruction of input activing specific second_hiddens_neurons


        output_second_RBM = np.zeros((Hidden_units_second + 1, RBM_obj_second.hidden_output.shape[1]))#copy.deepcopy(RBM_obj_second.hidden_output)

        #output_second_RBM[:, :] = 0

        for i in range(0, Hidden_units_second):

            output_second_RBM[i, i] = 1

        rec_hidden_first_RBM = np.dot(output_second_RBM, RBM_obj_second.input_weights.T)

        rec_hidden_first_RBM_potential = rec_hidden_first_RBM + RBM_obj_second.bias_hidden_weights

        rec_hidden_first_RBM = 1 / (1 + np.exp(-(rec_hidden_first_RBM_potential)))

        rec_input_first_RBM = np.dot(rec_hidden_first_RBM, RBM_obj_first.input_weights.T)

        rec_input_first_RBM_potential = rec_input_first_RBM + RBM_obj_first.bias_hidden_weights

        rec_input_first_RBM = 1 / (1 + np.exp(-(rec_input_first_RBM_potential)))

        self.receptive_fields_Second_hidden = []

        # to extract all of second_RBM_hiddens receptive fields

        for i in range(0, Hidden_units_second + 1):
            single_hidden_Second_receptive_field = rec_input_first_RBM[i, :]

            single_matrix_hidden_second = single_hidden_Second_receptive_field.reshape([int(RBM_obj_first.image_side), int(RBM_obj_first.image_side), 3], order='F')

            self.receptive_fields_Second_hidden.append(single_matrix_hidden_second)

        # to extract second_RBM_hiddens those partecipate to specific input_reconstruction

        self.selected_second_hiddens = [[] for _ in range(1)] # CLASSICAL BARBA - TRICK :  I HAVE TO MODIFY THIS PART TO ADAPT FOR ONLINE MODE

        for h in range(0, len(self.selected_second_hiddens)):

            #h = 0 # CLASSICAL BARBA - TRICK :  I HAVE TO MODIFY THIS PART TO ADAPT FOR ONLINE MODE

            single_input_hidden_rec_fields = output_second_RBM_initital#[h, :] # CLASSICAL BARBA - TRICK :  I HAVE TO MODIFY THIS PART TO ADAPT FOR ONLINE MODE

            for n in range(0, len(single_input_hidden_rec_fields)):

                if single_input_hidden_rec_fields[n] > 0.3:
                    self.selected_second_hiddens[h].append(n)

        self.selected_second_hiddens = self.selected_second_hiddens[0] # CLASSICAL BARBA - TRICK :  I HAVE TO MODIFY THIS PART TO ADAPT FOR ONLINE MODE

        self.receptive_fields_for_inp = [[] for _ in range(1)] # CLASSICAL BARBA - TRICK :  I HAVE TO MODIFY THIS PART TO ADAPT FOR ONLINE MODE
        self.receptive_fields_for_inp = self.receptive_fields_for_inp[0]
        #for i in range(0, len(self.selected_second_hiddens)):

        for l in range(0, len(self.selected_second_hiddens)):

            coupled_indices = self.selected_second_hiddens # CLASSICAL BARBA - TRICK :  I HAVE TO MODIFY THIS PART TO ADAPT FOR ONLINE MODE

            coupled_index = coupled_indices [l]

            self.receptive_fields_for_inp.append(self.receptive_fields_Second_hidden[coupled_index])



        # max = np.max(self.receptive_fields_for_inp)
        # min = np.min(self.receptive_fields_for_inp)
        # m = interp1d([min, max], [0, 1])
        # magnificated_fovea = m(self.receptive_fields_for_inp)
        # for i in range(0,len(self.receptive_fields_for_inp)):
        #
        #     self.receptive_fields_for_inp[i].append(self.receptive_fields_Second_hidden[-1])

    # GRAPHICAL RECONSTRUCTIONS (INPUTS, HIDDENS, OUTPUTS)

    def Graphical_poly_rec(self, single_input, plot_choice, hiddens_plotted,numbers_layers,int_ext):

        #VERTICAL LIMITS
        self.vertical_limit_graphic = 7

        if numbers_layers == 2:

            self.vertical_limit_graphic = 11


        #ORIZONTAL LIMITS
        self.oriz_limit_graphic = hiddens_plotted

        if hiddens_plotted < 7:
            self.oriz_limit_graphic = 7


        #PLOT FIRST IMAGE

        if int_ext == 1:
            graph = 2
        elif int_ext == 2:
            graph = 3

        self.figures = plt.figure(graph)

        if int_ext == 1:
            self.figures.suptitle('____Table____', fontsize=15)
        if int_ext == 2:
            self.figures.suptitle('____Deck____', fontsize=15)

        self.figures = plt.subplot2grid((self.vertical_limit_graphic, self.oriz_limit_graphic), (0, 0), colspan = 3, rowspan = 3)

        plt.imshow(self.original)

        self.figures.set_title(' Original image ')

        plt.axis('off')

        # PLOT SECOND IMAGE (RECONSTRUCTION)

        self.figures = plt.subplot2grid((self.vertical_limit_graphic, self.oriz_limit_graphic), (0, self.oriz_limit_graphic - 3), colspan = 3, rowspan = 3)

        plt.imshow(self.rec_matrix)

        self.figures.set_title('Rec image with Error = ' + str((np.around(self.errors_for_input[single_input], decimals=3, out=None) * 100)) + str("%"))

        plt.axis('off')


    def Graphical_hidden_rec(self,single_layer, single_inp,numbers_layers,RBM_obj_second = 0):

        shift = 0
        unit_correction = 0

        if single_layer == 2:

            shift = 4
            unit_correction = 1


        #Activation plot of hiddens

        self.figures = plt.subplot2grid((self.vertical_limit_graphic, self.oriz_limit_graphic), (4 + shift, 0), colspan = self.oriz_limit_graphic)

        Data_to_plot_Y = self.hidden_output[single_inp, :]

        if single_layer == 2:

            Data_to_plot_Y = copy.deepcopy(RBM_obj_second.real_activation_second_hidden[single_inp, :])


        indices_hiddens_data_to_plot = []

        for i in range(len(Data_to_plot_Y)):

            if Data_to_plot_Y[i] > 0.1:

                indices_hiddens_data_to_plot.append(i)

        indices_hiddens_data_to_plot.append(len(Data_to_plot_Y))


        plt.bar(range(len(Data_to_plot_Y)), Data_to_plot_Y)
        plt.xlim([0, len(Data_to_plot_Y)])
        plt.ylim(0, 1)
        plt.tick_params(axis='x',labelbottom='off')

        if single_layer == 1:

            self.figures = plt.title(" Hiddens activated ")

        if single_layer == 2:

            self.figures = plt.title(" Hiddens second layer activated ")


        if single_layer == 2:

            self.reconstructed_all_hidden = copy.deepcopy(self.receptive_fields_for_inp)


        #receptor fields of hiddens - plot

        pos_fig = 0

        for n in range(0, (len(self.reconstructed_all_hidden) - 1)):

            single_hidden_unit = self.reconstructed_all_hidden[n]

            pos_fig = n

            self.figures = plt.subplot2grid((self.vertical_limit_graphic, self.oriz_limit_graphic), (6 + shift, pos_fig))

            if n != (len(self.reconstructed_all_hidden) - 1):

                if single_layer == 1:

                    self.figures = plt.title("H. " + str(self.selected_max_hiddens_activation[n]))

                elif single_layer == 2:

                    self.figures = plt.title("H. " + str(indices_hiddens_data_to_plot[n]))


            plt.imshow(single_hidden_unit)

            plt.axis('off')

        # plot of bias

        self.figures = plt.subplot2grid((self.vertical_limit_graphic, self.oriz_limit_graphic), (6 + shift, pos_fig + 1))

        self.figures = plt.title("b. ")

        if single_layer == 1:

            plt.imshow(self.reconstructed_hidden_bias[0])

            plt.axis('off')

        if single_layer == 2:


            plt.imshow(self.reconstructed_all_hidden[-1])



        self.selected_max_hiddens_activation = []

        self.reconstructed_all_hidden = []

        # if numbers_layers == 1:
        #
        #     plt.show()



        if numbers_layers == 2:

            if single_layer == 2:

                plt.show()


def RBM_initialization_first(numbers_layers, Images_dimensions, Hidden_units, load_choice, MNIST = 0):

    # ASSIGNATION OF LAYERS
    first = 1  # FIRST LAYER
    second = 2  # SECOND LAYER
    RBM_obj_second = 0

    RBM_obj = RBM(1, (Hidden_units))  # init of first RBM
    RBM_obj.get_images(Images_dimensions, MNIST)  # loading inputs images
    RBM_obj.variables_changes_for_images(first) # function to make dynamical the RBM(depending on input the first RBM will have a topology)
    RBM_obj.initialization_weights(RBM_obj.input_units, (Hidden_units))  # initialization of weights_ first RBM
    if load_choice == 1:
        RBM_obj.load_weights(load_choice, first)

    return RBM_obj, RBM_obj_second

def RBM_initialization_second(load_choice_second, Hidden_units = 150, Hidden_units_second = 12):

    # ASSIGNATION OF LAYERS
    first = 1  # FIRST LAYER
    second = 2  # SECOND LAYER

    RBM_obj_second = RBM(2, (Hidden_units_second))  # init of second RBM
    RBM_obj_second.variables_changes_for_images(second, Hidden_units)#function to make dynamical the second RBM(depending on input the RBM will have a topology)
    RBM_obj_second.initialization_weights(Hidden_units,Hidden_units_second)  # initialization of weights_ second RBM
    if load_choice_second == 1:
        RBM_obj_second.load_weights(load_choice_second, second)

    return RBM_obj_second

def RBM_processing(fovea_img, numbers_layers, Graphic_on, proprierties, Batch_mode, RBM_obj, int_ext, RBM_obj_second = 0):

    # BATCH OR ONLINE MODE
    if Batch_mode == True:
        Batch_size_first = 64#9
        Total_inputs = 64#9
        batch_single = 1
    else:
        Batch_size_first = 1
        batch_single = 1
        Total_inputs = 1


    # ASSIGNATION OF LAYERS
    first = 1  # FIRST LAYER
    second = 2  # SECOND LAYER

    if (isinstance(fovea_img, int)) == False: # NOT USE THIS FUNCTION DURING TESTS
        RBM_obj.inputs_test_learn = RBM_obj.cortical_magnification(fovea_img)
    else:
        RBM_obj.test_RF = 1



    if numbers_layers == 1:


        RBM_obj.K = 0
        RBM_obj.get_input(first, batch_single, Batch_size_first)
        RBM_obj.get_output_first_layer(stochasticity = False)
        RBM_obj.input_reconstruction(0, 0)

        # GRAPHICAL REPRESENTATIONS

        RBM_obj.Graphical_reconstruction_inputs_hiddens_outputs(RBM_obj, Total_inputs, plot_choice,
                                                                       Hidden_units_second, hiddens_plotted,
                                                                       numbers_layers, int_ext, Graphic_on,
                                                                       RBM_obj_second)
    elif numbers_layers == 2:

        RBM_obj_second.K = 0

        Original_input = RBM_obj.get_input(first, batch_single, Batch_size_first)


        First_Hidden_Activations_hid = RBM_obj.get_output_first_layer(stochasticity = False)

        First_Hidden_Activations_vis = RBM_obj_second.get_input(second, batch_single, Batch_size_first, RBM_obj.hidden_output)

        Second_Hidden_Activations = RBM_obj_second.get_output_first_layer(stochasticity = False)

        Selected_proprierty, Second_Hidden_Activations_After_Selection, RBM_obj_second = Top_down_Manipulator(proprierties, RBM_obj_second)


        Rec_First_Hidden, Rec_Err_First_Hidden = RBM_obj_second.input_reconstruction(0, 0)

        RBM_obj.hidden_output = RBM_obj_second.input

        Rec_Original, Rec_Err_Original = RBM_obj.input_reconstruction(0, 0)

        # GRAPHICAL REPRESENTATIONS

        RBM_obj_second.Graphical_reconstruction_inputs_hiddens_outputs(RBM_obj, Total_inputs,
                                                                       plot_choice, Hidden_units_second,
                                                                       hiddens_plotted,
                                                                       numbers_layers, int_ext, Graphic_on,
                                                                       RBM_obj_second)


    return RBM_obj.original, RBM_obj.rec_matrix


Graphic_on = True

Images_dimensions = 1

int_ext = 1

numbers_layers = 2

load_choice = 1

Hidden_units = 150

Hidden_units_second = 12

plot_choice = 1

hiddens_plotted = 10

load_choice_second = 1

Hidden_units_second_plotted = 13

Batch_mode = False

proprierties = 0

fovea_img = 0




### MOTOR SYSTEMS AND SIMILAR ################################

#FOVEA SACCADES
def foveate_deck_tablet(fovea, image, deck):

    foveate(fovea, image)
    fovea.move(deck.center - fovea.center)

def foveate(fovea, image):
    """
    Foveate fovea.

    Keyword arguments:
    - fovea -- Fovea object
    - image -- Numpy array of the image the fovea is scanning

    Uses bottom-up attention (the {RGB --> Black/White --> Add noise
    --> (smooth) --> foveate} procedure). That is, RGB image is turned
    into an intensity image, then the fovea is moved to the coordinates
    of the most salient pixel in the image.
    """
    intensity_image = get_intensity_image(image)
    max_index = np.unravel_index(intensity_image.argmax(),
                                 intensity_image.shape
                                 )
    max_pos = np.flipud(np.array(max_index))/image.shape[0]
    fovea.move(max_pos - fovea.center)

#OBJECTS MOVEMENTS

def move_object(object_, vector, limits):

    startpoint = object_.center
    endpoint = object_.center + vector
    object_.move(vector)

def parameterised_skill(object_, end_position, limits):


    start_position = np.copy(object_.center)
    vector = end_position - start_position
    move_object(object_, vector, limits)


### OTHER FUNCTIONS (INCLUDED OLD FUNCTIONS FOR PERCEPTION) ################################


def get_intensity_image(image):
    """
    Translate RGB image to intensity image.

    Keyword arguments:
    - image -- numpy array of RGB image

    Takes the RGB image array, transforms it to black/white image,
    adds Gaussian noise, adds noise and returns this new image.
    """
    bw_image = np.mean(image, -1)
    blurred = ndimage.gaussian_filter(bw_image, sigma=1)
    noisy = blurred + (0.1*np.random.random_sample(blurred.shape) - 0.05)
    clipped = noisy.clip(0, 1)
    return clipped


def check_target_position(environment, target_xy, external_fovea):
    """Return focus image at target positon

    Keyword arguments:
    - environment -- image array of environment
    - target_xy -- array of target position coordinates
    - fovea -- fovea object

    The function creates and returns a temporary focus image using the
    attributes of the real focus image and the target position.
    """
    temp_fovea = Fovea(target_xy, external_fovea.size, [0, 0, 0], external_fovea.unit)
    temp_image = temp_fovea.get_focus_image(environment)
    return temp_image


def check_free_space(environment, target_xy, fovea):
    """Check if target area is free

    Keyword arguments:
    - env_image -- image array of the environment
    - target_xy -- the xy coordinates of the target position
    - fovea -- fovea object

    Check if the focus area around the target position enx_xy is free
    space. The method creates a temporary fovea image at the target
    position and checks if it contains only zeros.

    Returns True/False.
    """
    temp_image = check_target_position(environment, target_xy, fovea)
    if np.array_equal(temp_image, np.zeros(temp_image.shape)):
        return True
    else:
        return False

