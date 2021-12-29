<template>
  <div>
    <v-container fluid class="pa-1">
      <v-row align="stretch" justify="space-between" style="height: calc(100vh - 16px)" dense>
        <v-col cols="3" class="fill-height d-flex flex-column">
          <v-card outlined class="fill-height px-4 pb-4 mx-auto mb-2 flex-grow-1" style="width: 100%">
            <v-card-text>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="9" class="fill-height d-flex flex-column">
          <v-row dense justify="space-between">
            <v-col cols="12">
              <v-card outlined class="fill-height px-4 pb-4 mx-auto mb-2 flex-grow-1" style="width: 100%">
            <v-card-text>
              world
            </v-card-text>
          </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart, ScatterChart } from "echarts/charts";
import VChart, { THEME_KEY, UPDATE_OPTIONS_KEY } from "vue-echarts";
import axios from 'axios';

export default {
  name: "GroupView",
  components: {
    VChart
  },
  provide: {
    [THEME_KEY]: "light",
    [UPDATE_OPTIONS_KEY]: true
  },
  created() {
    axios({
      method: "get",
      url: `/group/list/${this.$store.state.dataset}/train`,
      baseURL: this.$store.state.helper.apiAddr
    }).then(res => res.data)
    .then(x => this.groupList = x)
  },
  mounted() {
    axios({
      method: "get",
      url: `/group/list/${this.$store.state.dataset}/train`,
      baseURL: this.$store.state.helper.apiAddr
    }).then(res => res.data)
    .then(x => this.groupList = x)
    .then(() => {
      axios({
      method: "post",
      url: `/feature/count_100`,
      baseURL: this.$store.state.helper.apiAddr,
      data: { dataset_name: this.$store.state.dataset, dataset_type: "train"}
      }).then(res => res.data)
      .then(x => this.featureCount.push(x))

      for(let group of this.groupList){
      axios({
      method: "post",
      url: `/feature/count_100`,
      baseURL: this.$store.state.helper.apiAddr,
      data: { dataset_name: this.$store.state.dataset, dataset_type: "train", group_id: group.id}
      }).then(res => res.data)
      .then(x=> this.featureCount.push(x))
      }
    })
  },
  data: () => ({
    featureCount: [],
    groupList: []
  }),
  methods: {

  }
}
</script>
