const webpack = require('webpack');
const nodeExternals = require('webpack-node-externals');
const WebpackShellPlugin = require('webpack-shell-plugin');
const IstanbulPlugin = require ('webpack-istanbul-plugin');
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
        }),

        new IstanbulPlugin({
                    test: /\.js$/,
                    include: [
                        path.join(__dirname, 'eventually/static/'),
                    ],
                    exclude: [
                        path.resolve('node_modules'),
                        path.resolve('test/index.js'),
                        /\.spec\.js$/,
                    ],
                }),
    ]
};

module.exports = config;
