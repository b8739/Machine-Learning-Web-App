<template>
  <div>
    <v-btn @click="getValue">get value</v-btn>
    <v-card dark color="#3f3f3f" class="rounded-0" elevation="0">
      <v-container>
        <v-row> <v-card-text class="pb-0">Standard Scaler</v-card-text></v-row>
        <v-row
          justify="center"
          align="center"
          v-for="(label, checkboxLabelIndex) in checkboxLabel"
          :key="checkboxLabelIndex"
        >
          <v-col cols="4" class="px-0">
            <v-subheader> {{ label }}</v-subheader></v-col
          >
          <v-col cols="4" class="px-0"
            ><v-checkbox
              @change="emitValue()"
              hide-details
              dense
              :label="scaleType[0]"
              v-model="checkboxModel[label][scaleType[0]]"
            ></v-checkbox
          ></v-col>
          <v-col cols="4" class="px-0">
            <v-checkbox
              @change="emitValue()"
              hide-details
              dense
              :label="scaleType[1]"
              v-model="checkboxModel[label][scaleType[1]]"
            ></v-checkbox
          ></v-col>
        </v-row>
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
      checkboxLabel: ["Test X", "Train X", "Valid X"],
      scaleType: ["Fit", "Transform"],
      checkboxModel: {
        "Test X": { Fit: false, Transform: false },
        "Train X": { Fit: false, Transform: false },
        "Valid X": { Fit: false, Transform: false }
      },
      selectAllFlag: false
    };
  },
  methods: {
    getValue() {
      console.log(this.checkboxModel["Test X"]);
    },

    emitValue() {
      this.$emit("input", this.checkboxModel);
    }
  },
  computed: {},
  created() {},
  mounted() {
    // this.inputFeatures = this.value.features;
  }
};
</script>
