const context = require.context('./eventually/static/src/containers/tests', true, /.js$/);
context.keys().forEach(context);
module.exports = context;
