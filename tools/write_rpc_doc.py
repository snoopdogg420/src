#!/usr/bin/env python2
import collections
import compiler


class CategoryParser:
    def __init__(self, filepath):
        self.filepath = filepath

        self.categories = {}

    def parse(self):
        with open(self.filepath, 'r') as f:
            for i, line in enumerate(f.readlines()):
                line = line.strip()
                if (not line.startswith('# --- ')) or (not line.endswith(' ---')):
                    continue
                self.addCategory(i + 1, line[6:-4].title())

    def addCategory(self, lineno, category):
        self.categories[lineno] = category

    def getCategory(self, lineno):
        for k in sorted(self.categories.keys()):
            if k > lineno:
                break
            category = self.categories[k]
        else:
            category = 'Unknown'
        return category


class MethodParser(CategoryParser):
    def __init__(self, filepath):
        CategoryParser.__init__(self, filepath)

        self.filepath = filepath

        # Order matters, so store the method information in an OrderedDict:
        self.methods = collections.OrderedDict()

    def parse(self):
        CategoryParser.parse(self)

        # Get the root node:
        node = compiler.parseFile(self.filepath).node

        # Parse any class objects:
        for child in node.getChildren():
            if isinstance(child, compiler.ast.Class):
                self.parseClass(child)

    def parseClass(self, node):
        # Skip past the class definition, and go into the body:
        stmt = node.getChildNodes()[-1]

        # Parse any function objects:
        for child in stmt.getChildren():
            if isinstance(child, compiler.ast.Function):
                self.parseFunction(child)

    def parseFunction(self, node):
        # First, verify that this is an RPC method:
        if not node.name.startswith('rpc_'):
            # RPC methods are required to have their name begin with 'rpc_'.
            return
        name = node.name[4:]
        if node.decorators is None:
            # RPC methods are also required to utilize the @rpcmethod
            # decorator.
            return
        for decorator in node.decorators:
            if decorator.node.name != 'rpcmethod':
                continue
            accessLevel = 'Unknown'
            for arg in decorator.args:
                if arg.name != 'accessLevel':
                    continue

                # Format the access level string:
                accessLevel = ' '.join(arg.expr.name.split('_')).title()
            break
        else:
            return

        # Documentation is nice, but not required:
        doc = node.doc or ''

        # If we have documentation, we'll want to get rid of the function level
        # indentation:
        if doc:
            lines = doc.split('\n')
            indentLevel = len(lines[0]) - len(lines[0].lstrip())
            for i, line in enumerate(lines):
                lines[i] = line[indentLevel:]
            doc = '\n'.join(lines)

        # Get the category in which this method is under:
        category = self.getCategory(node.lineno)

        # Store this method's information:
        self.methods.setdefault(category, []).append((name, accessLevel, doc))

    def getMethods(self):
        return self.methods


parser = MethodParser('toontown/rpc/ToontownRPCHandler.py')
parser.parse()
for k, v in parser.getMethods().items():
    print k
    for name, accessLevel, doc in v:
        print (' ' * 4) + name + ' | ' + accessLevel
        print doc
