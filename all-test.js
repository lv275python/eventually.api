const context = require.context('./eventually/static/src/containers/__tests__/event', true, /.js$/);
context.keys().forEach(context);
module.exports = context;
