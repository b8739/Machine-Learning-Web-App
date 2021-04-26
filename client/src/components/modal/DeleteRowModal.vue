<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="800px">
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" dark v-bind="attrs" v-on="on">
          Open Dialog
        </v-btn>
      </template>
      <v-card>
        <span class="headline">Delete Column Condition</span>

        <v-container fluid>
          <div class="my-4 subtitle-1">
            From
          </div>
          <v-row>
            <!-- 상단 autocomplete -->
            <v-col v-for="(formField, IndexOfFormField) in formFields" :key="IndexOfFormField">
              <v-autocomplete
                :items="getFormFieldItem(IndexOfFormField)"
                outlined
                dense
                :label="labels[IndexOfFormField]"
              ></v-autocomplete>
            </v-col>
          </v-row>
          <v-divider></v-divider>
          <div class="my-4 subtitle-1">
            To
          </div>
          <v-row>
            <!-- 하단 autocomplete -->
            <v-col v-for="(formField, IndexOfFormField) in formFields" :key="IndexOfFormField">
              <v-autocomplete
                :items="getFormFieldItem(IndexOfFormField)"
                outlined
                dense
                :label="labels[IndexOfFormField]"
              ></v-autocomplete>
            </v-col>
          </v-row>
        </v-container>
        <small>*indicates required field</small>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">
            Close
          </v-btn>
          <v-btn color="blue darken-1" text @click="dialog = false">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
export default {
  data: () => ({
    dialog: false,
    formFields: [1, 1, 2, 3, 4],
    labels: ["Year", "Month", "Day", "Hour", "Minute"],
    year: ["2015", "2016", "2017", "2018"]
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
      for (let i = 1; i <= 31; i++) {
        dayArray.push(i);
      }
      return dayArray;
    },
    getTime() {
      let timeArray = [];
      for (let i = 1; i <= 12; i++) {
        timeArray.push(i);
      }
      return timeArray;
    },
    getMinute() {
      let minuteArray = [];
      for (let i = 0; i <= 60; i++) {
        minuteArray.push(i);
      }
      return minuteArray;
    }
  },
  methods: {
    getFormFieldItem(indexOfFormField) {
      if (indexOfFormField == 0) {
        return this.year;
      } else if (indexOfFormField == 1) {
        return this.getMonth;
      } else if (indexOfFormField == 2) {
        return this.getDay;
      } else if (indexOfFormField == 3) {
        return this.getTime;
      } else {
        return this.getMinute;
      }
    }
  }
};
</script>
