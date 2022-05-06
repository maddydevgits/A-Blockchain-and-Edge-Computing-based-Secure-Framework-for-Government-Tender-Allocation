const tender = artifacts.require("tender");

module.exports = function (deployer) {
  deployer.deploy(tender);
};
