<template>
  <div>
    <v-card dark color="#3f3f3f" class="rounded-0" elevation="0">
      <v-container>
        <!-- <v-btn @click="getValue">get value</v-btn> -->
        <!-- <v-btn @click="test">Test</v-btn> -->
        <v-subheader>Select DataTable First</v-subheader>

        <div v-if="modelingDataset != null">
          <v-checkbox label="Select All" @change="selectAll"></v-checkbox>
          <v-checkbox
            v-for="(feature, index) in features"
            :key="index"
            v-model="checkedFeatures[index]"
            dense
            :label="feature"
            @change="featureUpdate(feature)"
          ></v-checkbox>
        </div>
      </v-container>
    </v-card>
  </div>
</template>
<script>
import Vue from "vue";
import { eventBus } from "@/main";

import { ButtonOption } from "@baklavajs/plugin-options-vue";
import { InputOption } from "@baklavajs/plugin-options-vue";
import { CheckboxOption } from "@baklavajs/plugin-options-vue";
import { mapState, mapGetters } from "vuex";
export default {
  extends: InputOption,
  props: ["node"],

  components: {
    ButtonOption,
    InputOption,
    CheckboxOption
  },
  data() {
    return {
      inputFeatures: null,
      selectedFeatures: [],
      checkedFeatures: [],
      selectAllFlag: false,
      gridValue: null
    };
  },

  methods: {
    test() {
      this.renameModel[this.modelingDataset].forEach(element => {
        console.log(element["from"]);
        // columns[element["from"]] = element["to"];
      });
    },
    selectAll() {
      // flag가 true일 때 (이미 selectall이 된 상태) 체크 해제
      this.selectedFeatures = [];
      this.checkedFeatures = [];
      // flag가 false일 때 (select all이 해제된 상태) 전부 체크
      if (this.selectAllFlag == false) {
        for (
          let i = 0;
          i <
          this.columnModel[this.modelingDataset][this.datasetToLoad[this.modelingDataset]].length;
          i++
        ) {
          this.selectedFeatures.push(
            this.columnModel[this.modelingDataset][this.datasetToLoad[this.modelingDataset]][i]
          );
          this.checkedFeatures.push(true);
        }
      }
      // 값 송출
      this.emitValue();
      this.selectAllFlag = !this.selectAllFlag;
    },
    getValue() {
      console.log(this.modelingDataset);
    },
    featureUpdate(feature) {
      // 배열에 없으면 추가
      console.log("featureupdate");
      if (this.selectedFeatures.includes(feature) == false) {
        this.selectedFeatures.push(feature);
      }
      // 배열에 있으면 삭제
      else {
        this.selectedFeatures.splice(this.selectedFeatures.indexOf(feature), 1);
      }
      this.$emit("input", this.selectedFeatures);
    },
    emitValue() {
      this.$emit("input", this.selectedFeatures);
    }
  },
  computed: {
    ...mapState({
      columnModel: state => state.aggrid.columnModel,
      datasetToLoad: state => state.aggrid.datasetToLoad,
      renameModel: state => state.aggrid.renameModel,
      modelingDataset: state => state.modelingData.modelingDataset
    }),
    features() {
      if (this.modelingDataset == null) {
        return null;
      } else {
        let columns = this.columnModel[this.modelingDataset][
          this.datasetToLoad[this.modelingDataset]
        ];
        if (this.renameModel[this.modelingDataset] != undefined) {
          this.renameModel[this.modelingDataset].forEach(element => {
            let index = columns.indexOf(element["from"]);
            Vue.set(columns, index, element["to"]);
          });
        }

        console.log(columns);
        return columns;
      }
    }
  },
  created() {
    eventBus.$on("gridChange", newGridValue => {
      this.gridValue = newGridValue;
    });
  },
  mounted() {
    //  다른 sidebar를 켰다가 다시 열면 값이 초기화되기 때문에, value값을 받아와서 다시 check 해줌
    // this.node.getOptionValue("Features")['features]로 하면 안되는데 이유를 모르겠음
    if (this.modelingDataset != null) {
      this.node.getOptionValue("Features").forEach(nodeValue => {
        this.columnModel[this.modelingDataset][this.datasetToLoad[this.modelingDataset]].forEach(
          (column, index) => {
            if (nodeValue == column) {
              Vue.set(this.selectedFeatures, index, nodeValue);
              Vue.set(this.checkedFeatures, index, true);
            }
          }
        );
      });
    }
  }
};
</script>
