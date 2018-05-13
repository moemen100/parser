import helper


class Follow(object):

    def __init__(self, rules, first_rules):
        self.follow_rules = {}
        self.follow_trans = {}
        self.follow(rules, first_rules)
        helper.update(self.follow_rules, self.follow_trans, -1)

    def follow(self, rules_by_non_terminal, first_rules):
        start = True
        for non_terminal in rules_by_non_terminal:
            if start:
                self.follow_rules[non_terminal] = ["'$'"]
                start = False
            for non_terminalB in rules_by_non_terminal:
                temp = []
                for rhs_part in rules_by_non_terminal[non_terminal]:
                    try:

                        splits = rhs_part.split(' ')
                        temp_index = splits.index(non_terminalB)

                        if (temp_index + 1) == len(splits):
                            if non_terminalB in self.follow_trans:
                                if non_terminal not in self.follow_trans[non_terminalB]:
                                    self.follow_trans[non_terminalB].append(non_terminal)
                            else:
                                self.follow_trans[non_terminalB] = [non_terminal]
                            continue

                        for first_of in splits[temp_index + 1:]:

                            if not first_of[0] == "'":
                                temp.extend([x for x in first_rules[first_of] if not (x == "'\\L'") and x not in temp])
                                if "'\\L'" not in first_rules[first_of]:
                                    break

                                if splits.index(first_of) == len(splits) - 1:
                                    if non_terminalB in self.follow_trans:
                                        if non_terminal not in self.follow_trans[non_terminalB]:
                                            self.follow_trans[non_terminalB].append(non_terminal)
                                    else:
                                        self.follow_trans[non_terminalB] = [non_terminal]
                                    break

                            elif not first_of == "'\\L'":
                                if first_of not in temp:
                                    temp.append(first_of)
                                break
                    except ValueError:
                        continue

                if len(temp) > 0:
                    if non_terminalB in self.follow_rules:
                        self.follow_rules[non_terminalB].extend(
                            [x for x in temp if x not in self.follow_rules[non_terminalB]])
                    else:
                        self.follow_rules[non_terminalB] = temp

                del temp
        return self.follow_rules, self.follow_trans
