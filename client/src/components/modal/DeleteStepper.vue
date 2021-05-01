<template>
  <v-stepper v-model="stepper" vertical non-linear>
    <v-stepper-step editable step="1">
      Time Series 조건 설정
      <!-- <small>Summarize if needed</small> -->
    </v-stepper-step>

    <v-stepper-content step="1">
      <DeleteRowModal2 />
      <v-btn color="primary" @click="stepper = 2">
        Continue
      </v-btn>
      <v-btn text @click="clickSkipEvent(1)">
        Skip
      </v-btn>
    </v-stepper-content>

    <v-stepper-step editable :complete="stepper > 2" step="2">
      Feature 조건 설정
    </v-stepper-step>

    <v-stepper-content step="2">
      <v-card color="rgb(245,245,245) " class="mb-12">
        <v-container>
          <!-- 상단 (타이틀)-->
          <v-row>
            <v-subheader>{{ columns.length }} 개 열</v-subheader>
          </v-row>
          <!-- 하단 (컨텐츠) -->
          <v-row align="center">
            <!-- 좌측 -->
            <v-col cols="3">
              <ColumnList :style="style_columnList"> </ColumnList>
            </v-col>
            <!-- 우측 -->
            <v-col cols="9" justify="center">
              <Condition />

              <v-spacer></v-spacer>
            </v-col>
          </v-row>
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="addCondition">
            Add Condition
          </v-btn>
          <v-btn color="red darken-1" text>
            Reset
          </v-btn>
        </v-card-actions>
      </v-card>
      <v-btn color="primary" @click="stepper = 3">
        Continue
      </v-btn>
      <v-btn text @click="clickSkipEvent(2)">
        Skip
      </v-btn>
    </v-stepper-content>
  </v-stepper>
</template>
<script>
import DeleteRowModal2 from "@/components/modal/DeleteRowModal2.vue";
import ColumnList from "@/components/delete/ColumnList.vue";
import Condition from "@/components/delete/Condition.vue";
//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
// eventBus
import { eventBus } from "@/main";
export default {
  data() {
    return {
      stepper: 2,

      style_columnList: {
        height: "230px",
        "overflow-y": "scroll"
      }
    };
  },
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
      eventBus.$emit("addCondition", true);
    }
  },
  computed: {
    ...mapState({
      columns: state => state.initialData.columns
      // columns: state => state.columns
    })
  },

  components: { DeleteRowModal2, ColumnList, Condition }
};
</script>
