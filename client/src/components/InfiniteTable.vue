<template>
  <div>
    <table>
      <thead>
        <tr>
          <th>Open</th>
          <th>High</th>
          <th>Low</th>
          <th>Close</th>
          <th>Volume</th>
          <th>Name</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(data, index) in dataset" :key="index">
          <td>{{ data.Open }}</td>
          <td>{{ data.High }}</td>
          <td>{{ data.Low }}</td>
          <td>{{ data.Close }}</td>
          <td>{{ data.Volume }}</td>
          <td>{{ data.Name }}</td>
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
      dataSet: []
    };
  },
  components: {
    InfiniteLoading
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
          console.log(data);
          if (data.length) {
            this.limit += 10;
            this.dataSet.push(...data);
            $state.loaded();
          } else {
            $state.complete();
          }
        });
    }
  },
  created() {}
};
</script>
