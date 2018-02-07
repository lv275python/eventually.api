const webpack = require('webpack');
const path = require('path');
const ExtractTextPlugin = require("extract-text-webpack-plugin");

const config = {
    entry:   path.join(__dirname, 'eventually/static/src/app.js'),
    output: {
        path: path.join(__dirname,'eventually/static/public'),
        filename: 'bundle.js'
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
        },
        {
            test: /\.less$/,
            use: ExtractTextPlugin.extract({
                fallback: 'style-loader',
                use: ['css-loader', 'less-loader']
            })
        },
        {
            test: /\.(jpe?g|png|gif|svg)$/i,
            loader: 'file-loader'
          }
        ]
    },
    plugins:[
        new ExtractTextPlugin({
            filename: 'style.css',
            disable: false,
            allChunks: true
        })
    ],
};

module.exports = config;
