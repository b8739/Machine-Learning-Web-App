<template>
  <div id="wrap">
    <Header> </Header>

    <v-main>
      <v-container fluid>
        <div style="height:110vh">
          <v-row>
            <!-- 화면 좌측 -->
            <!-- <v-col cols="2">
            </v-col> -->
            <!-- 화면 우측 -->
            <v-col cols="12" class="px-8">
              <!-- Preprocess/Table 교체 버튼 -->

              <!-- <v-toolbar elevation="1">
                <v-row>
                  <v-btn class="mr-2" @click="changeComponent('SummaryTable')">Features</v-btn>
                  <v-btn @click="changeComponent('AgContainer')">Table</v-btn>

                  <v-spacer></v-spacer>
                  <portal-target :name="summaryPortal"> </portal-target>
  
                </v-row>
              </v-toolbar> -->
              <v-row>
                <AgContainer />

                <!-- Table and Features (Dynamic Component) -->
                <!-- <keep-alive>
                  <component :ref="comp" v-bind:is="comp"></component>
                </keep-alive> -->
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
//components

// import SummaryTable from "@/components/preprocess/SummaryTable";
import DataTable from "@/components/preprocess/DataTable";
import AgContainer from "@/components/preprocess/AgContainer";

//vuex
import { mapActions, mapState, mapGetters, mapMutations } from "vuex";

// eventbus
import { eventBus } from "@/main";

export default {
  data() {
    return {
      // comp: "SummaryTable"
      comp: "AgContainer"
    };
  },
  watch: {},
  components: {
    // SummaryTable,
    DataTable,
    AgContainer
  },
  computed: {
    ...mapState({
      columns: state => state.initialData.columns,
      tableName: state => state.initialData.tableName,
      datasetSize: state => state.initialData.datasetSize,
      preprocessStatus: state => state.preprocessHandler.preprocessStatus,
      editStatus: state => state.preprocessHandler.editStatus,
      datasetItems: state => state.dataTableHandler.datasetItems,
      tableChangeFlag: state => state.dataTableHandler.tableChangeFlag
    }),
    ...mapGetters("summaryTableHandler", ["summaryChangeFlag"]),

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
    revertChanges() {
      const path = "http://localhost:8000/revertChanges";
      axios
        .get(path, {
          params: {
            tableName: this.tableName
          }
        })
        .then(res => {
          console.log(res);
        })
        .catch(error => {
          console.error(error);
        });
    },

    ...mapMutations("initialData", ["setNavStatus"]),
    ...mapMutations("preprocessHandler", ["setPreprocessStatus"]),
    ...mapMutations("preprocessHandler", ["setEditMode"]),
    ...mapMutations("preprocessHandler", ["setEditStatus"]),
    ...mapMutations("dataTableHandler", ["resetDataTableVuex"]),
    ...mapMutations("summaryTableHandler", ["resetSummaryTableVuex"]),
    ...mapMutations("edaHandler", ["resetEda"]),
    ...mapActions("preprocessHandler", ["cancelEvent"]),
    ...mapActions("initialData", ["loadColumns"]),
    ...mapActions("initialData", ["loadDatasetSize"]),
    ...mapActions("summaryTableHandler", ["cloneOriginalArray"]),

    changeComponent(componentName) {
      if (this.datasetItems.length == 0) {
        eventBus.$emit("reloadDataTable", true);
      }
      // this.setComponent(componentName);
      eventBus.$emit("changeComponent", componentName);
      this.comp = componentName;
    }
  },
  created() {
    this.resetEda();
    this.resetSummaryTableVuex();
    this.$root.$refs.preprocessComp = this;
    this.$root.$refs.preprocess = this;
    this.setNavStatus("preprocess");
    // this.loadDatasetSize();
  },
  mounted() {
    // console.log("preprocess mounted");
    // window.addEventListener("beforeunload", this.askSave); //새로고침 방지
  },
  beforeUnmount() {
    // window.removeEventListener("beforeunload", this.askSave);
  },

  beforeDestroy() {}
  // beforeRouteLeave(to, from, next) {
  //   if (confirm("변경사항이 아직 저장되지 않았습니다. 저장하시겠습니까?") == true) {
  //     const path = "http://localhost:8000/overwriteTable";
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
</style>
