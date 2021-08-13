<template>
  <v-dialog v-model="dialog" persistent max-width="800px">
    <!-- chip group -->
    <v-chip-group>
      <v-chip
        v-for="(featureCondition, IndexFeatureCondition) in featureConditions"
        :key="IndexFeatureCondition"
        close
        @click:close="featureConditions.splice(IndexFeatureCondition, 1)"
        small
        outlined
      >
        {{ featureCondition }}
      </v-chip>
      <v-chip
        v-if="tsCondition_from != null"
        close
        @click:close="tsCondition_from = null"
        small
        outlined
      >
        {{ tsCondition_from }}
      </v-chip>
    </v-chip-group>

    <v-stepper v-model="stepper" vertical non-linear>
      <v-stepper-header>
        <v-card-title>Delete Row by Condition</v-card-title> <v-spacer></v-spacer
        ><v-btn x-small min-width="20" min-height="30" @click="closeStepper"
          ><v-icon small>mdi-close</v-icon>
        </v-btn></v-stepper-header
      >
      <!-- step 1 (Title) -->
      <v-stepper-step editable step="1">
        Time Series 조건 설정
      </v-stepper-step>
      <!-- step 1 (Contents) -->
      <v-stepper-content step="1">
        <TimeCondition />
        <v-btn color="primary" @click="stepper = 2">
          Continue
        </v-btn>
      </v-stepper-content>
      <!-- step 2 (Title) -->
      <v-stepper-step editable :complete="stepper > 2" step="2">
        Feature 조건 설정
      </v-stepper-step>
      <!-- step 2 (Contents) -->
      <v-stepper-content step="2">
        <FeatureCondition> </FeatureCondition>
        <v-btn color="primary" @click="stepper = 3">
          Continue
        </v-btn>
      </v-stepper-content>
    </v-stepper>
    <v-spacer></v-spacer>
    <v-btn v-bind="dynamicDeleteButtonProps" color="error darken-1" @click="deleteRow">
      Delete
    </v-btn>
  </v-dialog>
</template>
<script>
import TimeCondition from "@/components/delete/TimeCondition.vue";
import FeatureCondition from "@/components/delete/FeatureCondition.vue";
import axios from "axios";
//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
// eventBus
import { eventBus } from "@/main";
export default {
  data() {
    return {
      dialog: false,
      stepper: 1,
      tsCondition_from: null,
      featureConditions: [],
      deleteButtonProps: {
        disabled: true
      }
    };
  },
  computed: {
    ...mapGetters({
      columns: state => state.initialData.columns
    }),
    dynamicDeleteButtonProps() {
      if (this.tsCondition_from != null || this.featureConditions.length != 0) {
        this.deleteButtonProps.disabled = false;
      } else this.deleteButtonProps.disabled = true;
      return this.deleteButtonProps;
    }
  },
  methods: {
    closeStepper() {
      this.dialog = false;
    },
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
      const path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/deleteRow";
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

  components: { TimeCondition, FeatureCondition },
  created() {
    eventBus.$on("openDeleteRowModal", modalStatus => {
      this.dialog = modalStatus;
    });
    eventBus.$on("tsCondition_from", tsCondition_from => {
      this.tsCondition_from = tsCondition_from;
    });
    eventBus.$on("featureConditions", featureConditions => {
      this.featureConditions.push(featureConditions);
    });
  }
};
</script>
