<template>
  <div>
    <!-- <v-btn @click="getValue">get value</v-btn> -->
    <v-card dark color="#3f3f3f" class="rounded-0" elevation="0">
      <v-container>
        <v-checkbox label="Select All" @change="selectAll"></v-checkbox>
        <v-checkbox
          v-for="(feature, index) in inputFeatures"
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
import { ButtonOption } from "@baklavajs/plugin-options-vue";
import { InputOption } from "@baklavajs/plugin-options-vue";
import { CheckboxOption } from "@baklavajs/plugin-options-vue";
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
      selectAllFlag: false
    };
  },
  methods: {
    selectAll() {
      // flag가 true일 때 (이미 selectall이 된 상태) 체크 해제
      this.selectedFeatures = [];
      this.checkedFeatures = [];
      // flag가 false일 때 (select all이 해제된 상태) 전부 체크
      if (this.selectAllFlag == false) {
        for (let i = 0; i < this.inputFeatures.length; i++) {
          this.selectedFeatures.push(this.inputFeatures[i]);
          this.checkedFeatures.push(true);
        }
      }
      // 값 송출
      this.emitValue();
      this.selectAllFlag = !this.selectAllFlag;
    },
    getValue() {
      console.log(this.value.features);
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
  computed: {},
  created() {},
  mounted() {
    this.inputFeatures = this.value.features;
  }
};
</script>
