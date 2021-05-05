<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" non-linear persistent max-width="800">
      <v-stepper v-model="e1">
        <!-- title -->
        <v-card-title class="headline">
          이동 평균 (Moving Average)
        </v-card-title>
        <!-- header -->
        <v-stepper-header>
          <v-stepper-step step="1" editable>
            Define Target Columns
          </v-stepper-step>
          <v-stepper-step step="2" editable>
            Define Time Unit
          </v-stepper-step>
        </v-stepper-header>
        <!-- contents -->
        <v-stepper-content step="1">
          <ColumnList />
        </v-stepper-content>
        <v-stepper-content step="2">
          <v-card>
            <v-card-text>이동 평균 (Moving Average)를 계산할 시간 단위를 입력하세요.</v-card-text>
            <v-row justify="center">
              <v-col
                cols="2"
                v-for="(formField, indexOfFormFields) in formFields"
                :key="indexOfFormFields"
              >
                <v-text-field
                  v-model="dateValues[indexOfFormFields]"
                  clearable
                  dense
                  :label="labels[indexOfFormFields]"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-card-actions>
              <v-spacer></v-spacer>

              <v-btn color="primary" @click="getMovingAverage">
                Confirm
              </v-btn>

              <v-btn text @click="dialog = false">
                Cancel
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-stepper-content>
      </v-stepper>
    </v-dialog>
  </v-row>
</template>
<script>
import { eventBus } from "@/main";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
import ColumnList from "@/components/average/ColumnList.vue";
export default {
  data() {
    return {
      e1: 1,
      dialog: false,
      formFields: [3, 4],
      labels: ["Hour", "Minute"],
      year: ["2016"],
      dateValues: ["", ""],
      selectedColumns: [],
      newDataset: {},
      counter: 0,
      total: 0
    };
  },
  components: {
    ColumnList
  },
  computed: {
    ...mapState({
      dataset: state => state.initialData.dataset,

      columns: state => state.initialData.columns
    }),
    fullTime() {
      let fullDate = "";

      fullDate += parseInt(this.getHour) + parseInt(this.dateValues[1]);
      fullDate = parseInt(fullDate);
      return fullDate;
    },
    getHour() {
      return this.dateValues[0] * 60;
    }
  },
  methods: {
    getMovingAverage() {
      let selectedColumns = this.selectedColumns;
      for (let i = 0; i < selectedColumns.length; i++) {
        let targetDataset = this.dataset[selectedColumns[i]];
        this.counter = 1;
        this.total = 0;

        this.newDataset[selectedColumns[i]] = [];
        for (let j = 0; j < Object.keys(targetDataset).length; j++) {
          if ((this.counter / this.fullTime) % 1 != 0) {
            this.total += targetDataset[j];
            this.counter++;
          } else if ((this.counter / this.fullTime) % 1 === 0) {
            let mean = this.total / this.fullTime;
            this.newDataset[selectedColumns[i]].push(mean.toFixed(3)); // 소수점 3번째 자리까지
            this.counter++;
            this.total = 0;
          }
        }
      }
    },
    getFormFieldItem(indexOfFormFields) {
      if (indexOfFormFields == 0) {
        return this.year;
      } else if (indexOfFormFields == 1) {
        return this.getMonth;
      } else if (indexOfFormFields == 2) {
        return this.getDay;
      } else if (indexOfFormFields == 3) {
        return this.getHour;
      } else {
        return this.getMinute;
      }
    }
  },

  created() {
    eventBus.$on("openMovingAverageModal", dialogStatus => {
      this.dialog = dialogStatus;
    });
    eventBus.$on("selectedColumns", selectedColumns => {
      this.selectedColumns = selectedColumns;
    });
    eventBus.$on("toStepTwo", step => {
      this.e1 = step;
    });
  }
};
</script>
