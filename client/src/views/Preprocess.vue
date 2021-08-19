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
    <v-main>
      <v-container id="mainWrapper" fluid>
       <div style=height:100vh>
          <v-row>
            <!-- 화면 좌측 -->
            <v-col cols="2">
              <SideMenu />
            </v-col>
            <!-- 화면 우측 -->
          <v-col cols="10" class=px-8>
              <v-toolbar elevation="1">
                <!-- Preprocess/Table 교체 버튼 -->
                <v-row>
                  <v-btn class="mr-2" @click="changeComponent('DataFeatures')">Feature</v-btn>
                  <v-btn @click="changeComponent('InfiniteTable')">Table</v-btn>

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
          </div>
        </v-card>
      </v-container>
    </v-main>
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

//vuex
import { mapActions, mapState, mapMutations } from "vuex";

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
      comp: "DataFeatures"
    };
  },
  watch: {},
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
    ChangeOrder
  },
  computed: {
    ...mapState({
      columns: state => state.initialData.columns,
      datasetSize: state => state.initialData.datasetSize
    })
  },
  methods: {
    ...mapMutations("initialData", ["setNavStatus"]),
    ...mapActions("initialData", ["loadSummarizedData"]),
    ...mapActions("initialData", ["loadColumns"]),
    ...mapActions("initialData", ["loadDatasetSize"]),

    changeComponent(componentName) {
      this.comp = componentName;
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
    this.setNavStatus("preprocess");
    this.loadColumns();
    console.log(this.columns);
    this.loadDatasetSize();
  },
  mounted() {
    console.log("preprocess mounted");
  },
  beforeDestroy() {
    // window.localStorage.clear();
    // console.log(window.localStorage);
  }
  // beforeRouteEnter(to, from, next) {
  //   next(vm => {
  //     vm.dialog1 = true;
  //   });
  // s}
  // beforeRouteLeave(to, from, next) {
  //   if (confirm("변경사항이 아직 저장되지 않았습니다. 저장하시겠습니까?") == true) {
  //     //
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
