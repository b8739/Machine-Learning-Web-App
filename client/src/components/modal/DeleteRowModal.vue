<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="800px">
      <!-- <template v-slot:activator="{ on, attrs }">
        <v-btn color="" v-bind="attrs" v-on="on">
          Delete Column
        </v-btn>
      </template> -->
      <v-card>
        <v-container fluid>
          <span class="headline">Delete Row by Date</span>
          <!-- 최상단 메뉴 탭 -->
          <v-tabs>
            <v-tab @click="changeDeleteMode('date')">날짜 선택</v-tab>
            <v-tab @click="changeDeleteMode('period')">기간 선택</v-tab>
          </v-tabs>
          <!-- 부연설명 -->
          <!-- dateMode -->
          <!-- 상단 Title -->
          <div v-show="dateMode">
            <v-card-subtitle
              >* 데이터베이스에서 <strong>선택한 날짜에 해당하는</strong>
              <span style="color:red"> 모든 행 데이터를 데이터베이스 삭제합니다.</span>
            </v-card-subtitle>
            <div class="my-4 subtitle-1">
              Date
            </div>
            <v-row>
              <v-col v-for="(formField, indexOfFormFields) in formFields" :key="indexOfFormFields">
                <v-autocomplete
                  v-model="fromDateValues[indexOfFormFields]"
                  :items="getFormFieldItem(indexOfFormFields)"
                  outlined
                  clearable
                  dense
                  :label="labels[indexOfFormFields]"
                ></v-autocomplete>
              </v-col>
            </v-row>
            <v-row justify="center"
              ><div class="fullTimeSeries">
                <input
                  disabled
                  v-model="getFullTimeSeries_from"
                  style="text-align:center; color:gray"
                /></div
            ></v-row>
          </div>

          <!-- period mode -->
          <div v-show="periodMode">
            <v-card-subtitle
              >* 데이터베이스에서 선택한 <strong>날짜 기간에 속한 </strong>
              <span style="color:red"> 모든 행 데이터를 데이터베이스 삭제합니다.</span>
            </v-card-subtitle>
            <div class="my-4 subtitle-1">
              From
            </div>
            <!-- 상단 autocomplete -->
            <v-row>
              <v-col v-for="(formField, indexOfFormFields) in formFields" :key="indexOfFormFields">
                <v-autocomplete
                  :items="getFormFieldItem(indexOfFormFields)"
                  v-model="fromDateValues[indexOfFormFields]"
                  outlined
                  dense
                  :label="labels[indexOfFormFields]"
                ></v-autocomplete>
              </v-col>
            </v-row>
            <v-row justify="center"
              ><div class="fullTimeSeries">
                <input
                  disabled
                  v-model="getFullTimeSeries_from"
                  style="text-align:center; color:gray"
                /></div
            ></v-row>
            <v-divider></v-divider>
            <!-- 하단 Title -->
            <div class="my-4 subtitle-1">
              To
            </div>
            <!-- 하단 autocomplete -->
            <v-row>
              <v-col v-for="(formField, indexOfFormFields) in formFields" :key="indexOfFormFields">
                <v-autocomplete
                  :items="getFormFieldItem(indexOfFormFields)"
                  v-model="toDateValues[indexOfFormFields]"
                  outlined
                  dense
                  :label="labels[indexOfFormFields]"
                ></v-autocomplete>
              </v-col>
            </v-row>
            <v-row justify="center"
              ><div class="fullTimeSeries">
                <input
                  disabled
                  v-model="getFullTimeSeries_to"
                  style="text-align:center; color:gray"
                /></div
            ></v-row>
          </div>
        </v-container>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="gray darken-1" text @click="closeModalEvent">
            Close
          </v-btn>
          <v-btn color="red darken-1" text @click="clickDeleteEvent">
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import axios from "axios";
import { eventBus } from "@/main";

