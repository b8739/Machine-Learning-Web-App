const state = {
  featureNameFlag: false,
  featureOrderFlag: false,
  modifiedColumns: []
};

const mutations = {
  ChangeColumnNameFlag(state, payload) {
    state.featureNameFlag = payload;
  },
  ChangeColumnOrderFlag(state, payload) {
    state.featureOrderFlag = payload;
  }
};

const actions = {
  // updateChangedColumn({ commit, rootState }, payload) {
  //   rootState.columns = [];
  //   payload.forEach(element => {
  //     console.log(rootState.columns);
  //     rootState.columns.push(element);
  //   });
  // }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
