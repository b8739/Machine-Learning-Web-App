const state = {
  inputs: [],
  targets: []
};

const mutations = {
  saveInputs(state, payload) {
    state.inputs = payload;
  },
  saveTargets(state, payload) {
    state.targets = payload;
  }
};

const actions = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
