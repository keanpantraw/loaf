from lettuce import step


@step(u'I go "([^"]*)"')
def whethever_i_go_group1(step, group1):
    pass

@step(u'I return at "([^"]*)"')
def always_i_return_at_group1(step, group1):
    pass

