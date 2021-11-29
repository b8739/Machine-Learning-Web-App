<template>
  <div>
    <v-card dark color="#3f3f3f" class="rounded-0" elevation="0">
      <v-container>
        <!-- <v-btn @click="getValue">get value</v-btn> -->

        <v-checkbox label="Select All" @change="selectAll"></v-checkbox>
        <v-checkbox
          v-if="columnModel[gridValue][datasetToLoad[gridValue]] != undefined"
          v-for="(feature, index) in columnModel[gridValue][datasetToLoad[gridValue]]"
          :key="index"
          v-model="checkedFeatures[index]"
          dense
          :label="feature"
          @change="featureUpdate(feature)"
        ></v-checkbox>
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
      gridValue: 0
    };
  },

  methods: {
    selectAll() {
      // flag가 true일 때 (이미 selectall이 된 상태) 체크 해제
      this.selectedFeatures = [];
      this.checkedFeatures = [];
      // flag가 false일 때 (select all이 해제된 상태) 전부 체크
      if (this.selectAllFlag == false) {
        for (
          let i = 0;
          i < this.columnModel[this.gridValue][this.datasetToLoad[this.gridValue]].length;
          i++
        ) {
          this.selectedFeatures.push(
            this.columnModel[this.gridValue][this.datasetToLoad[this.gridValue]][i]
          );
          this.checkedFeatures.push(true);
        }
      }
      // 값 송출
      this.emitValue();
      this.selectAllFlag = !this.selectAllFlag;
    },
    getValue() {
      console.log(this.gridValue);
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
      datasetToLoad: state => state.aggrid.datasetToLoad
    })
  },
  created() {
    eventBus.$on("gridChange", newGridValue => {
      this.gridValue = newGridValue;
    });
  },
  mounted() {
    //  다른 sidebar를 켰다가 다시 열면 값이 초기화되기 때문에, value값을 받아와서 다시 check 해줌
    console.log(`${this.node.name} mounted`);
    this.node.getOptionValue("Features").forEach(nodeValue => {
      this.columnModel[this.gridValue][this.datasetToLoad[this.gridValue]].forEach(
        (column, index) => {
          if (nodeValue == column) {
            Vue.set(this.selectedFeatures, index, nodeValue);
            Vue.set(this.checkedFeatures, index, true);
          }
        }
      );
    });
  }
};
</script>
