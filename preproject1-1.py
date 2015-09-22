#!/usr/bin/env python

from __future__ import print_function

__author__ = 'koo'

class Automata:
    def __init__(self, name):
        self.name = name
        self.states = {}
        self.voca = []
        self.init_state = None
        self.final_states = {}
        
    def __str__(self):
        return self.name

    def set_voca(self, voca):
        assert isinstance(voca, list)
        self.voca = voca

    def add_state(self, state_name):
        state = self.State(state_name)
        self.states[state_name] = state

    def add_final_state(self, state):
        self.final_states[state.get_name()] = state

    def set_init_state(self, state):
        self.init_state = state

    def get_init_state(self):
        return self.init_state

    # get State object by state name
    def get_state(self, state_name):
        if state_name in self.states.keys():
            return self.states[state_name]
        else:
            False

    def get_all_states(self):
        return self.states.values()

    def get_voca(self):
        return self.voca

    def show_all_states(self):
        for state in sorted(self.states.values()):
            print(state.get_name(), end=' ')
        print("")

    def show_voca(self):
        print(self.voca)

    def show_init_state(self):
        print(self.init_state)

    def show_final_states(self):
        for state in self.final_states.values():
            print(state.get_name())


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
        automata.add_state("q%d" % i)

    states = automata.get_all_states()
    voca = automata.get_voca()

    print("setting state transition function...")

    for state in sorted(states):
        for input_symbol in voca:
            next = False
            while not next:
                next = raw_input("delta(%s, %s) -> " % (state.get_name(), input_symbol))
                next = automata.get_state(next)
                if next:
                    success = state.set_trans_func(input_symbol, next)
                else:
                    print("State doesn't exist. Please try again.")


    init_state = raw_input("initial state? ")
    final_states = raw_input("final states? (seperated by space) ")
    final_states = final_states.split()

    automata.set_init_state(automata.get_state(init_state))
    for state in final_states:
        automata.add_final_state(automata.get_state(state))

    automata.show_all_states()
    automata.show_voca()

    while True:

        input_string = raw_input("input string? ")


        if automata.is_acceptable(input_string):
            print("string accepted.")
        else:
            print("string not accepted.")




make_dfa()