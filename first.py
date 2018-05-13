import re
import copy
import helper as helper


class First(object):

    def __init__(self, rules):
        self.rules_by_non_terminal = {}
        self.first_rules = {}
        self.trans = {}

        self.rules_by_non_terminal = rules
        self.get_firsts()

        # update(first_rules, trans)
        self.first_accept_epsilon()
        helper.update(self.first_rules, self.trans, -1)

    def get_firsts(self):
        for non_terminal in self.rules_by_non_terminal:
            for terminals in self.rules_by_non_terminal[non_terminal]:

                if terminals[0] == '\'':
                    result = re.search("'(.*)'", terminals)

                    if result:
                        first_terminal_exp = result.group(0).split(' ')[0]

                        try:
                            self.first_rules[non_terminal].append(first_terminal_exp)
                        except KeyError:
                            self.first_rules[non_terminal] = [first_terminal_exp]

                else:
                    first_non_terminal_exp = terminals.split(' ')[0]

                    try:
                        self.trans[non_terminal].append(first_non_terminal_exp)
                    except KeyError:
                        self.trans[non_terminal] = [first_non_terminal_exp]

    def first_accept_epsilon(self):
        copy_trans = copy.deepcopy(self.trans)
        # copy_first_rules = copy.deepcopy(first_rules)

        for non_terminal in reversed([*copy_trans.keys()]):
            for non_terminalB in copy_trans[non_terminal]:
                if (non_terminalB in self.first_rules and "'\\L'" not in self.first_rules[non_terminalB]) \
                        or non_terminalB not in self.first_rules:
                    continue
                else:
                    for exp in self.rules_by_non_terminal[non_terminal]:
                        try:
                            splits = exp.split(' ')
                            temp_index = splits.index(non_terminalB)

                            if (temp_index + 1) == len(splits) and "'\\L'" in self.first_rules[non_terminalB]:
                                if non_terminal in self.first_rules:
                                    if "'\\L'" not in self.first_rules[non_terminal]:
                                        self.first_rules[non_terminal].append("'\\L'")
                                else:
                                    self.first_rules[non_terminal] = ["'\\L'"]

                            for first_of in splits[temp_index + 1:]:

                                if not first_of[0] == "'":

                                    if first_of not in self.trans[non_terminal]:
                                        self.trans[non_terminal].append(first_of)

                                    if splits.index(first_of) == len(splits) - 1 and \
                                            "'\\L'" in self.first_rules[first_of]:
                                        if non_terminal in self.first_rules:
                                            if "'\\L'" not in self.first_rules[non_terminal]:
                                                self.first_rules[non_terminal].append("'\\L'")
                                        else:
                                            self.first_rules[non_terminal] = ["'\\L'"]

                                    if first_of in self.first_rules and "'\\L'" not in self.first_rules[first_of]:
                                        break

                                elif not first_of == "'\\L'":
                                    if non_terminal in self.first_rules:
                                        if first_of not in self.first_rules[non_terminal]:
                                            self.first_rules[non_terminal].append(first_of)
                                    else:
                                        self.first_rules[non_terminal] = [first_of]
                                    break

                        except ValueError:
                            continue
