const state = {
  inputs: [],
  targets: []
};

const mutations = {
  saveInputs(state, payload) {
    state.inputs = payload;
  }
};

const actions = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
