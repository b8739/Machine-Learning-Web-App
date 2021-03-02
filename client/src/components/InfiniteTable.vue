<template>
  <div>
    <table class="dataTable">
      <thead>
        <th v-for="(column, thIndex) in columns" :key="thIndex">{{ columns[thIndex] }}</th>
      </thead>
      <tbody>
        <tr
          v-for="(data, trIndex) in dataSet"
          :key="trIndex"
          :class="{ tableSelected: tableSelectedToggles[trIndex] }"
        >
          <td v-for="(column, thIndex) in columns" :key="thIndex">{{ data[columns[thIndex]] }}</td>
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
      tableSelectedToggles: []
    };
  },
  props: ["xaxis", "columns"],
  components: {
    InfiniteLoading
  },
  watch: {
    xaxis: function(xaxis) {
      this.changeTableSelectedToggle(xaxis);
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
    changeTableSelectedToggle(xaxis) {
      for (let i = xaxis.min; i <= xaxis.max; i++) {
        this.tableSelectedToggles[i] = true;
      }
    }
  },
  created() {
    // for (let i = 0; i < Object.keys(this.dataSet[this.columns[0]]).length; i++) {
    //   this.tableSelectedToggles.push(false);
    // }
    axios
      .get(api, {
        params: {
          limit: this.limit
        }
      })
      .then(({ data }) => {
        this.limit += 10;
        this.dataSet.push(...data);
      });
  }
};
</script>
<style scoped>
.dataTable tbody tr.tableSelected {
  background-color: rgba(78, 73, 73, 0.603);
}
/* .datatable */
.dataTable {
  text-transform: capitalize;
  font-size: 15px;
  margin: 0 auto;
  margin-top: 100px;
  text-align: center;
  vertical-align: middle;
}
.dataTable tr {
  background-color: #ecf1f6;
}
.dataTable tr:hover {
  background-color: #b1e6d2;
  cursor: pointer;
}
.dataTable tr:hover tr {
  background-color: #b1e6d2;
}
.dataTable td:first-child {
  font-weight: 600;
}
.dataTable td {
  border-right: 0.5px solid rgba(209, 229, 219, 0.8);
  padding: 15px;
}
/* datatable odd,even */
.dataTable tr:nth-child(odd) {
  background-color: #d9e1f2;
}
.dataTable tr:nth-child(even) {
  background-color: #f0f8ff;
}
</style>
