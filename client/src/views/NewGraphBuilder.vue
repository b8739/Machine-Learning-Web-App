<template>
  <v-navigation-drawer
    right
    :width="edaWidth"
    v-model="edaDrawer"
    absolute
    :mini-variant.sync="edaMini"
  >
    <v-container fill-height fluid>
      <v-row>
        <v-col>
          <v-btn
            @click="(edaDrawer = false), resetScreen(), setGraphSelectModel([])"
            elevation="0"
            color="white"
          >
            <v-icon>mdi-close</v-icon></v-btn
          >
        </v-col>
        <v-col>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="secondary" @click="openDash" v-bind="attrs" v-on="on" class="mr-2">
                Open in a New Tab (Datashader)</v-btn
              >
            </template>
            <span>Use Dash/Datashader in a new Tab (Recommended for large dataset)</span>
          </v-tooltip>
        </v-col>
      </v-row>
      <v-subheader>
        This EDA chart works okay with a dataset size around 50k <br />
        (if not use Datashader instead: click the button above)
      </v-subheader>
      <v-tabs>
        <v-tab
          v-for="(menu, menuIndex) in ['Data', 'Subplots', 'Transform']"
          :key="menuIndex"
          @click="setMenuState(menu.toLowerCase())"
          :disabled="menu == 'Transform'"
          >{{ menu }}
        </v-tab>
      </v-tabs>

      <v-main>
        <v-container fill-height class="pa-0 ">
          <v-row>
            <!-- 2nd -->
            <v-col cols="4" class="">
              <v-card height="100vh">
                <!-- <v-btn @click="graphUpdate">graphUpdate</v-btn>
                <v-btn @click="graphRelayout">Relayout</v-btn> -->
                <v-container v-show="menuState == 'data'">
                  <!-- <v-row class="px-0 mx-0" cols="4">
                    <v-btn @click="progressDialog = true">
                      개발 현황
                    </v-btn>
                  </v-row>
                  <v-row class="px-0 mx-0" cols="4">
                    <v-dialog width="50%" v-model="progressDialog">
                      <v-simple-table>
                        <template>
                          <thead>
                            <tr>
                              <th>Feature</th>
                              <th>Progress</th>
                              <th></th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(info, index) in devProgess" :key="index">
                              <td>{{ info.function }}</td>

                              <td>
                                <v-icon :color="iconColor(info.progress)">{{
                                  info.progress
                                }}</v-icon>
                              </td>
                            </tr>
                          </tbody>
                        </template>
                      </v-simple-table></v-dialog
                    >

                   </v-row
                  > -->
                  <v-row>
                    <v-btn small outlined @click="resetAll()">Reset All</v-btn>
                    <v-col class=""> <v-btn @click="addEmptyTrace()">+ Data</v-btn></v-col></v-row
                  >
                  <v-row> </v-row>
                  <v-row>
                    <v-expansion-panels multiple v-model="openedPanel">
                      <v-col>
                        <v-expansion-panel
                          v-for="(tracePanel, tpIndex) in numTracePanel"
                          :key="tpIndex"
                        >
                          <v-expansion-panel-header class="flexContainer">
                            <template v-slot:actions>
                              <v-icon class="expandIcon">$expand</v-icon>
                            </template>
                            <span class="header"> Data {{ tracePanel }}</span>
                            <v-btn
                              @click="deleteTrace(tpIndex)"
                              class="closeIcon pa-0"
                              elevation="0"
                              color="white"
                            >
                              <svg width="20px" height="20px">
                                <path
                                  d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"
                                ></path></svg
                            ></v-btn>
                          </v-expansion-panel-header>
                          <v-expansion-panel-content>
                            <v-container fluid>
                              <v-row v-if="tpIndex != 0">
                                <v-col class="pa-0 ma-0">
                                  <v-select
                                    dense
                                    label="Overlay"
                                    placeholder="Data 1"
                                    @change="value => changeOverlay(value, tpIndex)"
                                    v-model="overlayModel[tpIndex]"
                                    :items="overlayTargets"
                                  ></v-select></v-col
                              ></v-row>
                              <v-row>
                                <v-col class="pa-0 ma-0">
                                  <v-select
                                    label="Type"
                                    dense
                                    value="scatter"
                                    :items="['scatter', 'line', 'bar', 'histogram']"
                                    @input="graphType => changeGraphType(graphType, tpIndex)"
                                  ></v-select></v-col
                              ></v-row>
                              <v-row> </v-row>
                              <v-row>
                                <v-col class="pa-0 ma-0">
                                  <!-- :disabled="currentDraft == null || currentDraft == undefined" -->

                                  <v-select
                                    label="Dataset"
                                    @input="loadColumns(tpIndex)"
                                    dense
                                    :items="gridList"
                                    item-text="name"
                                    item-value="id"
                                    v-model="selectedGrid[tpIndex]"
                                  ></v-select>
                                </v-col>
                              </v-row>
                              <v-row v-for="(axisType, atIndex) in axisTypes" :key="atIndex">
                                <!-- x -->

                                <v-col class="pa-0 ma-0">
                                  <v-select
                                    :label="axisType"
                                    clearable
                                    @click:clear="removeData(axisType, tpIndex)"
                                    @change="
                                      featureName =>
                                        loadAxis(
                                          selectedGrid[tpIndex],
                                          featureName,
                                          axisType,
                                          tpIndex
                                        )
                                    "
                                    :items="columnsOfDataset[datasetToLoad[selectedGrid[tpIndex]]]"
                                    dense
                                    v-model="selectedData[axisType][tpIndex]"
                                  ></v-select
                                ></v-col>
                              </v-row>
                              <v-card v-show="numTracePanel.length > 1" elevation="0">
                                <v-card-subtitle v class="my-2">Axis To Use</v-card-subtitle>
                                <v-row v-for="(axisType, atIndex) in axisTypes" :key="atIndex">
                                  <!-- x -->

                                  <v-col class="pa-0 ma-0">
                                    <v-select
                                      :items="axisList[axisType]"
                                      item-text="id"
                                      item-value="value"
                                      placeholder="Data 1 "
                                      @change="
                                        selectedAxis =>
                                          changeAxis(
                                            selectedAxis,
                                            axisType,
                                            tpIndex,
                                            selectedData[axisType][
                                              Object.keys(axisList[axisType])[tpIndex]
                                            ],
                                            overlayModel[tpIndex]
                                          )
                                      "
                                      dense
                                      v-model="axisToUse[axisType][tpIndex]"
                                    >
                                    </v-select
                                  ></v-col>
                                  <v-col class="pa-0 ma-0" cols="1">
                                    <v-btn
                                      @click="addAxis"
                                      outlined
                                      class="px-0 mx-2"
                                      small
                                      elevation="0"
                                      :disabled="axisList.x.length == numTracePanel.length"
                                      ><v-icon small>mdi-plus</v-icon></v-btn
                                    >
                                  </v-col>
                                </v-row>
                              </v-card>
                            </v-container>
                          </v-expansion-panel-content>
                        </v-expansion-panel>
                      </v-col>
                    </v-expansion-panels>
                  </v-row>
                </v-container>
                <v-container fluid v-show="menuState == 'subplots'">
                  <v-card-subtitle>Grid Setting</v-card-subtitle>
                  <label class="caption ma-0 pa-0">
                    Only the graphs that use
                    <strong style="color:red"> own independent axis</strong>
                    and
                    <strong style="color:red">not overlayed</strong>
                    are displayed as Subplots
                  </label>

                  <v-row>
                    <v-col class="pt-4">
                      <v-text-field
                        label="Num of rows"
                        ref="rowField"
                        v-model.number="grid['rows']"
                        type="number"
                        outlined
                        dense
                        hide-details
                      ></v-text-field
                    ></v-col>
                  </v-row>
                  <v-row>
                    <v-col class="pt-4">
                      <v-text-field
                        label="Num of columns"
                        v-model.number="grid['columns']"
                        outlined
                        type="number"
                        dense
                        hide-details
                      ></v-text-field
                    ></v-col>
                  </v-row>
                  <v-row justify="center" align="center">
                    <!-- <div class="rectGrid"></div>
                    <div class="rectGrid"></div> -->
                    <table class="gridTable">
                      <tr v-for="(row, rowIndex) in grid['rows']" :key="rowIndex">
                        <td
                          v-for="(column, columnsIndex) in grid['columns']"
                          :key="columnsIndex"
                          class="rectGrid"
                        ></td>
                      </tr>
                    </table>
                  </v-row>
                </v-container>
                <v-container fluid v-show="menuState == 'transform'">
                  <v-card-subtitle>Transform Setting</v-card-subtitle>
                  {{ groupColumn }}
                  <v-row v-for="(axisType, atIndex) in axisTypes" :key="atIndex">
                    <!-- x -->
                    <v-col class="pa-0 ma-0" cols="3">
                      <v-subheader>{{ axisType }}</v-subheader></v-col
                    >
                    <v-col class="pa-0 ma-0" cols="9">
                      <v-select
                        @change="loadGroupingData(axisType)"
                        clearable
                        :items="columns"
                        dense
                        v-model="groupColumn[axisType]"
                      ></v-select
                    ></v-col>
                  </v-row>
                </v-container>
              </v-card>
            </v-col>

            <v-col class="">
              <v-card> <PlotlyEdaGraph :isEdit="false" /> </v-card
            ></v-col>
          </v-row>
        </v-container>
      </v-main>
      <!-- <v-navigation-drawer height="100vh" v-model="drawer" absolute>
      je
    </v-navigation-drawer> -->
    </v-container>
  </v-navigation-drawer>
