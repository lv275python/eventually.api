const context = require.context('./eventually/static/src/containers/__tests__', true, /.js$/);
context.keys().forEach(context);
module.exports = context;
