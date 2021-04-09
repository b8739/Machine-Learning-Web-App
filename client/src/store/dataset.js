//src/store/moduleName.js
const state = {
  //data
  dataset: {},
  summarizedInfo: [],
  indexNum: "",
  hadLoaded: false,
  columns: []
};

const getters = {};

const mutations = {
  loadDataset(state, payload) {
    state.dataset = payload.data;
  },
  loadIndexNum(state, payload) {
    state.indexNum = payload;
  },
  setHadLoaded(state, payload) {
    state.hadLoaded = payload;
  },
  saveResponseData(state) {
    if (state.hadLoaded == false) {
      let columnValues = Object.keys(state.dataset);
      for (const columnValue of columnValues) {
        state.columns.push(columnValue); //add했을 때 다시 loaddata되는데 push 때문에 중복된는 문제 해결 필요
        // state.updateForm[columnValue] = "";
        // state.addForm[columnValue] = "";
      }
    }
  },
  loadSummarizedInfo(state, payload) {
    state.summarizedInfo = payload;
  }
};

const actions = {
  loadFundamentalData({ commit }, path) {
    // const path = "http://localhost:5000/loadData";
    axios
      .get(path)
      .then(res => {
        commit("loadDataset", res);
        console.log(res);
        commit("loadIndexNum", Object.keys(res.data["ID"]).length - 1);
        // 데이터 추가 시 필요한 index number
        //'처음' 데이터를 받아올때만 columns 받아오도록 처리
        commit("saveResponseData");
      })
      .catch(error => {
        console.error(error);
      });
  }
};

export default {
  state: {
    ...state
  },
  getters,
  mutations,
  actions
};
