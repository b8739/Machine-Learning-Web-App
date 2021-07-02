const state = {
  inputs: [],
  targets: [],
  algorithm: null,
  parameters: []
};

const mutations = {
  saveAlgorithm(state, payload) {
    state.algorithm = payload;
  },
  saveInputs(state, payload) {
    state.inputs = payload;
  },
  saveTargets(state, payload) {
    state.targets = payload;
  },
  saveParameters(state, payload) {
    state.parameters = payload;
  }
};

const actions = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
