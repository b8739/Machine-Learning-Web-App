const state = {
  graphSources: null
};

const mutations = {
  saveGraphSources(state, payload) {
    state.graphSources = payload;
  }
};

const actions = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
