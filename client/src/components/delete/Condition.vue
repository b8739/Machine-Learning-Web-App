<template>
  <v-row align="center" justify="center">
    <v-col cols="4">
      <!-- textfield (Feature)-->
      <v-text-field
        v-model="featureName"
        :value="featureName"
        placeholder="Feature"
        outlined
        dense
        hide-details
      ></v-text-field
    ></v-col>
    <!-- 부등호 버튼 (menu) -->
    <v-col cols="2">
      <div class="text-center">
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <!-- 부등호 버튼 -->
            <v-btn class="ma-2" outlined fab color="indigo" x-small v-bind="attrs" v-on="on">
              <v-icon>{{ icons[iconIndex] }}</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item v-for="(item, index) in items" :key="index" @click="changeIcon(index)">
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div></v-col
    >
    <!-- textfield (Value) -->
    <v-col cols="4">
      <v-text-field
        :value="featureValue"
        v-model="featureValue"
        placeholder="Enter the Value"
        outlined
        dense
        hide-details
      ></v-text-field>
    </v-col>
  </v-row>
</template>
<script>
import { mapState } from "vuex";
import { eventBus } from "@/main";
export default {
  data() {
    return {
      iconIndex: 0,
      featureName: "",
      featureValue: "",
      conditionArray: [],
      items: [
        { title: "=" },
        { title: "!=" },
        { title: ">" },
        { title: "<" },
        { title: ">=" },
        { title: ">=" }
      ],
      icons: [
        "mdi-equal",
        "mdi-not-equal",
        "mdi-greater-than",
        "mdi-less-than",
        "mdi-greater-than-or-equal",
        "mdi-less-than-or-equal"
      ]
    };
  },
  methods: {
    changeIcon(index) {
      this.iconIndex = index;
      // console.log("d");
    }
  },

  created() {
    eventBus.$on("featureClickedEvent", column => {
      this.featureName = column;
    });
    eventBus.$on("stepTwoSkipEvent", skipStatus => {
      this.iconIndex = 0;
      this.featureName = null;
    });
    eventBus.$on("addCondition", addConditionStatus => {
      this.conditionArray.push(this.fullCondition);
    });
  },
  computed: {
    ...mapState({
      columns: state => state.initialData.columns
      // columns: state => state.columns
    }),
    fullCondition() {
      return this.featureName + " " + this.items[this.iconIndex].title + " " + this.featureValue;
    }
  }
};
</script>
<style scoped>
.condition {
  height: 50%;
}
</style>
