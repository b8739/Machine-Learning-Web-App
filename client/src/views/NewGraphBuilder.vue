<template>
  <v-dialog v-model="dialog" width="100%" class="ma-0">
    <v-container fill-height fluid class="pa-0">
      <v-navigation-drawer v-model="drawer" width="15%" height="100vh" :mini-variant.sync="mini">
        <v-list dense>
          <v-list-group v-model="depthStatus">
            <template v-slot:activator>
              <v-list-item-title active>Structure</v-list-item-title>
            </template>
            <v-list-item
              v-for="(structureMenu, menuIndex) in ['Data', 'Subplots', 'Transform']"
              :key="menuIndex"
              link
              @click="setMenuState(structureMenu.toLowerCase())"
            >
              <v-list-item-icon>
                <v-icon></v-icon>
              </v-list-item-icon>
              <v-list-item-title draggable label>{{ structureMenu }}</v-list-item-title>
            </v-list-item>
          </v-list-group>
        </v-list>
      </v-navigation-drawer>
      <v-main>
        <v-container fluid fill-height class="pa-0">
          <v-row>
            <!-- 2nd -->
            <v-col cols="3" class="pa-0 ma-0">
              <v-card class="pa-0 ma-0" height="100vh">
                <v-container fluid v-show="menuState == 'data'">
                  <v-row justify="end">
                    <v-col class="px-0 mx-0" cols="4"
                      ><v-btn @click="addEmptyTrace()">+ Data</v-btn></v-col
                    ></v-row
                  >
                  <v-row>
                    <v-expansion-panels multiple>
                      <v-col>
                        <v-expansion-panel
                          v-for="(tracePanel, tpIndex) in numTracePanel"
                          :key="tpIndex"
                        >
                          <v-expansion-panel-header class="flexContainer">
                            <template v-slot:actions>
                              <v-icon class="expandIcon">$expand</v-icon>
                            </template>
                            <span class="header"> Data {{ tpIndex + 1 }}</span>
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
                              <v-row>
                                <v-switch
                                  @change="value => changeOverlay(value, tpIndex)"
                                  v-if="tpIndex != 0"
                                  v-model="overlayModel[tpIndex]"
                                  label="Overlay"
                                ></v-switch>
                              </v-row>
                              <v-row>
                                <v-col class="pa-0 ma-0" cols="3">
                                  <v-subheader>Type</v-subheader></v-col
                                >
                                <v-col class="pa-0 ma-0" cols="9">
                                  <v-select dense></v-select></v-col
                              ></v-row>
                              <v-row v-for="(axisType, atIndex) in axisTypes" :key="atIndex">
                                <!-- x -->
                                <v-col class="pa-0 ma-0" cols="3">
                                  <v-subheader>{{ axisType }}</v-subheader></v-col
                                >
                                <v-col class="pa-0 ma-0" cols="9">
                                  <v-select
                                    clearable
                                    @click:clear="removeAxis(axisType, tpIndex)"
                                    @change="
                                      featureName => loadAxis(featureName, axisType, tpIndex)
                                    "
                                    :items="columns"
                                    dense
                                    v-model="selectedData[axisType][tpIndex]"
                                  ></v-select
                                ></v-col>
                              </v-row>
                              <v-card v-show="numTracePanel.length > 1" elevation="0">
                                <v-card-subtitle v class="my-2">Axis To Use</v-card-subtitle>
                                <v-row v-for="(axisType, atIndex) in axisTypes" :key="atIndex">
                                  <!-- x -->
                                  <v-col class="pa-0 ma-0" cols="3">
                                    <v-subheader>{{ axisType }}</v-subheader></v-col
                                  >
                                  <v-col class="pa-0 ma-0" cols="8">
                                    <v-select
                                      :items="axisList[axisType]"
                                      item-text="id"
                                      item-value="value"
                                      @change="
                                        selectedAxis =>
                                          changeAxis(
                                            selectedAxis,
                                            axisType,
                                            tpIndex,
                                            selectedData[axisType][tpIndex]
                                          )
                                      "
                                      dense
                                    ></v-select
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

                  <v-row>
                    <v-col cols="5" class="px-0 mx-0"><v-subheader>Num of rows</v-subheader></v-col>
                    <v-col class="pt-4">
                      <v-text-field
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
                    <v-col cols="5" class="px-0 mx-0"
                      ><v-subheader>Num of columns</v-subheader></v-col
                    >
                    <v-col class="pt-4">
                      <v-text-field
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

            <v-col class="pa-0 ma-0">
              <v-card height="100%">
                <PlotlyEdaGraph :graphWidth="700" :graphHeight="600" :isEdit="false" /> </v-card
            ></v-col>
          </v-row>
        </v-container>
      </v-main>
      <!-- <v-navigation-drawer height="100vh" v-model="drawer" absolute>
      je
    </v-navigation-drawer> -->
    </v-container>
  </v-dialog>
