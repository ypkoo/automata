# -*- coding:utf-8 -*-
#!/usr/bin/env python

from __future__ import print_function
import os
import xml.etree.ElementTree as ET
from automata import Automata

__author__ = 'koo'


# Mealy machine class
class Mealy(Automata):

    def __init__(self, name):
        self.name = name
        self.states = {}
        self.voca = []
        self.init_state = None
        self.final_states = []
        self.outputs = []

    def set_outputs(self, outputs):
        self.outputs = outputs

    def get_outputs(self):
        return self.outputs

    def show_outputs(self):
        print(self.outputs)

    def print_output(self, input_string):
        cur_state = self.init_state
        output = ""

        for symbol in input_string:
            output = output + cur_state.output(symbol)
            cur_state = cur_state.trans(symbol)

        print(output)

    class State(Automata.State):
        def __init__(self, name):
            self.name = name
            self.trans_func = {}
            self.output_func = {}

        def set_output_func(self, input, output):
            self.output_func[input] = output

        def output(self, input):
            return self.output_func[input]

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
def save_mealy(mealy):
    dir = "configs/"
    filename = dir + mealy.get_name() + ".xml"

    if not os.path.exists(dir):
        os.makedirs(dir)

    root = ET.Element("mealy")

    # automata name
    mealy_name = ET.SubElement(root, "name")
    mealy_name.text = mealy.get_name()

    # vocabulary
    voca = ET.SubElement(root, "voca")
    for symbol in mealy.get_voca():
        ET.SubElement(voca, "symbol").text = symbol

    # output
    #### to be implemented ###

    # initial state
    init_state = ET.SubElement(root, "init_state")
    init_state.text = mealy.get_init_state().get_name()

    # final states
    final_states = ET.SubElement(root, "final_states")
    for state in mealy.get_final_states():
        ET.SubElement(final_states, "state").text = state.get_name()

    # states
    states = ET.SubElement(root, "states")
    for state in mealy.get_all_states():
        s = ET.SubElement(states, "state")
        ET.SubElement(s, "name").text = state.get_name()

        trans_func = ET.SubElement(s, "trans_func")

        tf = state.get_trans_func()
        for input in tf:
            func = ET.SubElement(trans_func, "func")
            ET.SubElement(func, "input").text = input
            ET.SubElement(func, "next").text = tf[input].get_name()

    indent(root)

    ET.ElementTree(root).write(filename)

# load automata from xml file
def load_mealy(file):
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

# make and save a new automata
def make_mealy():
    print("Make a new mealy machine.\n")
    mealy_name = raw_input("Mealy machine name? ")

    mealy = Mealy(mealy_name)

    voca = raw_input("Vocabulary? (seperated by space) ")
    voca = list(set(voca.split()))

    mealy.set_voca(voca)

    print("Vocabulary (duplicates are removed.)")
    mealy.show_voca()

    outputs = raw_input("Outputs? (seperated by space) ")
    output = list(set(outputs.split()))

    mealy.set_outputs(outputs)
    print("Outputs (duplicates are removed.)")
    mealy.show_outputs()

    state_num = int(raw_input("How many states? "))

    for i in range(state_num):
        mealy.add_state("q%d" % i)

    dead_state = mealy.add_state("dead_state")

    print("%d states are created. (including dead state)" % (state_num+1))
    mealy.show_all_states()
    print()

    states = mealy.get_all_states()
    voca = mealy.get_voca()

    print("setting state transition function...")
    print("If you don't want to specify transition, enter 'None' (for allowing partial function)\n")

    for state in states:
        if not state is dead_state:
            for input_symbol in voca:
                success = False
                while not success:
                    next = raw_input("delta(%s, %s) -> " % (state.get_name(), input_symbol))
                    if next == "None": # daed state
                        next_state = mealy.get_state("dead_state")
                    else:
                        next_state = mealy.get_state(next)

                    if next_state:
                        state.set_trans_func(input_symbol, next_state)
                        success = True
                    else:
                        print("State doesn't exist. Please try again.")
        else:
            for input_symbol in voca:
                dead_state.set_trans_func(input_symbol, dead_state)

    print("setting state transition function...")
    print("Available outputs:", end=' ')
    mealy.show_outputs()

    for state in states:
        if not state is dead_state:
            for input_symbol in voca:
                output = raw_input("lambda(%s, %s) -> " % (state.get_name(), input_symbol))
                state.set_output_func(input_symbol, output)

    init_state = raw_input("initial state? ")
    final_states = raw_input("final states? (seperated by space) ")
    final_states = final_states.split()

    mealy.set_init_state(mealy.get_state(init_state))
    for state in final_states:
        mealy.add_final_state(mealy.get_state(state))

    """
    success = False
    while not success:
        save = raw_input("Do you want to save current mealy machine? (y/n)")
        if save == "y" or save == "Y" or save == "n" or save == "N":
            success = True
        else:
            print("wrong input.")

    if save == "y" or save == "Y":
        save_mealy(mealy)
        print("Current mealy machine is saved as configs/%s.xml" % mealy.get_name())
    """

    return mealy

def accept_test(automata):
    print("Acceptance test of automata %s" % automata.get_name())
    while True:
        input_string = raw_input("input string? ")

        if automata.is_acceptable(input_string):
            print("string accepted.")
        else:
            print("string not accepted.")

def mealy_test(mealy):
    print("Mealy machine test of %s" % mealy.get_name())
    while True:
        input_string = raw_input("input string? ")

        if mealy.is_acceptable(input_string):
            print("output:", end=' ')
            mealy.print_output(input_string)
        else:
            print("String not accepted. Please try again.")


if __name__ == "__main__":
    print ("""
2015 Fall CS322 project. Developed by YP Koo.

Welcome to Automata world!
""")

    """
    success = False

    if os.path.exists("configs/"):
        while not success:
            input = raw_input("Do you want to load existing Automata? (y/n) ")
            if input == "y" or input == "Y" or input == "n" or input == "N":
                success = True
            else:
                print("wrong input.")
    else:
        input = "n"

    if input == "y" or input == "Y":
        files = os.listdir("configs")
        for f in files:
            print(f)
        file = raw_input("Select one (without expansion) ")
        automata = load_automata(file)
    else:
        automata = make_automata()
    """

    mealy = make_mealy()
    mealy_test(mealy)