</template>
<script>
import Vue from "vue";
import { eventBus } from "@/main";
import PlotlyEdaGraph from "@/components/graph/PlotlyEdaGraph.vue";
import axios from "axios";

import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  data() {
    return this.getDefaultState();
  },
  watch: {
    grid: {
      handler: function() {
        eventBus.$emit("changeGridInfo", this.grid);
      },
      deep: true
    },
    edaDrawer: {
      handler: function() {
        if (this.edaDrawer) {
          console.log("split");
          this.splitScreen();
        } else {
          this.resetScreen();
        }
      },

      immediate: true
    }
  },
  methods: {
    ...mapMutations("edaMenuHandler", ["setMenuState"]),
    ...mapMutations("edaMenuHandler", ["resetEda"]),
    ...mapMutations("initialData", ["splitScreen"]),
    ...mapMutations("initialData", ["resetScreen"]),
    ...mapMutations("aggrid", ["setGraphSelectModel"]),
    openDash() {
      let w = 1000;
      let h = 700;
      let leftPosition = (screen.width - w) / 2;
      let topPosition = (screen.height - h) / 2;
      let url = "http://localhost:8000/dashapp1/";

      window.open(
        url,
        "dashapp",
        "width=" +
          w +
          ",height=" +
          h +
          ",top=" +
          topPosition +
          ",left=" +
          leftPosition +
          ", scrollbars=no"
      );
    },
    createNewDash() {
      let path = "http://localhost:8000/createNewDash";
      axios({
        method: "get",
        url: path
      })
        .then(res => {
          alert("created");
        })
        .catch(error => {
          console.error(error);
        });
    },
    iconColor(value) {
      if (value == "mdi-check") {
        return "blue";
      } else return "red";
    },
    getDefaultState() {
      return {
        edaDrawer: false,
        edaMini: false,
        progressDialog: false,
        devProgess: [
          { function: "Create Graph(s)", progress: "mdi-check" },
          { function: "Remove Graph", progress: "mdi-check" },
          { function: "Reset All", progress: "mdi-check" },
          { function: "Load X/Y Data", progress: "mdi-check" },
          { function: "Change Graph Type (ex. scatter,bar, histogram ...)", progress: "mdi-check" },
          { function: "Share Axis / Independent Axis", progress: "mdi-check" },
          { function: "Multiple Data in Single Graph", progress: "mdi-check" },
          { function: "Each Data in Independent Graph (Subplot)", progress: "mdi-check" },
          { function: "Delete Rows by 'Rectangle Selection'", progress: "mdi-triangle-outline" },
          { function: "Delete Rows by 'Lasso Selection'", progress: "mdi-close" },
          { function: "Transform (ex. Grouping)", progress: "mdi-close" }
        ],
        dialog: false,
        overlayAllSwitch: false,
        openedPanel: [null],
        selectedData: { x: [], y: [] },
        axisToUse: { x: { 0: 0 }, y: { 0: 0 } },
        overlayModel: ["Data 1 "],
        grid: {
          rows: 1,
          columns: 1
        },
        blurHandler: false,
        axisTypes: ["x", "y"],
        numTracePanel: [1],
        drawer: true,
        depthStatus: true,
        mini: false,
        axisList: {
          x: [{ id: "Data 1 ", value: "x" }],
          y: [{ id: "Data 1 ", value: "y" }]
        },
        groupColumn: {
          x: "",
          y: ""
        },
        loadedFeatures: [
          {
            x: null,
            y: null
          }
        ],
        selectedGrid: {},
        columnsOfDataset: {}
      };
    },

    resetAll() {
      Object.assign(this.$data, this.getDefaultState());
      this.$data.dialog = true;
      this.$data.edaDrawer = true;
      eventBus.$emit("resetAll", "yes"); //eda한테 보내서 createPlot
    },
    graphUpdate() {
      eventBus.$emit("graphUpdate", "yes");
    },
    graphRelayout() {
      eventBus.$emit("graphRelayout", "yes");
    },
    changeGraphType(graphType, tpIndex) {
      let payload = { graphType: graphType, tpIndex: tpIndex };
      eventBus.$emit("changeGraphType", payload);
    },
    loadColumns(tpIndex) {
      let datasetName = this.datasetToLoad[this.selectedGrid[tpIndex]];

      console.log("datasetName");
      console.log(datasetName);
      // if문을 통해서 해당 table의 column이 load되어 있지 않을 경우에만 loadColumns

      if (Object.keys(this.columnsOfDataset).includes(datasetName)) {
        return;
      } else {
        let path = "http://localhost:8000/loadColumns";
        axios({
          method: "post",
          url: path,
          data: {
            tableName: datasetName,
            projectName: this.projectName
          }
        })
          .then(res => {
            let tableName = datasetName;
            Vue.set(this.columnsOfDataset, tableName, res.data);
          })
          .catch(error => {
            console.error(error);
          });
      }
    },
    loadGroupingData(axisType) {
      // 현재는 단일 groupingfeature만 되는 상태
      let path = "http://localhost:8000/loadGroupingData";
      // axios
      this.$axios({
        method: "post",
        url: path,
        data: {
          tableName: this.tableName,
          groupingFeature: this.groupColumn[axisType],
          otherFeatures: [this.selectedData["x"][0], this.selectedData["y"][0]]
        }
      })
        .then(res => {
          // this.groupingData = res.data;
          let payload = { groupby: axisType, data: res.data };
          eventBus.$emit("applyGroupBy", payload);
          //subplot 나누기 (this.groupDataLength)
          // eventbus보내기 (로직은 for문 돌면서 하나씩 update)
        })
        .catch(error => {
          console.error(error);
        });
    },
    removeData(axisType, tpIndex) {
      let payload = { axisType: axisType, tpIndex: tpIndex };
      eventBus.$emit("removeData", payload);
    },
    addAxis() {
      let axisTypes = ["x", "y"];

      axisTypes.forEach(element => {
        let itemText = `Data ${this.numTracePanel.length}`;
        let itemValue = `${element}${this.numTracePanel.length}`;
        let item = { id: itemText, value: itemValue };
        this.axisList[element].push(item);
      });
    },
    changeOverlay(value, tpIndex) {
      let payload = { value: value, tpIndex: tpIndex };

      eventBus.$emit("changeOverlay", payload);
    },
    deleteTrace(tpIndex) {
      let axisList = ["x", "y"];
      axisList.forEach(axis => {
        Vue.delete(this.axisList[axis], tpIndex);
        Vue.delete(this.selectedData[axis], tpIndex);
        Vue.delete(this.axisToUse[axis], tpIndex);
      });

      Vue.delete(this.selectedGrid, tpIndex);
      Vue.delete(this.numTracePanel, tpIndex);

      this.overlayModel.splice(tpIndex, 1);
      eventBus.$emit("deleteTrace", tpIndex);
    },
    addEmptyTrace() {
      this.openedPanel = [];
      this.openedPanel.push(this.numTracePanel.length);

      this.numTracePanel.push(this.numTracePanel.length + 1);
      this.addAxis();

      this.overlayModel.push("Data 1 ");

      eventBus.$emit("addEmptyTrace", true);
    },
    loadAxis(gridID, featureName, axisType, tpIndex) {
      // console.log(draftInfo);
      if (featureName == null || featureName == undefined) {
        return;
      } else {
        let payload = {
          gridID: gridID,
          featureName: featureName,
          axisType: axisType,
          tpIndex: tpIndex
        };
        eventBus.$emit("loadAxis", payload);
      }
    },
    changeAxis(selectedAxis, axisType, tpIndex, featureName, overlayModel) {
      let payload = {
        selectedAxis: selectedAxis,
        axisType: axisType,
        tpIndex: tpIndex,
        featureName: featureName,
        overlayModel: overlayModel
      };
      eventBus.$emit("changeAxis", payload);
    }
  },
  computed: {
    ...mapState({
      edaWidth: state => state.initialData.edaWidth,
      currentDraft: state => state.aggrid.currentDraft,
      gridList: state => state.aggrid.gridList,
      projectName: state => state.initialData.projectName,
      tableList: state => state.initialData.tableList,
      datasetToLoad: state => state.aggrid.datasetToLoad,

      columns: state => state.initialData.columns,
      menuState: state => state.edaMenuHandler.menuState
    }),

    overlayTargets() {
      let array = ["None"];

      for (let i = 1; i < this.numTracePanel.length; i++) {
        array.push("Data " + i);
      }
      return array;
    },
    groupDataLength() {
      return this.groupingData.length;
    }
  },
  components: {
    PlotlyEdaGraph
  },
  created() {
    this.resetEda();
    eventBus.$on("openDialog", dialogStatus => {
      // this.dialog = dialogStatus;
      this.edaDrawer = !this.edaDrawer;
    });
  }
};
</script>
<style scoped>
.expandIcon {
  order: 1;
}

.header {
  order: 2;
  flex-grow: 10 !important;
  padding-left: 10px;
}
.closeIcon {
  order: 3;
  flex-grow: 1 !important;
}
.v-btn {
  min-width: 28px !important;
}
.gridTable {
  border-collapse: collapse;
}
.rectGrid {
  width: 33.5px;
  height: 33.5px;
  border-bottom: 0px;
  border-right: 0px;
  border-color: #d0d3d8 !important;
  /* float: left; */
  border-top: 1px solid;
  border-left: 1px solid;
  border-right: 1px solid;
  border-bottom: 1px solid;
}
.solidRight {
  border-right: 1px solid;
}
.solidBottom {
  border-bottom: 1px solid;
}
</style>
