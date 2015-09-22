#!/usr/bin/env python

__author__ = 'koo'


class Automata:
    def __init__(self, name):
        self.name = name
        self.states = {}
        self.final_states = {}
        self.voca = []
        self.init_state = None

    def __str__(self):
        return self.name

    def set_voca(self, voca):
        assert isinstance(voca, list)
        self.voca = voca

    def set_state(self, state_name):
        state = self.State(state_name)
        self.states[state_name] = state

    def set_final_states(self, state):
        self.final_states[state.get_name()] = state

    def set_init_state(self, state):
        self.init_state = state

    def get_init_state(self):
        return self.init_state

    def get_state(self, state_name):
        #assert state_name in self.states.keys()
        if state_name in self.states.keys():
            return self.states[state_name]
        else:
            False

    def get_states(self):
        return self.states.values()

    def get_voca(self):
        return self.voca

    def show_states(self):
        for state in self.states.values():
            print(state.get_name())

    def show_voca(self):
        print(self.voca)


    # check if input string is acceptable.
    def is_acceptable(self, input_string):
        cur_state = self.init_state

        for symbol in input_string:
            cur_state = cur_state.trans(symbol)

        if cur_state.get_name() in self.final_states:
            return True
        else:
            return False



    class State:
        def __init__(self, name):
            self.name = name
            self.trans_func = []

        def get_name(self):
            return self.name

        def set_trans_func(self, input, next):
            # add check input and next have proper type.
            self.trans_func.append([input, next])

        def trans(self, input):
            for func in self.trans_func:
                if func[0] == input:
                    return func[1]
            return None




def make_dfa():

    print("Make a new DFA.")
    dfa_name = raw_input("DFA name? ")

    automata = Automata(dfa_name)

    voca = raw_input("voca? (seperated by space) ")
    voca = voca.split()

    automata.set_voca(voca)

    state_num = input("How many states? ")

    for i in range(state_num):
        automata.set_state("q%d" % i)

    states = automata.get_states()
    voca = automata.get_voca()

    print("setting state transition function...")

    for state in states:
        for input_symbol in voca:
            success = False
            while not success:
                next = raw_input("delta(%s, %s) -> " % (state.get_name(), input_symbol))
                success = state.set_trans_func(input_symbol, automata.get_state(next))
                if not success:
                    print("State doesn't exist. Please try again.")


    init_state = raw_input("initial state? ")
    final_state = raw_input("final state? ")

    automata.set_init_state(automata.get_state(init_state))
    automata.set_final_states(automata.get_state(final_state))

    automata.show_states()
    automata.show_voca()

    input_string = raw_input("input string? ")


    if automata.is_acceptable(input_string):
        print("string accepted.")
    else:
        print("string not accepted.")




make_dfa()