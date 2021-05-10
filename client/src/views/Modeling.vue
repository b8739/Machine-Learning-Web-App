<template>
  <v-container fluid>
    <v-row>
      <v-col cols="2"> <ModelingSide /></v-col>
      <v-col cols="10">
        <v-card min-height="800px" elevation="1">
          <v-toolbar elevation="1" dense>
            <v-spacer></v-spacer
            ><v-btn><v-icon left small>mdi-play-outline</v-icon> Run</v-btn></v-toolbar
          >
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import { eventBus } from "@/main";
import ModelingSide from "@/components/modeling/ModelingSide.vue";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  data() {
    return {
      inputs: [],
      targets: []
    };
  },
  components: {
    ModelingSide
  },
  computed: {
    ...mapState({
      inputs: state => state.modelingData.inputs
    })
  },
  created() {
    eventBus.$on("inputFeatures", inputFeatures => {
      this.inputFeatures = inputFeatures;
    });
    eventBus.$on("targetFeatures", targetFeatures => {
      this.targetFeatures = targetFeatures;
    });
  }
};
</script>
