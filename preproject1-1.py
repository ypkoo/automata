#!/usr/bin/env python

from __future__ import print_function
import os
import xml.etree.ElementTree as ET

__author__ = 'koo'

class Automata:
    def __init__(self, name):
        self.name = name
        self.states = {}
        self.voca = []
        self.init_state = None
        self.final_states = []
        
    def get_name(self):
        return self.name

    def set_voca(self, voca):
        assert isinstance(voca, list)
        self.voca = voca

    def add_state(self, state_name):
        state = self.State(state_name)
        self.states[state_name] = state
        return state

    def add_final_state(self, state):
        self.final_states.append(state)

    def set_init_state(self, state):
        self.init_state = state

    def get_init_state(self):
        return self.init_state

    def get_final_states(self):
        return self.final_states

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
        for state in self.final_states:
            print(state.get_name(), end=' ')
        print("")


    # check if input string is acceptable.
    def is_acceptable(self, input_string):
        cur_state = self.init_state

        for symbol in input_string:
            cur_state = cur_state.trans(symbol)

        if cur_state in self.final_states:
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

        def get_trans_func(self):
            return self.trans_func

        def trans(self, input):
            for func in self.trans_func:
                if func[0] == input:
                    return func[1]
            return None

# indent function for formatting xml. (from https://wikidocs.net/42)
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

# save current automata to use later
def save_automata(automata):
    dir = "configs/"
    filename = dir + automata.get_name() + ".xml"

    if not os.path.exists(dir):
        os.makedirs(dir)

    root = ET.Element("automata")

    # automata name
    automata_name = ET.SubElement(root, "name")
    automata_name.text = automata.get_name()

    # vocabulary
    voca = ET.SubElement(root, "voca")
    for symbol in automata.get_voca():
        ET.SubElement(voca, "symbol").text = symbol

    # initial state
    init_state = ET.SubElement(root, "init_state")
    init_state.text = automata.get_init_state().get_name()

    # final states
    final_states = ET.SubElement(root, "final_states")
    for state in automata.get_final_states():
        ET.SubElement(final_states, "state").text = state.get_name()

    # states
    states = ET.SubElement(root, "states")
    for state in automata.get_all_states():
        s = ET.SubElement(states, "state")
        ET.SubElement(s, "name").text = state.get_name()

        trans_func = ET.SubElement(s, "trans_func")

        tf = state.get_trans_func()
        for pair in tf:
            func = ET.SubElement(trans_func, "func")
            ET.SubElement(func, "input").text = pair[0]
            ET.SubElement(func, "next").text = pair[1].get_name()

    indent(root)
    ET.dump(root)

    ET.ElementTree(root).write(filename)

# load automata from xml file
def load_automata(file):
    dir = "configs/"

    tree = ET.parse(dir + file + ".xml")
    root = tree.getroot()

    automata = Automata(root.find("name").text)

    voca = root.find("voca")
    voca_list = []
    for symbol in voca.getchildren():
        voca_list.append(symbol.text)
    automata.set_voca(voca_list)

    states = root.find("states")
    for state in states.iter("state"):
        automata.add_state(state.find("name").text)

    for state in states.iter("state"):
        s = automata.get_state(state.find("name").text)
        trans_func = state.find("trans_func")
        for func in trans_func.iter("func"):
            input = func.find("input").text
            next = func.find("next").text
            next = automata.get_state(next)
            s.set_trans_func(input, next)

    init_state = root.find("init_state").text
    automata.set_init_state(automata.get_state(init_state))

    final_states = root.find("final_states")
    for state in final_states.iter("state"):
        final_state = state.text
        automata.add_final_state(automata.get_state(final_state))


    return automata




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

    save_automata(automata)

    automata_temp = load_automata("hw1")
    print(automata_temp.get_name())

    while True:

        input_string = raw_input("input string? ")


        if automata_temp.is_acceptable(input_string):
            print("string accepted.")
        else:
            print("string not accepted.")


#make_dfa()

automata_temp = load_automata("hw1")
print(automata_temp.get_name())
print(automata_temp.get_init_state().get_name())

automata_temp.show_voca()
automata_temp.show_all_states()
automata_temp.show_final_states()
automata_temp.show_init_state()

while True:

    input_string = raw_input("input string? ")


    if automata_temp.is_acceptable(input_string):
        print("string accepted.")
    else:
        print("string not accepted.")