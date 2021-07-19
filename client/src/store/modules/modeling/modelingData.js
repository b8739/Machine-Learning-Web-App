const state = {
  modelingRequest: null,
  splitRatio: null
};

const mutations = {
  saveModelingRequest(state, payload) {
    state.modelingRequest = payload;
  },
  saveSplitRatio(state, payload) {
    state.splitRatio = payload;
  }
};

const actions = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