export default {
  data: () => ({
    dialog: false,
    formFields: [1, 1, 2, 3, 4],
    labels: ["Year", "Month", "Day", "Hour", "Minute"],
    year: ["2016"],

    // v-model values
    fromDateValues: ["", "", "", "", ""],
    toDateValues: ["", "", "", "", ""],

    // mode
    dateMode: true,
    periodMode: false,
    modeFlag: true, //true == dateMode, false ==periodMode
    fullTime_from: "",
    fullTime_to: "",
    fullDate_from: "",
    fullDate_to: ""
  }),
  computed: {
    // autocomplete items
    getMonth() {
      let monthArray = [];
      let addZeroAtFront;
      for (let i = 1; i <= 12; i++) {
        if (i < 10) {
          addZeroAtFront = "0" + i;
        } else {
          addZeroAtFront = i;
        }
        monthArray.push(addZeroAtFront);
      }
      return monthArray;
    },
    getDay() {
      let dayArray = [];
      let addZeroAtFront;
      for (let i = 1; i <= 31; i++) {
        if (i < 10) {
          addZeroAtFront = "0" + i;
        } else {
          addZeroAtFront = i;
        }
        dayArray.push(addZeroAtFront);
      }
      return dayArray;
    },
    getHour() {
      let hourArray = ["0"];

      for (let i = 1; i <= 12; i++) {
        hourArray.push(i);
      }
      return hourArray;
    },
    getMinute() {
      let minuteArray = [];
      let addZeroAtFront;
      for (let i = 0; i <= 60; i++) {
        if (i < 10) {
          addZeroAtFront = "0" + i;
        } else {
          addZeroAtFront = i;
        }
        minuteArray.push(addZeroAtFront);
      }
      return minuteArray;
    },
    // get specific time

    // from
    getFullDate_from() {
      let fromDateValues = this.fromDateValues;
      this.fullDate_from = "";
      for (let i = 0; i < 3; i++) {
        if (fromDateValues[i] != null && fromDateValues[i] != "") {
          if (i != 0) {
            this.fullDate_from = this.fullDate_from + "-";
          }
          this.fullDate_from = this.fullDate_from.concat(fromDateValues[i]);
        }
      }
      return this.fullDate_from;
    },
    getFullTime_from() {
      let fromDateValues = this.fromDateValues;
      this.fullTime_from = "";
      for (let i = 3; i < 5; i++) {
        if (fromDateValues[i] != null && fromDateValues[i] != "") {
          if (i != 3) {
            this.fullTime_from = this.fullTime_from + ":";
          }
          this.fullTime_from = this.fullTime_from.concat(fromDateValues[i]);
        }
      }
      return this.fullTime_from;
    },

    getFullTimeSeries_from() {
      let fullTimeSeries = this.getFullDate_from + " " + this.getFullTime_from;
      console.log(fullTimeSeries);
      return fullTimeSeries;
    },
    // to
    getFullDate_to() {
      let toDateValues = this.toDateValues;
      let formatter = "";
      if (toDateValues[1] != "") formatter = "-";
      this.fullDate_to =
        toDateValues[0] + formatter + toDateValues[1] + formatter + toDateValues[2];
      return this.fullDate_to;
    },
    getFullTime_to() {
      let toDateValues = this.toDateValues;
      let formatter = "";
      if (toDateValues[3] != "") formatter = ":";
      this.fullTime_to = toDateValues[3] + formatter + toDateValues[4];
      return this.fullTime_to;
    },

    getFullTimeSeries_to() {
      return this.getFullDate_to + " " + this.getFullTime_to;
    }
  },
  methods: {
    changeDeleteMode(mode) {
      if (mode == "date") {
        this.periodMode = false;
        this.dateMode = true;
        this.modeFlag = true;
      } else if (mode == "period") {
        this.dateMode = false;
        this.periodMode = true;
        this.modeFlag = false;
        //초기화
        this.fromDateValues = ["", "", "", "", ""];
        this.toDateValues = ["", "", "", "", ""];
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
    },
    clickDeleteEvent() {
      // date mode 일 때
      if (this.modeFlag == true) {
        const path = "http://localhost:5000/deleteRowByDate";
        axios
          .get(path, {
            params: {
              timeSeriesText: this.getFullTimeSeries_from
            }
          })
          .then(res => {})
          .catch(error => {
            console.error(error);
          });
      }
      // period mode 일 때
      else {
        const path = "http://localhost:5000/deleteRowByPeriod";
        axios
          .get(path, {
            params: {
              getFullTimeSeries_from: this.getFullTimeSeries_from,
              getFullTimeSeries_to: this.getFullTimeSeries_to
            }
          })
          .then(res => {})
          .catch(error => {
            console.error(error);
          });
      }
    },
    closeModalEvent() {
      this.fromDateValues = ["", "", "", "", ""];
      this.toDateValues = ["", "", "", "", ""];
      this.dialog = false;
    }
  },
  created() {
    eventBus.$on("openDeleteRowModal", modalStatus => {
      this.dialog = modalStatus;
    });
  }
};
</script>
