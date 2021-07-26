<template>
  <div id="wrap">
    <Header> </Header>
    <div class="text-center">
      <v-dialog v-model="dialog1" hide-overlay persistent width="300">
        <v-card color="primary" dark>
          <v-card-text>
            Please stand by
            <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
          </v-card-text>
        </v-card>
      </v-dialog>
    </div>
    <v-container id="mainWrapper" fluid>
      <v-row>
        <!-- 화면 좌측 -->
        <v-col cols=""><SideMenu /></v-col>
        <!-- 화면 우측 -->
        <v-col cols="10">
          <v-toolbar elevation="1">
            <!-- Preprocess/Table 교체 버튼 -->
            <v-row>
              <v-btn class="mr-2" @click="changeComponent('DataFeatures')">Feature</v-btn
              ><v-btn @click="changeComponent('InfiniteTable')">Table</v-btn>

              <v-spacer></v-spacer>

              <SaveMenu />
            </v-row>
          </v-toolbar>
          <v-row>
            <!-- <GraphBuilder :columns="columns" /> -->
            <DeleteStepper />
            <AverageModal />
            <ChangeOrder />
            <!-- Table and Features (Dynamic Component) -->
            <keep-alive>
              <component v-bind:is="comp"></component>
            </keep-alive>
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
      dialog1: false,
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
      modelingPreprocessFlag: false,
      comp: "DataFeatures"
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
    changeComponent(componentName) {
      this.comp = componentName;
    },
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
  // beforeRouteEnter(to, from, next) {
  //   next(vm => {
  //     vm.dialog1 = true;
  //   });
  // }
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
</style>
