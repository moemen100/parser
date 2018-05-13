import copy
import collections

def update(rules, trans, length_begin):
    for lhs in trans.keys():
        for rhs in trans[lhs]:
            copy_rules = copy.deepcopy(rules)
            if lhs in copy_rules and rhs in copy_rules:
                rules[lhs].extend([x for x in copy_rules[rhs] if not (x == "'None'") and x not in copy_rules[lhs]])
            elif rhs in copy_rules:
                rules[lhs] = [x for x in copy_rules[rhs] if not (x == "'None'")]

    length = rules.values().__len__()
    if length == length_begin:
        return True
    update(rules, trans, length)


def write(table, label):
    f = open(label + ".txt", 'w')
    print("{:<25} {:<10}".format('Key', label), file=f)

    for k, v in table.items():
        value_array = v
        print("{:<25}".format(k), end="",  file=f)
        for value in value_array:
            print("{:<10}".format(value), end="",  file=f)
        print( file=f)

    print("-----------------------------" + label + "-----------------------------------------------------")
    print("{:<25} {:<15}".format('Key', label))

    for k, v in table.items():
        value_array = v
        print("{:<25}".format(k), end="")
        for value in value_array:
            print("{:<10}".format(value), end="")
        print()
    print("--------------------------------------------------------------------------------------------")


def write_parsing_table(table, labels):
    f = open("paring table.txt", 'w')
    od = collections.OrderedDict(sorted(table.items()))
    labels = sorted(labels)
    print("{:<55}".format("key"), end="", file=f)

    for label in labels:
        print("{:<55}".format(label), end="", file=f)

    last = ""
    for (a, b) in od:
        value = od[(a, b)]
        if last == a:
            print("{:<55}".format(value), end="", file=f)
        else:
            print(file=f)
            print(file=f)
            print("{:<55}".format(a), end="", file=f)
            print("{:<55}".format(value), end="", file=f)
        last = a
    print(file=f)
    print("---------------------- another form for parsing table --------------------------------------")
    for (a, b) in od:
        value_array = od[(a, b)]
        print("{:<25}".format(a), end="")
        print("{:<25}".format(b), end="")
        print("{:<10}".format(value_array), end="")
        print()
    print("--------------------------------------------------------------------------------------------")
