const state = {
  graphSources: null,
  modelingSummary: null
};

const mutations = {
  saveGraphSources(state, payload) {
    state.graphSources = payload;
  },
  saveModelingSummary(state, payload) {
    state.modelingSummary = payload;
  }
};

const actions = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
