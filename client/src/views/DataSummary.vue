<template>
  <div id="wrap">
    <div class="sidebar">
      <div class="editData">
        <button class="editButto btn-1" type="button" v-b-modal.add-modal>Add Row</button>
        <button class="editButton btn-1" type="button" @click="showElement()">Update Row</button>
      </div>
    </div>
    <div id="mainContents">
      <div class="toggle-summary">
        <button class="btn-1" @click="displaySwitch()">Feature</button>
        <button class="btn-1" @click="displaySwitch()">Table</button>
      </div>
      <!-- <DataFeatures
        :class="{ visibilityHidden: showFeatures }"
        :columnsWithoutIndex="columnsWithoutIndex"
        :summarizedData="summarizedData"
        :dataSet="dataSet"
        :indexNum="indexNum"
      /> -->

      <!-- <DataTable
        :class="{ visibilityHidden: showTable }"
        :columns="columns"
        :dataSet="dataSet"
        :hadLoaded="hadLoaded"
        :isHidden="isHidden"
        :rowIndex="rowIndex"
      /> -->
      <InfiniteTable />
      <!-- rowIndex는 update 체크박스 만들기 위한 배열 (key: ID, value: true/false) -->
      <AddModal
        :columnsWithoutIndex="columnsWithoutIndex"
        :addForm="addForm"
        :indexNum="indexNum"
        @loadDataStatus="loadData"
      />
    </div>
  </div>
</template>
<script>
import axios from "axios";
//components
import DataTable from "../components/DataTable";
import Sidebar from "../components/Sidebar";
import AddModal from "../components/AddModal";
import DataFeatures from "../components/DataFeatures";
import InfiniteTable from "../components/InfiniteTable";

export default {
  data() {
    return {
      columns: [],
      dataSet: {},
      indexNum: "",
      addForm: {}, //ex. sepal-width:' ' , sepal-length: ' ' ...
      updateForm: {},
      hadLoaded: false,
      isHidden: true,
      rowIndex: [],
      showFeatures: false,
      showTable: true
    };
  },
  props: ["summarizedData"],
  components: {
    DataTable,
    Sidebar,
    AddModal,
    DataFeatures,
    InfiniteTable
  },
  computed: {
    columnsWithoutIndex() {
      const idIndex = this.columns.indexOf("ID");
      let tempColumns;
      if (idIndex != -1) {
        //처음엔 -1이라서 에러를 발생시킴, 때문에 if문으로 해당 경우의 수를 제거
        tempColumns = this.columns.slice(); //copy by value
        tempColumns.splice(this.columns, 1);
      }
      return tempColumns;
    }
  },
  methods: {
    loadData() {
      const path = "http://localhost:5000/loadData";
      axios
        .get(path)
        .then(res => {
          console.log(typeof res.data);
          console.log(res.data);
          this.dataSet = res.data;
          // 데이터 추가 시 필요한 index number
          this.indexNum = Object.keys(this.dataSet["ID"]).length - 1; //149
          //'처음' 데이터를 받아올때만 columns 받아오도록 처리
          if (this.hadLoaded == false) this.saveResponseData();
        })
        .catch(error => {
          console.error(error);
        });
    },
    displaySwitch() {
      this.showFeatures = !this.showFeatures;
      this.showTable = !this.showTable;
    },
    saveResponseData() {
      let columnValues = Object.keys(this.dataSet);
      for (const columnValue of columnValues) {
        this.columns.push(columnValue); //add했을 때 다시 loaddata되는데 push 때문에 중복된는 문제 해결 필요
        this.updateForm[columnValue] = "";
        this.addForm[columnValue] = "";
      }
    },

    // 변형시켜야 하는 메소드들

    getIndexForUpdate(targetIndex) {
      console.log(`targetIndex: ${targetIndex}`);
      this.updateForm["ID"] = targetIndex;
    },
    // for update
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.updateDataModal.hide();
      this.updateData(this.updateForm);

      // this.updateBook(payload, this.updateForm);
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.updateDataModal.hide();
      this.initForm();
      this.loadData(); // why?
    },
    updateData(payload) {
      console.log(payload);
      const path = `http://localhost:5000/updateData`;
      axios
        .put(path, payload)
        .then(() => {
          this.loadData();
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
          this.loadData();
        });
    },
    initForm() {
      this.addForm = {};
    },
    showElement() {
      this.isHidden = !this.isHidden;
      for (let i = 0; i < Object.keys(this.dataSet[this.columns[0]]).length; i++) {
        this.rowIndex.push(false);
      }
    }
  },
  created() {
    // this.loadData();
    // console.log("created");
  },
  mounted() {
    // console.log("mounted");
  },
  beforeUpdate() {
    // console.log("beforecreate");
  },
  updated() {
    // console.log("updated");
    this.hadLoaded = true;
  }
};
</script>

<style>
body {
  background-color: #f2f2f2;
}
a {
  text-decoration: none;
}
#wrap {
  overflow: hidden;
}
.sidebar {
  width: 30%;
  height: 100vh;
  border-right: 1px solid #dee4ea;
  float: left;
}

#mainContents {
  width: 70%;
  float: left;
}
.toggle-summary {
  top: 105px;
  left: 400px;
}
.toggle-summary button {
  width: 90px;
  margin-left: 5px;

  background: #d8d6d6;
  border: none;
  border-radius: 5px;
  color: rgb(29, 27, 27);
  display: inline-block;
  font-size: 0.9em;
  font-weight: bold;
  padding: 1px 0;
  text-align: center;
  position: relative;
  text-transform: capitalize;
}

/* button styling */
/* GENERAL BUTTON STYLING */
.toggle-summary button,
.toggle-summary button::after {
  -webkit-transition: all 0.3s;
  -moz-transition: all 0.3s;
  -o-transition: all 0.3s;
  transition: all 0.3s;
}

.toggle-summary button::before,
.toggle-summary button::after {
  background: rgb(13, 189, 113);
  content: "";
  position: absolute;
  z-index: -1;
  border-radius: 5px;
}

.toggle-summary button:hover {
  color: #fff;
  background: none;
}

/* BUTTON 1 */
.btn-1::after {
  height: 0;
  left: 0;
  top: 0;
  width: 100%;
}

.btn-1:hover:after {
  height: 100%;
}

/* editData */
.editData button {
  /* top: 10px; */
  width: 100%;
  height: 50px;
  display: block;
  border: 0.5px solid #d8d6d6;
  position: relative;
}

.editData button::before,
.editData button::after {
  background: rgb(13, 189, 113);
  content: "";
  position: absolute;
  z-index: -1;
  border-radius: 5px;
}

.editData button:hover {
  color: #fff;
  background: none;
}
.visibilityHidden {
  display: none;
}
</style>
