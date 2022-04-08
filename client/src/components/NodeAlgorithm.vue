<template>
  <v-container>
    <v-row justify="center">
      <v-card-text class="subheading pa-0">{{ name }}</v-card-text>
    </v-row>
    <v-row justify="center" v-if="hasParameter">
      <v-btn outlined x-small @click="parameterVisible = !parameterVisible">Parameters</v-btn>
    </v-row>
    <v-row>
      <v-card
        v-show="parameterVisible"
        class="vcard"
        rounded
        elevation="0"
        min-height="50px"
        max-width="220px"
      >
        <v-container>
          <v-row justify="center" v-for="(prop, index) in xgboost_props" :key="index">
            <v-col class="px-0" cols="3"
              ><v-subheader class="px-0">{{ prop }}</v-subheader></v-col
            >
            <v-col
              ><v-text-field
                persist-placehorder
                hide-details
                dense
                v-model="selectedProps[index]"
              ></v-text-field
            ></v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: ["name", "hasParameter"],

  data() {
    return {
      parameterVisible: false,

      xgboost_props: [
        "n_estimators",
        "learning_rate",
        "gamma",
        "eta",
        "subsample",
        "colsample_bytree",
        "max_depth"
      ],
      num: 0,
      selectedProps: [500, 0.08, 0.3, 0.04, 0.75, 0.5, 7]
    };
  },
  methods: {
    Clicked() {
      console.log(this.xgboost_props);
    }
  },
  created() {}
};
</script>
<style scoped>
.subheading {
  text-align: center;
}
</style>
