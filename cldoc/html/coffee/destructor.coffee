class cldoc.Destructor extends cldoc.Method
  @title = ['Destructor', 'Destructors']

  constructor: (@node) ->
    super(@node)

cldoc.Node.types.destructor = cldoc.Destructor


