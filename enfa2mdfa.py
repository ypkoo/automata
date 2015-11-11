from __future__ import print_function
from eNFA import *
from automata import *


__author__ = 'koo'


class Converter:
    def states_to_names(self, states):
        names = []
        for state in states:
            names.append(state.get_name())
        return " ".join(names)

    def names_to_states(self, enfa, names):
        states = []
        state_names = names.split()

        for state_name in state_names:
            states.append(enfa.get_state(state_name))
        return states

    def construct_table1(self, enfa):
        table = {}

        for state in enfa.get_all_states():
            table[state.get_name()] = {}
            for symbol in enfa.get_voca():
                if symbol == "epsilon":
                    table[state.get_name()][symbol] = self.states_to_names(state.get_e_closure())
                else:
                    table[state.get_name()][symbol] = self.states_to_names(state.trans(symbol))

        return table

    def construct_table2(self, enfa, table1):
        table2 = {}

        init_states = enfa.get_init_state().get_e_closure()
        state_set = set([self.states_to_names(init_states)])
        state_set_ = set([])

        while state_set != state_set_:
            for state_names in state_set - state_set_:
                table2[state_names] = {}
                for symbol in enfa.get_voca():
                    if symbol != "epsilon":
                        result1 = ""
                        result2 = ""
                        names = state_names.split()
                        for name in names:
                            if table1[name][symbol] != "dead_state":
                                result1 = result1 + " " + table1[name][symbol]
                        if result1 == "":
                            result1 = "dead_state"
                        else:
                            result1 = result1[1:]
                        for s in list(set(result1.split())):
                            result2 = result2 + " " + table1[s]["epsilon"]
                        result2 = result2[1:]
                        result2 = " ".join(list(set(result2.split())))
                        table2[state_names][symbol] = result2
                        if result2 != []:
                            state_set.add(result2)
                        state_set_.add(state_names)

        return table2, self.states_to_names(init_states)

    def convert(self, enfa):
        table1 = self.construct_table1(enfa)
        table2, init_state_name = self.construct_table2(enfa, table1)

        automata = Automata("dfa")

        for key in table2.keys():
            automata.add_state(key)
        #automata.add_state("dead_state")

        automata.set_voca(enfa.get_voca_without_e())

        dead_state = automata.get_state("dead_state")
        for state in automata.get_all_states():
            if not state is dead_state:
                for symbol in automata.get_voca():
                    next = table2[state.get_name()][symbol]
                    next_state = automata.get_state(next)
                    state.set_trans_func(symbol, next_state)
            else:
                for symbol in automata.get_voca():
                    state.set_trans_func(symbol, dead_state)

        automata.set_init_state(automata.get_state(init_state_name))

        final_state_names = []
        for state in enfa.get_final_states():
            final_state_names.append(state.get_name())
        final_state_names = set(final_state_names)

        for state in automata.get_all_states():
            state_names = set(state.get_name().split())
            if state_names & final_state_names:
                automata.add_final_state(state)

        return automata

class Minimizer:
    def minimize(self, dfa):
        pass


if __name__ == "__main__":
    enfa = make_sample2()
    con = Converter()
    dfa = con.convert(enfa)
    dfa.info()
    accept_test(dfa)