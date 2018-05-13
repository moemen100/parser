import re


class readParse():
    def __init__(self,file):
        self.nonterminals = []
        self.terminals = []
        self.terminals.append("'\\L'")
        self.grammer = {}
        self.f = open(file,'r')
        self.read()
        self.removeLeftRecursion()
        self.removeLeftFactoring()
        self.write()

    def read(self):
        data = self.f.readlines()
        splitted = None
        for line in data:
            line = line.replace("\n","")
            if line[0] == '#':
                line = line[1:]
                splitted = line.split("=")

                splitted[0] = splitted[0].strip()
                self.nonterminals.append(splitted[0])
                self.grammer[splitted[0]] = []

                afterequal = splitted[1].split("|")
                for grammer in afterequal:

                    grammer = " ".join(grammer.split())

                    self.grammer[splitted[0]].append(grammer)
                    grammer = grammer.split(" ")
                    for t in grammer:
                        if t[0] == '\'':
                            self.terminals.append(t)
                        else:
                            self.nonterminals.append(t)
            elif line[0] == "|":
                line = line[1:]
                self.grammer[splitted[0]].append(line.strip())

        self.terminals = list(set(self.terminals))
        self.nonterminals = list(set(self.nonterminals))

    def removeLeftRecursion(self):
        leftrecursion = []
        afterEditing = {}
        for key in self.grammer.keys():
            for rule in self.grammer[key]:
                if re.search(r'(^|\s)' + key + r'\s',rule):
                    if key not in leftrecursion:
                        leftrecursion.append(key)

        for key in leftrecursion:
            self.grammer[key + "`"] = []
            afterEditing[key] = []
            self.nonterminals.append(key + "`")
            for rule in self.grammer[key]:
                if re.search(r'(^|\s)' + key + r'\s',rule):
                    rule = rule.replace(key,"")
                    rule = rule + " " + key + "`"

                    rule = " ".join(rule.split())
                    self.grammer[key + "`"].append(rule.strip())
                    self.grammer[key + "`"].append("'\\L'")
                else:
                    afterEditing[key].append(rule + " " + key + "`")

        for key in afterEditing:
            self.grammer[key] = afterEditing[key]

    def removeLeftFactoring(self):
        leftfactoring = {}
        for key in self.grammer.keys():
            for rule in self.grammer[key]:
                objs = rule.split(" ")
                for obj in objs:
                    for rule2 in self.grammer[key]:
                        if rule != rule2:
                            if obj not in self.terminals:
                                if re.search(r'\b' + obj + r'\b',rule2):
                                    leftfactoring[key] = obj

        for key in leftfactoring.keys():
            if key + "`" not in self.grammer.keys():
                self.grammer[key + "`"] = []
                for rule in self.grammer[key]:
                    dup = False
                    entities = rule.split(" ")
                    newRule = ""
                    for entity in entities:
                        if entity != leftfactoring[key] or dup:
                            newRule = newRule + entity + " "
                        else:
                            dup = True
                    if newRule == "":
                        self.grammer[key + "`"].append("'\\L'")
                    else:
                        newRule = " ".join(newRule.split())
                        self.grammer[key + "`"].append(newRule)
                self.grammer[key] = [leftfactoring[key] + " " + key + "`"]

    def write(self):
        f = open("newCFG",'w')
        for key in self.grammer.keys():
            f.write("# " + key + " = ")
            first = True
            for rule in self.grammer[key]:
                if first:
                    f.write(rule)
                    first = False
                else:
                    f.write(" | " + rule)
            f.write("\n")