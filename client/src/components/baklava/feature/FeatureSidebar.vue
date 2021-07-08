<template>
  <div>
    <!-- <v-btn @click="getValue">get value</v-btn> -->
    <v-card dark rounded color="#3f3f3f" elevation="0">
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
      checkedFeatures: []
    };
  },
  methods: {
    selectAll() {
      if (this.checkedFeatures.length == this.inputFeatures.length) {
        this.checkedFeatures = [];
      } else {
        for (let i = 0; i < this.inputFeatures.length; i++) {
          this.checkedFeatures.push(this.inputFeatures[i]);
        }
      }
    },
    getValue() {
      console.log(this.node);
      console.log(this.selectedFeatures);
    },
    featureUpdate(feature) {
      // 배열에 없으면 추가
      if (this.selectedFeatures.includes(feature) == false) {
        this.selectedFeatures.push(feature);
      }
      // 배열에 있으면 삭제
      else {
        this.selectedFeatures.splice(this.selectedFeatures.indexOf(feature), 1);
      }
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
