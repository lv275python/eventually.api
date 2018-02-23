const webpack = require('webpack');
const nodeExternals = require('webpack-node-externals');
const WebpackShellPlugin = require('webpack-shell-plugin');
const path = require('path');

const config = {
    entry: './all-test.js',
    output: {
        path: path.join(__dirname,''),
        filename: 'testBundle.js'
    },
    target: 'node',
    externals: [nodeExternals()],
    node: {
        fs: 'empty'
    },
    resolve: {
        alias: {
            src: path.join(__dirname, 'eventually/static/src')
        }
    },

    module: {
        loaders: [
            {
                test: /\.jsx?/,
                include: path.join(__dirname, 'eventually/static/'),
                loader: 'babel-loader'
            }
        ]
    },

    plugins: [
        new WebpackShellPlugin({
            onBuildExit: 'mocha testBundle.js'
        })
    ]
};

module.exports = config;
