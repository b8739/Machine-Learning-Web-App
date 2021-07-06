<template>
  <div>
    <v-btn @click="getValue">get value</v-btn>
    <v-card dark rounded color="#3f3f3f" elevation="0">
      <v-container>
        <v-checkbox
          v-for="(feature, index) in inputFeatures"
          :key="index"
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
      selectedFeatures: []
    };
  },
  methods: {
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
  computed: {
    // selectedFeatures_string() {
    //   let stringConverted;
    //   this.selectedFeatures.forEach(element => {
    //     stringConverted += element;
    //   });
    //   return stringConverted;
    // }
  },
  created() {
    console.log(this.value);
  },
  mounted() {
    this.inputFeatures = this.value.features;
  }
};
</script>
