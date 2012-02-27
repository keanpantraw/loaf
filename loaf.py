'''
Created on Feb 27, 2012

@author: bfilippov
'''
import getopt
import re
import os
from sys import argv
from sys import exit
from lettuce import Feature

def usage():
    return """ %(name)s usage:
        %(name)s -h
        %(name)s --help :Display this message
        %(name)s test1.test -p Given,When,Then,And
        %(name)s test1.test --prepositions Given,When,Then,And :Assume given words as possible prepositions for steps
        %(name)s test1.test test2.test -t __init__.py
        %(name)s test1.test test2.test --to __init__.py :Generate stubs and store them in file __init__.py
        %(name)s -i template
        %(name)s --imports template :use imports from template in stubs
    """ % {'name' : argv[0]}

class Stub(object):
    
    __PARAMETER = re.compile(r'"[^"]*?"')
    __STEP_HACK = re.compile(r'(\w|").*')
    __EAT_PREFIX = re.compile(r'(?P<step>.*)')
    __STRIP = re.compile(r'\W+')
    
    def __init__(self, regex, signature):
        self.regex = regex
        self.signature = signature
        
    def __eq__(self, other):
        return self.regex == other.regex
    
    def __hash__(self):
        return self.regex.__hash__()
    
    def __str__(self):
        return str((self.regex, self.number_of_params))
    
    def stub(self):
        decorator = "@step(u'%s')" % self.regex
        method_name = Stub.__STRIP.sub('', self.regex)
        signature = 'def %s:' % self.signature
        return '%s\n%s\n    pass\n\n' % (decorator, signature)

    @staticmethod
    def __is_step(step):
        return Stub.__STEP_HACK.match(step) is not None

    @staticmethod
    def __eat_prefix(step):
        match = Stub.__EAT_PREFIX.match(step)
        if not match:
            return None
        return match.group('step')

    @staticmethod
    def make(regex, signature):
        if Stub.__is_step(regex):
            regex = Stub.__eat_prefix(regex)
            if regex:
                return Stub(regex, signature)
        return None
    
    @classmethod
    def set_prepositions(cls, prepositions):
        cls.__EAT_PREFIX =  re.compile(r'(%s)\s*(?P<step>.*)' % '|'.join(prepositions))

    
def generate_stubs(test):
    stubs = set()
    feature = Feature.from_file(test)
    for scenario in feature.scenarios:
        for step in scenario.steps:
            stub = Stub.make(step.proposed_sentence, step.proposed_method_name)
            if stub:
                stubs.add(stub)
    return stubs

def generate_text_stubs(stubs, header):
    text = '%s\n\n' % header
    for stub in stubs:
        text += stub.stub()
    return text

def write_stub(stub, filename):
    with open(filename, 'w+') as f:
        f.write(stub)

def generate(tests, prepositions, header, to_file):
    Stub.set_prepositions(prepositions)
    stubs = set()
    for test in tests:
        test_stubs = generate_stubs(test)
        if to_file:
            stubs |= test_stubs
        else:
            text = generate_text_stubs(test_stubs, header)
            stub_name = '%s.py' % os.path.splitext(test)[0]
            write_stub(text, stub_name)
    if to_file:
        text = generate_text_stubs(stubs, header)
        write_stub(text, to_file)
            
def _main():
    try:
        options, args = getopt.getopt(argv[1:], "tpi:h", 
                                      ['help', 'to=', 'prepositions=', 'imports='])
    except getopt.GetoptError as err:
        print usage()
        exit(1)
    
    to_file = None
    prepositions = ['Given', 'When', 'Then', 'And', 'Require', '']
    header = 'from lettuce import step\n'
    for o, a in options:
        if o in ('-h', '--help'):
            print usage()
            exit()
        elif o in ('-t', '--to'):
            to_file = a
        elif o in ('-p', '--prepositions'):
            prepositions = a.split(',')
        elif o in ('-i', '--imports'):
            with open(a) as f:
                header = f.read()
        else:
            print "Unhandled option: %s" % o
            exit(2)
            
    generate(args, prepositions, header, to_file = to_file)

if __name__ == '__main__':
    _main()