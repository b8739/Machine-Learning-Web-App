const state = {
  graphSources: null,
  modelingSummary: null,
  caseList: [],
  caseDataset: null
};

const mutations = {
  saveGraphSources(state, payload) {
    state.graphSources = payload;
  },
  saveModelingSummary(state, payload) {
    state.modelingSummary = payload;
  },
  saveCaseList(state, payload) {
    state.caseList = payload;
  },
  saveCaseDataset(state, payload) {
    state.caseDataset = payload;
  }
};

const actions = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
