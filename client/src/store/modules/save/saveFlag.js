const state = {
  columnNameFlag: false,
  columnOrderFlag: false,
  columnsModified: null
};

const mutations = {
  ChangeColmnNameFlag(state, payload) {
    state.columnNameFlag = payload;
  },
  ChangeColumnOrderFlag(state, payload) {
    state.columnOrderFlag = payload;
  }
};

const actions = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
