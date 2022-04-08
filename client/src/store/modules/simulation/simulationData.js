const state = {
  observedVariable: null,
  simulationMethod: null
};

const mutations = {
  saveObservedVariable(state, payload) {
    state.observedVariable = payload;
  },
  saveSimulationMethod(state, payload) {
    state.simulationMethod = payload;
  }
};

const actions = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
