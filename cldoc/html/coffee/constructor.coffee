class cldoc.Constructor extends cldoc.Method
  @title = ['Constructor', 'Constructors']

  constructor: (@node) ->
    super(@node)

cldoc.Node.types.constructor = cldoc.Constructor


