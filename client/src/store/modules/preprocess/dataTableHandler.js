import axios from "axios";
import Vue from "vue";

const getDefaultState = () => {
  return {
    /* Infinite Table */

    datasetItems: [],
    // Infinite Loading API로 테이블 데이터를 불러와서 담는 배열 (format: Objects wrapped by Object)
    limit: 0,
    // Infinite Loading으로 데이터를 몇 줄씩 가져올건지 나타내는 변수 (0으로 시작해서 매 차례 45씩 증가하며 45줄을 가져옴)
    numOfInsertion: 0,
    numOfDeletion: 0,
    insertedItems: [],
    // 데이터를 Edit하더라도 아직 Session에서 commit되지 않는 상태이기 때문에, 위 3개의 변수를 활용해서 테이블에 시각적으로 변화를 준다 (v-for)

    /* Data Edit */
    checkedRows: [],
    // <Delete 시 사용> checkbox가 체크된 Row들을 담는 배열
    editingRowIndex: null,
    columnField: {},
    // <Insert, Update 시 사용> Insert하거나 Update할 데이터 한 줄의 값들을 저장해서 이후에 Request를 보낼 때 사용 (v-textfield와 v-model되어 있음)
    originalColumnField: {},
    dialog: false
    // <Insert, Update 시 사용>
  };
};
const state = getDefaultState();

const getters = {
  fakeDatasetSize(state, getters, rootState) {
    return rootState.initialData.datasetSize + state.numOfInsertion - state.numOfDeletion;
  },
  // save flag
  tableChangeFlag(state, getters, rootState) {
    if (
      rootState.initialData.datasetSize ==
      rootState.initialData.datasetSize + state.numOfInsertion - state.numOfDeletion
    ) {
      return false;
    } else return true;
  },

  columnFieldChangeFlag(state, getters) {
    if (JSON.stringify(state.columnField) == JSON.stringify(state.originalColumnField)) {
      return false;
    } else return true;
  }
};

const mutations = {
  setEditingRowIndex(state, payload) {
    state.editingRowIndex = payload;
  },
  addLimit(state, payload) {
    state.limit += payload;
  },
  updateDatasetItem(state) {
    Vue.set(state.datasetItems, state.editingRowIndex, state.columnField);
  },
  setOriginalColumnField(state, payload) {
    state.originalColumnField = payload;
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
  setColumnFieldByKey(state, payload) {
    Vue.set(state.columnField, payload.columnName, payload.value);
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
  insertRow({ commit, state, getters, rootState }) {
    let path = "http://localhost:5000/insertRow";

    axios({
      method: "post",
      url: path,
      data: {
        tableName: rootState.initialData.tableName,
        rowToInsert: state.columnField,
        ID: getters.fakeDatasetSize
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
  deleteRow({ commit, state, rootState }) {
    let path = "http://localhost:5000/deleteRow";
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
  updateRow({ commit, state, rootState }) {
    let path = "http://localhost:5000/updateRow";
    if (state.columnFieldChangeFlag == false) {
      alert("No Changes to Update");
      return;
    }
    console.log(state.columnField);
    axios({
      method: "post",
      url: path,
      data: {
        tableName: rootState.initialData.tableName,
        rowToUpdate: state.columnField
      }
    })
      .then(res => {
        // 체크박스 초기화
        // 업데이트 알림
        alert(`Successfully Updated!`);
        commit("updateDatasetItem");
        // 초기화
        commit("preprocessHandler/setEditMode", false, { root: true });
        commit("preprocessHandler/setPreprocessStatus", null, { root: true });
        commit("setDialog", false);
      })
      .catch(error => {
        console.error(error);
      });
  },
  infiniteLoadingCreated({ commit, state, rootState }) {
    let api = "http://localhost:5000/infiniteLoading";
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
