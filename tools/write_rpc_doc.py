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
        category = 'Unknown'
        for k in sorted(self.categories.keys()):
            if k > lineno:
                break
            category = self.categories[k]
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

        # If we have documentation, we'll want to get rid of any indentation so
        # that we can have an easier time parsing it:
        if doc:
            lines = doc.split('\n')
            for i, line in enumerate(lines):
                lines[i] = line.lstrip()
            doc = '\n'.join(lines)

        # Get the category in which this method is under:
        category = self.getCategory(node.lineno)

        # Store this method's information:
        self.methods.setdefault(category, []).append((name, accessLevel, doc))

    def getMethods(self):
        return self.methods


class MediaWikiGenerator:
    def __init__(self, methods):
        self.methods = methods

        self.content = ''

    def generate(self):
        self.content = ''
        self.writeHeader()

        for category, methods in self.methods.items():
            self.writeCategory(category)
            for name, accessLevel, doc in methods:
                self.writeMethod(name, accessLevel, doc)

        self.writeFooter()
        return self.content

    def writeHeader(self):
        # Force a table of contents:
        self.content += '__TOC__\n'

    def writeCategory(self, category):
        self.content += '= %s =\n' % category

    def writeMethod(self, name, accessLevel, doc):
        # First, add the method name:
        self.content += '== %s ==\n' % name

        # Next, add the access level header:
        self.content += '<h5>%s</h5>\n' % accessLevel

        # Parse out the summary and write it to a block quote:
        if 'Summary:' in doc:
            doc = doc[doc.find('Summary:') + 9:]
            self.writeBlockQuote(' '.join(doc.split('\n\n', 1)[0].split('\n')))
            doc = doc[doc.find('\n\n') + 2:].lstrip()

        # Parse out the parameters and write them to a table:
        if ('Parameters: None' not in doc) and ('Parameters:' in doc):
            doc = doc[doc.find('Parameters:') + 12:]
            args = doc.split('\n\n', 1)[0][1:].split('\n[')
            doc = doc[doc.find('\n\n') + 2:].lstrip()

            for arg in args:
                name, description = arg.split(' = ', 1)
                name = name.rstrip()[:-1]
                description = ' '.join(description.split('\n'))
                type, name = name.split(' ', 1)

            self.content += '{|\n'
            self.content += '|-\n'
            self.content += '!colspan="3"|Parameters\n'
            self.content += '|-\n'
            self.content += '! Name\n'
            self.content += '! Type\n'
            self.content += '! Description\n'
            self.content += '|-\n'
            self.content += '| %s\n' % name
            self.content += '| %s\n' % type
            self.content += '| %s\n' % description
            self.content += '|}\n'

        # Finally, parse out the example response, and write it to a table:
        if 'Example response:' in doc:
            doc = doc[18:]
            self.content += '{|\n'
            self.content += '|-\n'
            self.content += '! rowspan="2"|Example Response\n'
            # TODO: Handle on success.
            self.content += '| TODO\n'
            self.content += '|}\n'

        return self.content

    def writeBlockQuote(self, data):
        self.content += '<blockquote>%s</blockquote>' % data

    def writeFooter(self):
        # Let the reader know that this documentation is automatically
        # generated:
        self.content += '----\n'
        self.content += ("''This document was automatically generated by the "
                         "<code>write_rpc_doc.py</code> utility.''\n")


parser = MethodParser('toontown/rpc/ToontownRPCHandler.py')
parser.parse()
generator = MediaWikiGenerator(parser.getMethods())
with open('test.txt', 'w') as f:
    f.write(generator.generate())
