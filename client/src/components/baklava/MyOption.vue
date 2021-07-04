<template>
  <div></div>
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
      xgboost_props: [
        "n_estimators",
        "learning_rate",
        "gamma",
        "eta",
        "subsample",
        "colsample_bytree",
        "max_depth"
      ],
      svr_props: ["kernel", "C", "epsilon", "gamma"],
      randomForest_props: ["n_estimators", "min_samples_split"],
      // options
      selectedProps: [500, 0.08, 0.3, 0.04, 0.75, 0.5, 7],
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
