import reader as reader
import first as create_first
import follow as create_follow
import helper as helper
import parsing_table as parsing_table


class Parser(object):

    def __init__(self, file="cfg"):
        self.file = file

    def parse(self):
        n = reader.readParse(self.file)
        print(n.grammer)

        first = create_first.First(n.grammer)
        helper.write(first.first_rules, "Firsts")

        follow = create_follow.Follow(first.rules_by_non_terminal, first.first_rules)
        helper.write(follow.follow_rules, "Follows")

        pt = parsing_table.ParsingTable(first.first_rules, follow.follow_rules, first.rules_by_non_terminal)
        helper.write_parsing_table(pt.parsing_table, pt.expressions)
