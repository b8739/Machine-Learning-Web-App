<template>
  <div id="wrap">
    <!-- <div class="sidebar">
      <div class="editData">
        <button class="editButton btn-1" type="button" v-b-modal.add-modal>Add Row</button>
        <button class="editButton btn-1" type="button" @click="showElement()">Update Row</button>
      </div>
    </div> -->
    <v-app>
      <v-container id="mainWrapper" fluid>
        <v-row>
          <!-- 화면 좌측 -->
          <v-col cols="2"><SideMenu /></v-col>
          <!-- 화면 우측 -->
          <v-col cols="10">
            <v-row class="mainContainer">
              <!-- DataSummary/Table 교체 버튼 -->
              <v-col>
                <v-btn @click="displaySwitch()">Feature</v-btn
                ><v-btn @click="displaySwitch()">Table</v-btn>
              </v-col>

              <v-spacer></v-spacer>
              <!-- <v-btn elevation="2" @click="openSaveChangeDialog">Save Changes</v-btn>
             -->
              <v-col>
                <SaveMenu />
              </v-col>
            </v-row>
            <v-row>
              <GraphBuilder :columns="columns" />
              <DeleteStepper />
              <AverageModal />
              <DataFeatures
                :class="{ visibilityHidden: showFeatures }"
                :columnsWithoutIndex="columnsWithoutIndex"
                :columns="columns"
                :indexNum="indexNum"
              />

              <InfiniteTable :class="{ visibilityHidden: showTable }" :columns="columns" />
              <!-- rowIndex는 update 체크박스 만들기 위한 배열 (key: ID, value: true/false) -->
              <AddModal
                :columnsWithoutIndex="columnsWithoutIndex"
                :addForm="addForm"
                :indexNum="indexNum"
                @loadDataStatus="loadData"
              />
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-app>
  </div>
</template>
<script>
import axios from "axios";
//views
import GraphBuilder from "./GraphBuilder.vue";
import DeleteStepper from "./DeleteStepper.vue";
import AverageModal from "@/components/average/AverageModal.vue";
//components
import DataTable from "@/components/DataTable";
import Sidebar from "@/components/layout/Sidebar";
import AddModal from "@/components/modal/AddModal";
import DataFeatures from "@/components/layout/DataFeatures";
import InfiniteTable from "@/components/layout/InfiniteTable";
import SideMenu from "@/components/layout/SideMenu.vue";
import SaveMenu from "@/components/save/SaveMenu.vue";
//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

// eventbus
import { eventBus } from "@/main";

export default {
  data() {
    return {
      // dataSet: {},
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
  components: {
    DataTable,
    Sidebar,
    AddModal,
    DataFeatures,
    InfiniteTable,
    GraphBuilder,
    SideMenu,
    SaveMenu,
    DeleteStepper,
    AverageModal
  },
  // props: ["summarizedInfo"],
  computed: {
    ...mapState({
      columns: state => state.initialData.columns
      // summarizedInfo: state => state.initialData.summarizedInfo
    }),
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
    ...mapMutations("initialData", ["setHadLoaded"]),
    // ...mapMutations("initialData", ["loadSummarizedInfo"]),
    ...mapActions("initialData", ["loadFundamentalData"]),
    // showDrawer() {
    //   eventBus.$emit("showDrawer", true);
    // },
    loadData() {
      const path = "http://localhost:5000/loadData";
      axios
        .get(path)
        .then(res => {
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
    duplicateTable() {
      const path = "http://localhost:5000/duplicateTable";
      axios.get(path).catch(error => {
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
    },
    openSaveChangeDialog() {
      eventBus.$emit("openSaveChange", true);
    }
  },
  created() {
    // this.loadData(); //store.js 실험하기 위해서 일단 주석 처리
    this.loadFundamentalData("http://localhost:5000/loadData");
    // this.loadSummarizedInfo(this.summarizedData);

    // this.$store.dispatch("loadFundamentalData", "http://localhost:5000/loadData");
    // this.loadData();
  },
  mounted() {},
  beforeUpdate() {},
  updated() {}
};
</script>

<style>
#wrap {
  overflow: hidden;
}
.sidebar {
  width: 20%;
  height: 100vh;
  border-right: 1px solid #dee4ea;
  float: left;
}
#mainWrapper {
  /* width: 70%; */
  /* float: left; */
  /* padding: 20px; */
}
.mainContainer {
  min-width: 1200px;
  max-width: 1900px;
  margin: 0 auto;
}
.toggle-summary button {
  width: 8%;
  height: 8%;
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