</template>
<script>
import Vue from "vue";
import { eventBus } from "@/main";
import PlotlyEdaGraph from "@/components/graph/PlotlyEdaGraph.vue";

import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  data() {
    return {
      selectedData: { x: [], y: [] },
      overlayModel: [0],
      grid: {
        rows: 1,
        columns: 1
      },
      blurHandler: false,
      axisTypes: ["x", "y"],
      numTracePanel: [0],
      dialog: true,
      drawer: true,
      depthStatus: true,
      mini: false,
      axisList: {
        x: [{ id: "Data 1", value: "x" }],
        y: [{ id: "Data 1", value: "y" }]
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
      ]
    };
  },
  watch: {
    grid: {
      handler: function() {
        eventBus.$emit("changeGridInfo", this.grid);
      },
      deep: true
    }
  },
  methods: {
    ...mapMutations("edaMenuHandler", ["setMenuState"]),
    loadGroupingData(axisType) {
      // 현재는 단일 groupingfeature만 되는 상태
      let path = "http://localhost:5000/loadGroupingData";
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

          eventBus.$emit("applyGroupBy", res.data);
          //subplot 나누기 (this.groupDataLength)
          // eventbus보내기 (로직은 for문 돌면서 하나씩 update)
        })
        .catch(error => {
          console.error(error);
        });
    },
    removeAxis(axisType, tpIndex) {
      let payload = { axisType: axisType, tpIndex: tpIndex };

      eventBus.$emit("removeAxis", payload);
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
      Vue.delete(this.numTracePanel, tpIndex);
      Vue.delete(this.axisList["x"], tpIndex);
      Vue.delete(this.axisList["y"], tpIndex);
      eventBus.$emit("deleteTrace", tpIndex);
    },
    addEmptyTrace() {
      this.numTracePanel.push(0);
      this.overlayModel.push(true);
      eventBus.$emit("addEmptyTrace", true);
    },
    loadAxis(featureName, axisType, tpIndex) {
      if (featureName == null || featureName == undefined) {
        return;
      } else {
        let payload = { featureName: featureName, axisType: axisType, tpIndex: tpIndex };
        eventBus.$emit("loadAxis", payload);
      }
    },
    changeAxis(selectedAxis, axisType, tpIndex, featureName) {
      let payload = {
        selectedAxis: selectedAxis,
        axisType: axisType,
        tpIndex: tpIndex,
        featureName: featureName
      };
      eventBus.$emit("changeAxis", payload);
    }
  },
  computed: {
    ...mapState({
      tableName: state => state.initialData.tableName,

      columns: state => state.initialData.columns,
      menuState: state => state.edaMenuHandler.menuState
    }),
    groupDataLength() {
      return this.groupingData.length;
    }
  },
  components: {
    PlotlyEdaGraph
  },
  created() {
    eventBus.$on("openDialog", dialogStatus => {
      this.dialog = dialogStatus;
      this.drawer = true;
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
