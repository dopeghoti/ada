from db import DB
from optimizer import Optimizer

class Satisfaction:
    def __init__(self):
        self.__db = DB("data.json")
        self.__opt = Optimizer(self.__db)

    def items(self, *args):
        print("calling !items with", len(args), "arguments:", ', '.join(args))

        if len(args) == 0:
            out = []
            for item in sorted(self.__db.items()):
                out.append(item)
            return '\n'.join(out)
        if len(args) == 1:
            item = args[0]
            if item not in self.__db.items():
                return "Unknown item: " + item
            return self.__db.items()[item].details()

    def recipes(self, *args):
        print("calling !recipes with", len(args), "arguments:", ', '.join(args))

        out = []
        if len(args) == 0:
            for recipe in sorted(self.__db.recipes()):
                out.append(recipe)
        elif len(args) == 1:
            arg = args[0]
            if arg not in self.__db.items() and arg not in self.__db.recipes():
                return "Unknown recipe or item: " + arg
            if arg in self.__db.recipes():
                return self.__db.recipes()[arg].details()
            if arg in self.__db.items():
                for recipe in self.__db.recipes_for_product(arg):
                    out.append(recipe.details())
        elif len(args) == 2:
            if args[0] != "using" and args[0] != "for":
                return "Input must be in the form \"!recipes\" \"for\" | \"using\" <item>"
            if args[1] not in self.__db.items():
                 return "Unknown item: " + args[1]
            if args[0] == "using":
                for recipe in self.__db.recipes_for_ingredient(args[1]):
                    out.append(recipe.details())
            elif args[0] == "for":
                for recipe in self.__db.recipes_for_product(args[1]):
                    out.append(recipe.details())
        return '\n'.join(out)

    def min(self, *args):
        print("calling !min with", len(args), "arguments:", ', '.join(args))
        return self.__opt.optimize(False, *args)

    def max(self, *args):
        print("calling !max with", len(args), "arguments:", ', '.join(args))
        return self.__opt.optimize(True, *args)