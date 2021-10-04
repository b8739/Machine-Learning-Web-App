<template>
  <div id="wrap">
    <Header> </Header>
    <!-- <v-btn @click="apiCheck"></v-btn> -->
    <!-- <div>preprocessStatus:{{ preprocessStatus }}</div>
    <div>editStatus:{{ editStatus }}</div>
    <div>activatedEvent:{{ activatedEvent }}</div>

    <div>additionalCancelEvent:{{ additionalCancelEvent }}</div>
    <div>router:{{ $router.name }}</div> -->

    <v-main>
      <v-container id="mainWrapper" fluid>
        <div style="height:100vh">
          <v-row>
            <!-- 화면 좌측 -->
            <v-col cols="2">
              <SideMenu />
            </v-col>
            <!-- 화면 우측 -->
            <v-col cols="10" class="px-8">
              <v-toolbar elevation="1">
                <!-- Preprocess/Table 교체 버튼 -->
                <v-row>
                  <v-btn class="mr-2" @click="changeComponent('SummaryTable')">Features</v-btn>
                  <v-btn @click="changeComponent('DataTable')">Table</v-btn>

                  <v-spacer></v-spacer>
                  <portal-target :name="summaryPortal"> </portal-target>
                  <SaveMenu />
                </v-row>
              </v-toolbar>
              <v-row>
                <!-- <GraphBuilder :columns="columns" /> -->
                <NewGraphBuilder />
                <DeleteStepper />
                <AverageModal />

                <!-- Table and Features (Dynamic Component) -->
                <keep-alive>
                  <component :ref="comp" v-bind:is="comp"></component>
                </keep-alive>
              </v-row>
            </v-col>
          </v-row>
        </div>
      </v-container>
    </v-main>
    <portal :to="confirmButtonSpot">
      <v-btn color="error" @click="confirmEvent()">Confirm</v-btn>
      <v-btn @click="cancelEvent()">Cancel</v-btn>
    </portal>
  </div>
</template>
<script>
import axios from "axios";
//views
import GraphBuilder from "./GraphBuilder.vue";
import NewGraphBuilder from "./NewGraphBuilder.vue";
import DeleteStepper from "./DeleteStepper.vue";
import AverageModal from "@/components/average/AverageModal.vue";
//components

import SummaryTable from "@/components/preprocess/SummaryTable";
import DataTable from "@/components/preprocess/DataTable";
import SideMenu from "@/components/preprocess/SideMenu.vue";
import SaveMenu from "@/components/save/SaveMenu.vue";

//vuex
import { mapActions, mapState, mapGetters, mapMutations } from "vuex";

// eventbus
import { eventBus } from "@/main";

export default {
  data() {
    return {
      chartMountCount: 0,
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
      // comp: "SummaryTable"
      comp: "DataTable"

      // activatedEvent:null
    };
  },
  watch: {},
  components: {
    SummaryTable,
    DataTable,
    GraphBuilder,
    NewGraphBuilder,
    SideMenu,
    SaveMenu,
    DeleteStepper,
    AverageModal
  },
  computed: {
    ...mapState({
      columns: state => state.initialData.columns,
      datasetSize: state => state.initialData.datasetSize,
      preprocessStatus: state => state.preprocessHandler.preprocessStatus,
      activatedEvent: state => state.preprocessHandler.activatedEvent,
      additionalCancelEvent: state => state.preprocessHandler.additionalCancelEvent,
      editStatus: state => state.preprocessHandler.editStatus,
      datasetItems: state => state.dataTableHandler.datasetItems
    }),
    ...mapGetters("summaryTableHandler", ["summaryChangeFlag"]),
    ...mapGetters("dataTableHandler", ["tableChangeFlag"]),

    confirmButtonSpot() {
      return this.preprocessStatus;
    },
    summaryPortal() {
      let includeSubstring = "summary";
      let exclueSubstring = "Modal";
      if (this.preprocessStatus != null) {
        if (
          this.preprocessStatus.includes(includeSubstring) &&
          !this.preprocessStatus.includes(exclueSubstring)
        ) {
          return this.preprocessStatus;
        } else return "";
      } else return "";
    }
  },
  methods: {
    confirmEvent() {
      this.activatedEvent();
    },

    ...mapMutations("initialData", ["setNavStatus"]),
    ...mapMutations("preprocessHandler", ["setPreprocessStatus"]),
    ...mapMutations("preprocessHandler", ["setEditMode"]),
    ...mapMutations("preprocessHandler", ["setEditStatus"]),
    ...mapMutations("dataTableHandler", ["resetDataTableVuex"]),
    ...mapMutations("summaryTableHandler", ["resetSummaryTableVuex"]),
    ...mapMutations("edaHandler", ["resetEda"]),
    ...mapActions("preprocessHandler", ["cancelEvent"]),
    ...mapActions("initialData", ["loadSummarizedData"]),
    ...mapActions("initialData", ["loadColumns"]),
    ...mapActions("initialData", ["loadDatasetSize"]),
    ...mapActions("summaryTableHandler", ["cloneOriginalArray"]),

    changeComponent(componentName) {
      this.askSave();
      if (this.datasetItems.length == 0) {
        eventBus.$emit("reloadDataTable", true);
      }
      // this.setComponent(componentName);
      eventBus.$emit("changeComponent", componentName);
      this.comp = componentName;
    },

    displaySwitch() {
      this.showFeatures = !this.showFeatures;
      this.showTable = !this.showTable;
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
    },
    // rollback() {
    //   const path = "http://localhost:5000/rollback";
    //   axios.get(path).catch(error => {
    //     console.error(error);
    //   });
    // },
    askSave() {
      // 변경사항 있을 때
      if (
        (this.comp == "SummaryTable" && this.summaryChangeFlag == true) ||
        (this.comp == "DataTable" && this.tableChangeFlag == true)
      ) {
        if (confirm("변경사항이 아직 저장되지 않았습니다. 저장하시겠습니까?") == true) {
          eventBus.$emit("saveChanges", true);
        }
        // 취소했을때
        else {
          // this.rollback();
          // rollback 대신에 뭐가 들어가야 함
          if (this.comp == "DataTable") {
            this.resetDataTableVuex();
          } else if (this.comp == "SummaryTable") {
            this.resetSummaryTableVuex();
            this.selectionTimer = setTimeout(() => {
              this.cloneOriginalArray();
            }, 1000);
          }
        }
      }
      // 변경사항 없을 때
    }
  },
  created() {
    this.resetEda();
    this.resetSummaryTableVuex();
    this.$root.$refs.preprocessComp = this;
    // const path = "http://localhost:5000/startPreprocess"; //gsession -> trigger
    // axios.get(path).catch(error => {
    //   console.error(error);
    // });
    this.$root.$refs.preprocess = this;
    this.setNavStatus("preprocess");
    this.loadColumns();
    this.loadDatasetSize();
  },
  mounted() {
    console.log("preprocess mounted");
    window.addEventListener("beforeunload", this.askSave); //새로고침 방지
  },
  beforeUnmount() {
    window.removeEventListener("beforeunload", this.askSave);
  },
  // beforeRouteEnter(to, from, next) {
  //   next(vm => {
  //     vm.dialog1 = true;
  //   });
  // s}

  beforeDestroy() {
    this.askSave();
  }
  // beforeRouteLeave(to, from, next) {
  //   if (confirm("변경사항이 아직 저장되지 않았습니다. 저장하시겠습니까?") == true) {
  //     const path = "http://localhost:5000/overwriteTable";
  //     axios.get(path).catch(error => {
  //       console.error(error);
  //     });
  //   } else {
  //     next();
  //   }
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
