<template>
  <div id="wrap">
    <Header> </Header>

    <v-container id="mainWrapper" fluid>
      <v-row>
        <!-- 화면 좌측 -->
        <v-col cols=""><SideMenu /></v-col>
        <!-- 화면 우측 -->
        <v-col cols="10">
          <v-toolbar elevation="1">
            <!-- Preprocess/Table 교체 버튼 -->
            <v-row>
              <v-btn class="mr-2" @click="displaySwitch()">Feature</v-btn
              ><v-btn @click="displaySwitch()">Table</v-btn>

              <v-spacer></v-spacer>

              <SaveMenu />
            </v-row>
          </v-toolbar>
          <v-row>
            <!-- <GraphBuilder :columns="columns" /> -->
            <DeleteStepper />
            <AverageModal />
            <ChangeOrder />

            <DataFeatures :class="{ visibilityHidden: showFeatures }" />

            <InfiniteTable :class="{ visibilityHidden: showTable }" :columns="columns" />
            <!-- rowIndex는 update 체크박스 만들기 위한 배열 (key: ID, value: true/false) -->
            <!-- <AddModal :addForm="addForm" :indexNum="indexNum" @loadDataStatus="loadData" /> -->
          </v-row>
        </v-col>
      </v-row>
    </v-container>
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

import AddModal from "@/components/modal/AddModal";
import DataFeatures from "@/components/layout/DataFeatures";
import InfiniteTable from "@/components/layout/InfiniteTable";
import SideMenu from "@/components/layout/SideMenu.vue";
import SaveMenu from "@/components/save/SaveMenu.vue";
import ChangeOrder from "@/components/changeOrder/ChangeOrder.vue";

import ModelingProcess from "./modeling/ModelingProcess.vue";

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
      showTable: true,
      // flag
      featureFlag: true,
      modelingPreprocessFlag: false
    };
  },
  components: {
    DataTable,

    AddModal,
    DataFeatures,
    InfiniteTable,
    GraphBuilder,
    SideMenu,
    SaveMenu,
    DeleteStepper,
    AverageModal,
    ChangeOrder,

    ModelingProcess
  },
  // props: ["summarizedInfo"],
  computed: {
    ...mapGetters("initialData", ["columns"])
  },
  methods: {
    ...mapMutations("initialData", ["setHadLoaded"]),
    ...mapMutations("initialData", ["setNavStatus"]),
    // ...mapMutations("initialData", ["loadSummarizedInfo"]),
    ...mapActions("initialData", ["loadFundamentalData"]),
    ...mapActions("initialData", ["loadSummarizedData"]),
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
    this.loadFundamentalData("http://localhost:5000/loadData");
    this.loadSummarizedData();
    this.setNavStatus("preprocess");
  }
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
