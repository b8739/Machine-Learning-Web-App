const state = {
  simulationInput: [],
  simulationMethod: null
};

const mutations = {
  saveSimulationInput(state, payload) {
    state.simulationInput = payload;
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
