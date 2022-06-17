module.exports = function (api) {
  api.cache(true);

  const presets = [
    ['@babel/preset-env', {targets: {node: 'current'}}],
    "@babel/preset-react",
    "@babel/preset-typescript"
  ]

  const plugins = [
    "@babel/plugin-syntax-jsx"
  ]

  return {
    presets,
    plugins
  }
}
