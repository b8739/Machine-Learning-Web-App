<template>
  <!-- <div style="width:700px">layout:{{ layout }}</div> -->

  <div ref="edaGraph"></div>
</template>
<script>
import { eventBus } from "@/main";
import Vue from "vue";

import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
let cloneDeep = require("lodash/cloneDeep");
export default {
  data() {
    return this.getDefaultState();
  },
  props: ["graphWidth", "graphHeight", "isEdit"],
  computed: {
    ...mapState({
      tableName: state => state.initialData.tableName,
      projectName: state => state.initialData.projectName,
      featureGraphData: state => state.apexchartGraph.featureGraphData,
      xaxisColumns: state => state.edaHandler.xaxisColumns,
      xaxisEvent: state => state.edaHandler.xaxisEvent,
      yaxisColumns: state => state.edaHandler.yaxisColumns,
      yaxisEvent: state => state.edaHandler.yaxisEvent,
      // aggrid

      // gridapi
      progressBar: state => state.aggrid.progressBar,

      gridApi: state => state.aggrid.gridApi,
      gridColumnApi: state => state.aggrid.gridColumnApi,
      currentGrid: state => state.aggrid.currentGrid,

      // transaction
      updateTransaction: state => state.aggrid.updateTransaction,
      deleteModel: state => state.aggrid.deleteModel,
      // model
      datasetToLoad: state => state.aggrid.datasetToLoad,

      renameModel: state => state.aggrid.renameModel,
      columnState: state => state.aggrid.columnState,
      typeModel: state => state.aggrid.typeModel,
      fillNaModel: state => state.aggrid.fillNaModel,
      deleteNaModel: state => state.aggrid.deleteNaModel,
      filterModel: state => state.aggrid.filterModel,
      gridType: state => state.aggrid.gridType,
      graphSelectModel: state => state.aggrid.graphSelectModel
    }),
    plotContainer() {
      return this.$refs["edaGraph"];
    }
  },
  methods: {
    ...mapMutations("aggrid", ["setGraphSelectModel"]),
    ...mapMutations("modelingData", ["showProgressBar"]),

    getDefaultState() {
      return {
        selectedData: [],

        dataFormat: {
          type: "scattergl",
          mode: "markers",
          // type: "bar",

          marker: {
            size: 2
          },
          line: {
            width: 1
          }
        },

        data: [
          {
            // scatter
            type: "scattergl",
            mode: "markers",
            // type: "bar",
            marker: {
              size: 2
              // marker is an object, valid marker keys: #scatter-marker
            },
            line: {
              // color: "rgb(219, 64, 82)",
              width: 1
            },
            showlegend: true
          }
        ],
        layout: {
          width: this.graphWidth,
          height: this.graphHeight,
          margin: {
            l: 30,
            r: 20,
            b: 20,
            t: 40,
            pad: 4
          },
          colorway: ["#2E93fA", "#66DA26", "#546E7A", "#E91E63", "#FF9800"],
          xaxis: {
            automargin: true
          },
          yaxis: {
            automargin: true
          },
          title: {
            text: "EDA Graph"
          }
        },
        config: {
          showSendToCloud: false,
          displaylogo: false,
          responsive: true,
          showEditInChartStudio: false,

          modeBarButtonsToRemove: ["sendDataToCloud"],
          modeBarButtonsToAdd: [
            {
              name: "Delete Selected Data",
              icon: {
                path:
                  "M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"
              },
              click: () => {
                var confirmflag = confirm("선택한 데이터를 삭제하시겠습니까?");
                // 삭제하는 경우
                if (confirmflag) {
                  if (this.selectedData.length != 0) {
                    this.selectedData.forEach(element => {
                      // 그래프상에서 삭제
                      if (this.data[0].x != undefined) Vue.set(this.data[0].x, element, null);
                      if (this.data[0].y != undefined) Vue.set(this.data[0].y, element, null);
                    });
                    // 기존 데이터 벡업
                    if (this.data[0].x != undefined) this.data[0].x = [this.data[0].x]; //array로 wrap
                    if (this.data[0].y != undefined) this.data[0].y = [this.data[0].y]; //array로 wrap
                    Plotly.restyle(this.plotContainer, this.data[0]);
                    //AgGrid에도 반영
                    eventBus.$emit("deleteRowsByGraph", this.selectedData);
                    this.setGraphSelectModel([]);
                  }
                } else {
                }
              }
            }
          ]
        }
      };
    },
    createPlot() {
      let vm = this;

      Object.assign(this.$data, this.getDefaultState());

      Plotly.newPlot(this.plotContainer, this.data, this.layout, this.config);
      // 선택되었을 때 selecedData에 넣어둠
      this.plotContainer.on("plotly_selected", async function(eventData) {
        vm.selectedData = [];

        await eventData.points.forEach(element => {
          vm.selectedData.push(element.pointIndex);
        });
        // 그래프에서 선택한거 AgGrid에 반영
        vm.setGraphSelectModel(vm.selectedData);
      });
    },

    addNewTrace() {
      let newTrace = cloneDeep(this.dataFormat);
      // newTrace["x"] = [[]];
      // newTrace["y"] = [[]];

      Plotly.addTraces(this.plotContainer, newTrace);
    },
    deleteTrace(tpIndex) {
      Plotly.deleteTraces(this.plotContainer, tpIndex);
    },
    updatePlot(featureName, data, axisType, tpIndex) {
      // 입력하는 축의 데이터 (ex. x)
      this.data[tpIndex][axisType] = [data];
      // 반대 축 데이터도 다시 입력해주어야 초기화가 안됨 (ex. y)
      let oppositeAxis = this.getOppositeAxis(axisType);
      if (this.data[tpIndex][oppositeAxis] != undefined) {
        this.data[tpIndex][oppositeAxis] = [this.data[tpIndex][oppositeAxis]];
      }
      this.data[tpIndex]["name"] = `Data ${tpIndex + 1}`;
      let fullAxis = this.getAxisName(axisType) + this.getAxisNumber(tpIndex);
      this.layout[fullAxis] = this.getFontFormat(featureName, axisType, tpIndex);
      Plotly.update(this.plotContainer, this.data[tpIndex], this.layout, tpIndex);

      // Plotly.restyle(this.plotContainer, this.data[tpIndex], tpIndex);
    },

    // Load Grid
    loadFullData(gridID, featureName, axisType, tpIndex) {
      // 1) Filter Model
      let filterModel;
      if (this.filterModel[gridID] != undefined) {
        filterModel = this.filterModel[gridID];
      } else {
        filterModel = {};
      }
      // 2) Delete Model
      let deleteModel;
      if (this.deleteModel[gridID] != undefined) {
        deleteModel = this.deleteModel[gridID];
      } else {
        deleteModel = [];
      }
      // 3) Rename Model
      let renameModel;
      if (this.renameModel[gridID] != undefined) {
        renameModel = this.renameModel[gridID];
      } else {
        renameModel = [];
      }
      // 3) Type Model
      let typeModel;
      if (this.typeModel[gridID] != undefined) {
        typeModel = this.typeModel[gridID];
      } else {
        typeModel = [];
      }
      // 4) fill Na Model

      let fillNaModel;
      if (this.fillNaModel[gridID] != undefined) {
        fillNaModel = this.fillNaModel[gridID];
      } else {
        fillNaModel = [];
      }
      // 5) delete Na Model

      let deleteNaModel;
      if (this.deleteNaModel[gridID] != undefined) {
        deleteNaModel = this.deleteNaModel[gridID];
      } else {
        deleteNaModel = [];
      }
      let path = "http://localhost:8000/loadEditGraphData";
      // axios
      this.$axios({
        method: "post",
        url: path,
        data: {
          columnModel: [featureName],

          tableName: this.datasetToLoad[gridID],
          projectName: this.projectName,
          deleteModel: deleteModel,
          filterModel: filterModel,
          renameModel: renameModel,
          typeModel: typeModel,
          fillNaModel: fillNaModel,
          deleteNaModel: deleteNaModel,
          gridType: this.gridType[gridID]
        }
      })
        .then(res => {
          // console.log(res.data);
          this.updatePlot(featureName, res.data[featureName], axisType, tpIndex);
        })
        .catch(error => {
          console.error(error);
        })
        .finally(() => {
          // this.showProgressBar(false);
        });
    },
    renderGroupingGraph(groupingData) {
      Object.keys(groupingData).forEach((element, index) => {
        console.log(index);
        // Data 1이 있는 상태에서 시작하므로, 1은 존재하는 것 재활용하고 없을 때 새로 만듦
        if (this.data[index] == undefined) {
          this.addNewTrace();
        }
        // Data Setting
        this.data[index]["x"] = groupingData[element][0];
        this.data[index]["y"] = groupingData[element][1];
        this.data[index]["name"] = element;
        // Layout Setting (Axis 분리)
        if (index != 0) {
          ["x", "y"].forEach(element => {
            //layout
            let axisNum = element + "axis" + parseInt(index + 1);
            this.layout[axisNum] = {};
            // this.layout[axisNum]["overlaying"] = axisType;
            this.layout[axisNum]["automargin"] = true;
            this.layout[axisNum]["title"] = {};
            Vue.set(this.data[index], element + "axis", element + parseInt(index + 1));
          });
        }
      });
      // let fullAxis = this.getAxisName(axisType) + this.getAxisNumber(tpIndex);
      // this.layout[fullAxis] = this.getFontFormat(featureName, axisType, tpIndex);
      Plotly.update(this.plotContainer, this.data, this.layout);
    },
    getOppositeAxis(axisName) {
      if (axisName == "x") return "y";
      else return "x";
    },
    getAxisName(axisType) {
      if (axisType == "x") {
        return "xaxis";
      } else {
        return "yaxis";
      }
    },
    getFullAxisName(axisType, tpIndex) {
      if (tpIndex == 0) {
        return axisType + "axis" + "";
      } else {
        return axisType + "axis" + (parseInt(tpIndex) + 1);
      }
    },
    getAxisNumber(tpIndex) {
      if (tpIndex == 0) {
        return "";
      } else return tpIndex + 1;
    },
    getFontFormat(featureName, axisType, tpIndex) {
      let axisInfo = {
        automargin: true,
        title: {
          //
          text: featureName,
          // standoff: 20,
          font: {
            size: 14,
            color: "#7f7f7f"
          }
        }
      };
      return axisInfo;
    },
    changeAxis(selectedAxis, axisType, tpIndex, featureName, overlayModel) {
      let axis = this.getAxisName(axisType);
      this.data[tpIndex][axis] = selectedAxis;
      // update를 하면 data가 유실되어서 wrap해서 다시 넣어주어야 하는데, 변경하는 axis의 값만 넣어줘야 한다. ex) changeAxis의 axisType이 y라면 y의 값만 wrap해서 다시 넣어준다.
      // 안그러면 trace가 사라진다
      let axisTypes = ["x", "y"];
      axisTypes.forEach(axis => {
        if (this.data[tpIndex][axis] != undefined) {
          this.data[tpIndex][axis] = [this.data[tpIndex][axis]];
        }
      });

      let fullAxis = this.getFullAxisName(axisType, tpIndex);
      // this.layout[axisNum] = this.getFontFormat(featureName, axisType, tpIndex);
      // change overlay (overlay가 none이면 changeaxis할때도 반영해준다)
      console.log("axisType");
      console.log(axisType);
      console.log("overlayModel");
      console.log(overlayModel);

      this.layout[fullAxis]["overlaying"] = axisType;
      // this.changeOverlay(overlayModel, tpIndex);
      Plotly.update(this.plotContainer, this.data[tpIndex], this.layout, tpIndex);
    },
    changeGridInfo(rows, columns) {
      // grid: { rows: 2, columns: 2, pattern: "independent" },

      this.layout["grid"] = {};
      this.layout["grid"]["rows"] = rows;
      this.layout["grid"]["columns"] = columns;
      this.layout["grid"]["pattern"] = "independent";
      Plotly.relayout(this.plotContainer, this.layout);
    },
    changeOverlay(overlayModel, tpIndex) {
      console.log(overlayModel);
      let xaxis = "xaxis" + (parseInt(tpIndex) + 1);
      let yaxis = "yaxis" + (parseInt(tpIndex) + 1);
      // undefined일 때만 initialize (안그러면 getfontformat에서 세팅한 layout를 초기화해버리게됨)
      if (this.layout[xaxis] == undefined) {
        this.layout[xaxis] = {};
      }
      if (this.layout[yaxis] == undefined) {
        this.layout[yaxis] = {};
      }
      if (overlayModel == "Data 1") {
        this.layout[xaxis]["overlaying"] = "x";
        this.layout[yaxis]["overlaying"] = "y";
      } else if (overlayModel == "None") {
        Vue.delete(this.layout[xaxis], "overlaying");
        Vue.delete(this.layout[yaxis], "overlaying");
      } else {
        let axisIndex = overlayModel.substring(5);
        this.layout[xaxis]["overlaying"] = "x" + axisIndex;
        this.layout[yaxis]["overlaying"] = "y" + axisIndex;
      }
      Plotly.relayout(this.plotContainer, this.layout);
    },
    removeData(axisType, tpIndex) {
      console.log(axisType);
      console.log(tpIndex);
      // Delete Data
      Vue.delete(this.data[tpIndex], axisType);
      // 반대쪽 데이터는 사라지지 않도록 다시 넣어줌
      let oppositeAxis = this.getOppositeAxis(axisType);
      if (this.data[tpIndex][oppositeAxis] != undefined) {
        this.data[tpIndex][oppositeAxis] = [this.data[tpIndex][oppositeAxis]];
      }
      // Delete Name
      let axisName = this.getFullAxisName(axisType, tpIndex); //xaxis,xaxis2
      console.log(axisName);
      Vue.delete(this.layout, axisName);

      // Plotly.restyle(this.plotContainer, this.data[tpIndex], tpIndex);
      Plotly.update(this.plotContainer, this.data[tpIndex], this.layout, tpIndex);
    },
    changeGraphType(payload) {
      console.log(payload);
      let update;
      switch (payload.graphType) {
        case "scatter":
          update = {
            type: "scattergl",
            mode: "markers"
          };

          break;
        case "line":
          update = {
            type: "scattergl",
            mode: ""
          };
          break;
        case "bar":
          update = {
            type: "bar",
            mode: ""
          };
          break;
        case "histogram":
          update = {
            type: "histogram",
            histnorm: "count",
            mode: ""
          };
          break;
        default:
          return;
      }
      console.log(this.data[payload.tpIndex]);
      // Plotly.restyle(this.plotContainer, this.data[payload.tpIndex], payload.tpIndex);
      Plotly.restyle(this.plotContainer, update, payload.tpIndex);
    }
  },
  created() {
    eventBus.$on("resetAll", payload => {
      this.createPlot();
    });
    eventBus.$on("graphUpdate", payload => {
      Plotly.update(this.plotContainer, this.data, this.layout);
    });
    eventBus.$on("graphRelayout", payload => {
      console.log("relayout");
      Plotly.relayout(this.plotContainer, this.layout);
    });
    eventBus.$on("loadAxis", payload => {
      this.showProgressBar(true);

      this.loadFullData(payload.gridID, payload.featureName, payload.axisType, payload.tpIndex);
    });
    eventBus.$on("changeAxis", payload => {
      console.log(payload);
      this.changeAxis(
        payload.selectedAxis,
        payload.axisType,
        payload.tpIndex,
        payload.featureName,
        payload.overlayModel
      );
    });
    eventBus.$on("changeGridInfo", grid => {
      this.changeGridInfo(grid.rows, grid.columns);
    });
    eventBus.$on("changeOverlay", payload => {
      this.changeOverlay(payload.value, payload.tpIndex);
    });
    eventBus.$on("removeData", payload => {
      this.removeData(payload.axisType, payload.tpIndex);
    });
    eventBus.$on("addEmptyTrace", status => {
      this.addNewTrace();
    });
    eventBus.$on("deleteTrace", tpIndex => {
      this.deleteTrace(tpIndex);
    });
    eventBus.$on("applyGroupBy", payload => {
      let groupLength = Object.keys(payload.data).length;
      if (payload.groupby == "x") {
        this.changeGridInfo(1, groupLength);
      } else {
        this.changeGridInfo(groupLength, 1);
      }
      this.renderGroupingGraph(payload.data);
      console.log(payload.data);
    });
    eventBus.$on("changeGraphType", payload => {
      this.changeGraphType(payload);
    });
  },
  mounted() {
    (this.config["modeBarButtonsToAdd"] = [
      {
        name: "Edit in Graph Studio",
        icon: Plotly.Icons.pencil,
        click: () => {
          this.openEditModal(this.seriesName);
        }
      }
    ]),
      (this.config["modeBarButtonsToRemove"] = ["Delete Selected Data"]);

    this.createPlot();
  }
};
</script>
<style scoped></style>
