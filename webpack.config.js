module.exports = [
  {
    entry: "./projector/static/src/dashboard.scss",
    output: {
      filename: "style-bundle.js",
    },
    module: {
      rules: [
        {
          test: /\.scss$/,
          use: [
            {
              loader: "file-loader",
              options: { name: "dashboard.css" },
            },
            { loader: "extract-loader" },
            { loader: "css-loader" },
            {
              loader: "sass-loader",
              options: {
                implementation: require("node-sass"),
                webpackImporter: false,
              },
            },
          ],
        },
      ],
    },
  },
];
