module.exports = [
  {
    entry: {
      dashboard: "./projector/static/src/dashboard.ts",
    },
    output: {
      filename: "[name].js",
    },
    module: {
      rules: [
        {
          test: /\.scss$/,
          exclude: /node_modules/,
          use: [
            { loader: "file-loader", options: { name: "dashboard.css" } },
            { loader: "extract-loader" },
            { loader: "css-loader" },
            {
              loader: "sass-loader",
              options: {
                implementation: require("sass"),
                webpackImporter: false,
                sassOptions: {
                  includePaths: ["./node_modules"],
                },
              },
            },
          ],
        },
        { test: /\.tsx?$/, loader: "ts-loader", exclude: /node_modules/ },
      ],
    },
  },
];
