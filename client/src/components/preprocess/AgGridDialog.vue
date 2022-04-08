<template>
  <v-dialog v-model="dialog" @click:outside="closeDialog" width="600">
    <v-card class="pa-4">
      <v-container>
        <v-row justify="end">
          <v-btn small @click="closeDialog()" elevation="0" color="white">
            <v-icon>mdi-close</v-icon></v-btn
          >
        </v-row>
        <slot name="default"></slot>
        <slot
          name="deleteColumn"
          :saveSelectedColumns="saveSelectedColumns"
          :select="select"
        ></slot>
        <slot name="changeType" :dataTypes="dataTypes" :dataTypeModel="dataTypeModel"></slot>
        <slot name="fillNA" :fillNaModel="fillNaModel"></slot>
        <slot name="deleteNA" :deleteNaModel="deleteNaModel"></slot>
      </v-container>
      <v-card-actions>
        <slot name="changeName_action" :updateColumnName="updateColumnName"> </slot>
        <slot name="changeType_action" :updateDataType="updateDataType"> </slot>
        <slot name="changeOrder_action"> </slot>
        <slot name="deleteColumn_action" :dropColumn="dropColumn"> </slot>
        <slot name="fillNa-action" :applyFillNa="applyFillNa"> </slot>
        <slot name="deleteNa_action" :applyDeleteNa="applyDeleteNa"> </slot>
        <slot name="mergeTable_action"> </slot>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import { mapState, mapGetters, mapMutations, mapActions } from "vuex";
import axios from "axios";

export default {
  props: ["dialog", "dialogName", "gridColumns", "dataTypes"],
  data() {
    return this.getDefaultState();
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
    }),
    ...mapGetters("aggrid", ["currentDataset"])
  },

  methods: {
    getDefaultState() {
      return {
        sampleDataTypes: ["float", "int", "double"],
        dataTypeItems: ["double", "string", "bool", "date", "int", "long", "decimal"],
        dataTypeModel: [],
        fillNaModel: {},
        deleteNaModel: {},
        selectedColumns: [],
        select: 0
      };
    },
    ...mapMutations("aggrid", ["setRenameModel"]),
    ...mapMutations("aggrid", ["setTypeModel"]),
    ...mapMutations("aggrid", ["setFillNaModel"]),
    ...mapMutations("aggrid", ["setDeleteNaModel"]),
    ...mapMutations("aggrid", ["delColumnModelElement"]),

    saveSelectedColumns(value) {
      this.selectedColumns = value;
      console.log(this.selectedColumns);
    },
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
    applyDeleteNa() {
      this.setDeleteNaModel(this.deleteNaModel);
      this.closeDialog();
      this.gridApi[this.currentGrid].refreshInfiniteCache();
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
      Object.assign(this.$data, this.getDefaultState());

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
    dropColumn() {
      var confirmflag = confirm("선택한 컬럼을 데이터 테이블에서 삭제하시겠습니까?");
      // 삭제하는 경우
      if (confirmflag) {
        this.selectedColumns.forEach(col => {
          let index = this.columnModel[this.currentGrid][this.currentDataset].indexOf(col);
          let payload = { datasetName: this.currentDataset, index: index };
          this.delColumnModelElement(payload); // Vuex columnModel상에서 삭제
          this.gridColumnApi[this.currentGrid].applyColumnState({
            state: [{ colId: col, hide: true }]
          });
        });

        this.closeDialog();
        this.select = 0;
        this.gridApi[this.currentGrid].refreshInfiniteCache();
      }
    }
  }
};
</script>
