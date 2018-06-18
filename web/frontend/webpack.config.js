const webpack = require("webpack");
const path = require("path");

var CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
  context: path.resolve(__dirname, "./src/js"),

  entry: {
    scripts: './scripts.js',
    indexPage: './indexPage.js',
    categoryPage: "./categoryPage.js",
    productPage: "./productPage.js",
    cartPage: "./cartPage.js",
    deliveryPage: './deliveryPage.js',
    admin: './admin.js',
    md_admin: './md-admin.js',
    login: './login.js'
  },
  output: {
    path: path.resolve(__dirname, "./static/js"),
    publicPath: "/static/js/",
    filename: "[name].js"
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: "vue-loader",
        options: {
          loaders: {
            scss: "vue-style-loader!css-loader!sass-loader",
            sass: "vue-style-loader!css-loader!sass-loader?indentedSyntax",
            js: 'babel-loader?presets[]=es2015,presets[]=es2016'
          }
        }
      },
      {
        test: /\.js$/,
        loader: "babel-loader",
        exclude: /node_modules/,
        query: {
          presets: ['es2015', 'es2016'],
          plugins: ["dynamic-import-webpack"]
        }
      },
      {
        test: /\.css$/,
        use: [ 'style-loader', 'css-loader' ]
      }
    ]
  },
  resolve: {
    modules: [path.resolve(__dirname, "./src"), "node_modules"],
    alias: {
      vue$: "vue/dist/vue.common.js"
      //vue$: 'vue/dist/vue.esm.js'
    }
  },
  devtool: 'source-map',
  devServer: {
    publicPath: "/static/js/",
    disableHostCheck: true,
    // contentBase: path.resolve(__dirname, "./static/js"), //__dirname + '/frontend/',
    proxy: {
      "/": "http://localhost:8000"
    }
  },
};

module.exports.plugins = (module.exports.plugins || []).concat([

  new webpack.optimize.CommonsChunkPlugin({
    name: 'common',
    filename: 'common.js',
    chunks: ['scripts', 'index', 'catalog', 'product', 'cart']
  }),

]);

if (process.env.NODE_ENV === "production") {
  module.exports.devtool = false;

  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      "process.env.NODE_ENV": '"production"',
      "GEO_IP_HOST": JSON.stringify("http://kubomarket.ru:8282")
    }),

    new webpack.optimize.UglifyJsPlugin({
      comments: false,
      except: ['$super', '$', 'exports', 'require', 'self', 'STORE'],
      compress: { warnings: false }
    }),

    new webpack.optimize.CommonsChunkPlugin({
      name: 'common',
      filename: 'common.js',
      chunks: ['scripts', 'index', 'catalog', 'product', 'cart']
    }),

    new CopyWebpackPlugin([
      { from: './jquery-3.2.1.min.js', to: "./jquery-3.2.1.min.js" },
      { from: './plugins/jquery.fancybox.min.js', to: "./jquery.fancybox.min.js" },
      { from: './plugins/owl.carousel.min.js', to: "./owl.carousel.min.js" },
    ]),

    new webpack.LoaderOptionsPlugin({
      //minimize: true
    })
  ]);
} else {
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      "GEO_IP_HOST": JSON.stringify("http://127.0.0.1:8282")
    }),
    new CopyWebpackPlugin([
      { from: './jquery-3.2.1.min.js', to: "./jquery-3.2.1.min.js" },
      { from: './plugins/jquery.fancybox.min.js', to: "./jquery.fancybox.min.js" },
      { from: './plugins/owl.carousel.min.js', to: "./owl.carousel.min.js" },
    ]),
    new webpack.optimize.UglifyJsPlugin({
      comments: false,
      except: ['$super', '$', 'exports', 'require', 'self', 'STORE'],
      compress: { warnings: false }
    }),
  ]);
}
