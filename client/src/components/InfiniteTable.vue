<template>
  <div class="wrapper">
    <table class="dataTable">
      <thead>
        <th v-for="(column, thIndex) in columns" :key="thIndex">{{ columns[thIndex] }}</th>
      </thead>
      <tbody>
        <tr
          v-for="(data, trIndex) in dataSet"
          :key="trIndex"
          :class="{ rowSelected: rowSelectedFlags[trIndex] }"
        >
          <td
            v-for="(column, thIndex) in columns"
            :key="thIndex"
            :class="{ columnSelected: columnSelectedFlags[thIndex] && rowSelectedFlags[trIndex] }"
          >
            {{ data[columns[thIndex]] }}
          </td>
        </tr>
      </tbody>
    </table>
    <infinite-loading @infinite="infiniteHandler" spinner="waveDots"></infinite-loading>
  </div>
</template>
<script>
import InfiniteLoading from "vue-infinite-loading";
import axios from "axios";
const api = "http://localhost:5000/infiniteLoading";

export default {
  data() {
    return {
      limit: 0,
      dataSet: [],
      rowSelectedFlags: [],
      columnSelectedFlags: []
    };
  },
  props: ["xaxis", "columns", "date", "selectedColumnIndex"],
  components: {
    InfiniteLoading
  },
  watch: {
    xaxis: function(data) {
      this.toggleRowFlags(data);
      this.toggleColumnFlags(this.selectedColumnIndex);
    }
  },
  methods: {
    infiniteHandler($state) {
      axios
        .get(api, {
          params: {
            limit: this.limit
          }
        })
        .then(({ data }) => {
          // console.log(data);
          if (data.length) {
            this.limit += 10;
            this.dataSet.push(...data);
            $state.loaded();
          } else {
            $state.complete();
          }
        });
    },
    toggleRowFlags(xaxis) {
      let dateObjectLength = Object.keys(this.date).length;
      for (const key in this.date) {
        let dateTime = new Date(this.date[key]).getTime();
        if (xaxis.min <= dateTime && dateTime <= xaxis.max) {
          this.rowSelectedFlags[key] = true;
        }
      }
    },
    toggleColumnFlags(selectedColumnIndex) {
      this.columnSelectedFlags[selectedColumnIndex + 1] = true;
    }
  },
  created() {
    axios
      .get(api, {
        params: {
          limit: this.limit
        }
      })
      .then(({ data }) => {
        this.limit += 17; //이 값을 app.py의 192줄의 값과 똑같게 해준다.
        this.dataSet.push(...data);
      });
  }
};
</script>
<style scoped>
.wrapper {
  max-height: 85vh;
  overflow: scroll;
}
.dataTable {
  text-transform: capitalize;
  font-size: 11px;
  margin: 0 auto;
  margin-top: 50px;
  text-align: center;
  vertical-align: middle;
}
.dataTable tbody tr.rowSelected {
  background-color: rgba(154, 189, 243, 0.863);
}
.dataTable tbody tr td.columnSelected {
  background-color: rgba(57, 132, 243, 0.863);
}
/* .datatable */

.dataTable tr:hover {
  background-color: #b6b6b6;
  cursor: pointer;
}
.dataTable tr:hover tr {
  background-color: #b6b6b6;
}
.dataTable td:first-child {
  font-weight: 600;
}
.dataTable td {
  border: 0.5px solid rgba(212, 214, 213, 0.623);
}
.dataTable th {
  min-width: 70px;
  border: 0.5px solid rgba(212, 214, 213, 0.623);
  background-color: rgba(239, 239, 239, 0.907);
  padding: 5px 10px;
}

/* datatable odd,even */
.dataTable tr:nth-child(odd) {
  /* background-color: #d9e1f2; */
}
.dataTable tr:nth-child(even) {
  /* background-color: #f0f8ff; */
}
</style>
