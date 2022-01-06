<template>
  <div>
    <v-container fluid class="pa-1">
      <v-row align="stretch" justify="space-between" style="height: calc(100vh - 16px)" dense>  
        <v-col cols="9" class="fill-height d-flex flex-column">
          <v-row dense justify="space-between">
            <v-col cols="12">
              <v-card outlined class="fill-height px-4 pb-4 mx-auto mb-2 flex-grow-1" style="width: 100%">
                <v-card-text class="d-flex flex-column align-center justify-center rounded pb-0" style="height: calc(100% - 72px)">
                  <v-chart style="height: 100%; width: 100%;" :option="option" autoresize />              
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="3" class="fill-height d-flex flex-column">
          <v-card outlined class="fill-height px-4 pb-4 mx-auto mb-2 flex-grow-1" style="width: 100%">
            <v-card-text class="px-0 pb-0 mb-0 fill-height">
              <v-row v-for="item in graphFilters" :key="item._id.$oid" dense justify="space-between">
                <v-col cols="12">
                <v-btn color="warning" style="width: 100%" small block depressed outlined @click="filterOnClick(item._id.$oid)">
                  {{ item.group_name }}
                </v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { HeatmapChart } from "echarts/charts";
import { GridComponent, TooltipComponent, VisualMapComponent } from 'echarts/components'
import VChart, { THEME_KEY, UPDATE_OPTIONS_KEY } from "vue-echarts";
import axios from 'axios';

use([
  HeatmapChart,
  CanvasRenderer,
  GridComponent,
  VisualMapComponent,
  TooltipComponent
]);

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
  },
  mounted() {
    this.redrawGraph();
    this.loadGroupFilters()
    .then( res => res.data )
    .then( res => {
      this.graphFilters = res.groups;
    })
  },
  data: () => ({
    graphFilters: [],
    option: {
      xAxis: { 
        type: "category",
        data: [], 
        splitArea: { show: true},
        axisLabel: { interval: 0}
      },
      yAxis: {
        type: "category",
        data: [],
        splitArea: { show: true} },
      tooltip: {
        formatter: (params) => {
          return `${params.data[0]}<br>${params.data[1]}<br>${params.data[2]}`
        }
      },
      grid: { height: '80%', top: '10%' },
      visualMap: {
      min: 20,
      max: 200,
      calculable: true,
      realtime: false,
      },
      series: [{
        type: "heatmap",
        data: [],

      }]
    }
  }),
  methods: {
    loadGroupFilters(){
      return axios({
        method: "get",
        url: `/group/load/${this.$store.state.dataset}/train`,
        baseURL: this.$store.state.helper.apiAddr
      })
    },
    redrawGraph(oid){
      axios({
      method: "get",
      url: `/heatmap/${this.$store.state.dataset}/train`,
      baseURL: this.$store.state.helper.apiAddr,
      params: {filter_id: oid? oid:null}
      }).then( res => res.data)
      .then( res => {
        this.option.xAxis.data = res.echart_x;
        this.option.yAxis.data = res.echart_y;
        this.option.series[0].data = res.echart_data;
      })
    },
    filterOnClick(oid){
      this.redrawGraph(oid);
    }
  }
}
</script>
