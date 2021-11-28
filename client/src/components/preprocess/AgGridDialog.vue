<template>
  <v-dialog v-model="dialog" @click:outside="closeDialog" width="600">
    <v-card class="pa-4">
      <v-container>
        <slot name="insideContainer"></slot>
        <slot
          name="insideContainer_type"
          :dataTypes="dataTypes"
          :dataTypeModel="dataTypeModel"
        ></slot>
        <slot name="insideContainer_na" :fillNaModel="fillNaModel"></slot>
      </v-container>
      <v-card-actions>
        <slot name="changeNameAction" :updateColumnName="updateColumnName"> </slot>
        <slot name="changeTypeAction" :updateDataType="updateDataType"> </slot>
        <slot name="changeOrderAction"> </slot>
        <slot name="deleteColumnAction" :hideColumn="hideColumn"> </slot>
        <slot name="fillNaAction" :applyFillNa="applyFillNa"> </slot>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import { mapState, mapGetters, mapMutations, mapActions } from "vuex";
import axios from "axios";

export default {
  props: ["dialog", "dialogName", "gridColumns", "selectedColumns", "dataTypes"],
  data() {
    return {
      sampleDataTypes: ["float", "int", "double"],
      dataTypeItems: ["double", "string", "bool", "date", "int", "long", "decimal"],
      dataTypeModel: [],
      fillNaModel: {}
    };
  },

  computed: {
    ...mapState({
      // gridapi
      projectName: state => state.initialData.projectName,
      gridApi: state => state.aggrid.gridApi,
      gridColumnApi: state => state.aggrid.gridColumnApi,
      currentGrid: state => state.aggrid.currentGrid,

      //loadSetting
      columnsForGrid: state => state.aggrid.columnsForGrid,
      columnModel: state => state.aggrid.columnModel,
      datasetToLoad: state => state.aggrid.datasetToLoad
    })
  },

  methods: {
    ...mapMutations("aggrid", ["setRenameModel"]),
    ...mapMutations("aggrid", ["setTypeModel"]),
    ...mapMutations("aggrid", ["setFillNaModel"]),
    ...mapMutations("aggrid", ["delColumnModelElement"]),
    getFinalDataTypeModel() {
      let vm = this;
      let finalResult = this.dataTypeModel.reduce(function(result, value, index) {
        if (value != null || value != undefined) {
          let key = vm.columnModel[vm.currentGrid][vm.datasetToLoad[vm.currentGrid]][index];
          let resultValue = {};

          resultValue[key] = { $convert: { input: "$" + key, to: value } };
          result.push(resultValue);
        }
        return result;
      }, []);
      console.log(finalResult);
      return finalResult;
    },
    // getFinalFillNaModel() {
    //   let vm = this;
    //   let finalResult = this.fillNaModel.reduce(function(result, value, index) {
    //     if (value != null || value != undefined) {
    //       let key = vm.columnModel[vm.currentGrid][vm.datasetToLoad[vm.currentGrid]][index];
    //       let resultValue = {};

    //       resultValue[key] = { $ifNull: ["$" + key, value] };
    //       result.push(resultValue);
    //     }
    //     return result;
    //   }, []);
    //   console.log(finalResult);
    //   return finalResult;
    // },
    getFinalFillNaModel() {
      let vm = this;
      let finalResult = this.fillNaModel.reduce(function(result, value, index) {
        if (value != null || value != undefined) {
          let key = vm.columnModel[vm.currentGrid][vm.datasetToLoad[vm.currentGrid]][index];
          let resultValue = {};

          resultValue[key] = value;
          result.push(resultValue);
        }
        return result;
      }, []);
      console.log(finalResult);
      return finalResult;
    },
    applyFillNa() {
      // let finalNaModel = this.getFinalFillNaModel();
      this.setFillNaModel(this.fillNaModel);
      this.closeDialog();
      this.gridApi[this.currentGrid].refreshInfiniteCache();
    },
    updateDataType() {
      let finalDataTypeModel = this.getFinalDataTypeModel();
      this.setTypeModel(finalDataTypeModel);
      this.closeDialog();
      this.gridApi[this.currentGrid].refreshInfiniteCache();
    },
    closeDialog() {
      this.$emit("update:dialog", false);
    },
    // change Column Name
    updateColumnName() {
      const columnDefs = this.gridApi[this.currentGrid].getColumnDefs();

      // Server side
      let serverSideRenameModel = this.gridColumns.reduce(function(result, renamedColumn, index) {
        if (renamedColumn != undefined) {
          result.push({ from: columnDefs[index].colId, to: renamedColumn });
        }
        return result;
      }, []);

      this.setRenameModel(serverSideRenameModel);
      // Client side

      this.gridColumns.forEach((renamedColumn, index) => {
        if (renamedColumn != null || renamedColumn != undefined) {
          columnDefs[index].headerName = renamedColumn;
        }
      });
      this.gridApi[this.currentGrid].setColumnDefs(columnDefs);

      // 초기화
      this.gridColumns.splice(0);
      //닫기
      this.closeDialog();
    },
    hideColumn() {
      //방법 1) columnExclude에 추가
      Object.keys(this.selectedColumns).forEach(datasetName => {
        // columnModel에서 삭제함으로써 reset되었을 때 불러오지도 않고, mount되면 columnDef에서도 삭제됨
        this.selectedColumns[datasetName].forEach(element => {
          let index = this.columnModel[this.currentGrid][datasetName].indexOf(element);
          let payload = { datasetName: datasetName, index: index };
          this.delColumnModelElement(payload);
          // mounted되면 계산되어서 columnDef에서도 삭제되지만, 그전에는 계산이 안되므로 일단 hide
          this.gridColumnApi[this.currentGrid].applyColumnState({
            state: [{ colId: element, hide: true }]
          });
        });
      });

      this.closeDialog();

      this.selectedColumns = {};
      this.gridApi[this.currentGrid].refreshInfiniteCache();
    }
  }
};
</script>
