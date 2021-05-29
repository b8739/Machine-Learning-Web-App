const state = {
  inputs: [],
  targets: [],
  snippet: null
};

const mutations = {
  saveSnippet(state, payload) {
    state.snippet = payload;
  },
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
