<template>
  <v-stepper v-model="stepper" vertical non-linear>
    <!-- step 1 (Title) -->
    <v-stepper-step editable step="1">
      Time Series 조건 설정
    </v-stepper-step>
    <!-- step 1 (Contents) -->
    <v-stepper-content step="1">
      <TsCondition />
      <v-btn color="primary" @click="stepper = 2">
        Continue
      </v-btn>
      <v-btn text @click="deleteRow">
        Delete
      </v-btn>
    </v-stepper-content>
    <!-- step 2 (Title) -->
    <v-stepper-step editable :complete="stepper > 2" step="2">
      Feature 조건 설정
    </v-stepper-step>
    <!-- step 2 (Contents) -->
    <v-stepper-content step="2">
      <FeatureCondition>
        <!-- chip group -->
        <v-chip-group>
          <v-chip
            v-for="(featureCondition, IndexFeatureCondition) in featureConditions"
            :key="IndexFeatureCondition"
            small
            outlined
          >
            {{ featureCondition }}
          </v-chip>
        </v-chip-group>
      </FeatureCondition>
      <v-btn color="primary" @click="stepper = 3">
        Continue
      </v-btn>
      <v-btn text @click="deleteRow">
        Delete
      </v-btn>
    </v-stepper-content>
  </v-stepper>
</template>
<script>
import TsCondition from "@/components/delete/TsCondition.vue";
import ColumnList from "@/components/delete/ColumnList.vue";
import FeatureCondition from "@/components/delete/FeatureCondition.vue";
import axios from "axios";
//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
// eventBus
import { eventBus } from "@/main";
export default {
  data() {
    return {
      stepper: 1,
      tsCondition_from: null,
      featureConditions: []
    };
  },
  computed: {},
  methods: {
    clickSkipEvent(step) {
      if (step == 1) {
        this.stepper = 2;
        eventBus.$emit("stepOneSkipEvent", true);
      } else {
        this.stepper = 1;
        eventBus.$emit("stepTwoSkipEvent", true);
      }
    },
    addCondition() {
      eventBus.$emit("addCondition", true); // -> Condition
    },
    deleteRow() {
      // date mode 일 때
      const path = "http://localhost:5000/deleteRow";
      axios
        .get(path, {
          params: {
            timeSeriesCondition: this.tsCondition_from,
            featureConditions: this.featureConditions
          }
        })
        .then(res => {
          console.log(this.tsCondition_from);
        })
        .catch(error => {
          console.error(error);
        });

      // eventBus.$emit("reloadInfiniteTable", true);
      // this.resetValues();
    }
  },
  computed: {
    ...mapState({
      columns: state => state.initialData.columns
      // columns: state => state.columns
    })
  },

  components: { TsCondition, ColumnList, FeatureCondition },
  created() {
    eventBus.$on("tsCondition_from", tsCondition_from => {
      this.tsCondition_from = tsCondition_from;
    });
    eventBus.$on("featureConditions", featureConditions => {
      this.featureConditions.push(featureConditions);
    });
  }
};
</script>
