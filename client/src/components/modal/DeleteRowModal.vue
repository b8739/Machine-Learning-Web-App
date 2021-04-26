<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="800px">
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="" v-bind="attrs" v-on="on">
          Delete Column
        </v-btn>
      </template>
      <v-card>
        <v-container fluid>
          <span class="headline">Delete Row Condition</span>
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
                  v-model="dateValues[indexOfFormFields]"
                  :items="getFormFieldItem(indexOfFormFields)"
                  outlined
                  dense
                  :label="labels[indexOfFormFields]"
                ></v-autocomplete>
              </v-col>
            </v-row>
            <v-row justify="center"
              ><div>
                <input
                  disabled
                  v-model="getFullTimeSeries"
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
                  outlined
                  dense
                  :label="labels[indexOfFormFields]"
                ></v-autocomplete>
              </v-col>
            </v-row>
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
                  outlined
                  dense
                  :label="labels[indexOfFormFields]"
                ></v-autocomplete>
              </v-col>
            </v-row>
          </div>
        </v-container>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="gray darken-1" text @click="dialog = false">
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
export default {
  data: () => ({
    dialog: false,
    formFields: [1, 1, 2, 3, 4],
    labels: ["Year", "Month", "Day", "Hour", "Minute"],
    year: ["2016"],

    // v-model values
    dateValues: ["", "", "", "", ""],

    // mode
    dateMode: true,
    periodMode: false,
    fullTime: "",
    fillDate: ""
  }),
  computed: {
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
      let addZeroAtFront;
      for (let i = 1; i <= 12; i++) {
        if (i < 10) {
          addZeroAtFront = "0" + i;
        } else {
          addZeroAtFront = i;
        }
        hourArray.push(addZeroAtFront);
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
    getFullDate() {
      let dateValues = this.dateValues;
      let formatter = "";
      if (dateValues[1] != "") formatter = "-";
      this.fullDate = dateValues[0] + formatter + dateValues[1] + formatter + dateValues[2];
      return this.fullDate;
    },
    getFullTime() {
      let dateValues = this.dateValues;
      let formatter = "";
      if (dateValues[3] != "") formatter = ":";
      this.fullTime = dateValues[3] + formatter + dateValues[4];
      return this.fullTime;
    },

    getFullTimeSeries() {
      return this.getFullDate + " " + this.getFullTime;
    }
  },
  methods: {
    changeDeleteMode(mode) {
      if (mode == "date") {
        this.periodMode = false;
        this.dateMode = true;
      } else if (mode == "period") {
        this.dateMode = false;
        this.periodMode = true;
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
      const path = "http://localhost:5000/deleteRow";
      axios
        .get(path, {
          params: {
            timeSeriesText: this.getFullTimeSeries
          }
        })
        .then(res => {})
        .catch(error => {
          console.error(error);
        });
    }
  }
};
</script>
