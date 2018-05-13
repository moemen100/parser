class ParsingTable(object):
    def __init__(self, first_rules, follow_rules, rules):
        self.symbol_stack = ['}', ";", 'num', 'assign', 'id', '{', ')', 'num', 'relop', 'id', '(', 'if', ';', 'num',
                             'assign', 'id', ';', 'id', 'int']
        #self.symbol_stack = ['b', 'a', 'a']
        #self.symbol_stack = [')', 'id', '*', '(', '+', 'id', '(']
        #self.symbol_stack = ['*', 'id', '(', '+', ')', 'id', '+', '*']
        self.parsing_stack = []
        self.expressions = []
        self.parsing_table = {}
        self.create_parse_table(first_rules, follow_rules, rules)
        self.parsing_stack.append("'$'")
        self.parsing_stack.append([*rules.keys()][0])
        self.parse(first_rules)

    def create_parse_table(self, first_rules, follow_rules, rules):

        ep = False
        for non_terminal in rules:

            if "'\\L'" in first_rules[non_terminal]:
                for follow_terminal in follow_rules[non_terminal]:
                    self.parsing_table[(non_terminal, follow_terminal)] = "'\\L'"

            for rule in rules[non_terminal]:
                rules_splits = rule.split(' ')
                for t_or_nt in rules_splits:

                    if t_or_nt == "'\\L'":
                        continue

                    if t_or_nt[0] == "'":

                        if (non_terminal, t_or_nt) in self.parsing_table and not (rule ==
                                                                                  self.parsing_table[
                                                                                      (non_terminal, t_or_nt)]):
                            print("grammar is ambiguous ")
                            exit()
                        self.parsing_table[(non_terminal, t_or_nt)] = rule
                        break

                    for terminal in first_rules[t_or_nt]:
                        if terminal == "'\\L'":
                            ep = True
                        else:
                            if (non_terminal, terminal) in self.parsing_table and not (rule ==
                                                                                       self.parsing_table[
                                                                                           (non_terminal, terminal)]):
                                print("grammar is ambiguous ")
                                exit()
                            self.parsing_table[(non_terminal, terminal)] = rule
                    if ep:
                        ep = False
                    else:
                        break

        for non_terminal in first_rules:
            self.expressions.extend([x for x in first_rules[non_terminal]
                                     if x not in self.expressions and not (x == "'\\L'")])
            self.expressions.extend([x for x in follow_rules[non_terminal] if x not in self.expressions])

        for non_terminal in first_rules:
            for expression in self.expressions:
                if (non_terminal, expression) not in self.parsing_table:
                    if expression not in follow_rules[non_terminal]:
                        self.parsing_table[(non_terminal, expression)] = "error"
                    else:
                        self.parsing_table[(non_terminal, expression)] = "sync"

    def parse(self, first_rules):
        print("-------------------------------- parsing output --------------------------------------------------")
        f = open("output.txt", 'w')
        i = 0
        get_symbol = True
        next_symbol = ""
        while i in range(1000):
            i += 1
            rule = None

            next_parsing_exp = self.parsing_stack.pop()

            if len(self.symbol_stack) == 0:
                self.symbol_stack.append("$")

            if next_parsing_exp == "'$'" and next_parsing_exp == "'" + next_symbol + "'":
                print("accept")
                print("accept", file=f)
                break

            if next_parsing_exp == "'$'":
                print("error in " + next_symbol + " $ " + "with no rules")
                print("error in " + next_symbol + " $ " + "with no rules",  file=f)
                break

            if get_symbol:
                next_symbol = self.symbol_stack.pop()

            get_symbol = True

            if "'" + next_symbol + "'" == next_parsing_exp:
                continue

            if next_parsing_exp[0] == "'" and not (next_parsing_exp == next_symbol):
                print("Error missing " + next_parsing_exp + " inserted")
                print("Error missing " + next_parsing_exp + " inserted", file=f)
                get_symbol = False
                continue

            elif not (next_parsing_exp[0] == "'"):

                if (next_parsing_exp, "'" + next_symbol + "'") in self.parsing_table:
                    rule = self.parsing_table[(next_parsing_exp, "'" + next_symbol + "'")]
                else:
                    rule = "error"

                if rule == "error":
                    if next_symbol == "$":
                        break
                    print("Error:(illegal " + next_parsing_exp + ") – discard " + next_symbol)
                    print("Error:(illegal " + next_parsing_exp + ") – discard " + next_symbol, file=f)

                    get_symbol = True
                    self.parsing_stack.append(next_parsing_exp)
                    continue

                elif not rule == "sync":
                    print(next_parsing_exp + " => ", end="")
                    print(next_parsing_exp + " => ", end="", file=f)

                    if " " in rule:
                        splits = rule.split(" ")

                        for split in splits:
                            print(split + " ", end="")
                            print(split + " ", end="", file=f)

                        for split in reversed(splits):
                            if not split == "'\\L'":
                                self.parsing_stack.append(split)
                    else:
                        print(rule + " ", end="")
                        print(rule + " ", end="",file=f)
                        if not rule == "'\\L'":
                            self.parsing_stack.append(rule)
                    print()
                    print(file=f)
                    get_symbol = False
                elif rule == "sync":
                    if next_parsing_exp in first_rules:
                        print("sync found expecting first of " + next_parsing_exp)
                        print("sync found expecting first of " + next_parsing_exp,file=f)
                        print(first_rules[next_parsing_exp])
                        print(first_rules[next_parsing_exp],file=f)
                        get_symbol = False
