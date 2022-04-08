<template>
  <v-navigation-drawer v-model="drawer" width="100%">
    <v-tabs v-model="tab" centered>
      <v-tab>Build</v-tab>
      <v-tab>Settings</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-list>
          <!-- Algorithm Nodes-->
          <v-list-group :value="true">
            <template v-slot:activator>
              <v-list-item-title class="py-5">Algorithm</v-list-item-title>
            </template>

            <v-sheet
              v-for="(algorithmType, algorithmTypeIndex) in algorithmTypes"
              :key="algorithmTypeIndex"
              class="mb-5 "
            >
              <v-card-text class="subheading font-weight-bold py-0">
                <v-icon left>mdi-circle-small</v-icon>{{ algorithmType }}</v-card-text
              >
              <v-chip-group class="ml-10">
                <v-chip
                  class="ml-1"
                  v-for="(algorithm, algorithmIndex) in algorithms[algorithmType]"
                  :key="algorithmIndex"
                  @click="sendNodeInfo(algorithm, nodeType[0])"
                  >{{ algorithm }}</v-chip
                >
              </v-chip-group>
            </v-sheet>
          </v-list-group>
          <!-- Feature Nodes-->
          <v-list-group :value="true">
            <template v-slot:activator>
              <v-list-item-title class="py-5">Feature</v-list-item-title>
            </template>

            <v-sheet class="mb-5 ">
              <v-chip-group class="ml-10">
                <v-chip
                  class="ml-1"
                  v-for="(feature, featureIndex) in features"
                  :key="featureIndex"
                  @click="sendNodeInfo(feature, nodeType[1])"
                  >{{ feature }}</v-chip
                >
              </v-chip-group>
            </v-sheet>
          </v-list-group>
          <!-- scaler -->
        </v-list>
      </v-tab-item>
    </v-tabs-items>
  </v-navigation-drawer>
</template>
<script>
import { mapState, mapGetters, mapMutations } from "vuex";
import { eventBus } from "@/main";
// import draggable from "vuedraggable";
export default {
  data() {
    return {
      tab: null,
      drawer: true,
      mini: true,
      nodeType: ["algorithm", "feature"],
      features: ["Input", "Target"],
      algorithms: {
        Regression: ["XGBoost", "SVR"],
        Classification: ["Random Forest"],
        Clustering: []
      },
      algorithmTypes: ["Regression", "Classification", "Clustering"],
      blocks: ["Input", "Target"]
    };
  },
  methods: {
    ...mapMutations("modelingData", ["saveAlgorithm"]),
    sendNodeInfo(node, nodeType) {
      if (nodeType == "algorithm") {
        this.saveAlgorithm(node);
      }
      let nodeInfo = { node: node, nodeType: nodeType };
      eventBus.$emit("sendNodeInfo", nodeInfo);
    }
  },
  components: {
    // draggable
  }
};
</script>
