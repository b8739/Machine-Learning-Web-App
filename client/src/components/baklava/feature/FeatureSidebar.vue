<template>
  <div>
    <v-card dark rounded color="#3f3f3f" elevation="0">
      <v-container>
        <v-checkbox
          v-for="(feature, index) in value.features"
          :key="index"
          dense
          :label="feature"
        ></v-checkbox>
      </v-container>
    </v-card>
  </div>
</template>
<script>
import { ButtonOption } from "@baklavajs/plugin-options-vue";
import { InputOption } from "@baklavajs/plugin-options-vue";
import { TextOption } from "@baklavajs/plugin-options-vue";
export default {
  props: ["value", "name"],
  components: {
    ButtonOption,
    InputOption
  },
  data() {
    return {
      xTrain: [
        "CRIM",
        "ZN",
        "INDUS",
        "CHAS",
        "NOX",
        "RM",
        "AGE",
        "DIS",
        "RAD",
        "TAX",
        "PTRATIO",
        "B",
        "LSTAT"
      ],
      yTrain: ["MEDV"]
    };
  },
  created() {
    console.log(this.value);
  }
};
</script>
