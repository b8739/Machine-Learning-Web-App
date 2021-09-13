import axios from "axios";
import Vue from "vue";

const getDefaultState = () => {
  return {
    //   overall
    datasetItems: [],
    //deleteData
    checkedRows: [],
    limit: 0,
    //insertData
    columnField: {},
    numOfInsertion: 0,
    numOfDeletion: 0,
    insertedItems: [],
    dialog: false
  };
};
const state = getDefaultState();

const getters = {
  tableChangeFlag(state, getters, rootState) {
    if (
      rootState.initialData.datasetSize ==
      rootState.initialData.datasetSize + state.numOfInsertion - state.numOfDeletion
    ) {
      return false;
    } else return true;
  }
};

const mutations = {
  addLimit(state, payload) {
    state.limit += payload;
  },

  deleteDatasetItems(state, payload) {
    payload.forEach(element => {
      Vue.delete(state.datasetItems, element);
    });
  },
  addDatasetItems(state, payload) {
    state.datasetItems.push(...payload);
  },
  setCheckedRows(state, payload) {
    state.checkedRows = payload;
  },
  pushCheckedRows(state, payload) {
    state.checkedRows.push(payload);
  },
  setColumnField(state, payload) {
    state.columnField = payload;
  },
  setNumOfInsertion(state, payload) {
    state.numOfInsertion = payload;
  },
  addInsertItems(state, payload) {
    state.insertedItems.push(payload);
  },
  setDialog(state, payload) {
    state.dialog = payload;
  },
  resetDataTableVuex(state) {
    Object.assign(state, getDefaultState());
  },
  setNumOfDeletion(state, payload) {
    state.numOfDeletion += payload;
  }
};

const actions = {
  //   cancelEvent({ commit, state }) {

  //   },
  deleteRow({ commit, state, rootState }) {
    let path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/deleteSingleRow";
    axios({
      method: "post",
      url: path,
      data: {
        tableName: rootState.initialData.tableName,
        idNumbers: state.checkedRows
      }
    })
      .then(res => {
        // 데이터 삭제 (updating frontend)
        commit("deleteDatasetItems", state.checkedRows);
        let numOfRows = state.checkedRows.length;
        // 체크박스 초기화
        let emptyArray = [];
        commit("setCheckedRows", emptyArray);
        commit("setNumOfDeletion", numOfRows);
        // commit("initialData/setDatasetSize", rootState.initialData.datasetSize - numOfRows, {
        //   root: true
        // });
        alert(`Total ${numOfRows} row(s) Successfully Deleted!`); //삭제 알림
        // 초기화
        commit("preprocessHandler/setEditMode", false, { root: true });
        commit("preprocessHandler/setPreprocessStatus", null, { root: true });
      })
      .catch(error => {
        console.error(error);
      });
  },

  insertRow({ commit, state, rootState }) {
    let path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/insertRow";
    axios({
      method: "post",
      url: path,
      data: {
        tableName: rootState.initialData.tableName,
        rowToInsert: state.columnField
      }
    })
      .then(res => {
        alert("Data Added");
        commit("setNumOfInsertion", state.numOfInsertion + 1);
        commit("addInsertItems", JSON.parse(JSON.stringify(state.columnField)));
        //   초기화
        commit("preprocessHandler/setPreprocessStatus", null, { root: true });
        commit("setDialog", false);
      })
      .catch(error => {
        console.error(error);
      });
  },
  infiniteLoadingCreated({ commit, state, rootState }) {
    let api = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/infiniteLoading";
    axios
      .get(api, {
        params: {
          limit: state.limit
        }
      })
      .then(({ data }) => {
        // this.limit += 45; //이 값을 app.py의 192줄의 값과 똑같게 해준다.

        commit("addLimit", 45);
        commit("addDatasetItems", data);
      });
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
